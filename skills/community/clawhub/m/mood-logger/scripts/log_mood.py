#!/usr/bin/env python3
"""
心情记录工具 - 生成固定格式的心情记录文件

用法:
    python3 log_mood.py --date 2026-03-27 --score 8 --tags "开心,充实" --note "今天完成了重要任务"
    python3 log_mood.py --score 6 --tags "平静" --note "普通的一天"
    python3 log_mood.py --score 4 --tags "疲惫,焦虑"

参数:
    --date: 日期 (默认今天，格式 YYYY-MM-DD)
    --score: 心情评分 (1-10)
    --tags: 心情标签，逗号分隔
    --note: 备注/原因 (可选)
"""

import argparse
import os
from datetime import datetime

# 配置
VAULT_PATH = "/mnt/c/Users/loong/iCloudDrive/iCloud~md~obsidian/HomeMo.Art"
DAILY_DIR = os.path.join(VAULT_PATH, "05-Daily")


def get_mood_emoji(score: int) -> str:
    """根据评分返回表情"""
    if score >= 9:
        return "😄"
    elif score >= 7:
        return "😊"
    elif score >= 5:
        return "😐"
    elif score >= 3:
        return "😔"
    else:
        return "😢"


def get_template(date_str: str) -> str:
    """获取文件模板"""
    return f"""# {date_str} 心情日记

## 今日心情

---
*记录时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""


def parse_tags(tags_str: str) -> list:
    """解析标签列表"""
    return [tag.strip() for tag in tags_str.split(",") if tag.strip()]


def format_tags(tags: list) -> str:
    """格式化标签为 markdown"""
    return " ".join([f"`{tag}`" for tag in tags])


def read_or_create_file(filepath: str, date_str: str) -> str:
    """读取文件，如果不存在则创建"""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return get_template(date_str)


def update_mood(content: str, score: int, tags: list, note: str = None) -> str:
    """更新心情记录"""
    emoji = get_mood_emoji(score)
    tags_md = format_tags(tags)
    
    # 构建心情条目
    mood_entry = f"""
### {emoji} 评分: {score}/10

**标签**: {tags_md}
"""
    if note:
        mood_entry += f"\n**备注**: {note}\n"
    
    # 在 "## 今日心情" 后插入
    lines = content.split("\n")
    result = []
    mood_section_found = False
    
    for i, line in enumerate(lines):
        result.append(line)
        if line.strip() == "## 今日心情":
            mood_section_found = True
            # 在标题后插入心情记录
            result.append(mood_entry)
    
    # 如果没找到心情段落，追加到最后（在分隔线之前）
    if not mood_section_found:
        # 找到分隔线位置
        for i in range(len(result) - 1, -1, -1):
            if result[i].strip().startswith("---"):
                # 在分隔线前插入
                result.insert(i, f"## 今日心情\n{mood_entry}")
                break
        else:
            # 没找到分隔线，追加到末尾
            result.append(f"## 今日心情\n{mood_entry}")
    
    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(description="记录心情")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                        help="日期 (YYYY-MM-DD)")
    parser.add_argument("--score", type=int, required=True,
                        help="心情评分 (1-10)")
    parser.add_argument("--tags", required=True,
                        help="心情标签，逗号分隔")
    parser.add_argument("--note", default=None,
                        help="备注/原因 (可选)")
    
    args = parser.parse_args()
    
    # 验证评分范围
    if not 1 <= args.score <= 10:
        print("错误: 评分必须在 1-10 之间")
        return
    
    # 确保目录存在
    os.makedirs(DAILY_DIR, exist_ok=True)
    
    # 文件路径
    filename = f"心情日记-{args.date}.md"
    filepath = os.path.join(DAILY_DIR, filename)
    
    # 读取或创建文件
    content = read_or_create_file(filepath, args.date)
    
    # 解析标签
    tags = parse_tags(args.tags)
    
    # 更新内容
    new_content = update_mood(content, args.score, tags, args.note)
    
    # 保存文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    emoji = get_mood_emoji(args.score)
    print(f"✅ 已记录心情: {emoji} {args.score}/10")
    print(f"🏷️ 标签: {', '.join(tags)}")
    if args.note:
        print(f"📝 备注: {args.note}")
    print(f"📁 文件: {filepath}")


if __name__ == "__main__":
    main()
