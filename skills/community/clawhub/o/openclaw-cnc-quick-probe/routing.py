#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNC快速探明 - 路由配置
定义何时自动触发此Skill

作者: 海狸 🦫
"""

# 路由规则
ROUTING_RULES = {
    "cnc-quick-probe": {
        # 触发条件
        "trigger_conditions": {
            "intent": ["cnc_quote", "报价", "CNC报价"],
            "convergence_max": 0.8,  # 收敛度低于此值时触发
            "priority": "P1"
        },
        
        # 排除条件（满足任一则不触发）
        "exclude_conditions": {
            "has_complete_params": True,  # 参数已完整
            "user_explicit_skip": True     # 用户明确跳过
        },
        
        # 自动路由优先级
        "route_priority": 10,  # 高优先级
        
        # 路由后的行为
        "after_route": {
            "pause_execution": True,     # 暂停后续执行
            "wait_for_user_input": True,  # 等待用户输入
            "max_retries": 3              # 最多追问3次
        },
        
        # 收敛后自动执行
        "on_converged": {
            "auto_route_to": "cnc-quote-system",
            "pass_context": True
        }
    }
}


# 意图关键词映射
INTENT_KEYWORDS = {
    "cnc_quote": [
        "报价", "CNC", "加工", "零件", "图纸",
        "STEP", "STP", "PDF", "材料", "精度",
        "表面处理", "公差", "Ra", "铝合金", "不锈钢"
    ]
}


def detect_intent(text: str) -> str:
    """检测意图"""
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return intent
    return "unknown"


def should_route_to_quick_probe(context: dict) -> tuple:
    """
    判断是否应该路由到快速探明
    
    Args:
        context: {
            "intent": str,
            "convergence_rate": float,
            "has_file": bool,
            "user_input": str
        }
    
    Returns:
        (should_route: bool, reason: str)
    """
    rules = ROUTING_RULES["cnc-quick-probe"]
    trigger = rules["trigger_conditions"]
    exclude = rules["exclude_conditions"]
    
    # 检查意图
    if context.get("intent") not in trigger["intent"]:
        return False, "非报价意图"
    
    # 检查收敛度
    conv = context.get("convergence_rate", 0)
    if conv >= trigger["convergence_max"]:
        return False, f"收敛度{conv*100:.0f}%已达标"
    
    # 检查排除条件
    if context.get("params_complete") and exclude.get("has_complete_params"):
        return False, "参数已完整"
    
    # 触发
    return True, f"收敛度{conv*100:.0f}%不足，需要探明"


# 导出
__all__ = ["ROUTING_RULES", "INTENT_KEYWORDS", "detect_intent", "should_route_to_quick_probe"]