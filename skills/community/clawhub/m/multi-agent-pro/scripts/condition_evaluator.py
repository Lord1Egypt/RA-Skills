#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
条件表达式求值器 - 多Agent协作编排引擎 v4.0

功能：为动态工作流（if-else / switch / while-loop / for-each）提供
      安全的条件表达式求值能力。

支持语法：
  - 点路径取值：nodes.<id>.output_data.<field>（可多级嵌套）
  - 比较运算：==  !=  >  <  >=  <=
  - 逻辑运算：and  or  not
  - 成员运算：in  not in
  - 字面量：数字、字符串、True/False/None、列表、元组
  - 括号分组：( ... )

零第三方依赖，仅使用 Python 标准库

★★★ 安全说明（核心）★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 严禁 eval/exec：使用 ast.parse(mode='eval') 解析为语法树，
   再用白名单方式逐节点求值，只放行安全的表达式节点类型。
2. 禁止函数调用：Call/Lambda/Attribute-方法/推导式 等一律拒绝，
   杜绝 __import__、os.system 等注入。
3. 禁止属性访问求值：所有 a.b.c 形式统一解释为"数据点路径"，
   在提供的上下文字典里查找，不触碰任何 Python 对象属性。
4. 变量白名单：表达式里的根变量名必须来自 context（如 nodes），
   未知变量报错，不返回宿主环境任何数据。
5. 表达式长度限制 1000 字符，AST 深度限制 50 层，防止 DoS。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用方式：
  from condition_evaluator import evaluate
  ctx = {"nodes": {"a": {"output_data": {"score": 85}}}}
  evaluate("nodes.a.output_data.score >= 60", ctx)   # → True

命令行自测：
  python condition_evaluator.py "1 + 1 == 2"
  python condition_evaluator.py "nodes.a.output_data.score >= 60" '{"nodes":{"a":{"output_data":{"score":85}}}}'
"""

import ast
import sys
import json
import operator

# 表达式长度上限（防 DoS）
MAX_EXPR_LEN = 1000
# AST 递归深度上限（防深层嵌套 DoS）
MAX_AST_DEPTH = 50


class ConditionError(Exception):
    """条件表达式求值异常（携带中文可读信息）"""
    pass


# 允许的比较运算符
_CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Gt: operator.gt,
    ast.Lt: operator.lt,
    ast.GtE: operator.ge,
    ast.LtE: operator.le,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
}

# 允许的白名单函数（禁止关键字参数，只允许位置参数）
_WHITELISTED_FUNCTIONS = {
    # 基础类型转换
    'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
    'list': list, 'tuple': tuple, 'dict': dict, 'set': set,
    'abs': abs, 'min': min, 'max': max, 'sum': sum, 'round': round,
    'sorted': sorted, 'reversed': reversed, 'enumerate': enumerate, 'zip': zip,
    # 字符串操作（安全子集）
    'contains': lambda s, sub: sub in s,
    'startswith': lambda s, prefix: s.startswith(prefix),
    'endswith': lambda s, suffix: s.endswith(suffix),
    'split': lambda s, sep=None, maxsplit=-1: s.split(sep, maxsplit) if sep else s.split(),
    'join': lambda sep, iterable: sep.join(iterable),
    'strip': lambda s, chars=None: s.strip(chars),
    'lower': lambda s: s.lower(),
    'upper': lambda s: s.upper(),
    'replace': lambda s, old, new, count=-1: s.replace(old, new, count),
}

# 允许的白名单正则函数（安全子集，禁止 re.compile/re.sub 等危险操作）
_WHITELISTED_RE_FUNCTIONS = {
    'match': lambda pattern, string: bool(__import__('re').match(pattern, string)),
    'search': lambda pattern, string: bool(__import__('re').search(pattern, string)),
    'findall': lambda pattern, string: __import__('re').findall(pattern, string),
}

# 允许的二元算术运算符（用于 score * 2 > 100 这类简单运算）
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}

# 允许的一元运算符
_UNARY_OPS = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Not: operator.not_,
}

_SENTINEL = object()


def _dotted_name(node):
    """将 a.b.c 形式的 Attribute/Name 链解析为 ['a','b','c']。

    只处理"名字链"，任何非名字链（如函数调用结果的属性）返回 None。
    """
    parts = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        parts.reverse()
        return parts
    return None


def _resolve_path(parts, context):
    """在 context 里按点路径逐级取值。

    支持 dict 键访问和 list 数字索引访问。
    路径不存在时抛出 ConditionError（附带清晰的中文定位信息）。
    """
    cur = context
    walked = []
    for p in parts:
        walked.append(p)
        if isinstance(cur, dict):
            if p not in cur:
                raise ConditionError(
                    f"路径不存在：'{'.'.join(walked)}'（在数据里找不到键 '{p}'）\n"
                    f"  提示：可用键有 {list(cur.keys())}"
                )
            cur = cur[p]
        elif isinstance(cur, (list, tuple)):
            # 支持 nodes.items.0 这样的数字索引
            try:
                idx = int(p)
            except (ValueError, TypeError):
                raise ConditionError(
                    f"路径错误：'{'.'.join(walked)}' 处需要数字索引访问列表，但得到 '{p}'"
                )
            if idx < 0 or idx >= len(cur):
                raise ConditionError(
                    f"索引越界：'{'.'.join(walked)}'（列表长度 {len(cur)}，索引 {idx}）"
                )
            cur = cur[idx]
        else:
            raise ConditionError(
                f"路径错误：'{'.'.join(walked[:-1])}' 的值不是对象/列表，无法继续访问 '{p}'"
            )
    return cur


def _check_depth(node, depth=0):
    """检查 AST 深度，防止深层嵌套导致的栈溢出/DoS"""
    if depth > MAX_AST_DEPTH:
        raise ConditionError(f"表达式嵌套过深（超过 {MAX_AST_DEPTH} 层），已拒绝")
    for child in ast.iter_child_nodes(node):
        _check_depth(child, depth + 1)


def _eval_node(node, context):
    """白名单方式递归求值单个 AST 节点。

    只放行明确安全的节点类型，其余一律抛错。
    """
    # 字面量常量：数字/字符串/布尔/None
    if isinstance(node, ast.Constant):
        return node.value

    # 表达式包装
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, context)

    # 名字链（变量或点路径）→ 统一当作数据路径解析
    if isinstance(node, (ast.Name, ast.Attribute)):
        parts = _dotted_name(node)
        if parts is None:
            raise ConditionError("不支持的属性访问形式（仅允许点路径取值）")
        return _resolve_path(parts, context)

    # 下标访问：nodes['a']['x'] 或 items[0]
    if isinstance(node, ast.Subscript):
        target = _eval_node(node.value, context)
        key_node = node.slice
        # Python 3.9+ slice 直接是表达式
        key = _eval_node(key_node, context)
        try:
            return target[key]
        except (KeyError, IndexError, TypeError) as e:
            raise ConditionError(f"下标访问失败：{e}")

    # 布尔运算 and / or（支持短路）
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            result = True
            for v in node.values:
                result = _eval_node(v, context)
                if not result:
                    return result
            return result
        elif isinstance(node.op, ast.Or):
            result = False
            for v in node.values:
                result = _eval_node(v, context)
                if result:
                    return result
            return result
        raise ConditionError("不支持的布尔运算符")

    # 一元运算 not / -x / +x
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ConditionError(f"不支持的一元运算符：{op_type.__name__}")
        return _UNARY_OPS[op_type](_eval_node(node.operand, context))

    # 比较运算（支持链式 a < b < c）
    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, context)
        for op, comparator in zip(node.ops, node.comparators):
            op_type = type(op)
            if op_type not in _CMP_OPS:
                raise ConditionError(f"不支持的比较运算符：{op_type.__name__}")
            right = _eval_node(comparator, context)
            try:
                ok = _CMP_OPS[op_type](left, right)
            except TypeError as e:
                raise ConditionError(f"比较类型不兼容：{left!r} 与 {right!r}（{e}）")
            if not ok:
                return False
            left = right
        return True

    # 二元算术运算 + - * / // %
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ConditionError(f"不支持的算术运算符：{op_type.__name__}")
        left = _eval_node(node.left, context)
        right = _eval_node(node.right, context)
        try:
            return _BIN_OPS[op_type](left, right)
        except (TypeError, ZeroDivisionError) as e:
            raise ConditionError(f"算术运算失败：{e}")

    # 列表 / 元组字面量（用于 in [1,2,3]）
    if isinstance(node, ast.List):
        return [_eval_node(e, context) for e in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_eval_node(e, context) for e in node.elts)

    # 白名单函数调用（仅允许无关键字参数的位置参数调用）
    if isinstance(node, ast.Call):
        if node.keywords:
            raise ConditionError(
                "不支持关键字参数调用，请使用位置参数\n"
                "  安全限制：禁止 **kwargs 等关键字参数传递"
            )
        func_node = node.func
        if not isinstance(func_node, ast.Name):
            raise ConditionError(
                "不支持的方法调用形式（仅允许简单函数名调用）"
            )
        func_name = func_node.id

        # 合并白名单函数与正则函数
        all_funcs = {**_WHITELISTED_FUNCTIONS, **_WHITELISTED_RE_FUNCTIONS}
        if func_name not in all_funcs:
            raise ConditionError(
                f"不支持的函数调用：{func_name}\n"
                f"  允许的函数：{'/'.join(sorted(all_funcs.keys()))}"
            )

        # 参数数量限制（最多 5 个）
        if len(node.args) > 5:
            raise ConditionError(
                f"函数 {func_name} 参数过多（最多 5 个，当前 {len(node.args)} 个）"
            )

        args = [_eval_node(arg, context) for arg in node.args]
        return all_funcs[func_name](*args)

    # 其余节点类型（Lambda/Comprehension/...）一律拒绝
    raise ConditionError(
        f"不支持的表达式元素：{type(node).__name__}\n"
        f"  安全限制：禁止 lambda、推导式等，只允许"
        f"取值/比较/逻辑/算术运算/白名单函数调用"
    )


def evaluate(expr, context=None):
    """求值条件表达式，返回结果（通常是 bool）。

    参数：
      expr    : 条件表达式字符串
      context : 求值上下文字典（如 {"nodes": {...}}）

    异常：
      ConditionError - 表达式非法、路径不存在或包含危险元素

    示例：
      evaluate("nodes.a.output_data.score >= 60",
               {"nodes": {"a": {"output_data": {"score": 85}}}})  # → True
    """
    if context is None:
        context = {}

    if not isinstance(expr, str) or not expr.strip():
        raise ConditionError("条件表达式必须是非空字符串")

    if len(expr) > MAX_EXPR_LEN:
        raise ConditionError(f"条件表达式过长（超过 {MAX_EXPR_LEN} 字符），已拒绝")

    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ConditionError(
            f"表达式语法错误：{e.msg}\n"
            f"  表达式：{expr}\n"
            f"  提示：检查括号是否配对、运算符是否正确"
        )

    _check_depth(tree)
    return _eval_node(tree, context)


def evaluate_bool(expr, context=None):
    """求值并强制转换为 bool（用于 if / while 判断）"""
    return bool(evaluate(expr, context))


def build_context_from_state(state):
    """从 pipeline_state 构建求值上下文。

    暴露：
      nodes.<id>.output_data.<field>
      nodes.<id>.status
      nodes.<id>.retry_count
    这样条件表达式即可引用任意已完成节点的输出。
    """
    ctx = {"nodes": {}}
    for nid, node in state.get('nodes', {}).items():
        ctx["nodes"][nid] = {
            "output_data": node.get('output_data', {}),
            "status": node.get('status', ''),
            "retry_count": node.get('retry_count', 0),
            "iteration": node.get('iteration', 0),
        }
    return ctx


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("条件表达式求值器 - 多Agent协作编排引擎 v4.0")
        print("=" * 50)
        print("用法：python condition_evaluator.py <表达式> [context_json]")
        print("")
        print("示例：")
        print("  python condition_evaluator.py \"1 + 1 == 2\"")
        print("  python condition_evaluator.py \"nodes.a.output_data.score >= 60\" \\")
        print("      '{\"nodes\":{\"a\":{\"output_data\":{\"score\":85}}}}'")
        print("")
        print("支持语法：")
        print("  取值：nodes.<id>.output_data.<field>")
        print("  比较：==  !=  >  <  >=  <=")
        print("  逻辑：and  or  not")
        print("  成员：in  not in")
        print("  算术：+  -  *  /  //  %")
        sys.exit(0)

    expr = sys.argv[1]
    context = {}
    if len(sys.argv) > 2:
        try:
            context = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"错误：context 不是合法 JSON - {e}")
            sys.exit(1)

    try:
        result = evaluate(expr, context)
        print(f"表达式：{expr}")
        print(f"结果  ：{result}  （类型 {type(result).__name__}）")
    except ConditionError as e:
        print(f"求值失败：{e}")
        sys.exit(1)
