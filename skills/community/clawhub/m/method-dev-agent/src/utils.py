"""
工具函数
Method Development Agent - MVP
"""
import re
from datetime import datetime
from typing import Optional


def generate_experiment_number() -> str:
    """生成实验编号"""
    today = datetime.now()
    return f"EXP-{today.strftime('%Y%m%d')}-001"


def validate_cas_number(cas: str) -> bool:
    """验证CAS号格式"""
    if not cas:
        return True  # 可选字段
    
    # CAS号格式: XXXXXXX-XX-X
    pattern = r'^\d{2,7}-\d{2}-\d$'
    return bool(re.match(pattern, cas))


def format_retention_time(rt: float) -> str:
    """格式化保留时间"""
    return f"{rt:.2f} min"


def calculate_resolution(tR1: float, tR2: float, w1: float, w2: float) -> float:
    """
    计算分离度 (Resolution)
    Rs = 2(tR2 - tR1) / (w1 + w2)
    """
    if w1 + w2 == 0:
        return 0.0
    return 2 * (tR2 - tR1) / (w1 + w2)


def calculate_theoretical_plates(tR: float, w: float) -> int:
    """
    计算理论塔板数
    N = 16 * (tR / w)^2
    """
    if w == 0:
        return 0
    return int(16 * (tR / w) ** 2)


def calculate_tailing_factor(f10: float, f05: float) -> float:
    """
    计算拖尾因子
    T = f10 / f05
    f10: 峰高10%处的后沿宽度
    f05: 峰高10%处的前沿宽度
    """
    if f05 == 0:
        return 1.0
    return f10 / f05


def assess_peak_quality(resolution: Optional[float], 
                        tailing_factor: Optional[float],
                        theoretical_plates: Optional[int]) -> str:
    """评估峰质量"""
    issues = []
    
    if resolution is not None and resolution < 1.5:
        issues.append("分离度不足")
    
    if tailing_factor is not None:
        if tailing_factor < 0.9:
            issues.append("前沿峰")
        elif tailing_factor > 2.0:
            issues.append("严重拖尾")
        elif tailing_factor > 1.2:
            issues.append("轻微拖尾")
    
    if theoretical_plates is not None and theoretical_plates < 2000:
        issues.append("柱效较低")
    
    if not issues:
        return "✅ 峰形良好"
    else:
        return "⚠️ " + "；".join(issues)


def suggest_optimization(observations: str, current_conditions: dict) -> list:
    """
    基于观察结果给出优化建议
    这是MVP版本的简单规则引擎
    """
    suggestions = []
    obs_lower = observations.lower()
    
    # 拖尾问题
    if any(word in obs_lower for word in ['拖尾', 'tailing', 'tail']):
        suggestions.append("💡 尝试降低pH或添加离子对试剂改善拖尾")
        suggestions.append("💡 检查色谱柱是否需要更换")
    
    # 分离度问题
    if any(word in obs_lower for word in ['分离', 'resolution', '分离度', '重叠']):
        suggestions.append("💡 尝试降低流速或优化梯度程序")
        suggestions.append("💡 考虑更换色谱柱类型（如C18→苯基柱）")
    
    # 保留时间问题
    if any(word in obs_lower for word in ['保留', 'retention', '太快', '太慢']):
        if '太快' in observations or 'too fast' in obs_lower:
            suggestions.append("💡 增加初始有机相比例或提高流速")
        else:
            suggestions.append("💡 降低初始有机相比例或降低流速")
    
    # 峰形问题
    if any(word in obs_lower for word in ['峰形', 'peak shape', '分叉', 'split']):
        suggestions.append("💡 检查样品溶剂是否与流动相匹配")
        suggestions.append("💡 尝试降低进样量")
    
    if not suggestions:
        suggestions.append("💡 记录当前条件作为参考方法")
        suggestions.append("💡 考虑进行重复性实验验证")
    
    return suggestions


def export_to_csv(data: list, filename: str) -> str:
    """导出数据到CSV"""
    import csv
    import os
    
    filepath = os.path.join('data', 'exports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if not data:
        return ""
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    return filepath
