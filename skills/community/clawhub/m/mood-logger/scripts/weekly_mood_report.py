#!/usr/bin/env python3
"""
心情周报生成工具 - 分析本周心情记录并生成报告

用法:
    python3 weekly_mood_report.py --date 2026-03-27

参数:
    --date: 指定日期，计算该日期所在周的报告 (默认今天)
    --output: 输出文件路径 (可选，默认打印到控制台)
"""

import argparse
import os
import re
from datetime import datetime, timedelta
from collections import Counter

# 配置
VAULT_PATH = "/mnt/c/Users/loong/iCloudDrive/iCloud~md~obsidian/HomeMo.Art"
DAILY_DIR = os.path.join(VAULT_PATH, "05-Daily")


def get_week_range(date: datetime) -> tuple:
    """获取指定日期所在周的起止日期 (周一到周日)"""
    # 找到本周一
    monday = date - timedelta(days=date.weekday())
    # 本周日
    sunday = monday + timedelta(days=6)
    return monday, sunday


def parse_mood_file(filepath: str) -> list:
    """解析心情记录文件，返回记录列表"""
    records = []
    if not os.path.exists(filepath):
        return records
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取日期
    date_match = re.search(r'# (\d{4}-\d{2}-\d{2})', content)
    if not date_match:
        return records
    date_str = date_match.group(1)
    
    # 提取每条心情记录
    # 匹配模式: ### 😊 评分: 8/10
    mood_blocks = re.findall(
        r'### .+ 评分: (\d+)/10\s*\n\s*\*\*标签\*\*: (.+?)(?:\s*\n\s*\*\*备注\*\*: (.+?))?(?=\n### |\n---|$)',
        content,
        re.DOTALL
    )
    
    for score_str, tags_str, note in mood_blocks:
        score = int(score_str)
        # 解析标签 `标签1` `标签2`
        tags = re.findall(r'`([^`]+)`', tags_str)
        records.append({
            'date': date_str,
            'score': score,
            'tags': tags,
            'note': note.strip() if note else None
        })
    
    return records


def get_weekly_records(monday: datetime, sunday: datetime) -> list:
    """获取本周所有心情记录"""
    all_records = []
    
    for i in range(7):
        current_date = monday + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        filepath = os.path.join(DAILY_DIR, f"心情日记-{date_str}.md")
        
        records = parse_mood_file(filepath)
        all_records.extend(records)
    
    return all_records


def generate_report(records: list, week_start: datetime, week_end: datetime) -> str:
    """生成周报"""
    if not records:
        return "本周没有心情记录。"
    
    # 基础统计
    scores = [r['score'] for r in records]
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)
    min_score = min(scores)
    
    # 标签统计
    all_tags = []
    for r in records:
        all_tags.extend(r['tags'])
    tag_counter = Counter(all_tags)
    top_tags = tag_counter.most_common(5)
    
    # 按日期分组
    daily_scores = {}
    for r in records:
        date = r['date']
        if date not in daily_scores:
            daily_scores[date] = []
        daily_scores[date].append(r['score'])
    
    # 计算每日平均
    daily_avg = {date: sum(scores)/len(scores) for date, scores in daily_scores.items()}
    
    # 趋势判断
    trend = "平稳"
    if len(daily_avg) >= 3:
        dates = sorted(daily_avg.keys())
        first_half = [daily_avg[d] for d in dates[:len(dates)//2]]
        second_half = [daily_avg[d] for d in dates[len(dates)//2:]]
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg - first_avg > 1:
            trend = "上升 📈"
        elif first_avg - second_avg > 1:
            trend = "下降 📉"
    
    # 生成报告
    week_start_str = week_start.strftime("%m月%d日")
    week_end_str = week_end.strftime("%m月%d日")
    
    report = f"""# 📊 心情周报 ({week_start_str} - {week_end_str})

## 本周概览

| 指标 | 数值 |
|------|------|
| 平均心情 | {avg_score:.1f}/10 {'😊' if avg_score >= 7 else '😐' if avg_score >= 5 else '😔'} |
| 最高心情 | {max_score}/10 |
| 最低心情 | {min_score}/10 |
| 记录次数 | {len(records)} 次 |
| 有记录天数 | {len(daily_scores)} 天 |
| 整体趋势 | {trend} |

## 心情标签 TOP5

"""
    
    for tag, count in top_tags:
        report += f"- `{tag}`: {count} 次\n"
    
    # 每日详情
    report += "\n## 每日心情\n\n"
    for i in range(7):
        date = week_start + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        weekday_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][i]
        
        if date_str in daily_avg:
            score = daily_avg[date_str]
            emoji = "😄" if score >= 9 else "😊" if score >= 7 else "😐" if score >= 5 else "😔"
            report += f"- **{weekday_name}** ({date_str}): {emoji} {score:.1f}/10\n"
        else:
            report += f"- **{weekday_name}** ({date_str}): 无记录\n"
    
    # 备注摘录
    notes = [r for r in records if r['note']]
    if notes:
        report += "\n## 本周备注\n\n"
        for r in notes[:5]:  # 最多显示5条
            report += f"- **{r['date']}** ({r['score']}/10): {r['note']}\n"
    
    report += f"\n---\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
    
    return report


def main():
    parser = argparse.ArgumentParser(description="生成心情周报")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                        help="指定日期 (YYYY-MM-DD)，计算该日期所在周的报告")
    parser.add_argument("--output", default=None,
                        help="输出文件路径 (可选)")
    
    args = parser.parse_args()
    
    # 解析日期
    try:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("错误: 日期格式应为 YYYY-MM-DD")
        return
    
    # 获取本周范围
    monday, sunday = get_week_range(target_date)
    
    print(f"正在生成周报: {monday.strftime('%Y-%m-%d')} 至 {sunday.strftime('%Y-%m-%d')}")
    
    # 获取记录
    records = get_weekly_records(monday, sunday)
    
    # 生成报告
    report = generate_report(records, monday, sunday)
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已保存: {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
