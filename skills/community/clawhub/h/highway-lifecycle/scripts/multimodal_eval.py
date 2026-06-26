#!/usr/bin/env python3
"""
多模态模型评测工具
用于高速公路事件检测、隧道特征分析、道路病害检测的模型评测
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    HIGHWAY_EVENT = "highway_event"
    TUNNEL_FEATURE = "tunnel_feature"
    ROAD_DAMAGE = "road_damage"


@dataclass
class EvalResult:
    task_type: TaskType
    model_name: str
    precision: float
    recall: float
    f1: float
    accuracy: Optional[float] = None


# 事件检测标签
HIGHWAY_EVENT_LABELS = [
    "is_normal_status",
    "is_congestion",
    "is_abnormal_stop",
    "is_accident",
    "is_fire",
    "is_spillage",
    "is_pedestrian",
    "is_illegal_vehicle",
    "is_construction_rescue",
]

# 道路病害标签
ROAD_DAMAGE_LABELS = ["D00", "D10", "D20", "D40", "Repair"]


def calculate_metrics(tp: int, fp: int, fn: int) -> Dict[str, float]:
    """计算Precision, Recall, F1"""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return {"precision": precision, "recall": recall, "f1": f1}


def evaluate_multilabel(
    predictions: List[Dict], ground_truths: List[Dict], labels: List[str]
) -> Dict:
    """评估多标签分类任务"""
    results = {}
    
    for label in labels:
        tp = fp = fn = 0
        for pred, gt in zip(predictions, ground_truths):
            pred_val = pred.get(label, False)
            gt_val = gt.get(label, False)
            
            if pred_val and gt_val:
                tp += 1
            elif pred_val and not gt_val:
                fp += 1
            elif not pred_val and gt_val:
                fn += 1
        
        metrics = calculate_metrics(tp, fp, fn)
        results[label] = metrics
    
    # 计算Macro F1
    macro_f1 = sum(r["f1"] for r in results.values()) / len(results)
    macro_precision = sum(r["precision"] for r in results.values()) / len(results)
    macro_recall = sum(r["recall"] for r in results.values()) / len(results)
    
    results["macro"] = {
        "precision": macro_precision,
        "recall": macro_recall,
        "f1": macro_f1,
    }
    
    return results


def evaluate_tunnel_qa(
    predictions: List[str], ground_truths: List[str], llm_judge=None
) -> Dict:
    """评估隧道特征问答任务（LLM-as-judge）"""
    correct = 0
    total = len(predictions)
    
    for pred, gt in zip(predictions, ground_truths):
        # 简单字符串匹配（实际应用中使用LLM-as-judge）
        if gt.lower() in pred.lower() or pred.lower() in gt.lower():
            correct += 1
        elif llm_judge:
            # 使用LLM判断
            is_correct = llm_judge(gt, pred)
            if is_correct:
                correct += 1
    
    accuracy = correct / total if total > 0 else 0
    return {"accuracy": accuracy, "correct": correct, "total": total}


def generate_eval_report(results: Dict, task_type: TaskType) -> str:
    """生成评测报告"""
    report = []
    report.append(f"# {task_type.value} 评测报告\n")
    
    if task_type == TaskType.HIGHWAY_EVENT:
        report.append("## 各类别指标\n")
        report.append("| 类别 | Precision | Recall | F1 |\n")
        report.append("|------|-----------|--------|----|\n")
        
        for label, metrics in results.items():
            if label != "macro":
                report.append(
                    f"| {label} | {metrics['precision']:.4f} | "
                    f"{metrics['recall']:.4f} | {metrics['f1']:.4f} |\n"
                )
        
        report.append("\n## 整体指标\n")
        macro = results.get("macro", {})
        report.append(f"- **Macro Precision**: {macro.get('precision', 0):.4f}\n")
        report.append(f"- **Macro Recall**: {macro.get('recall', 0):.4f}\n")
        report.append(f"- **Macro F1**: {macro.get('f1', 0):.4f}\n")
    
    elif task_type == TaskType.TUNNEL_FEATURE:
        report.append("## 问答准确率\n")
        report.append(f"- **Accuracy**: {results['accuracy']:.4f}\n")
        report.append(f"- **Correct**: {results['correct']}/{results['total']}\n")
    
    elif task_type == TaskType.ROAD_DAMAGE:
        report.append("## 各病害类型指标\n")
        report.append("| 病害代码 | Precision | Recall | F1 |\n")
        report.append("|---------|-----------|--------|----|\n")
        
        for label, metrics in results.items():
            if label != "macro":
                report.append(
                    f"| {label} | {metrics['precision']:.4f} | "
                    f"{metrics['recall']:.4f} | {metrics['f1']:.4f} |\n"
                )
    
    return "\n".join(report)


def run_evaluation(
    task_type: TaskType,
    predictions_file: str,
    ground_truth_file: str,
    output_file: Optional[str] = None,
) -> Dict:
    """运行评测"""
    # 加载数据
    predictions = json.loads(Path(predictions_file).read_text())
    ground_truths = json.loads(Path(ground_truth_file).read_text())
    
    # 选择评测方法
    if task_type == TaskType.HIGHWAY_EVENT:
        results = evaluate_multilabel(predictions, ground_truths, HIGHWAY_EVENT_LABELS)
    elif task_type == TaskType.ROAD_DAMAGE:
        results = evaluate_multilabel(predictions, ground_truths, ROAD_DAMAGE_LABELS)
    elif task_type == TaskType.TUNNEL_FEATURE:
        results = evaluate_tunnel_qa(predictions, ground_truths)
    else:
        raise ValueError(f"Unknown task type: {task_type}")
    
    # 生成报告
    report = generate_eval_report(results, task_type)
    print(report)
    
    # 保存结果
    if output_file:
        Path(output_file).write_text(json.dumps(results, indent=2, ensure_ascii=False))
    
    return results


def model_selection_guide(requirements: Dict) -> str:
    """模型选型建议"""
    guide = []
    guide.append("# 模型选型建议\n")
    
    task = requirements.get("task", "")
    priority = requirements.get("priority", "balanced")
    resources = requirements.get("resources", "limited")
    
    if "事件检测" in task:
        guide.append("## 高速事件检测\n")
        if priority == "speed":
            guide.append("- 推荐：Qwen3-VL-30B（性价比高，1卡A800）\n")
        elif priority == "accuracy":
            guide.append("- 推荐：Qwen3-VL-235B（精度最高，8卡A800）\n")
        else:
            guide.append("- 推荐：Qwen3-VL-30B（初筛） + Qwen3-VL-235B（复核）\n")
        guide.append("- 注意：禁用Think模式\n")
    
    elif "隧道" in task:
        guide.append("## 隧道特征分析\n")
        if priority == "accuracy":
            guide.append("- 推荐：Qwen3-VL-235B-Think（推理最强）\n")
        else:
            guide.append("- 推荐：GLM-4.5V-106B（地质知识好，4卡A800）\n")
        guide.append("- 建议：启用Think模式\n")
    
    elif "病害" in task or "路面" in task:
        guide.append("## 道路病害检测\n")
        guide.append("- 推荐：Qwen3-VL-235B（综合最优）\n")
        guide.append("- 备选：InternVL-241B（修补识别好）\n")
        guide.append("- 建议：启用Think模式减少误判\n")
    
    return "\n".join(guide)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="多模态模型评测工具")
    parser.add_argument("task", choices=["highway", "tunnel", "damage"], help="任务类型")
    parser.add_argument("--pred", required=True, help="预测结果文件")
    parser.add_argument("--gt", required=True, help="真值文件")
    parser.add_argument("--output", help="输出文件")
    
    args = parser.parse_args()
    
    task_map = {
        "highway": TaskType.HIGHWAY_EVENT,
        "tunnel": TaskType.TUNNEL_FEATURE,
        "damage": TaskType.ROAD_DAMAGE,
    }
    
    run_evaluation(task_map[args.task], args.pred, args.gt, args.output)