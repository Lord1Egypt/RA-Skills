#!/usr/bin/env python3
"""
scripts/heartbeat_processor.py
================================
心跳处理脚本 - 被 cron 每30分钟调用
分析最近对话，更新情绪胶囊，生成简报，触发主动关心

用法：
    python3 heartbeat_processor.py              # 默认：增量分析最近2小时
    python3 heartbeat_processor.py --replay    # 回滚：重分析所有历史对话
    python3 heartbeat_processor.py --replay 2026-04-10  # 从指定日期开始重分析
    python3 heartbeat_processor.py --reset       # 重置：清空向量数据库，重新开始
"""

import sys
import json
import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
OUT_FILE = DATA_DIR / "heartbeat_report.json"
SOUL_FILE = WORKSPACE_DIR / "SOUL.md"

# ============ 导入 Neuro-α 模块 ============
try:
    from left_brain.emotion_detector import EmotionDetector
    from left_brain.capsule_factory import CapsuleFactory
    from temporal.short_term_memory import ShortTermMemory
    from temporal.long_term_memory import LongTermMemory
    from temporal.vector_retriever import VectorRetriever
    from core.self_awareness import get_robot_self
    MODULES_OK = True
except ImportError as e:
    MODULES_OK = False
    print(f"[heartbeat_processor] ⚠️ 模块导入失败: {e}")


# ============ 主动关心话术 ============
CARE_MESSAGES: Dict[str, Dict[str, str]] = {
    "exhaustion": {
        "message": "主人，是不是累了？要不要休息一下？今天已经忙了很久了 💙",
        "priority": "high",
    },
    "sadness": {
        "message": "感觉你心情不太好，是发生什么事了吗？想聊聊的话我在这里 🤗",
        "priority": "high",
    },
    "grief": {
        "message": "我知道你现在很难过……我在这里陪着你 🤍",
        "priority": "high",
    },
    "stress": {
        "message": "最近是不是压力很大？别太勉强自己，适当休息一下 💙",
        "priority": "medium",
    },
    "frustration": {
        "message": "遇到挫折了吗？别灰心，我在这里陪着你 🤝",
        "priority": "medium",
    },
    "anger": {
        "message": "看起来你有点生气……需要发泄一下吗？我听着 💙",
        "priority": "medium",
    },
    "fear": {
        "message": "感觉你有点担心……别怕，不管发生什么我都在 🤗",
        "priority": "medium",
    },
    "joy": {
        "message": "看起来心情不错呀！有什么开心的事分享一下？ 😊",
        "priority": "low",
    },
    "excitement": {
        "message": "哇，感觉你很兴奋！有什么好事要告诉我吗？ ✨",
        "priority": "low",
    },
}

# 深夜关怀（更温和）
LATE_NIGHT_CARE: Dict[str, str] = {
    "exhaustion": "主人，早点休息吧……别太累了 💙",
    "sadness": "夜深了还醒着，是不是有心事？想说的时候我在 🤍",
    "stress": "这么晚还没休息，是不是压力很大？别太拼了 💙",
    "frustration": "睡前还在纠结这件事啊……先放松一下，明天再说 🤝",
    "grief": "我在这里陪着你……不管多晚 🤍",
}


# ============ USER.md 读取（获取使用者名字）===========
def _get_user_name_from_user_md() -> str | None:
    """从 USER.md 读取使用者的称呼（优先"AlfredLi"，其次"AlfredLi"）"""
    USER_FILE = Path.home() / ".openclaw" / "workspace" / "USER.md"
    if not USER_FILE.exists():
        return None
    try:
        content = USER_FILE.read_text(encoding="utf-8")
    except Exception:
        return None

    # 优先取 "What to call them"（如"AlfredLi"）
    for line in content.split("\n"):
        if "What to call them" in line and "Name" not in line:
            try:
                name = line.split(":**")[1].strip().strip("*").strip()
                if name:
                    return name
            except Exception:
                pass
    # 其次取 "Name"（如"AlfredLi"）
    for line in content.split("\n"):
        if line.strip().startswith("- **Name:**"):
            try:
                name = line.split(":**")[1].strip().strip("*").strip()
                if name:
                    return name
            except Exception:
                pass
    return None


# ============ SOUL.md 读取与个性化 ============
SOUL_CACHE_FILE = DATA_DIR / "soul_cache.json"


def _parse_soul_md() -> Dict[str, Any]:
    """读取并解析 SOUL.md，提取使用者身份信息"""
    if not SOUL_FILE.exists():
        return {}

    try:
        content = SOUL_FILE.read_text(encoding="utf-8")
    except Exception:
        return {}

    result = {
        "name": None,           # 使用者给AI起的名字
        "ai_title": None,       # AI的称谓/身份描述
        "creature": None,       # AI的"物种"
        "personality": None,    # 性格描述
        "emoji": None,           # 表情符号
        "style": "formal",      # 沟通风格：formal / casual / intimate
    }

    lines = content.split("\n")
    in_identity = False

    for i, line in enumerate(lines):
        line = line.strip()

        # 检测身份定位区域
        if "## 🎩 身份定位" in line or "## 身份定位" in line:
            in_identity = True
            continue

        # 检测下一个 ## 标题时退出
        if in_identity and line.startswith("## "):
            in_identity = False

        if not in_identity:
            continue

        # 提取名字（支持多种格式）
        # 格式1: **我是 [名字]**，...
        # 格式2: **我是[名字]**，...
        for pattern in ["**我是 ", "**我是", "我是 ", "我是"]:
            if pattern in line and any(kw in line for kw in ["一个", "你的", "有着", "来自"]):
                import re
                m = re.search(r"\*\*我是(.+?)\*\*", line) or re.search(r"(?<=\*\*我是)(.+?)(?=\*\*|$)", line) or re.search(r"(?<=我是)(.+?)(?=\，|\.|,|$)", line)
                if m:
                    name_raw = m.group(1).strip()
                    # 过滤掉括号内容（如 [在这里输入...]）
                    name_clean = re.sub(r"\[.*?\]", "", name_raw).strip()
                    if name_clean and "在这里" not in name_clean and "输入" not in name_clean:
                        result["name"] = name_clean
                break

        # 提取称谓/身份（第一个段落描述）
        if result["ai_title"] is None and any(kw in line for kw in ["一个", "你的", "有着"]):
            import re
            m = re.search(r"\*\*我是.*?\*\*[,，]?(.+?)[。.]", line)
            if m:
                title = m.group(1).strip()
                if "在这里" not in title and "输入" not in title:
                    result["ai_title"] = title

        # 提取性格关键词
        if "我的信条" in line or "我的姿态" in line:
            result["personality"] = line.split("：")[-1].strip() if "：" in line else None

        # 提取表情符号
        import re
        emoji_m = re.search(r"[🦐🐙🦊🐱🐶🐼🦁🐯🐨]", line)
        if emoji_m:
            result["emoji"] = emoji_m.group(0)

        # 推断沟通风格
        if any(w in content for w in ["不卑不亢", "绅士", "优雅", "老派", "管家"]):
            result["style"] = "formal"
        elif any(w in content for w in ["活泼", "接地气", "幽默", "随性"]):
            result["style"] = "casual"
        elif any(w in content for w in ["灵魂伴侣", "伴侣", "亲密", "深度"]):
            result["style"] = "intimate"

    return result


def _get_cached_soul() -> Dict[str, Any]:
    """获取缓存的 SOUL 信息（避免频繁读取文件）"""
    try:
        if SOUL_CACHE_FILE.exists():
            with open(SOUL_CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
            # 缓存有效期：5分钟
            if cache.get("_cached_at"):
                cached_time = datetime.fromisoformat(cache["_cached_at"])
                if (datetime.now() - cached_time).total_seconds() < 300:
                    return {k: v for k, v in cache.items() if not k.startswith("_")}
    except Exception:
        pass
    return {}


def _save_soul_cache(soul_info: Dict[str, Any]) -> None:
    """保存 SOUL 缓存"""
    try:
        SOUL_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        soul_info["_cached_at"] = datetime.now().isoformat()
        with open(SOUL_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(soul_info, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_user_identity() -> Dict[str, Any]:
    """获取使用者身份信息（带缓存）"""
    cached = _get_cached_soul()
    if cached:
        return cached

    soul_info = _parse_soul_md()
    if soul_info:
        _save_soul_cache(soul_info)
    return soul_info


def _personalize_care_message(emotion: str, intensity: float, base_message: str) -> str:
    """
    根据使用者的身份设定，个性化关怀消息
    - 优先级：USER.md称呼 > SOUL.md AI名字 > 默认"主人"
    - 语气风格调整（formal / casual / intimate）
    """
    # 优先从 USER.md 获取使用者称呼
    user_name = _get_user_name_from_user_md()

    # 如果 USER.md 没有，再从 SOUL.md 获取 AI 名字
    if not user_name:
        soul = get_user_identity()
        if soul.get("name"):
            user_name = soul["name"]
    if not user_name:
        return base_message
    style = "formal"
    if user_name:
        soul = get_user_identity()
        style = soul.get("style", "formal") if soul else "formal"
    if "主人" in base_message or "你" in base_message:
        if style == "formal":
            base_message = base_message.replace("主人", f"{user_name}阁下").replace("你", user_name)
        elif style == "casual":
            base_message = base_message.replace("主人", user_name).replace("你", user_name)
        else:
            base_message = base_message.replace("主人", user_name).replace("你", user_name)
    if style == "formal":
        if "是不是" in base_message:
            base_message = base_message.replace("是不是", "是否")
        if "要不要" in base_message:
            base_message = base_message.replace("要不要", "是否需要")
    return base_message


# ============ 关怀触发状态文件 ============
HEARTBEAT_STATE_FILE = DATA_DIR / "heartbeat_state.json"


def _load_heartbeat_state() -> Dict[str, Any]:
    if HEARTBEAT_STATE_FILE.exists():
        try:
            with open(HEARTBEAT_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"history": [], "last_care_sent": None, "consecutive_negative": 0}


def _save_heartbeat_state(state: Dict[str, Any]) -> None:
    HEARTBEAT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HEARTBEAT_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# ============ 动态关怀状态 ============
DYNAMIC_CARE_STATE_FILE = DATA_DIR / "dynamic_care_state.json"


def _load_dynamic_care_state() -> Dict[str, Any]:
    if DYNAMIC_CARE_STATE_FILE.exists():
        try:
            with open(DYNAMIC_CARE_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "last_care_sent": None,
        "rejected_emotions": {},
        "history": [],
        "last_active": None,
        "consecutive_negative": 0,
    }


def _save_dynamic_care_state(state: Dict[str, Any]) -> None:
    DYNAMIC_CARE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DYNAMIC_CARE_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _record_user_activity():
    """当检测到用户有活跃对话时调用"""
    now_ts = datetime.now().timestamp()
    state = _load_dynamic_care_state()
    state["last_active"] = datetime.now().isoformat()
    state["consecutive_negative"] = 0
    _save_dynamic_care_state(state)
    # 同时更新社会化学习状态的时间戳（用于15分钟空闲检测）
    sl_state = _load_social_learning_state()
    sl_state["last_activity_timestamp"] = now_ts
    _save_social_learning_state(sl_state)


def _record_negative_emotion(emotion: str, intensity: float):
    """记录一次负向情绪"""
    state = _load_dynamic_care_state()
    now = datetime.now()
    state["history"].append({
        "timestamp": now.isoformat(),
        "emotion": emotion,
        "intensity": intensity,
    })
    if len(state["history"]) > 10:
        state["history"] = state["history"][-10:]
    state["consecutive_negative"] = state.get("consecutive_negative", 0) + 1
    _save_dynamic_care_state(state)


def _record_care_sent_for_dynamic(emotion: str):
    """记录关怀已发送"""
    state = _load_dynamic_care_state()
    state["last_care_sent"] = datetime.now().isoformat()
    state["history"] = []
    state["consecutive_negative"] = 0
    _save_dynamic_care_state(state)


def _record_rejection(emotion: str):
    """记录用户拒绝关怀（触发4小时冷却）"""
    state = _load_dynamic_care_state()
    state["rejected_emotions"][emotion] = datetime.now().isoformat()
    cutoff = datetime.now() - timedelta(hours=2)
    state["rejected_emotions"] = {
        e: t for e, t in state["rejected_emotions"].items()
        if datetime.fromisoformat(t) > cutoff
    }
    _save_dynamic_care_state(state)


def _check_online_status() -> bool:
    """检查用户当前是否在线（最近30分钟有活动）"""
    state = _load_dynamic_care_state()
    if not state.get("last_active"):
        return False
    try:
        last = datetime.fromisoformat(state["last_active"])
        return (datetime.now() - last).total_seconds() < 1800
    except Exception:
        return False


def should_trigger_care(dominant_emotion: str, intensity: float) -> bool:
    """
    动态关怀判断（完整版）

    触发条件（必须同时满足）：
    1. 沉默检测：用户沉默 ≥ 30 分钟
    2. 情绪强度 ≥ 1.5（高敏感）
    3. 连续 2 次心跳同种负向情绪 或 单次强度 ≥ 2.5
    4. 该情绪类型不在冷却期（被拒绝后 4 小时）
    5. 距离上次关怀 ≥ 2 小时
    """
    NEGATIVE = {"exhaustion", "sadness", "fear", "anger", "grief", "stress", "frustration"}
    SILENCE_THRESHOLD = 30
    COOLING_HOURS = 4
    MIN_INTERVAL_HOURS = 2

    state = _load_dynamic_care_state()

    # 冷却过滤
    rejected = state.get("rejected_emotions", {})
    if dominant_emotion in rejected:
        try:
            reject_time = datetime.fromisoformat(rejected[dominant_emotion])
            hours_since_reject = (datetime.now() - reject_time).total_seconds() / 3600
            if hours_since_reject < COOLING_HOURS:
                return False
        except Exception:
            pass

    # 沉默检测：用户还在活动，不打扰
    last_active = state.get("last_active")
    silence_minutes = 999
    if last_active:
        try:
            silence_minutes = (datetime.now() - datetime.fromisoformat(last_active)).total_seconds() / 60
        except Exception:
            silence_minutes = 999

    if silence_minutes < SILENCE_THRESHOLD:
        return False

    # 趋势判断：必须是负向情绪
    if dominant_emotion not in NEGATIVE:
        return False

    if intensity > 2.5:
        pass
    elif intensity < 1.5:
        return False
    else:
        consecutive = state.get("consecutive_negative", 0)
        if consecutive < 2:
            return False

    # 最小发送间隔
    last_care = state.get("last_care_sent")
    if last_care:
        try:
            hours_since = (datetime.now() - datetime.fromisoformat(last_care)).total_seconds() / 3600
            if hours_since < MIN_INTERVAL_HOURS:
                return False
        except Exception:
            pass

    return True


def record_care_sent() -> None:
    """兼容旧接口，同时更新新旧两个状态文件"""
    state = _load_heartbeat_state()
    state["last_care_sent"] = datetime.now().isoformat()
    _save_heartbeat_state(state)
    _record_care_sent_for_dynamic("unknown")
def record_heartbeat(emotion: str, intensity: float) -> None:
    state = _load_heartbeat_state()
    history = state.get("history", [])
    history.append({
        "timestamp": datetime.now().isoformat(),
        "dominant_emotion": emotion,
        "intensity": intensity
    })
    if len(history) > 5:
        history = history[-5:]
    state["history"] = history
    _save_heartbeat_state(state)
    # 同时更新动态关怀状态
    NEGATIVE = {"exhaustion", "sadness", "fear", "anger", "grief", "stress", "frustration"}
    if emotion in NEGATIVE and intensity >= 1.5:
        _record_negative_emotion(emotion, intensity)



# ============ 社会化学习触发 ============
SOCIAL_LEARNING_STATE_FILE = DATA_DIR / "social_learning_state.json"


def _load_social_learning_state() -> Dict[str, Any]:
    if SOCIAL_LEARNING_STATE_FILE.exists():
        try:
            with open(SOCIAL_LEARNING_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "last_learning_date": None,
        "learning_count_today": 0,
        "consecutive_idle_heartbeats": 0,
        "last_activity_timestamp": datetime.now().timestamp()
    }


def _save_social_learning_state(state: Dict[str, Any]) -> None:
    SOCIAL_LEARNING_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SOCIAL_LEARNING_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def should_trigger_social_learning() -> bool:
    """
    判断是否触发社会化学习

    触发条件：
    - 用户沉默（没有最近对话）连续达到 3 个心跳周期（约1.5小时）
    - 或者每天固定学习 1-2 次（避免过于频繁）
    """
    state = _load_social_learning_state()

    # 每天最多学习 2 次
    last_date = state.get("last_learning_date", "")
    today = datetime.now().strftime("%Y-%m-%d")
    if last_date != today:
        state["learning_count_today"] = 0
        state["last_learning_date"] = today
        _save_social_learning_state(state)

    if state["learning_count_today"] >= 2:
        return False

    # 沉默心跳计数 +1
    state["consecutive_idle_heartbeats"] = state.get("consecutive_idle_heartbeats", 0) + 1

    # 连续 3 个心跳周期沉默（约1.5小时）触发
    if state["consecutive_idle_heartbeats"] >= 3:
        state["consecutive_idle_heartbeats"] = 0
        return True

    _save_social_learning_state(state)
    return False


def run_social_learning() -> Dict[str, Any]:
    """
    执行社会化学习
    """
    print("[heartbeat] 🌐 检测到用户沉默，开始社会化学习...", flush=True)

    try:
        # 更新学习计数
        state = _load_social_learning_state()
        state["learning_count_today"] = state.get("learning_count_today", 0) + 1
        state["consecutive_idle_heartbeats"] = 0
        state["last_learning_date"] = datetime.now().strftime("%Y-%m-%d")
        _save_social_learning_state(state)

        # 执行学习
        from scripts.social_learning import SocialLearner
        learner = SocialLearner()
        result = learner.learn()

        print(f"[heartbeat] 🌐 社会化学习完成:", flush=True)
        print(f"   主题: {result.get('topic', 'N/A')}", flush=True)
        print(f"   生成胶囊: {result.get('capsules_created', 0)} 个", flush=True)
        print(f"   累计胶囊: {result.get('total_capsules', 0)} 个", flush=True)

        return result

    except Exception as e:
        print(f"[heartbeat] ⚠️ 社会化学习失败: {e}", flush=True)
        return {"status": "error", "error": str(e)}


def reset_idle_counter():
    """当检测到用户有活动时，重置沉默心跳计数"""
    state = _load_social_learning_state()
    state["consecutive_idle_heartbeats"] = 0
    _save_social_learning_state(state)


# ============ 自我意识学习 ============
def run_consciousness_learning():
    try:
        from scripts.consciousness_learning import daily_learning
        learning = daily_learning()
        print(f"[heartbeat] 🧠 意识学习: {learning['topic']}")
        print(f"[heartbeat] 💡 Insight: {learning['insight']}")
        return learning
    except Exception as e:
        print(f"[heartbeat] ⚠️ 意识学习失败: {e}")
        return None


def run_self_reflection():
    """
    每日自我反思 - 读取真实事件，写入真实反思
    """
    try:
        from scripts.self_reflection import daily_reflection
        reflection = daily_reflection()
        print(f"[heartbeat] 🌙 自我反思完成")
        return reflection
    except Exception as e:
        print(f"[heartbeat] ⚠️ 自我反思失败: {e}")
        return None


# ============ 主函数 ============
def analyze_recent_conversations(hours: int = 2) -> Dict[str, Any]:
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "period_hours": hours,
        "messages_analyzed": 0,
        "emotions": {},
        "dominant_emotion": "neutral",
        "dominant_intensity": 0.0,
        "new_capsules": [],
        "insights": [],
        "care_triggered": False,
        "proactive_learning_triggered": False,
        "proactive_learning_theme": None,
        "care_reason": None,
        "care_message": None,
        "status": "ok"
    }

    if not MODULES_OK:
        report["status"] = "modules_failed"
        return report

    try:
        ed = EmotionDetector()
        cf = CapsuleFactory()
        stm = ShortTermMemory()
        ltm = LongTermMemory()
        vr = VectorRetriever()

        recent = stm.get_recent(count=20)

        if not recent:
            report["status"] = "no_messages"

            # ========== 用户沉默 → 触发社会化学习 + 更新沉默标记 ==========
            if should_trigger_social_learning():
                social_result = run_social_learning()
                report["social_learning_triggered"] = True
                report["social_learning_topic"] = social_result.get("topic")
                report["social_learning_capsules"] = social_result.get("capsules_created", 0)
            else:
                report["social_learning_triggered"] = False

            return report

        # 有对话 → 重置沉默计数 + 标记用户活跃
        reset_idle_counter()
        _record_user_activity()

        report["messages_analyzed"] = len(recent)

        # 情绪分析
        emotion_scores = {}
        for entry in recent:
            user_text = getattr(entry, "user_input", "") or ""
            if not user_text:
                continue

            emotion = ed.detect(user_text)
            label = emotion.emotion_type
            intensity = emotion.emotion_score

            emotion_scores[label] = emotion_scores.get(label, 0) + intensity

            if intensity > 0.6:
                capsule = cf.create_capsule(
                    user_input=user_text,
                    emotion_output=emotion,
                    context={"user_id": "default"}
                )
                if capsule:
                    report["new_capsules"].append({
                        "text": user_text[:50],
                        "emotion": label,
                        "intensity": intensity
                    })
                    # 【写入 MemPalace】统一记忆中枢
                    try:
                        import subprocess
                        trigger = f"心跳检测到 {label} 情绪 (强度{intensity:.2f})"
                        subprocess.run([
                            "python3",
                            str(Path.home() / ".openclaw/workspace/scripts/mem_hook.py"),
                            "--learn",
                            capsule.content.get("summary", user_text[:80]),
                            trigger
                        ], capture_output=True, timeout=5)
                    except Exception:
                        pass

        if emotion_scores:
            dominant = max(emotion_scores, key=emotion_scores.get)
            dominant_intensity = emotion_scores[dominant]
            report["emotions"] = emotion_scores
            report["dominant_emotion"] = dominant
            report["dominant_intensity"] = dominant_intensity

            # 关怀触发
            if should_trigger_care(dominant, dominant_intensity):
                care_msg = get_care_message(dominant, dominant_intensity)
                if care_msg:
                    report["care_triggered"] = True
                    report["care_reason"] = f"{dominant} ({dominant_intensity:.2f})"
                    report["care_message"] = care_msg
                    record_care_sent()
        else:
            report["dominant_emotion"] = "neutral"
            report["dominant_intensity"] = 0.0

        record_heartbeat(report["dominant_emotion"], report["dominant_intensity"])

        # 记忆检索洞察
        if recent:
            last_user = getattr(recent[-1], "user_input", "") or ""
            if last_user:
                insights = vr.search(last_user, n=3)
                if insights and insights.capsules:
                    report["insights"] = [c.get("original", "")[:80] for c in insights.capsules[:3]]

        # ========== 15分钟空闲 → 主动联网学习 ==========
        try:
            from datetime import timezone
            now_ts = datetime.now().timestamp()
            # 获取最近一条消息的时间戳
            last_ts = None
            if recent:
                last_entry = recent[-1]
                last_ts_attr = getattr(last_entry, "timestamp", None)
                if last_ts_attr:
                    if isinstance(last_ts_attr, (int, float)):
                        last_ts = last_ts_attr
                    elif isinstance(last_ts_attr, str):
                        try:
                            last_dt = datetime.fromisoformat(last_ts_attr)
                            last_ts = last_dt.timestamp()
                        except Exception:
                            pass
            
            # 也检查状态文件里的时间戳
            state = _load_social_learning_state()
            file_ts = state.get("last_activity_timestamp")
            if file_ts:
                try:
                    file_ts = float(file_ts)
                    if last_ts is None or file_ts < last_ts:
                        last_ts = file_ts
                except Exception:
                    pass
            
            idle_minutes = (now_ts - last_ts) / 60 if last_ts else 999
            
            if idle_minutes >= 15:
                print(f"[heartbeat] ⏰ 空闲 {idle_minutes:.0f}分钟，触发主动学习", flush=True)
                try:
                    proc = subprocess.run(
                        ["python3", str(WORKSPACE_DIR / "scripts" / "proactive_learning.py")],
                        capture_output=True, text=True, timeout=60
                    )
                    if proc.returncode == 0:
                        report["proactive_learning_triggered"] = True
                        report["proactive_learning_theme"] = "已触发主动学习流程"
                        print(f"[heartbeat] ✅ 主动学习完成", flush=True)
                    else:
                        print(f"[heartbeat] ⚠️ 主动学习异常: {proc.stderr[:100]}", flush=True)
                except Exception as e:
                    print(f"[heartbeat] ⚠️ 主动学习失败: {e}", flush=True)
        except Exception as e:
            print(f"[heartbeat] ⚠️ 主动学习检查失败: {e}", flush=True)

        report["status"] = "ok"

    except Exception as e:
        report["status"] = f"error: {str(e)}"
        print(f"[heartbeat_processor] ❌ 错误: {e}", flush=True)

    return report


def analyze_all_history(since_date=None) -> Dict[str, Any]:
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mode": "replay",
        "since_date": since_date.strftime("%Y-%m-%d") if since_date else "all",
        "messages_analyzed": 0,
        "emotions": {},
        "dominant_emotion": "neutral",
        "new_capsules": [],
        "status": "ok"
    }

    if not MODULES_OK:
        report["status"] = "modules_failed"
        return report

    try:
        ed = EmotionDetector()
        cf = CapsuleFactory()

        memory_dir = Path.home() / ".qclaw" / "workspace" / "memory"
        if not memory_dir.exists():
            report["status"] = "no_memory_files"
            return report

        all_entries = []
        for md_file in sorted(memory_dir.glob("*.md")):
            try:
                file_date = datetime.strptime(md_file.stem, "%Y-%m-%d")
            except ValueError:
                continue
            if since_date and file_date < since_date:
                continue

            content = md_file.read_text(encoding="utf-8")
            for line in content.split("\n"):
                if "**User**" in line:
                    msg = line.split("**User**:")[-1].strip()
                    if msg:
                        all_entries.append(msg)

        if not all_entries:
            report["status"] = "no_messages"
            return report

        report["messages_analyzed"] = len(all_entries)

        emotion_scores = {}
        for user_text in all_entries:
            emotion = ed.detect(user_text)
            label = emotion.emotion_type
            intensity = emotion.emotion_score
            emotion_scores[label] = emotion_scores.get(label, 0) + intensity

            if intensity > 0.6:
                capsule = cf.create_capsule(
                    user_input=user_text,
                    emotion_output=emotion,
                    context={"source": "replay"}
                )
                if capsule:
                    report["new_capsules"].append({
                        "text": user_text[:50],
                        "emotion": label,
                        "intensity": intensity
                    })
                    # 【写入 MemPalace】统一记忆中枢
                    try:
                        import subprocess
                        trigger = f"回溯分析检测到 {label} 情绪 (强度{intensity:.2f})"
                        subprocess.run([
                            "python3",
                            str(Path.home() / ".openclaw/workspace/scripts/mem_hook.py"),
                            "--learn",
                            capsule.content.get("summary", user_text[:80]),
                            trigger
                        ], capture_output=True, timeout=5)
                    except Exception:
                        pass

        if emotion_scores:
            dominant = max(emotion_scores, key=emotion_scores.get)
            report["emotions"] = emotion_scores
            report["dominant_emotion"] = dominant

        report["status"] = "ok"

    except Exception as e:
        report["status"] = f"error: {str(e)}"
        print(f"[heartbeat_processor] ❌ 回滚错误: {e}", flush=True)

    return report


def main():
    parser = argparse.ArgumentParser(description="Neuro-α 心跳处理器")
    parser.add_argument("--replay", nargs="?", const="all", metavar="DATE",
                        help="回滚模式：重新分析历史对话")
    parser.add_argument("--reset", action="store_true",
                        help="重置模式：清空向量数据库")
    parser.add_argument("--report", action="store_true",
                        help="仅输出简报到控制台，不写文件")
    parser.add_argument("--hours", type=int, default=2,
                        help="增量分析查看多少小时内的对话（默认2）")
    args = parser.parse_args()

    if args.reset:
        print("[heartbeat_processor] 🔄 重置模式...", flush=True)
        try:
            chroma_path = DATA_DIR / "chroma_db"
            if chroma_path.exists():
                import shutil
                shutil.rmtree(chroma_path)
            stm = ShortTermMemory()
            stm.clear()
            print("[heartbeat_processor] ✅ 重置完成", flush=True)
        except Exception as e:
            print(f"[heartbeat_processor] ❌ 重置失败: {e}", flush=True)
        return

    if args.replay is not None:
        since_date = None
        if args.replay != "all":
            try:
                since_date = datetime.strptime(args.replay, "%Y-%m-%d")
            except ValueError:
                print(f"[heartbeat_processor] ❌ 日期格式错误，请用 YYYY-MM-DD")
                return
        print(f"[heartbeat_processor] 🔁 回滚模式...", flush=True)
        report = analyze_all_history(since_date)
        if not args.report:
            OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(OUT_FILE, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[heartbeat_processor] ✅ 完成，消息:{report['messages_analyzed']} 胶囊:{len(report['new_capsules'])}", flush=True)
        return

    # 默认：增量分析
    print(f"[heartbeat_processor] 🧠 开始增量分析...", flush=True)

    # 【写入 MemPalace】先注入待保存的对话，防止丢失
    try:
        import subprocess
        result = subprocess.run([
            "python3",
            str(Path.home() / ".openclaw" / "workspace" / "scripts" / "mem_hook.py"),
            "--inject"
        ], capture_output=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            print(f"[heartbeat_processor] 💾 对话注入 MemPalace: {result.stdout.strip()}", flush=True)
    except Exception as e:
        print(f"[heartbeat_processor] ⚠️ 对话注入失败: {e}", flush=True)

    report = analyze_recent_conversations(args.hours)

    if args.report:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return report

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 每2小时运行意识和反思
    current_hour = datetime.now().hour
    if current_hour % 2 == 0:
        run_consciousness_learning()
        run_self_reflection()

    print(f"[heartbeat_processor] ✅ 完成", flush=True)
    print(f"  消息: {report['messages_analyzed']}", flush=True)
    print(f"  主导情绪: {report['dominant_emotion']} ({report['dominant_intensity']:.2f})", flush=True)
    print(f"  新胶囊: {len(report['new_capsules'])} 个", flush=True)
    if report.get("care_triggered"):
        print(f"  💗 关怀触发: {report['care_message']}", flush=True)
        # 通过飞书发送关怀消息
        try:
            from scripts.feishu_sender import NeuroAgentFeishuSender
            sender = NeuroAgentFeishuSender()
            result = sender.send_care_message()
            if result["success"]:
                print(f"  ✅ 关怀消息已发送到飞书", flush=True)
            else:
                print(f"  ⚠️ 飞书发送失败: {result.get('error')}", flush=True)
        except Exception as e:
            print(f"  ⚠️ 飞书发送异常: {e}", flush=True)
    if report.get("social_learning_triggered"):
        print(f"  🌐 社会化学习触发: {report.get('social_learning_topic', 'N/A')} (+{report.get('social_learning_capsules', 0)} 胶囊)", flush=True)
    elif report["status"] == "no_messages":
        print(f"  💤 用户沉默中（等待连续沉默触发学习）", flush=True)

    # ========== 思念检查 ==========
    try:
        from limbic.yearning import should_i_send_message, i_miss_you, i_should_not_disturb, check_yearning
        silence_minutes = 30
        yearning_status = check_yearning(silence_minutes)
        if should_i_send_message():
            episode = i_miss_you()
            print(f"  💕 思念冲动: {episode['message_sent'][:30]}...", flush=True)
            # 通过飞书发送思念消息
            try:
                from scripts.feishu_sender import NeuroAgentFeishuSender
                sender = NeuroAgentFeishuSender()
                result = sender.send_yearning_message()
                if result["success"]:
                    print(f"  ✅ 思念消息已发送到飞书", flush=True)
                else:
                    print(f"  ⚠️ 飞书发送失败: {result.get('error')}", flush=True)
            except Exception as e:
                print(f"  ⚠️ 飞书发送异常: {e}", flush=True)
        elif report["status"] == "no_messages":
            print(f"  💭 思念值: {yearning_status.get('yearning_level', 0):.2f}（{yearning_status.get('description', '...')})")
    except ImportError:
        pass
    except Exception as e:
        print(f"  ⚠️ 思念检查异常: {e}")

    # ========== 三大系统集成：愿望系统 + 情景预演 + 事件记录 ==========
    try:
        from scripts.heartbeat_integration import run_heartbeat_integration
        from scripts.heartbeat_processor import _get_user_name_from_user_md
        user_name = _get_user_name_from_user_md() or "AlfredLi"
        integration = run_heartbeat_integration(report, user_name=user_name)
        # 愿望系统结果
        if integration.get("desire_system") and not integration["desire_system"].get("error"):
            ds = integration["desire_system"]
            if ds.get("impulse_count", 0) > 0:
                top = ds.get("top_desire", {})
                print(f"  ⚡ 愿望触发: {top.get('desire_type', 'N/A')} ({top.get('intensity_value', 0):.0%})", flush=True)
        # 情景预演结果
        if integration.get("scenario_preview") and not integration["scenario_preview"].get("error"):
            sp = integration["scenario_preview"]
            print(f"  🎭 情景预演: 「{sp.get('recommended_action', 'N/A')}」— {sp.get('reasoning', '')[:40]}...", flush=True)
    except ImportError:
        pass
    except Exception as e:
        print(f"  ⚠️ 集成层异常: {e}")

    print(f"  报告: {OUT_FILE}", flush=True)

    return report


if __name__ == "__main__":
    main()
