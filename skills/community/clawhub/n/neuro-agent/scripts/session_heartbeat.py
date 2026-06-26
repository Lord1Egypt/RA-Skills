#!/usr/bin/env python3
"""
session_heartbeat.py
====================
从 OpenClaw session 日志直接读取对话，生成情绪胶囊和每日摘要。
解决 short_term.json 不存在的问题。

数据源：~/.openclaw/workspace/agents/main/sessions/*.jsonl
输出：~/.openclaw/workspace/neuro_claw/memory/capsules/YYYY-MM-DD.jsonl
     ~/.openclaw/workspace/neuro_claw/heartbeat_report.json
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 路径配置
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

SESSION_DIR = Path("/home/gem/workspace/agent/agents/main/sessions")
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
OUT_FILE = DATA_DIR / "heartbeat_report.json"
CAPSULE_DIR = DATA_DIR / "memory" / "capsules"

# 确保目录存在
CAPSULE_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_latest_session_file() -> Path:
    """获取最新的 session 文件"""
    if not SESSION_DIR.exists():
        return None
    files = list(SESSION_DIR.glob("*.jsonl"))
    if not files:
        return None
    # 按修改时间排序，返回最新的
    return max(files, key=lambda f: f.stat().st_mtime)


def extract_messages(session_file: Path, hours: int = 2) -> List[Dict]:
    """
    从 session JSONL 提取最近 N 小时的对话消息
    用户消息格式：[Day YYYY-MM-DD HH:MM GMT+8] 实际内容
    """
    if not session_file or not session_file.exists():
        return []
    
    cutoff = datetime.now() - timedelta(hours=hours)
    cutoff_ts = cutoff.isoformat()
    
    messages = []
    try:
        with open(session_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("type") != "message":
                        continue
                    msg = entry.get("message", {})
                    role = msg.get("role", "")
                    if role not in ("user",):  # 只取用户消息
                        continue
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        raw_texts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                        raw_text = " ".join(raw_texts)
                    else:
                        raw_text = str(content) if content else ""
                    
                    # 从 <relevant-memories>...</relevant-memories> 标签后提取真实用户消息
                    # 格式：[Day YYYY-MM-DD HH:MM GMT+8] 实际内容
                    import re
                    
                    # 先提取 relevant-memories 里的对话历史摘要（这是真正的对话内容）
                    memories_content = re.findall(r'<relevant-memories>(.*?)</relevant-memories>', raw_text, re.DOTALL)
                    
                    # 从 relevant-memories 中提取"今天"的用户消息（以GMT+8日期开头）
                    today = datetime.now().strftime("%Y-%m-%d")
                    today_pattern = today.replace("-", "-")
                    
                    conversation_snippets = []
                    for mem in memories_content:
                        # 找以日期格式开头的行，这些是真实对话历史
                        lines = mem.split('\n')
                        for line in lines:
                            # 匹配日期格式行（如 "2026年4月14日（周二）GMT+8时间09:46"）
                            if re.search(r'\d{4}年\d{1,2}月\d{1,2}日', line):
                                # 去掉结尾的描述性文字，保留用户说的话
                                # 格式："2026年4月14日（周二）GMT+8时间09:46，用户向OpenClaw发送问候语「早啊」开启本次对话"
                                match = re.search(r'用户[向将].*?「([^」]+)」', line)
                                if match:
                                    quote = match.group(1)
                                    if len(quote) > 1:
                                        conversation_snippets.append(quote.strip())
                    
                    # 同时提取 Feishu 元数据行（如果有的话）
                    feishu_matches = re.findall(r'\[([^\]]+ GMT[^\]]+)\]\s*([^\[]+?)(?:\[|$)', raw_text)
                    
                    # 合并所有提取到的文本
                    all_texts = conversation_snippets.copy()
                    for ts, content in feishu_matches:
                        content = content.strip()
                        if content and len(content) > 2:
                            all_texts.append(content)
                    
                    # 用提取到的内容组合（去重，保持顺序）
                    seen = set()
                    clean_parts = []
                    for t in all_texts:
                        if t not in seen and len(t) > 2:
                            seen.add(t)
                            clean_parts.append(t)
                    
                    clean = ' | '.join(clean_parts[:5])  # 最多5段
                    
                    # 如果没提取到任何内容，用简洁的清理
                    if not clean or len(clean) < 3:
                        clean = re.sub(r'<relevant-memories>.*?</relevant-memories>', '', raw_text, flags=re.DOTALL)
                        clean = re.sub(r'Sender.*?:', '', clean)
                        clean = re.sub(r'```json\s*\{[^}]+\}\s*```', '', clean)
                        clean = re.sub(r'System \(untrusted\):.*', '', clean)
                        clean = re.sub(r'\[35m.*?\[39m', '', clean)
                        clean = clean.strip()[:200]
                    
                    if not clean or len(clean) < 2:
                        continue
                    
                    # 时间过滤（从日期格式中提取时间）
                    date_pattern = re.search(r'\[([A-Za-z]{3} \d{4}-\d{2}-\d{2} \d{2}:\d{2} GMT[^\]]+)\]', raw_text)
                    if date_pattern:
                        date_str = date_pattern.group(1)
                        try:
                            # 解析 [Tue 2026-04-14 22:13 GMT+8] 格式
                            ts_part = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', date_str)
                            if ts_part:
                                msg_time = datetime.strptime(ts_part.group(1), "%Y-%m-%d %H:%M")
                                if msg_time < cutoff:
                                    continue
                        except:
                            pass
                    
                    # 截断
                    clean = clean[:300]
                    messages.append({"role": "user", "content": clean})
                    
                except Exception:
                    continue
    except Exception as e:
        print(f"[session_heartbeat] 读取session失败: {e}")
    
    return messages


def detect_emotion(text: str) -> Dict[str, Any]:
    """简单情绪检测（无 Neuro Agent 模块时使用）"""
    text_lower = text.lower()
    emotion_scores = {}
    
    # 关键词情绪映射
    keyword_emotions = {
        "开心": {"joy": 0.9}, "高兴": {"joy": 0.8}, "快乐": {"joy": 0.8},
        "哈哈": {"joy": 0.7}, "笑": {"joy": 0.6},
        "谢谢": {"gratitude": 0.8}, "感谢": {"gratitude": 0.7},
        "喜欢": {"joy": 0.7, "love": 0.6},
        "累": {"exhaustion": 0.7}, "困": {"exhaustion": 0.6},
        "难过": {"sadness": 0.8}, "伤心": {"sadness": 0.9},
        "生气": {"anger": 0.8}, "烦": {"anger": 0.6},
        "担心": {"fear": 0.6}, "怕": {"fear": 0.6},
        "忙": {"stress": 0.6}, "压力": {"stress": 0.7},
        "对不起": {"sadness": 0.5, "remorse": 0.6},
        "抱歉": {"sadness": 0.4, "remorse": 0.5},
        "傻": {"frustration": 0.5, "joy": 0.3},  # "太傻了"可能是自嘲/轻松
        "厉害": {"joy": 0.6, "admiration": 0.6},
        "牛逼": {"joy": 0.7, "admiration": 0.7},
        "加油": {"joy": 0.5, "hope": 0.6},
        "困了": {"exhaustion": 0.7},
    }
    
    for keyword, scores in keyword_emotions.items():
        if keyword in text_lower:
            for emotion, score in scores.items():
                emotion_scores[emotion] = max(emotion_scores.get(emotion, 0), score)
    
    if not emotion_scores:
        return {"emotion_type": "neutral", "emotion_score": 0.0, "emotions": {}}
    
    dominant = max(emotion_scores, key=emotion_scores.get)
    return {
        "emotion_type": dominant,
        "emotion_score": emotion_scores[dominant],
        "emotions": emotion_scores
    }


def create_capsule(user_text: str, emotion_data: Dict, timestamp: str) -> Dict:
    """创建情绪胶囊 - 使用 ThreeLayerMemory 兼容格式"""
    capsule_id = f"capsule_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(user_text[:50]) % 10000:04d}"
    return {
        "id": capsule_id,
        "timestamp": timestamp,
        "content": user_text[:200],  # ThreeLayerMemory 读取 content 字段
        "user_input": user_text[:200],  # 保留原字段
        "importance": 3 if emotion_data.get("emotion_score", 0) > 0.5 else 2,  # 3=medium, 2=low
        "layer": "capsule",  # 关键：ThreeLayerMemory 需要这个字段
        "tags": [emotion_data.get("emotion_type", "neutral")],
        "user_emotion": emotion_data.get("emotion_type", "neutral"),
        "agent_emotion": "",
        "decisions": [],
        "outcome": "",
        "related_capsule_id": None,
        "source": "session_heartbeat",
        # 额外情绪数据
        "emotion_type": emotion_data.get("emotion_type", "neutral"),
        "emotion_score": emotion_data.get("emotion_score", 0.0),
        "emotions": emotion_data.get("emotions", {}),
    }


def save_capsule(capsule: Dict) -> bool:
    """追加胶囊到今日文件（去重：同一 user_input 只存一次）"""
    date = datetime.now().strftime("%Y-%m-%d")
    path = CAPSULE_DIR / f"{date}.jsonl"
    # 去重：检查是否已存在相同 user_input 的胶囊
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    existing = json.loads(line.strip())
                    # 比对 user_input 前60字符（避免完全重复）
                    if existing.get("user_input", "")[:60] == capsule.get("user_input", "")[:60]:
                        return False  # 已存在，跳过
                except:
                    pass
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(capsule, ensure_ascii=False) + "\n")
    return True


def count_today_capsules() -> int:
    """统计今日胶囊数"""
    date = datetime.now().strftime("%Y-%m-%d")
    path = CAPSULE_DIR / f"{date}.jsonl"
    if not path.exists():
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def run():
    """主流程"""
    print(f"[session_heartbeat] 开始处理... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取最新 session
    session_file = get_latest_session_file()
    print(f"[session_heartbeat] Session文件: {session_file}")
    
    # 提取消息（最近2小时）
    messages = extract_messages(session_file, hours=2)
    print(f"[session_heartbeat] 提取消息: {len(messages)} 条")
    
    # 构建报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "period_hours": 2,
        "messages_analyzed": len(messages),
        "emotions": {},
        "dominant_emotion": "neutral",
        "dominant_intensity": 0.0,
        "new_capsules": [],
        "insights": [],
        "care_triggered": False,
        "care_reason": None,
        "care_message": None,
        "status": "ok"
    }
    
    if not messages:
        report["status"] = "no_messages"
        print("[session_heartbeat] 无新消息")
    else:
        # 分析用户消息
        user_messages = [m for m in messages if m["role"] == "user"]
        all_emotions = {}
        timestamp = datetime.now().isoformat()
        
        for msg in user_messages:
            text = msg["content"]
            emotion_data = detect_emotion(text)
            
            # 累加情绪
            for emotion, score in emotion_data.get("emotions", {}).items():
                all_emotions[emotion] = all_emotions.get(emotion, 0) + score
            
            # 创建胶囊（只对有明显情绪的创建）
            if emotion_data.get("emotion_score", 0) > 0.4:
                capsule = create_capsule(text, emotion_data, timestamp)
                if save_capsule(capsule):
                    report["new_capsules"].append(capsule["id"])
                    print(f"[session_heartbeat] 创建胶囊: {capsule['id']} | {emotion_data['emotion_type']} | {text[:30]}...")
                else:
                    print(f"[session_heartbeat] 跳过重复胶囊: {text[:30]}...")
        
        # 统计主导情绪
        if all_emotions:
            dominant = max(all_emotions, key=all_emotions.get)
            report["emotions"] = all_emotions
            report["dominant_emotion"] = dominant
            report["dominant_intensity"] = all_emotions[dominant]
            
            # 关怀触发
            if dominant in ("exhaustion", "sadness", "stress") and all_emotions[dominant] > 1.5:
                report["care_triggered"] = True
                report["care_reason"] = f"检测到{dominant}情绪"
                report["care_message"] = f"感觉你有些{dominant}，我在这里陪你 💙"
        
        print(f"[session_heartbeat] 情绪统计: {all_emotions}")
    
    # 今日胶囊总数
    report["today_capsules"] = count_today_capsules()
    
    # 写入报告
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"[session_heartbeat] 完成! 今日胶囊:{report['today_capsules']} 新建:{len(report['new_capsules'])}")
    return report


if __name__ == "__main__":
    run()
