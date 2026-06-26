#!/usr/bin/env python3
"""可解释报告生成器"""

import json
from datetime import datetime

def generate_report(eval_results):
    """生成Markdown报告"""
    retention = eval_results['capability_retention']

    report = f"""# 模型蒸馏评估报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 执行摘要

| 指标 | 数值 |
|------|------|
| 能力保持率 | {retention['retention_rate']:.1%} |
| 基线准确率 | {retention['baseline_accuracy']:.1%} |
| 蒸馏后准确率 | {retention['distilled_accuracy']:.1%} |
| 教师准确率 | {retention['teacher_accuracy']:.1%} |

## 评估结论

{generate_assessment(retention['retention_rate'])}

## 建议

1. 如果保持率 > 80%: 蒸馏成功，可部署
2. 如果保持率 60-80%: 基本可用，可考虑优化
3. 如果保持率 < 60%: 需重新评估目标

---
*自动生成的报告*
"""
    return report

def generate_assessment(retention):
    if retention > 0.8:
        return "✅ **蒸馏非常成功**。学生模型成功学习教师核心能力。"
    elif retention > 0.6:
        return "🟡 **蒸馏基本成功**。有提升空间，建议检查Level 3数据。"
    else:
        return "🔴 **蒸馏未达预期**。建议调整目标或换更大模型。"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-results", required=True)
    parser.add_argument("--output", default="outputs/report.md")
    args = parser.parse_args()

    with open(args.eval_results) as f:
        results = json.load(f)

    report = generate_report(results)
    with open(args.output, 'w') as f:
        f.write(report)

    print(f"报告已生成: {args.output}")
