#!/usr/bin/env python3
"""情感分析引擎：追踪对话情绪变化曲线"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# 中文情感词典
EMOTION_LEXICON = {
    "positive": {
        "happy": ["开心", "高兴", "哈哈", "好棒", "太好了", "赞", "nice", "喜欢", "爱", "满足",
                  "兴奋", "期待", "有趣", "厉害", "优秀", "完美", "成功", "搞定", "酷", "牛",
                  "爽", "乐", "笑", "感恩", "感谢", "幸运", "自豪", "骄傲", "舒服", "愉快",
                  "认可", "欣赏", "惊喜", "激动", "幸福", "甜蜜", "温暖"],
        "calm": ["好的", "嗯", "可以", "行", "没问题", "了解", "明白", "知道", "收到",
                 "OK", "ok", "嗯嗯", "行吧", "随便", "都可以", "也行", "无所谓的",
                 "正常", "还行", "不错", "一般", "说得对", "有道理", "认同"],
        "engaged": ["搞", "做", "试试", "看看", "思考", "研究", "分析", "怎么", "如何",
                    "什么", "为什么", "呢", "吧", "啊", "嘛", "这个", "那个", "想法",
                    "思路", "方案", "计划", "设计", "实现", "优化", "改进", "升级"],
    },
    "negative": {
        "frustrated": ["烦", "恼火", "无语", "崩溃", "受不了", "搞不懂", "太难了",
                       "不行", "失败", "出错", "bug", "报错", "崩溃", "卡住", "卡死",
                       "慢", "卡", "延迟", "超时", "挂了", "断了", "连不上"],
        "worried": ["担心", "焦虑", "紧张", "怕", "害怕", "不确定", "风险", "危险",
                    "问题", "麻烦", "困难", "挑战", "隐患", "担忧", "顾虑", "纠结"],
        "sad": ["可惜", "遗憾", "失望", "难过", "伤心", "不开心", "不舒服", "无聊",
                "没意思", "算了", "无所谓了", "不想", "累了", "倦", "丧", "低落"],
        "confused": ["不懂", "不理解", "不明白", "迷糊", "混乱", "复杂", "搞混",
                     "什么意思", "看不懂", "听不懂", "不清楚", "不确定", "迷茫"],
    },
    "neutral": {
        "info": ["告诉", "说明", "介绍", "描述", "解释", "提醒", "通知", "告知",
                 "请注意", "重要", "需要", "记得", "别忘了"],
    }
}


def analyze_message(text: str) -> dict:
    """分析单条消息的情感"""
    text_lower = text.lower()
    scores = defaultdict(float)
    matched = []

    for category, subcategories in EMOTION_LEXICON.items():
        for sub, keywords in subcategories.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                scores[sub] += count
                matched.extend([kw for kw in keywords if kw in text_lower])

    if not scores:
        return {"primary": "neutral", "sub": "info", "score": 0, "matched": []}

    primary = max(scores, key=scores.get)
    return {"primary": "negative" if primary in EMOTION_LEXICON.get("negative", {}) 
            else "positive" if primary in EMOTION_LEXICON.get("positive", {}) else "neutral",
            "sub": primary, "score": scores[primary], "matched": list(set(matched))}


def analyze_conversation(content: str, date_str: str) -> dict:
    """分析一次对话的整体情感"""
    user_msgs = re.findall(r'\*\*用户[：:]\*\*\s*(.+)', content)
    assistant_msgs = re.findall(r'\*\*助手[：:]\*\*\s*(.+)', content)

    user_emotions = [analyze_message(m) for m in user_msgs]
    assistant_emotions = [analyze_message(m) for m in assistant_msgs]

    # 按时间序列
    timeline = []
    all_msgs = re.findall(r'##\s*\[(\d{2}:\d{2})\].*?(?=##\s*\[|\Z)', content, re.DOTALL)
    for section in all_msgs:
        user_in_section = re.findall(r'\*\*用户[：:]\*\*\s*(.+)', section)
        for msg in user_in_section:
            emo = analyze_message(msg)
            timeline.append(emo)

    # 整体情绪
    emotion_counts = Counter(e["primary"] for e in timeline)
    dominant = emotion_counts.most_common(1)[0][0] if emotion_counts else "neutral"

    sub_counts = Counter(e["sub"] for e in timeline)

    return {
        "date": date_str,
        "user_messages": len(user_msgs),
        "assistant_messages": len(assistant_msgs),
        "dominant_emotion": dominant,
        "emotion_distribution": dict(emotion_counts),
        "sub_distribution": dict(sub_counts.most_common(5)),
        "timeline": timeline,
        "valence": round(sum(1 if e["primary"] == "positive" else -1 if e["primary"] == "negative" else 0 for e in timeline) / max(len(timeline), 1), 3),
    }


def analyze_all(memory_dir: Path, days: int | None = None) -> dict:
    """分析所有对话的情感"""
    from datetime import timedelta
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return {"conversations": [], "summary": {}}

    cutoff = datetime.now() - timedelta(days=days) if days else None
    results = []

    for fp in sorted(conv_dir.glob("*.md")):
        if cutoff:
            try:
                file_date = datetime.strptime(fp.stem, "%Y-%m-%d")
                if file_date < cutoff:
                    continue
            except ValueError:
                continue

        content = fp.read_text(encoding="utf-8")
        analysis = analyze_conversation(content, fp.stem)
        results.append(analysis)

    # 整体趋势
    all_valences = [r["valence"] for r in results]
    avg_valence = round(sum(all_valences) / max(len(all_valences), 1), 3)
    
    emotion_totals = Counter()
    for r in results:
        for e, c in r["emotion_distribution"].items():
            emotion_totals[e] += c

    return {
        "conversations": results,
        "summary": {
            "total_days": len(results),
            "avg_valence": avg_valence,
            "overall_mood": "积极" if avg_valence > 0.2 else "消极" if avg_valence < -0.2 else "中性",
            "emotion_totals": dict(emotion_totals),
            "date_range": f"{results[0]['date']} ~ {results[-1]['date']}" if results else "无",
        },
    }


def print_report(analysis: dict, verbose: bool = False):
    summary = analysis["summary"]
    print("=" * 60)
    print(f"💝 情感分析报告（{summary['date_range']}）")
    print("=" * 60)
    print(f"\n📊 总览：{summary['total_days']} 天对话")
    print(f"   整体情绪：{summary['overall_mood']}（效价: {summary['avg_valence']}）")
    print(f"   情绪分布：{json.dumps(summary['emotion_totals'], ensure_ascii=False)}")

    if verbose:
        print(f"\n📅 逐日分析：")
        for conv in analysis["conversations"]:
            valence_icon = "😊" if conv["valence"] > 0.2 else "😐" if conv["valence"] > -0.2 else "😔"
            print(f"   {conv['date']} {valence_icon} 效价={conv['valence']:+.2f} "
                  f"主导={conv['dominant_emotion']} "
                  f"({conv['user_messages']}用户/{conv['assistant_messages']}助手)")
            print(f"      细分: {json.dumps(conv['sub_distribution'], ensure_ascii=False)}")

    # 情绪曲线（ASCII）
    print(f"\n📈 情绪曲线：")
    for conv in analysis["conversations"]:
        v = conv["valence"]
        bar_len = int((v + 1) * 15)  # -1 to 1 → 0 to 30
        bar = "█" * max(bar_len, 1)
        marker = "🟢" if v > 0.2 else "🟡" if v > -0.2 else "🔴"
        print(f"   {marker} {conv['date']} |{bar:<30s}| {v:+.2f}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="情感分析")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    analysis = analyze_all(md, args.days)

    if args.json:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print_report(analysis, args.verbose)
