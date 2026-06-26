#!/usr/bin/env python3
"""
PRD 评审引擎 CLI v3.0

支持命令行调用 requirement-reviewer
"""

import sys
import os
import json
import argparse

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from review_engine import PRDReviewer, IterativeReviewer


def main():
    parser = argparse.ArgumentParser(description='PRD 评审引擎')
    parser.add_argument('--prd', required=True, help='PRD 文件路径')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    parser.add_argument('--auto-detect', action='store_true', help='自动识别场景')
    parser.add_argument('--scenario', choices=['default', 'financial', 'internet'], help='手动指定场景')
    parser.add_argument('--iterative', action='store_true', help='启用迭代评审')
    parser.add_argument('--max-loops', type=int, default=3, help='最大迭代轮数')
    parser.add_argument('--target-score', type=int, default=80, help='目标分数')
    
    args = parser.parse_args()
    
    # 读取 PRD 文件
    if not os.path.exists(args.prd):
        print(json.dumps({
            "error": f"PRD 文件不存在：{args.prd}",
            "overall_score": 0
        }), file=sys.stdout)
        sys.exit(1)
    
    with open(args.prd, 'r', encoding='utf-8') as f:
        prd_content = f.read()
    
    # 创建评审器（静默模式，不打印日志）
    auto_detect = args.auto_detect or (not args.scenario)
    
    # 重定向 stdout 以抑制日志输出
    import io
    old_stdout = sys.stdout
    if args.format == 'json' and not args.iterative:
        sys.stdout = io.StringIO()  # 静默模式（迭代模式需要打印日志）
    
    # 执行评审
    if args.iterative:
        # 迭代评审
        print(f"🔄 启用迭代评审（最多{args.max_loops}轮，目标{args.target_score}分）")
        iterative_reviewer = IterativeReviewer(
            max_loops=args.max_loops,
            target_score=args.target_score,
            auto_fix=True
        )
        result = iterative_reviewer.review_with_iteration(prd_content)
    else:
        # 单次评审
        reviewer = PRDReviewer(
            scenario=args.scenario,
            auto_detect=auto_detect
        )
        result = reviewer.review(prd_content, auto_detect=auto_detect)
    
    # 恢复 stdout
    if args.format == 'json' and not args.iterative:
        sys.stdout = old_stdout
    
    # 输出结果
    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 文本格式
        print(f"PRD 评审报告")
        print(f"============")
        print(f"总分：{result['overall_score']}/100")
        print(f"状态：{result['status']}")
        print(f"场景：{result['scenario']}")
        print(f"问题数：{result['total_issues']}（严重：{result['critical_issues']}）")
        print()
        print("评审器得分:")
        for name, res in result['check_results'].items():
            print(f"  {name}: {res.get('score', 'N/A')}/100")
        print()
        if result['issues']:
            print("主要问题:")
            for issue in result['issues'][:10]:
                print(f"  - [{issue.get('severity', 'N/A')}] {issue.get('title', issue.get('description', 'N/A'))}")


if __name__ == '__main__':
    main()
