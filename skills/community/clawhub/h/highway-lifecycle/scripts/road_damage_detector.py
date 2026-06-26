#!/usr/bin/env python3
"""
道路病害检测工具
基于RDD标准的道路损害分类检测
"""

import json
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class DamageType(Enum):
    """道路病害类型（RDD标准）"""
    D00 = "纵向裂缝"  # Longitudinal crack
    D10 = "横向裂缝"  # Transverse crack
    D20 = "龟裂"      # Alligator crack
    D40 = "坑槽"      # Pothole
    REPAIR = "修补"   # Repair patch


@dataclass
class DamageDetection:
    """病害检测结果"""
    damage_type: DamageType
    confidence: float
    bbox: Optional[List[float]] = None  # [x1, y1, x2, y2]
    severity: Optional[str] = None      # light/medium/severe
    area: Optional[float] = None        # 面积（平方米）


# 病害优先级（紧急修复顺序）
DAMAGE_PRIORITY = {
    DamageType.D40: 1,    # 坑槽 - 最紧急
    DamageType.D20: 2,    # 龟裂
    DamageType.D00: 3,    # 纵向裂缝
    DamageType.D10: 4,    # 横向裂缝
    DamageType.REPAIR: 5, # 修补 - 不需处理
}


# 病害特征描述
DAMAGE_FEATURES = {
    DamageType.D00: {
        "name": "纵向裂缝",
        "description": "平行于行车方向的裂缝",
        "features": ["沿车道方向延伸", "通常与路肩或车道线平行"],
        "confusion": ["车道线", "轮胎印", "路肩边缘"],
        "difficulty": "中等",
    },
    DamageType.D10: {
        "name": "横向裂缝",
        "description": "垂直于行车方向的裂缝",
        "features": ["横穿车道", "特征明显", "不易与车道线混淆"],
        "confusion": ["施工缝", "温度裂缝"],
        "difficulty": "低",
    },
    DamageType.D20: {
        "name": "龟裂",
        "description": "网状密集裂缝",
        "features": ["网状纹理", "多方向交织", "面积较大"],
        "confusion": ["粗糙路面", "老化沥青"],
        "difficulty": "高",
    },
    DamageType.D40: {
        "name": "坑槽",
        "description": "路面凹陷破损",
        "features": ["3D凹陷特征", "边缘清晰", "可见底部"],
        "confusion": ["修补区域", "阴影"],
        "difficulty": "高",
        "urgency": "紧急",
    },
    DamageType.REPAIR: {
        "name": "修补",
        "description": "已修复区域",
        "features": ["色块差异", "边界清晰", "材料不同"],
        "confusion": ["坑槽"],
        "difficulty": "中等",
    },
}


def analyze_damage_confusion(predictions: List[Dict], ground_truths: List[Dict]) -> Dict:
    """分析病害混淆矩阵"""
    confusion = {dt.value: {} for dt in DamageType}
    
    for pred, gt in zip(predictions, ground_truths):
        pred_type = pred.get("damage_type", "unknown")
        gt_type = gt.get("damage_type", "unknown")
        
        if gt_type not in confusion:
            confusion[gt_type] = {}
        if pred_type not in confusion[gt_type]:
            confusion[gt_type][pred_type] = 0
        confusion[gt_type][pred_type] += 1
    
    return confusion


def prioritize_damages(detections: List[DamageDetection]) -> List[DamageDetection]:
    """按紧急程度排序病害"""
    return sorted(
        detections,
        key=lambda d: DAMAGE_PRIORITY.get(d.damage_type, 999)
    )


def calculate_far(predictions: List[Dict], threshold: float = 0.5) -> float:
    """计算误报率（False Alarm Rate）"""
    false_alarms = sum(1 for p in predictions if p.get("confidence", 0) >= threshold and not p.get("is_damage", True))
    total = len(predictions)
    return false_alarms / total if total > 0 else 0


def generate_damage_report(detections: List[DamageDetection]) -> str:
    """生成病害检测报告"""
    report = []
    report.append("# 道路病害检测报告\n")
    
    # 统计
    damage_counts = {}
    for dt in DamageType:
        count = sum(1 for d in detections if d.damage_type == dt)
        if count > 0:
            damage_counts[dt] = count
    
    report.append("## 检测统计\n")
    report.append("| 病害类型 | 数量 | 紧急程度 |\n")
    report.append("|---------|------|----------|\n")
    
    for dt, count in sorted(damage_counts.items(), key=lambda x: DAMAGE_PRIORITY.get(x[0], 999)):
        priority = "紧急" if DAMAGE_PRIORITY.get(dt, 999) == 1 else "一般"
        report.append(f"| {dt.value} | {count} | {priority} |\n")
    
    # 详细列表
    report.append("\n## 详细病害列表\n")
    
    for i, det in enumerate(prioritize_damages(detections), 1):
        report.append(f"### {i}. {det.damage_type.value}\n")
        report.append(f"- **置信度**: {det.confidence:.2%}\n")
        if det.severity:
            report.append(f"- **严重程度**: {det.severity}\n")
        if det.area:
            report.append(f"- **面积**: {det.area:.2f} m²\n")
        if det.bbox:
            report.append(f"- **位置**: [{det.bbox[0]:.0f}, {det.bbox[1]:.0f}, {det.bbox[2]:.0f}, {det.bbox[3]:.0f}]\n")
        report.append("\n")
    
    # 修复建议
    report.append("## 修复建议\n")
    
    urgent = [d for d in detections if d.damage_type == DamageType.D40]
    if urgent:
        report.append(f"- **紧急**: 发现 {len(urgent)} 处坑槽，建议立即修复\n")
    
    alligator = [d for d in detections if d.damage_type == DamageType.D20]
    if alligator:
        report.append(f"- **重要**: 发现 {len(alligator)} 处龟裂，建议近期修复\n")
    
    cracks = [d for d in detections if d.damage_type in (DamageType.D00, DamageType.D10)]
    if cracks:
        report.append(f"- **一般**: 发现 {len(cracks)} 条裂缝，建议定期维护\n")
    
    return "\n".join(report)


def check_model_confusion_pattern(predictions: List[Dict]) -> Dict:
    """检测模型混淆模式"""
    patterns = {
        "横纵混淆": 0,  # 横向判断为纵向或反之
        "病害修补混淆": 0,  # 坑槽判断为修补或反之
        "裂缝遗漏": 0,  # 存在裂缝但未检测
    }
    
    for pred in predictions:
        pred_type = pred.get("predicted", "")
        true_type = pred.get("ground_truth", "")
        
        # 横纵裂缝混淆
        if (pred_type in ("D00", "D10") and true_type in ("D00", "D10") and pred_type != true_type):
            patterns["横纵混淆"] += 1
        
        # 坑槽与修补混淆
        if (pred_type in ("D40", "REPAIR") and true_type in ("D40", "REPAIR") and pred_type != true_type):
            patterns["病害修补混淆"] += 1
    
    return patterns


def suggest_model_optimization(patterns: Dict) -> List[str]:
    """根据混淆模式提出优化建议"""
    suggestions = []
    
    if patterns.get("横纵混淆", 0) > 5:
        suggestions.append(
            "横纵裂缝混淆严重，建议：\n"
            "1. 提供车道线作为参照物\n"
            "2. 增加方向性标注\n"
            "3. 考虑合并横纵裂缝类别"
        )
    
    if patterns.get("病害修补混淆", 0) > 3:
        suggestions.append(
            "坑槽与修补混淆较多，建议：\n"
            "1. 增加修补样本的负样本\n"
            "2. 标注边缘特征差异\n"
            "3. 使用纹理特征增强"
        )
    
    if not suggestions:
        suggestions.append("模型表现良好，暂无特殊优化建议")
    
    return suggestions


if __name__ == "__main__":
    # 示例使用
    sample_detections = [
        DamageDetection(DamageType.D40, 0.92, [100, 200, 150, 260], "severe", 0.5),
        DamageDetection(DamageType.D20, 0.78, [300, 400, 400, 500], "medium", 1.2),
        DamageDetection(DamageType.D10, 0.85, [500, 100, 700, 110], "light"),
    ]
    
    report = generate_damage_report(sample_detections)
    print(report)