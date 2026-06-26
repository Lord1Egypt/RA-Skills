#!/usr/bin/env python3
"""
积极心理学 - 情绪追踪工具

功能：
- 记录每日情绪（情绪、强度、触发事件、身体感受）
- 生成情绪周报（积极/消极比例、模式分析）
- 基于 Fredrickson 3:1 理论评估情绪健康

数据存储：当前目录下的 emotion_log.jsonl
"""

import json
import sys
import os
from datetime import datetime, timedelta
from collections import Counter


DATA_FILE = "emotion_log.jsonl"


def get_data_path():
    """获取数据文件路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, DATA_FILE)


def log_emotion(emotion, intensity, trigger="", body_feeling="", context=""):
    """记录一条情绪"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "emotion": emotion,
        "intensity": int(intensity),
        "trigger": trigger,
        "body_feeling": body_feeling,
        "context": context,
    }
    path = get_data_path()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def load_entries(days=30):
    """加载最近 N 天的记录"""
    path = get_data_path()
    if not os.path.exists(path):
        return []
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry["date"] >= cutoff:
                entries.append(entry)
    return entries


# 积极情绪和消极情绪分类
POSITIVE_EMOTIONS = {
    "喜悦", "快乐", "幸福", "满足", "欣慰", "感恩", "自豪", "自信",
    "充满活力", "兴奋", "平静", "安宁", "放松", "温暖", "甜蜜",
    "自在", "充实", "期待", "好奇", "专注", "愉快", "舒适",
    "振奋", "欢喜", "惬意", "舒畅", "释然", "甜蜜", "亲切",
    "归属感", "信任", "热情", "灵感", "欢快", "欣喜",
    "happy", "joy", "grateful", "calm", "excited", "peaceful",
    "content", "proud", "confident", "hopeful", "energetic",
    "love", "warm", "relaxed", "inspired", "curious",
}

NEGATIVE_EMOTIONS = {
    "悲伤", "焦虑", "愤怒", "恐惧", "沮丧", "孤独", "烦躁", "疲惫",
    "失落", "无助", "迷茫", "羞耻", "内疚", "厌恶", "嫉妒",
    "恐慌", "担忧", "紧张", "无奈", "委屈", "尴尬", "自责",
    "空虚", "麻木", "倦怠", "难过的", "忧伤", "心痛", "哀伤",
    "苦闷", "郁闷", "恐惧", "害怕", "不安", "挫折",
    "sad", "anxious", "angry", "fearful", "depressed", "lonely",
    "frustrated", "exhausted", "guilty", "ashamed", "jealous",
    "worried", "stressed", "overwhelmed", "hopeless",
}


def classify_emotion(emotion):
    """判断情绪是积极还是消极"""
    emotion_lower = emotion.lower()
    for pos in POSITIVE_EMOTIONS:
        if pos in emotion_lower:
            return "positive"
    for neg in NEGATIVE_EMOTIONS:
        if neg in emotion_lower:
            return "negative"
    return "neutral"


def generate_weekly_report(entries=None):
    """生成情绪周报"""
    if entries is None:
        entries = load_entries(days=7)
    if not entries:
        return None

    positive_count = 0
    negative_count = 0
    neutral_count = 0
    emotion_counter = Counter()
    daily_intensity = {}
    daily_emotions = {}

    for entry in entries:
        category = classify_emotion(entry["emotion"])
        if category == "positive":
            positive_count += 1
        elif category == "negative":
            negative_count += 1
        else:
            neutral_count += 1

        emotion_counter[entry["emotion"]] += 1

        date = entry["date"]
        daily_intensity.setdefault(date, []).append(entry["intensity"])
        daily_emotions.setdefault(date, []).append(category)

    # 计算积极/消极比
    if negative_count == 0:
        ratio = float("inf") if positive_count > 0 else 0
    else:
        ratio = positive_count / negative_count

    # 每日平均强度
    daily_avg = {}
    for date, intensities in daily_intensity.items():
        daily_avg[date] = round(sum(intensities) / len(intensities), 1)

    # 每日积极比例
    daily_positive_ratio = {}
    for date, emotions in daily_emotions.items():
        p = emotions.count("positive")
        total = len(emotions)
        daily_positive_ratio[date] = round(p / total * 100) if total > 0 else 0

    # Top 情绪
    top_emotions = emotion_counter.most_common(5)

    # 构建报告
    report_lines = [
        "=" * 50,
        "  积极心理学 - 情绪周报",
        f"  统计周期：{entries[0]['date']} ~ {entries[-1]['date']}",
        f"  总记录数：{len(entries)} 条",
        "=" * 50,
        "",
        "【核心指标】",
        f"  积极情绪记录：{positive_count} 次",
        f"  消极情绪记录：{negative_count} 次",
        f"  中性/其他记录：{neutral_count} 次",
        f"  积极/消极比：{ratio:.2f}:1",
    ]

    # 3:1 理论评估
    if ratio >= 3.0:
        report_lines.append("  理论评估：繁荣状态（Fredrickson 3:1 阈值以上）")
    elif ratio >= 2.0:
        report_lines.append("  理论评估：接近繁荣，建议增加积极体验")
    elif ratio >= 1.0:
        report_lines.append("  理论评估：需要关注，建议尝试'三件好事'练习")
    else:
        report_lines.append("  理论评估：消极情绪占主导，建议关注情绪调节")

    report_lines.extend([
        "",
        "【高频情绪 TOP 5】",
    ])
    for emotion, count in top_emotions:
        cat = classify_emotion(emotion)
        tag = "[+]" if cat == "positive" else "[-]" if cat == "negative" else "[=]"
        report_lines.append(f"  {tag} {emotion}: {count} 次")

    report_lines.extend([
        "",
        "【每日情绪趋势】",
    ])
    for date in sorted(daily_avg.keys()):
        avg_int = daily_avg[date]
        pos_ratio = daily_positive_ratio.get(date, 0)
        report_lines.append(f"  {date} | 平均强度: {avg_int}/10 | 积极占比: {pos_ratio}%")

    report_lines.extend([
        "",
        "【建议】",
    ])
    if ratio < 2.0:
        report_lines.extend([
        "  1. 尝试每天记录'三件好事'，训练关注积极面",
        "  2. 安排一项让你进入'心流'的活动",
        "  3. 联系一位重要的朋友或家人",
        ])
    else:
        report_lines.extend([
        "  1. 继续保持当前的情绪管理方式",
        "  2. 可以尝试更深入的优势探索",
        "  3. 考虑感恩拜访练习来巩固积极体验",
        ])

    report_lines.append("")
    report_lines.append("=" * 50)
    return "\n".join(report_lines)


def show_log(days=7):
    """显示最近的情绪记录"""
    entries = load_entries(days=days)
    if not entries:
        print(f"最近 {days} 天没有情绪记录。")
        return
    print(f"\n最近 {days} 天的情绪记录（共 {len(entries)} 条）：\n")
    for entry in entries:
        cat = classify_emotion(entry["emotion"])
        tag = "[+]" if cat == "positive" else "[-]" if cat == "negative" else "[=]"
        trigger = f" | 触发: {entry['trigger']}" if entry.get('trigger') else ""
        body = f" | 身体: {entry['body_feeling']}" if entry.get('body_feeling') else ""
        print(f"  {entry['date']} {entry['timestamp'][11:16]} {tag} "
              f"{entry['emotion']} ({entry['intensity']}/10){trigger}{body}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("用法：")
        print("  python emotion_tracker.py log <情绪> <强度1-10> [触发事件] [身体感受]")
        print("  python emotion_tracker.py report [天数]")
        print("  python emotion_tracker.py show [天数]")
        print("")
        print("示例：")
        print("  python emotion_tracker.py log 平静 7 散步后 肩膀放松了")
        print("  python emotion_tracker.py report 7")
        print("  python emotion_tracker.py show 7")
        sys.exit(0)

    command = sys.argv[1]

    if command == "log":
        if len(sys.argv) < 4:
            print("用法：python emotion_tracker.py log <情绪> <强度1-10> [触发事件] [身体感受]")
            sys.exit(1)
        emotion = sys.argv[2]
        intensity = sys.argv[3]
        trigger = sys.argv[4] if len(sys.argv) > 4 else ""
        body = sys.argv[5] if len(sys.argv) > 5 else ""
        entry = log_emotion(emotion, intensity, trigger, body)
        cat = classify_emotion(emotion)
        tag = "[积极]" if cat == "positive" else "[消极]" if cat == "negative" else "[中性]"
        print(f"已记录：{entry['date']} {tag} {emotion} ({intensity}/10)")

    elif command == "report":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        report = generate_weekly_report(load_entries(days=days))
        if report:
            print(report)
        else:
            print(f"最近 {days} 天没有记录，无法生成报告。")

    elif command == "show":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        show_log(days)

    else:
        print(f"未知命令: {command}")
        print("可用命令：log, report, show")


if __name__ == "__main__":
    main()
