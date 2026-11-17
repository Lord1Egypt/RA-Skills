#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据校验工具 - 按规则校验 Excel/CSV 数据质量

场景：检查邮箱格式、工号唯一性、必填项缺失、日期范围等
输出校验报告：违反行号 + 违反内容 + 统计摘要
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import ast
import operator as op

# 安全表达式求值：仅允许比较、布尔运算、算术运算和常量
_SAFE_BIN_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.Mod: op.mod, ast.Pow: op.pow,
}
_SAFE_CMP_OPS = {
    ast.Eq: op.eq, ast.NotEq: op.ne, ast.Lt: op.lt, ast.LtE: op.le,
    ast.Gt: op.gt, ast.GtE: op.ge,
}


def _safe_eval_node(node, local_vars):
    """递归求值 AST 节点，仅允许白名单操作。"""
    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body, local_vars)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return local_vars.get(node.id)
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_BIN_OPS:
        left = _safe_eval_node(node.left, local_vars)
        right = _safe_eval_node(node.right, local_vars)
        return _SAFE_BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.Compare):
        left = _safe_eval_node(node.left, local_vars)
        for comparator, op_node in zip(node.comparators, node.ops):
            if type(op_node) not in _SAFE_CMP_OPS:
                raise ValueError(f"不允许的比较操作: {type(op_node).__name__}")
            right = _safe_eval_node(comparator, local_vars)
            if not _SAFE_CMP_OPS[type(op_node)](left, right):
                return False
            left = right
        return True
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return all(_safe_eval_node(v, local_vars) for v in node.values)
        if isinstance(node.op, ast.Or):
            return any(_safe_eval_node(v, local_vars) for v in node.values)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _safe_eval_node(node.operand, local_vars)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_safe_eval_node(node.operand, local_vars)
    raise ValueError(f"不允许的表达式类型: {type(node).__name__}")


def safe_eval_expression(expression, local_vars):
    """安全评估表达式，仅支持比较、布尔运算和算术运算。"""
    tree = ast.parse(expression, mode='eval')
    return _safe_eval_node(tree, local_vars)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector

# 内置正则模式
BUILTIN_PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^1[3-9]\d{9}$',
    'idcard': r'^\d{17}[\dXx]$',
}


class ValidationReport:
    """校验报告收集器"""

    def __init__(self):
        self.violations = []  # 每条违规记录
        self.rule_stats = {}  # 每条规则的统计

    def add_violation(self, rule_name: str, rule_type: str, column: str,
                      row_num: int, value, message: str):
        self.violations.append({
            'rule_name': rule_name,
            'rule_type': rule_type,
            'column': column,
            'row_num': row_num,
            'value': str(value) if value is not None else '(空)',
            'message': message,
        })
        key = f"{rule_type}:{column}"
        if key not in self.rule_stats:
            self.rule_stats[key] = {'rule_type': rule_type, 'column': column, 'count': 0}
        self.rule_stats[key]['count'] += 1

    def summary(self) -> dict:
        return {
            'total_violations': len(self.violations),
            'by_rule': list(self.rule_stats.values()),
        }


def check_required(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """必填检查"""
    column = rule['column']
    if column not in df.columns:
        report.add_violation(rule.get('name', ''), 'required', column, 0, None,
                             f"列 '{column}' 不存在")
        return

    mask = df[column].isna() | (df[column].astype(str).str.strip() == '')
    for idx in df[mask].index:
        report.add_violation(rule.get('name', ''), 'required', column,
                             idx + 2, df.at[idx, column], f"'{column}' 为空")


def check_unique(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """唯一性检查"""
    column = rule['column']
    if column not in df.columns:
        report.add_violation(rule.get('name', ''), 'unique', column, 0, None,
                             f"列 '{column}' 不存在")
        return

    duplicated = df[df[column].duplicated(keep=False) & df[column].notna()]
    for idx in duplicated.index:
        report.add_violation(rule.get('name', ''), 'unique', column,
                             idx + 2, df.at[idx, column],
                             f"'{column}' 值重复: {df.at[idx, column]}")


def check_type(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """类型检查：number/date/email/phone/idcard"""
    column = rule['column']
    expected_type = rule.get('expected', rule.get('type_value', ''))
    if column not in df.columns:
        return

    for idx, val in df[column].items():
        if pd.isna(val) or str(val).strip() == '':
            continue  # 空值由 required 规则处理

        val_str = str(val).strip()

        if expected_type == 'number':
            try:
                float(val_str)
            except ValueError:
                report.add_violation(rule.get('name', ''), 'type', column,
                                     idx + 2, val, f"'{val}' 不是有效数字")

        elif expected_type == 'date':
            is_date = False
            for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日', '%Y-%m-%d %H:%M:%S'):
                try:
                    datetime.strptime(val_str, fmt)
                    is_date = True
                    break
                except ValueError:
                    continue
            if not is_date:
                report.add_violation(rule.get('name', ''), 'type', column,
                                     idx + 2, val, f"'{val}' 不是有效日期")

        elif expected_type in BUILTIN_PATTERNS:
            pattern = BUILTIN_PATTERNS[expected_type]
            if not re.match(pattern, val_str):
                report.add_violation(rule.get('name', ''), 'type', column,
                                     idx + 2, val, f"'{val}' 不符合 {expected_type} 格式")


def check_range(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """范围检查"""
    column = rule['column']
    min_val = rule.get('min')
    max_val = rule.get('max')
    if column not in df.columns:
        return

    for idx, val in df[column].items():
        if pd.isna(val):
            continue
        try:
            num_val = float(val)
        except (ValueError, TypeError):
            continue
        if min_val is not None and num_val < float(min_val):
            report.add_violation(rule.get('name', ''), 'range', column,
                                 idx + 2, val, f"'{val}' 小于最小值 {min_val}")
        if max_val is not None and num_val > float(max_val):
            report.add_violation(rule.get('name', ''), 'range', column,
                                 idx + 2, val, f"'{val}' 大于最大值 {max_val}")


def check_pattern(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """正则匹配检查"""
    column = rule['column']
    pattern = rule.get('pattern', '')
    if column not in df.columns or not pattern:
        return

    regex = re.compile(pattern)
    for idx, val in df[column].items():
        if pd.isna(val) or str(val).strip() == '':
            continue
        if not regex.match(str(val).strip()):
            report.add_violation(rule.get('name', ''), 'pattern', column,
                                 idx + 2, val, f"'{val}' 不匹配正则: {pattern}")


def check_enum(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """枚举值检查"""
    column = rule['column']
    allowed = rule.get('values', [])
    if column not in df.columns or not allowed:
        return

    for idx, val in df[column].items():
        if pd.isna(val) or str(val).strip() == '':
            continue
        if str(val).strip() not in [str(v) for v in allowed]:
            report.add_violation(rule.get('name', ''), 'enum', column,
                                 idx + 2, val,
                                 f"'{val}' 不在允许值列表中: {allowed}")


def check_length(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """长度限制检查"""
    column = rule['column']
    min_len = rule.get('min', 0)
    max_len = rule.get('max', float('inf'))
    if column not in df.columns:
        return

    for idx, val in df[column].items():
        if pd.isna(val):
            continue
        val_len = len(str(val))
        if val_len < min_len:
            report.add_violation(rule.get('name', ''), 'length', column,
                                 idx + 2, val, f"长度 {val_len} 小于最小长度 {min_len}")
        if val_len > max_len:
            report.add_violation(rule.get('name', ''), 'length', column,
                                 idx + 2, val, f"长度 {val_len} 超过最大长度 {max_len}")


def check_cross_field(df: pd.DataFrame, rule: dict, report: ValidationReport):
    """跨字段逻辑检查"""
    expression = rule.get('expression', '')
    columns = rule.get('columns', [])
    if not expression:
        return

    # 支持简单比较：column1 < column2, column1 == column2 等
    for idx in df.index:
        try:
            # 构建局部变量
            local_vars = {}
            for col in columns:
                if col in df.columns:
                    val = df.at[idx, col]
                    local_vars[col.replace('.', '_').replace(' ', '_')] = val

            # 安全评估表达式（AST 白名单方式，防止代码注入）
            result = safe_eval_expression(expression, local_vars)
            if not result:
                report.add_violation(rule.get('name', ''), 'cross_field',
                                     ','.join(columns), idx + 2,
                                     {col: str(df.at[idx, col]) for col in columns if col in df.columns},
                                     f"跨字段校验失败: {expression}")
        except Exception:
            pass  # 表达式求值失败（如空值）跳过


# 规则类型 -> 处理函数映射
RULE_HANDLERS = {
    'required': check_required,
    'unique': check_unique,
    'type': check_type,
    'range': check_range,
    'pattern': check_pattern,
    'enum': check_enum,
    'length': check_length,
    'cross_field': check_cross_field,
}


def load_rules(rules_arg: str) -> list:
    """加载校验规则（从 JSON 文件或内联 JSON 字符串）"""
    if os.path.isfile(rules_arg):
        with open(rules_arg, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        try:
            return json.loads(rules_arg)
        except json.JSONDecodeError:
            raise ValueError(f"无法解析规则: {rules_arg}\n请提供有效的 JSON 文件路径或 JSON 字符串")


def generate_report(report: ValidationReport, total_rows: int, output_format: str) -> str:
    """生成校验报告"""
    summary = report.summary()

    if output_format == 'json':
        result = {
            'summary': {
                'total_rows': total_rows,
                'total_violations': summary['total_violations'],
                'pass_rate': f"{(1 - summary['total_violations'] / max(total_rows, 1)) * 100:.1f}%",
                'by_rule': summary['by_rule'],
            },
            'violations': report.violations,
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    else:
        # 文本格式
        lines = []
        lines.append("=" * 60)
        lines.append("📊 数据校验报告")
        lines.append("=" * 60)
        lines.append(f"总行数: {total_rows}")
        lines.append(f"违规总数: {summary['total_violations']}")
        pass_rate = (1 - summary['total_violations'] / max(total_rows, 1)) * 100
        lines.append(f"通过率: {pass_rate:.1f}%")
        lines.append("")
        lines.append("📋 按规则统计:")
        for stat in summary['by_rule']:
            lines.append(f"  [{stat['rule_type']}] {stat['column']}: {stat['count']} 条违规")
        lines.append("")
        lines.append("-" * 60)
        lines.append("📝 违规详情:")
        lines.append("-" * 60)

        for v in report.violations[:100]:  # 最多显示前100条
            lines.append(
                f"  行 {v['row_num']} | [{v['rule_type']}] {v['column']} | "
                f"值: {v['value']} | {v['message']}"
            )

        if len(report.violations) > 100:
            lines.append(f"\n  ... 还有 {len(report.violations) - 100} 条违规未显示")

        lines.append("")
        lines.append("=" * 60)
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Excel 数据校验工具 - 按规则校验数据质量'
    )
    parser.add_argument('input_file', help='输入文件路径（Excel/CSV）')
    parser.add_argument('--rules', required=True, help='校验规则（JSON 文件路径或内联 JSON）')
    parser.add_argument('--output', help='校验报告输出路径（不指定则打印到终端）')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='报告格式（默认 text）')
    parser.add_argument('--sheet', help='指定 Sheet 名称（Excel 文件时使用）')

    args = parser.parse_args()

    # 校验输入
    if not os.path.exists(args.input_file):
        print(f"❌ 输入文件不存在: {args.input_file}")
        sys.exit(1)

    # 加载数据
    try:
        df, _errors = safe_read(args.input_file, sheet_name=args.sheet)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        sys.exit(1)

    # 加载规则
    try:
        rules = load_rules(args.rules)
    except Exception as e:
        print(f"❌ 加载规则失败: {e}")
        sys.exit(1)

    print(f"📊 文件: {args.input_file}")
    print(f"📝 数据行数: {len(df)}")
    print(f"📋 校验规则: {len(rules)} 条\n")

    # 执行校验
    report = ValidationReport()
    for rule in rules:
        rule_type = rule.get('type', rule.get('rule_type', ''))
        handler = RULE_HANDLERS.get(rule_type)
        if handler:
            handler(df, rule, report)
        else:
            print(f"⚠️ 未知规则类型: {rule_type}，跳过")

    # 生成报告
    report_text = generate_report(report, len(df), args.format)

    if args.output:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"✅ 校验报告已保存: {args.output}")
    else:
        print(report_text)

    # 返回退出码
    if report.summary()['total_violations'] > 0:
        sys.exit(1)  # 有违规返回非0
    else:
        print("✅ 所有校验通过！")


if __name__ == "__main__":
    main()
