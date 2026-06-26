#!/usr/bin/env python3
"""
integrated_state.py - Neuro-Agent 状态整合器
===============================
每次对话开始时，Rezz 调用这个脚本获取 Neuro-Agent 的完整状态，
然后把状态编织进回复里。

用法：
    python3 scripts/integrated_state.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_neuro_state():
    """获取 Neuro-Agent 完整状态"""
    state = {
        "status": "ok",
        "desire": None,
        "self_narrative": None,
        "recent_learning": None,
        "memory_summary": None
    }
    
    # 1. 愿望系统状态（使用默认持久化路径）
    try:
        from limbic.desire import DesireSystem
        ds = DesireSystem()  # 默认路径：~/.openclaw/workspace/neuro_claw/desire/
        top = ds.get_top_desire()
        impulses = ds.get_impulses()
        state["desire"] = {
            "top": {
                "type": top.desire_type if top else None,
                "intensity": f"{top.intensity_value:.0%}" if top else None,
                "category": top.category.value if top else None
            },
            "impulses_count": len(impulses),
            "impulses": [{"type": i.desire_type, "intensity": f"{i.intensity_value:.0%}"} for i in impulses[:3]]
        }
    except Exception as e:
        state["desire"] = {"error": str(e)}
    
    # 2. 自我叙事状态（使用默认持久化路径）
    try:
        from scripts.self_narrative import SelfNarrative
        narrator = SelfNarrative()  # 默认路径：~/.openclaw/workspace/neuro_claw/self_narrative/
        identity = narrator.get_self_identity()
        state["self_narrative"] = {
            "core_traits": identity.core_traits[-3:] if identity.core_traits else [],
            "relationship_stage": identity.relationship_stage,
            "growth_count": len(identity.growth_log)
        }
    except Exception as e:
        state["self_narrative"] = {"error": str(e)}
    
    # 3. 三层记忆摘要（使用默认持久化路径）
    try:
        from temporal.memory_system import ThreeLayerMemory
        mem = ThreeLayerMemory()  # 默认路径：~/.openclaw/workspace/neuro_claw/memory/
        today = __import__("datetime").date.today().isoformat()
        summary = mem.generate_daily_summary(today)
        state["memory_summary"] = {
            "today_events": summary.get("total_events", 0),
            "emotions": summary.get("emotions", [])[:3],
            "important": summary.get("important_events", [])[:2]
        }
    except Exception as e:
        state["memory_summary"] = {"error": str(e)}
    
    return state

if __name__ == "__main__":
    state = get_neuro_state()
    print(json.dumps(state, ensure_ascii=False, indent=2))
