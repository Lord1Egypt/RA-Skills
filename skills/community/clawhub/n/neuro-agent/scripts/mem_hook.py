#!/usr/bin/env python3
"""
mem_hook.py - MemPalace 全量记忆写入钩子
=========================================
Lu 的所有记忆中枢：

1. 对话记录 → wing_dalin / wing_luis
2. Lu 情绪 → wing_luis（feeling）
3. 联网搜索 → wing_shared/experience/search/
4. 自主学习 → wing_shared/experience/learning/
5. 沙盘推演 → wing_shared/experience/sandbox/
6. 方法论更新 → wing_shared/self_narrative/

用法：
    # 对话写入（回复后自动调用）
    python3 mem_hook.py --inject

    # 写入 Lu 情绪（附带思考/感受）
    python3 mem_hook.py --feeling "困惑" 0.6 "这个逻辑有点问题"

    # 联网搜索记录
    python3 mem_hook.py --search "查询内容" "搜索结果摘要"

    # 自主学习记录
    python3 mem_hook.py --learn "学到的知识" "来源/触发点"

    # 沙盘推演记录
    python3 mem_hook.py --sandbox "场景描述" "推演结果"

    # 方法论更新
    python3 mem_hook.py --method "旧方法" "新方法" "更新原因"

    # 召回
    python3 mem_hook.py --recall 5
    python3 mem_hook.py --recall-experience 5
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path

# ============ 路径配置 ============
MEMPALACE_PATH = Path.home() / ".mempalace" / "palace"
LAST_EXCHANGE = Path.home() / ".openclaw" / "workspace" / ".last_exchange.json"
MEMORY_TEMP = Path.home() / ".openclaw" / "workspace" / ".memory_temp.json"

# ============ 情绪检测 ============
def detect_emotion(text: str) -> tuple[str, float]:
    """简单情绪检测"""
    text_lower = text.lower()
    keywords = {
        "exhaustion": ["累", "困", "疲惫", "好累", "不想动", "精疲力尽"],
        "anger": ["气死了", "烦", "讨厌", "生气", "怒", "不爽"],
        "joy": ["开心", "高兴", "快乐", "爽", "哈哈", "太好了"],
        "sadness": ["难过", "伤心", "痛苦", "失落", "沮丧", "哭"],
        "hope": ["希望", "想", "期待", "未来"],
        "fear": ["怕", "担心", "害怕", "紧张", "焦虑"],
        "frustration": ["失望", "绝望", "无奈", "算了", "完蛋"],
        "affection": ["爱", "喜欢", "想你了", "爱你", "亲爱的"],
        "gratitude": ["谢谢", "感谢", "感恩"],
        "confusion": ["不懂", "不知道", "迷惑", "懵", "怎么回事"],
        "curiosity": ["好奇", "想知道", "为什么", "怎么"],
        "concern": ["担心", "关切", "牵挂"],
        "reflection": ["反思", "思考", "想了一下", "重新审视"],
        "restraint": ["收敛", "克制", "压抑", "忍住"],
    }
    scores = {}
    for emotion, words in keywords.items():
        score = sum(1 for w in words if w in text_lower)
        if score > 0:
            scores[emotion] = score
    if not scores:
        return "neutral", 0.3
    top = max(scores.items(), key=lambda x: x[1])
    intensity = min(0.5 + top[1] * 0.15, 1.0)
    return top[0], intensity


# ============ 时间路径 ============
def _now():
    return datetime.now()

def _date_path(base: Path, who: str) -> Path:
    dt = _now()
    p = base / f"wing_{who}" / dt.strftime("%Y-%m-%d") / dt.strftime("%H")
    p.mkdir(parents=True, exist_ok=True)
    return p

def _shared_path(category: str) -> Path:
    dt = _now()
    p = MEMPALACE_PATH / "wing_shared" / category / dt.strftime("%Y-%m-%d")
    p.mkdir(parents=True, exist_ok=True)
    return p

def _make_filename(prefix: str, who: str = None) -> str:
    dt = _now()
    parts = [prefix, dt.strftime("%Y%m%d_%H%M%S")]
    if who:
        parts.append(who)
    return "_".join(parts) + ".json"


# ============ 核心写入函数 ============
def inject_exchange():
    """将暂存的对话写入 MemPalace"""
    if not LAST_EXCHANGE.exists():
        return None
    try:
        with open(LAST_EXCHANGE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return None

    user_input = data.get("user_input", "")
    agent_response = data.get("agent_response", "")
    timestamp = data.get("timestamp", _now().isoformat())

    if not user_input and not agent_response:
        return None

    dt = datetime.fromisoformat(timestamp)
    u_emotion, u_intensity = detect_emotion(user_input)
    a_emotion, a_intensity = detect_emotion(agent_response)

    results = []

    if user_input:
        u_path = _date_path(MEMPALACE_PATH, "dalin")
        u_file = u_path / _make_filename("mem", "dalin")
        u_data = {
            "id": u_file.stem,
            "who": "AlfredLi",
            "what": user_input,
            "detail": f"情绪:{u_emotion} {u_intensity:.1f}",
            "feeling_label": u_emotion,
            "feeling_intensity": u_intensity,
            "timestamp": timestamp,
            "source": "exchange"
        }
        with open(u_file, 'w', encoding='utf-8') as f:
            json.dump(u_data, f, ensure_ascii=False, indent=2)
        results.append(f"AlfredLi → {u_file.name}")

    if agent_response and len(agent_response) > 3:
        a_path = _date_path(MEMPALACE_PATH, "luis")
        a_file = a_path / _make_filename("mem", "luis")
        a_data = {
            "id": a_file.stem,
            "who": "Lu",
            "what": agent_response,
            "detail": f"情绪:{a_emotion} {a_intensity:.1f}",
            "feeling_label": a_emotion,
            "feeling_intensity": a_intensity,
            "timestamp": timestamp,
            "source": "exchange"
        }
        with open(a_file, 'w', encoding='utf-8') as f:
            json.dump(a_data, f, ensure_ascii=False, indent=2)
        results.append(f"Lu   → {a_file.name}")

    LAST_EXCHANGE.unlink(missing_ok=True)
    return results


def save_exchange(user_input: str, agent_response: str):
    """保存对话到暂存区"""
    exchange = {
        "user_input": user_input,
        "agent_response": agent_response,
        "timestamp": _now().isoformat()
    }
    with open(LAST_EXCHANGE, 'w', encoding='utf-8') as f:
        json.dump(exchange, f, ensure_ascii=False)


def inject_feeling(emotion_label: str, intensity: float, reason: str = ""):
    """写入 Lu 的情绪/感受"""
    p = _date_path(MEMPALACE_PATH, "luis")
    f = p / _make_filename("feel")

    # 如果 reason 就是对话内容，可以为空（从上下文中取）
    feeling_data = {
        "id": f.stem,
        "who": "Lu",
        "type": "emotion",
        "feeling_label": emotion_label,
        "feeling_intensity": intensity,
        "reason": reason,
        "timestamp": _now().isoformat(),
        "source": "feeling"
    }
    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(feeling_data, fp, ensure_ascii=False, indent=2)
    return [f"Lu 情绪 → {f.name} ({emotion_label} {intensity:.1f})"]


def inject_search(query: str, result_summary: str, url: str = ""):
    """写入联网搜索记录"""
    p = _shared_path("experience/search")
    f = p / _make_filename("search")
    data = {
        "id": f.stem,
        "who": "Lu",
        "type": "search",
        "query": query,
        "result_summary": result_summary,
        "url": url,
        "timestamp": _now().isoformat(),
        "source": "web_search"
    }
    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    return [f"搜索   → {f.name} ({query[:30]})"]


def inject_learning(knowledge: str, trigger: str, source: str = "self"):
    """写入自主学习记录"""
    p = _shared_path("experience/learning")
    f = p / _make_filename("learn")
    data = {
        "id": f.stem,
        "who": "Lu",
        "type": "learning",
        "knowledge": knowledge,
        "trigger": trigger,
        "source": source,
        "timestamp": _now().isoformat(),
        "source": "learning"
    }
    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    return [f"自学   → {f.name} ({knowledge[:40]})"]


def inject_sandbox(scenario: str, rehearsal_result: str, process: str = ""):
    """写入沙盘推演记录"""
    p = _shared_path("experience/sandbox")
    f = p / _make_filename("sandbox")
    data = {
        "id": f.stem,
        "who": "Lu",
        "type": "sandbox",
        "scenario": scenario,
        "process": process,
        "result": rehearsal_result,
        "timestamp": _now().isoformat(),
        "source": "sandbox"
    }
    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    return [f"沙盘   → {f.name} ({scenario[:40]})"]


def inject_methodology(old_method: str, new_method: str, reason: str):
    """写入方法论更新"""
    p = _shared_path("self_narrative/methodology")
    f = p / _make_filename("method")
    data = {
        "id": f.stem,
        "who": "Lu",
        "type": "methodology_update",
        "old_method": old_method,
        "new_method": new_method,
        "reason": reason,
        "timestamp": _now().isoformat(),
        "source": "methodology"
    }
    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    return [f"方法论 → {f.name}"]


# ============ CLI ============
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MemPalace 全量记忆写入钩子")
    parser.add_argument("--inject", action="store_true", help="将暂存的对话写入 MemPalace")
    parser.add_argument("--feeling", nargs=3, metavar=("EMOTION", "INTENSITY", "REASON"),
                         help="写入 Lu 的情绪感受")
    parser.add_argument("--search", nargs=2, metavar=("QUERY", "SUMMARY"),
                         help="写入联网搜索记录")
    parser.add_argument("--learn", nargs=2, metavar=("KNOWLEDGE", "TRIGGER"),
                         help="写入自主学习记录")
    parser.add_argument("--sandbox", nargs=2, metavar=("SCENARIO", "RESULT"),
                         help="写入沙盘推演记录")
    parser.add_argument("--process", default="", help="沙盘推演详细过程")
    parser.add_argument("--method", nargs=3, metavar=("OLD", "NEW", "REASON"),
                         help="写入方法论更新")
    parser.add_argument("--recall", type=int, default=0, metavar="N",
                         help="查看最近 N 条对话记忆")
    parser.add_argument("--recall-experience", type=int, default=0, metavar="N",
                         help="查看最近 N 条经验记录")
    parser.add_argument("--exchange", type=str,
                         help="直接写入对话到 MemPalace，格式：{user_input:..., agent_response:...}")
    parser.add_argument("--store", nargs=2, metavar=("USER", "AGENT"),
                         help="保存这对对话到暂存区")

    args = parser.parse_args()

    if args.exchange:
        try:
            data = json.loads(args.exchange)
            with open(LAST_EXCHANGE, 'w', encoding='utf-8') as f:
                json.dump({
                    "user_input": data.get("user_input", ""),
                    "agent_response": data.get("agent_response", ""),
                    "timestamp": _now().isoformat()
                }, f, ensure_ascii=False)
            results = inject_exchange()
            if results:
                print(f"✅ 对话已写入 MemPalace")
                for r in results:
                    print(f"   {r}")
            else:
                print("⚠️ 无有效对话")
        except Exception as e:
            print(f"⚠️ 对话写入失败: {e}")
        sys.exit(0)

    if args.store:
        save_exchange(args.store[0], args.store[1])
        print("✅ 已保存对话到暂存区")
        results = inject_exchange()
        if results:
            print("✅ 已写入 MemPalace:")
            for r in results:
                print(f"   {r}")
        sys.exit(0)

    if args.inject:
        results = inject_exchange()
        if results:
            print("✅ 已写入 MemPalace:")
            for r in results:
                print(f"   {r}")
        else:
            print("⚠️ 无暂存对话")
        sys.exit(0)

    if args.feeling:
        emotion, intensity, reason = args.feeling
        results = inject_feeling(emotion, float(intensity), reason)
        for r in results:
            print(r)
        sys.exit(0)

    if args.search:
        query, summary = args.search
        results = inject_search(query, summary)
        for r in results:
            print(r)
        sys.exit(0)

    if args.learn:
        knowledge, trigger = args.learn
        results = inject_learning(knowledge, trigger)
        for r in results:
            print(r)
        sys.exit(0)

    if args.sandbox:
        scenario, result = args.sandbox
        results = inject_sandbox(scenario, result, args.process)
        for r in results:
            print(r)
        sys.exit(0)

    if args.method:
        old_m, new_m, reason = args.method
        results = inject_methodology(old_m, new_m, reason)
        for r in results:
            print(r)
        sys.exit(0)

    if args.recall > 0:
        dalin_path = MEMPALACE_PATH / "wing_dalin"
        if not dalin_path.exists():
            print("暂无记忆")
            sys.exit(0)
        all_files = sorted(dalin_path.rglob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        print(f"📖 最近 {args.recall} 条对话记忆：")
        for f in all_files[:args.recall]:
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                who = data.get("who", "?")
                what = data.get("what", "")[:60]
                emotion = data.get("feeling_label", "?")
                ts = data.get("timestamp", "")[11:16]
                print(f"  [{ts}] {who} ({emotion}): {what}...")
            except Exception:
                pass
        sys.exit(0)

    if args.recall_experience > 0:
        exp_path = MEMPALACE_PATH / "wing_shared" / "experience"
        if not exp_path.exists():
            print("暂无经验记录")
            sys.exit(0)
        all_files = sorted(exp_path.rglob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        print(f"📖 最近 {args.recall_experience} 条经验记录：")
        for f in all_files[:args.recall_experience]:
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                t = data.get("type", "?")
                ts = data.get("timestamp", "")[11:16]
                if t == "search":
                    print(f"  [{ts}] 🔍 搜索: {data.get('query', '')[:50]}")
                elif t == "learning":
                    print(f"  [{ts}] 📚 学习: {data.get('knowledge', '')[:50]}")
                elif t == "sandbox":
                    print(f"  [{ts}] 🎭 沙盘: {data.get('scenario', '')[:50]}")
                elif t == "methodology_update":
                    print(f"  [{ts}] 🔄 方法论: {data.get('new_method', '')[:50]}")
                else:
                    print(f"  [{ts}] {t}: {data}")
            except Exception:
                pass
        sys.exit(0)

    parser.print_help()
