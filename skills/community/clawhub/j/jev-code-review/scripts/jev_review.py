#!/usr/bin/env python3
"""
Jev 模拟代码评审 - 主脚本
对代码变更进行结构化评审
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from primitives import JevPrimitive


def get_code_from_file(filepath: str) -> str:
    """从文件读取代码"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def get_code_from_diff(diff_file: str) -> str:
    """从 diff 文件读取变更"""
    with open(diff_file, 'r', encoding='utf-8') as f:
        return f.read()


def get_code_from_commit(commit_ref: str) -> str:
    """从 Git 提交获取变更"""
    try:
        result = subprocess.run(
            ["git", "show", commit_ref],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"Error getting commit: {e}"


def get_code_from_stdin() -> str:
    """从标准输入读取"""
    return sys.stdin.read()


def review_code(code: str, filename: str = "unknown") -> dict:
    """
    对代码进行 Jev 模拟评审
    
    并行提问 5 个原子问题：
    1. 安全性 (Noul)
    2. 正确性 (Noul)
    3. 可维护性 (Score 1-5)
    4. 性能 (Score 1-5)
    5. 需要人工审查 (Noul)
    """
    jev = JevPrimitive()
    
    # 截断过长的代码
    code_truncated = code[:6000] if len(code) > 6000 else code
    state = f"文件: {filename}\n\n代码内容:\n```\n{code_truncated}\n```"
    
    # 定义问题
    questions = {
        "security": {
            "type": "noul",
            "instructions": "这段代码是否引入了安全风险？",
            "criteria": {
                "true": "存在 SQL注入、XSS、硬编码密钥、路径遍历、命令注入等安全风险",
                "false": "未发现明显的安全风险"
            },
            "threshold": 0.7,
            "flag_condition": lambda x: x > 0.7
        },
        "correctness": {
            "type": "noul",
            "instructions": "这段代码是否可能引入 bug？",
            "criteria": {
                "true": "存在空指针、边界条件错误、资源泄漏、并发问题、逻辑错误等",
                "false": "代码逻辑正确，不易引入 bug"
            },
            "threshold": 0.6,
            "flag_condition": lambda x: x > 0.6
        },
        "maintainability": {
            "type": "score",
            "instructions": "代码的可维护性如何？",
            "scale": (1, 5),
            "criteria": {
                "1": "难以维护，命名混乱，函数过长，无注释，复杂度高",
                "2": "可维护性较差，部分问题明显",
                "3": "中等水平，基本可维护但有改进空间",
                "4": "良好，命名清晰，结构合理",
                "5": "优秀，代码清晰，注释完善，易于维护"
            },
            "threshold": 3,
            "flag_condition": lambda x: x < 3
        },
        "performance": {
            "type": "score",
            "instructions": "这段代码是否有性能隐患？",
            "scale": (1, 5),
            "criteria": {
                "1": "严重性能问题，如 N+1 查询、循环内 IO、大数据量无分页",
                "2": "较明显的性能隐患",
                "3": "一般，可能存在性能问题取决于使用场景",
                "4": "性能良好，无明显隐患",
                "5": "性能优秀，经过优化"
            },
            "threshold": 3,
            "flag_condition": lambda x: x < 3
        }
    }
    
    # 并行评审（实际串行，但逻辑上是独立的）
    results = {}
    flagged = []
    
    for key, q in questions.items():
        print(f"[Jev] Evaluating {key}...", file=sys.stderr)
        
        if q["type"] == "noul":
            result = jev.noul(state, q["instructions"], q.get("criteria"))
            is_flagged = q["flag_condition"](result["answer"])
        elif q["type"] == "score":
            result = jev.score(state, q["instructions"], q.get("scale", (1, 5)), q.get("criteria"))
            is_flagged = q["flag_condition"](result["answer"])
        else:
            continue
        
        result["threshold"] = q["threshold"]
        result["flagged"] = is_flagged
        results[key] = result
        
        if is_flagged:
            flagged.append(key)
    
    # 综合判断：是否需要人工审查
    needs_human_prob = 0.0
    if flagged:
        # 如果有任何标记，根据严重程度计算概率
        if "security" in flagged:
            needs_human_prob = 0.9
        elif "correctness" in flagged:
            needs_human_prob = 0.7
        elif len(flagged) >= 2:
            needs_human_prob = 0.6
        else:
            needs_human_prob = 0.4
    
    results["needs_human"] = {
        "type": "noul",
        "question": "是否需要人工介入审查？",
        "answer": needs_human_prob,
        "threshold": 0.5,
        "flagged": needs_human_prob > 0.5
    }
    
    # 生成总结
    max_risk = None
    max_risk_value = 0
    for key in ["security", "correctness"]:
        if key in results:
            val = results[key]["answer"]
            if val > max_risk_value:
                max_risk_value = val
                max_risk = f"{key} ({val:.2f})"
    
    if "maintainability" in results:
        val = 5 - results["maintainability"]["answer"]  # 反转，分数越低风险越高
        if val > max_risk_value:
            max_risk_value = val
            max_risk = f"maintainability ({results['maintainability']['answer']}/5)"
    
    recommendation = "PASS"
    if results["security"]["flagged"]:
        recommendation = "BLOCK"
    elif results["needs_human"]["flagged"]:
        recommendation = "REVIEW"
    elif len(flagged) > 0:
        recommendation = "WARN"
    
    return {
        "file": filename,
        "timestamp": datetime.now().isoformat(),
        "code_length": len(code),
        "review": results,
        "summary": {
            "flagged_count": len(flagged),
            "flagged_items": flagged,
            "max_risk": max_risk,
            "recommendation": recommendation
        }
    }


def format_output(result: dict, use_json: bool = False):
    """格式化输出"""
    if use_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    # 人类可读格式
    print(f"\n{'='*60}")
    print(f"Jev Code Review: {result['file']}")
    print(f"{'='*60}")
    print(f"Code length: {result['code_length']} chars")
    print(f"Timestamp: {result['timestamp']}")
    print()
    
    # 各维度结果
    for key, data in result["review"].items():
        icon = "✅" if not data["flagged"] else "🚩"
        print(f"{icon} {key.upper():20}", end="")
        
        if data["type"] == "noul":
            print(f" {data['answer']:.2f} (threshold: {data['threshold']})")
        elif data["type"] == "score":
            print(f" {data['answer']}/5 (confidence: {data.get('confidence', 0):.2f})")
        
        if data["flagged"]:
            print(f"   ⚠️  FLAGGED: {data['question']}")
        print()
    
    # 总结
    summary = result["summary"]
    print(f"{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Flagged items: {summary['flagged_count']}")
    if summary['flagged_items']:
        print(f"  - {', '.join(summary['flagged_items'])}")
    print(f"Max risk: {summary['max_risk']}")
    print(f"Recommendation: ", end="")
    
    rec = summary['recommendation']
    if rec == "PASS":
        print("✅ PASS - 代码通过评审")
    elif rec == "WARN":
        print("🟡 WARN - 建议修复标记项")
    elif rec == "REVIEW":
        print("👀 REVIEW - 需要人工审查")
    elif rec == "BLOCK":
        print("🔴 BLOCK - 必须修复安全问题")
    print()


def main():
    parser = argparse.ArgumentParser(description="Jev Code Review (LLM 模拟)")
    parser.add_argument("--file", help="要评审的文件路径")
    parser.add_argument("--diff", help="要评审的 diff 文件")
    parser.add_argument("--commit", help="要评审的 Git 提交")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取代码")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--threshold-security", type=float, default=0.7, help="安全阈值")
    parser.add_argument("--threshold-correctness", type=float, default=0.6, help="正确性阈值")
    
    args = parser.parse_args()
    
    # 获取代码
    code = ""
    filename = "unknown"
    
    if args.file:
        code = get_code_from_file(args.file)
        filename = args.file
    elif args.diff:
        code = get_code_from_diff(args.diff)
        filename = f"diff:{args.diff}"
    elif args.commit:
        code = get_code_from_commit(args.commit)
        filename = f"commit:{args.commit}"
    elif args.stdin:
        code = get_code_from_stdin()
        filename = "stdin"
    else:
        parser.print_help()
        sys.exit(1)
    
    # 评审
    result = review_code(code, filename)
    
    # 输出
    format_output(result, args.json)


if __name__ == "__main__":
    main()
