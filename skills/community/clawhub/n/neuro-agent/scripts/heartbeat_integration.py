"""
scripts/heartbeat_integration.py
===================================
心跳集成层 - 将三个核心系统接入心跳主流程

集成内容：
1. 愿望系统  → 心跳时触发欲望
2. 情景预演  → 心跳时预演下一步陪伴策略
3. 自我叙事  → 记录每日重大事件供复盘使用

调用时机：
  heartbeat_processor.py 的 analyze_recent_conversations() 末尾
  即每次心跳（每30分钟）自动调用

调用方式：
  from scripts.heartbeat_integration import run_heartbeat_integration
  result = run_heartbeat_integration(report, user_name="AlfredLi")
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
DAILY_EVENTS_FILE = DATA_DIR / "daily_events.jsonl"


# ============ 每日事件记录 ============


def record_daily_event(
    event_type: str,
    event_desc: str,
    emotion: Optional[str] = None,
    intensity: float = 0.0,
    metadata: Optional[Dict] = None
) -> None:
    """
    记录一天的重大事件，供 dream_process.py 复盘使用

    event_type:
      - care_sent        : 发送了关怀消息
      - emotion_spike    : 检测到情绪波动
      - desire_triggered  : 触发了强烈欲望
      - social_learning  : 执行了社会化学习
      - conversation     : 有重要对话
      - rejection        : 用户拒绝了关怀
    """
    event = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "event_type": event_type,
        "description": event_desc,
        "emotion": emotion,
        "intensity": intensity,
        "metadata": metadata or {},
    }

    DAILY_EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DAILY_EVENTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def get_today_events() -> list[Dict]:
    """读取今天的所有事件"""
    today = datetime.now().strftime("%Y-%m-%d")
    events = []
    if DAILY_EVENTS_FILE.exists():
        try:
            with open(DAILY_EVENTS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        if event.get("date") == today:
                            events.append(event)
                    except Exception:
                        continue
        except Exception:
            pass
    return events


# ============ 三大系统集成 ============


def run_heartbeat_integration(
    heartbeat_report: Dict[str, Any],
    user_name: str = "AlfredLi"
) -> Dict[str, Any]:
    """
    心跳集成主函数

    在 heartbeat_processor 每次运行完毕后调用
    依次触发：愿望系统 → 情景预演 → 事件记录

    参数：
      heartbeat_report: heartbeat_processor 返回的报告字典
      user_name: 用户称呼（用于个性化）

    返回：
      集成结果，包含三个子系统的输出摘要
    """
    result = {
        "timestamp": datetime.now().isoformat(),
        "desire_system": None,
        "scenario_preview": None,
        "event_recorded": None,
    }

    dominant = heartbeat_report.get("dominant_emotion", "neutral")
    intensity = heartbeat_report.get("dominant_intensity", 0.0)
    emotion_scores = heartbeat_report.get("emotions", {})
    messages_count = heartbeat_report.get("messages_analyzed", 0)
    care_triggered = heartbeat_report.get("care_triggered", False)

    # ─── 1. 愿望系统 ───────────────────────────────
    try:
        from limbic.desire import trigger_wishes_from_heartbeat
        desire_result = trigger_wishes_from_heartbeat(
            dominant_emotion=dominant,
            emotion_intensity=intensity,
            emotion_scores=emotion_scores,
            messages_analyzed=messages_count,
            care_triggered=care_triggered,
            user_name=user_name,
        )
        result["desire_system"] = desire_result

        # 如果有冲动，记录事件
        if desire_result.get("impulse_count", 0) > 0:
            top = desire_result.get("top_desire")
            if top:
                record_daily_event(
                    event_type="desire_triggered",
                    event_desc=f"触发欲望：{top.get('desire_type', '')}",
                    emotion=dominant,
                    intensity=intensity,
                    metadata={"top_desire": top}
                )
    except Exception as e:
        result["desire_system"] = {"error": str(e)}

    # ─── 2. 情景预演 ───────────────────────────────
    try:
        from prefrontal.preview_engine import run_scenario_preview
        preview_result = run_scenario_preview(
            current_emotion=dominant,
            emotion_intensity=intensity,
            context={
                "messages_analyzed": messages_count,
                "care_triggered": care_triggered,
                "user_name": user_name,
            }
        )
        result["scenario_preview"] = preview_result
    except Exception as e:
        result["scenario_preview"] = {"error": str(e)}

    # ─── 3. 事件记录 ───────────────────────────────
    try:
        if care_triggered:
            record_daily_event(
                event_type="care_sent",
                event_desc=f"发送关怀消息：{heartbeat_report.get('care_message', '')}",
                emotion=dominant,
                intensity=intensity,
            )
        elif intensity >= 0.8:
            record_daily_event(
                event_type="emotion_spike",
                event_desc=f"检测到高强度情绪：{dominant} ({intensity:.2f})",
                emotion=dominant,
                intensity=intensity,
            )
        elif messages_count > 0:
            record_daily_event(
                event_type="conversation",
                event_desc=f"分析了 {messages_count} 条消息",
                emotion=dominant,
                intensity=intensity,
            )
        result["event_recorded"] = {"status": "ok", "today_events": len(get_today_events())}
    except Exception as e:
        result["event_recorded"] = {"error": str(e)}

    return result


# ============ CLI 入口 ============

if __name__ == "__main__":
    # 测试用
    print("=== 心跳集成层测试 ===")
    test_report = {
        "dominant_emotion": "exhaustion",
        "dominant_intensity": 1.5,
        "emotions": {"exhaustion": 1.5, "stress": 0.8},
        "messages_analyzed": 12,
        "care_triggered": True,
        "care_message": "AlfredLi阁下，是否累了？",
    }
    result = run_heartbeat_integration(test_report, user_name="AlfredLi")
    print(json.dumps(result, ensure_ascii=False, indent=2))
