#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
holmes_case_logger.py
交互式案件记录器 - 用于 holmes-perspective-v2 skill
"""
import os
import re
import argparse
from datetime import datetime
from pathlib import Path

# ========== 全局配置 ==========
SKILL_DIR = Path(__file__).parent.parent.resolve()
AUTORESEARCH_DIR = SKILL_DIR / ".autoresearch"
CASES_DIR = AUTORESEARCH_DIR / "cases"
INDEX_FILE = AUTORESEARCH_DIR / "index.md"

# CASE 文件必填字段
REQUIRED_FIELDS = ["problem", "model", "formula", "result", "description", "time", "experiments"]
# CASE 文件非必填字段
OPTIONAL_FIELDS = ["switch"]

# 有效选项
VALID_MODELS = ["链条因果", "排除法", "反向工程", "异常锚定", "主动验证", "压缩推理", "阁楼心智"]
VALID_FORMULAS = ["排除法", "选言推理", "假言推理", "逆否推理", "传递公式", "必要条件", "矛盾触发", "因果链", "或然性推理", "异常锚定", "主动验证", "反向工程", "归谬法"]
VALID_RESULTS = ["成功", "失败", "部分成功"]

# 正则
PATTERN_CASE_COUNT = re.compile(r"\*\*案件计数\*\*:\s*(\d+)", re.MULTILINE)
PATTERN_CASE_ENTRY = re.compile(r"^\| (CASE_\d+) \|")

# ========== 初始化 ==========
def init_dirs():
    """初始化 .autoresearch 目录"""
    AUTORESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.touch(exist_ok=True)

def get_case_count() -> int:
    """获取当前案件计数"""
    if not INDEX_FILE.exists():
        return 0
    content = INDEX_FILE.read_text(encoding="utf-8")
    match = PATTERN_CASE_COUNT.search(content)
    if match:
        return int(match.group(1).strip())
    return 0

def parse_case_id(timestamp: str) -> str:
    """生成 CASE_ID: CASE_XXX_YYYYMMDD_HHMMSS"""
    count = get_case_count() + 1
    return f"CASE_{count:03d}_{timestamp}"

def get_next_case_id() -> str:
    """获取下一个 CASE_ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return parse_case_id(timestamp)

# ========== 校验函数 ==========
def validate_required(args) -> list:
    """校验所有必填字段，返回错误列表"""
    errors = []
    
    if not args.problem or not args.problem.strip():
        errors.append("--problem 为必填，不能为空")
    
    if not args.model or not args.model.strip():
        errors.append("--model 为必填，不能为空")
    elif args.model not in VALID_MODELS:
        errors.append(f"--model 无效，有效值：{', '.join(VALID_MODELS)}")
    
    if not args.formula or not args.formula.strip():
        errors.append("--formula 为必填，不能为空")
    else:
        formulas = [f.strip() for f in args.formula.split(",")]
        invalid = [f for f in formulas if f not in VALID_FORMULAS]
        if invalid:
            errors.append(f"--formula 包含无效值：{', '.join(invalid)}，有效值：{', '.join(VALID_FORMULAS)}")
    
    if not args.result or not args.result.strip():
        errors.append("--result 为必填，不能为空")
    elif args.result not in VALID_RESULTS:
        errors.append(f"--result 无效，有效值：{', '.join(VALID_RESULTS)}")
    
    if not args.description or not args.description.strip():
        errors.append("--description 为必填，不能为空")
    elif args.result == "成功" and not args.description.startswith("成功原因："):
        errors.append("--description 格式错误：成功时必须以「成功原因：」开头")
    elif args.result == "失败" and not args.description.startswith("失败原因："):
        errors.append("--description 格式错误：失败时必须以「失败原因：」开头")
    elif args.result == "部分成功" and not args.description.startswith("部分成功："):
        errors.append("--description 格式错误：部分成功时必须以「部分成功：」开头")
    
    if args.time is None:
        errors.append("--time 为必填，不能为空")
    elif not isinstance(args.time, int) or args.time < 0:
        errors.append("--time 必须为非负整数")
    
    if args.experiments is None:
        errors.append("--experiments 为必填，不能为空")
    elif not isinstance(args.experiments, int) or args.experiments < 0:
        errors.append("--experiments 必须为非负整数")
    
    return errors

# ========== CASE 文件操作 ==========
def create_case_file(case_id: str, args) -> Path:
    """创建 CASE 文件"""
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# {case_id}

**创建时间**: {create_time}

---

## 编号
{case_id}

---

## 问题
{args.problem.strip()}

---

## 心智模型
{args.model.strip()}

---

## 逻辑公式
{args.formula.strip()}

---

## 结果
{args.result.strip()}

---

## 结果描述
{args.description.strip()}

---

## 处理时间（分钟）
{args.time}

---

## 实验次数
{args.experiments}

"""

    # 只有当 switch 有值时才添加
    if args.switch and args.switch.strip():
        content += f"""---

## 切换记录
{args.switch.strip()}

"""

    content += f"""---

_由 holmes_case_logger.py 自动生成_
"""
    
    case_file = CASES_DIR / f"{case_id}.md"
    case_file.write_text(content, encoding="utf-8")
    return case_file

# ========== INDEX 文件操作 ==========
def update_index(case_id: str, args) -> int:
    """更新 index.md，返回案件计数"""
    count = get_case_count() + 1
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    problem_short = args.problem.strip()[:30] + "..." if len(args.problem.strip()) > 30 else args.problem.strip()
    
    if not INDEX_FILE.exists() or INDEX_FILE.read_text(encoding="utf-8").strip() == "":
        # 创建新的 index.md
        index_content = f"""# Autoresearch 案件总览

**案件计数**: {count}
**最后更新**: {create_time}

---

## 案件索引

| 编号 | 日期 | 问题摘要 | 结果 | 处理时间 | 实验次数 |
|------|------|----------|------|----------|----------|
| {case_id} | {create_time} | {problem_short} | {args.result.strip()} | {args.time}分钟 | {args.experiments}次 |
"""
        INDEX_FILE.write_text(index_content, encoding="utf-8")
    else:
        # 追加到现有 index.md
        lines = INDEX_FILE.read_text(encoding="utf-8").split("\n")
        
        # 更新计数
        for i, line in enumerate(lines):
            if "**案件计数**:" in line:
                lines[i] = f"**案件计数**: {count}"
            elif "**最后更新**:" in line:
                lines[i] = f"**最后更新**: {create_time}"
        
        # 在表格最后一行后插入新条目
        new_entry = f"| {case_id} | {create_time} | {problem_short} | {args.result.strip()} | {args.time}分钟 | {args.experiments}次 |"
        
        # 找到表格最后一行（|------）的位置，在其后插入
        for i in range(len(lines) - 1, -1, -1):
            if re.match(r"^\|[-: ]+\|", lines[i]):
                lines.insert(i + 1, new_entry)
                break
        
        INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")
    
    return count

# ========== 主逻辑 ==========
def main():
    parser = argparse.ArgumentParser(
        description="Holmes 案件记录器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
心智模型（--model）：
  链条因果 / 排除法 / 反向工程 / 异常锚定 / 主动验证 / 压缩推理 / 阁楼心智

逻辑公式（--formula，逗号分隔多选）：
  排除法 / 选言推理 / 假言推理 / 逆否推理 / 传递公式 / 必要条件 / 矛盾触发 / 因果链 / 或然性推理 / 异常锚定 / 主动验证 / 反向工程 / 归谬法

结果（--result）：成功 / 失败 / 部分成功

示例：
  成功：
    python3 scripts/holmes_case_logger.py --problem "系统bug排查" --model "链条因果" --formula "因果链,逆否推理" --result "成功" --description "成功原因：采用了XX方法..." --time 5 --experiments 1

  失败：
    python3 scripts/holmes_case_logger.py --problem "推理题" --model "异常锚定" --formula "排除法,因果链" --result "失败" --description "失败原因：推理深度不足..." --time 15 --experiments 1

  部分成功（有切换）：
    python3 scripts/holmes_case_logger.py --problem "用户分析" --model "排除法" --formula "排除法,或然性推理" --result "部分成功" --description "部分成功：XX部分做到了...；XX部分没做到..." --time 20 --experiments 2 --switch "线索不足：从行为数据切换到访谈法"
"""
    )
    
    parser.add_argument("--problem", type=str, help="问题描述（一句话）")
    parser.add_argument("--model", type=str, help=f"心智模型（必须是有效值之一）")
    parser.add_argument("--formula", type=str, help=f"逻辑公式（逗号分隔，可多选）")
    parser.add_argument("--result", type=str, help=f"结果（{', '.join(VALID_RESULTS)}）")
    parser.add_argument("--description", type=str, help="结果描述（必填，成功以「成功原因：」开头，失败以「失败原因：」开头，部分成功以「部分成功：」开头）")
    parser.add_argument("--time", type=int, help="处理时间（分钟）")
    parser.add_argument("--experiments", type=int, help="实验次数")
    parser.add_argument("--switch", type=str, help="切换记录（非必填，有切换时填写）")
    
    args = parser.parse_args()
    
    # 初始化目录
    init_dirs()
    
    # 校验必填字段
    errors = validate_required(args)
    if errors:
        print("❌ 参数校验失败：")
        for e in errors:
            print(f"   - {e}")
        print("\n使用 --help 查看帮助")
        exit(1)
    
    # 生成 CASE_ID
    case_id = get_next_case_id()
    
    # 创建 CASE 文件
    case_file = create_case_file(case_id, args)
    print(f"✅ CASE 文件已创建：{case_file}")
    
    # 更新 INDEX
    count = update_index(case_id, args)
    print(f"📊 当前案件计数：{count}")
    
    # 检查是否触发 Autoresearch
    if count % 3 == 0:
        print("\n" + "=" * 50)
        print("🚨 达到 3 个案件触发阈值！")
        print("=" * 50)
        print("请执行迭代分析：")
        print("1. 读取 .autoresearch/cases/ 下最近 3 个 CASE 文件")
        print("2. 按 references/autoresearch.md 流程执行迭代分析")
        print("3. 更新 SKILL.md / holmes-learnings.md / holmes-lessons.md")
        print("4. Git commit 提交变更")
        print("\n完整流程见：references/autoresearch.md")
    else:
        remaining = 3 - (count % 3)
        print(f"\n💡 还差 {remaining} 个案件触发 Autoresearch")

if __name__ == "__main__":
    main()