#!/usr/bin/env python3
"""训练监控与智能诊断"""

import json
import math

def diagnose(loss_history, eval_history=None):
    """诊断训练问题"""
    if not loss_history:
        return {"status": "unknown"}

    initial = loss_history[0]
    final = loss_history[-1]

    # 检查NaN
    if any(math.isnan(x) for x in loss_history):
        return {
            "status": "nan_loss",
            "issue": "损失出现NaN",
            "solution": ["降低学习率至1e-5", "检查数据异常值"]
        }

    # 检查plateau
    if final > initial * 0.9:
        return {
            "status": "underfitting",
            "issue": "损失下降不明显",
            "solution": ["增加学习率", "增加训练轮数"]
        }

    # 检查过拟合
    if eval_history and max(eval_history) > min(eval_history) * 1.5:
        return {
            "status": "overfitting",
            "issue": "验证损失上升",
            "solution": ["早停", "增加dropout", "增加正则化"]
        }

    return {
        "status": "normal",
        "message": f"训练正常: {initial:.3f} -> {final:.3f}"
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--loss-file", required=True)
    args = parser.parse_args()

    with open(args.loss_file) as f:
        data = json.load(f)

    result = diagnose(data.get('train', []), data.get('eval'))
    print(json.dumps(result, indent=2, ensure_ascii=False))
