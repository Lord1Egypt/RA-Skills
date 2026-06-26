#!/usr/bin/env python3
"""
Format news data into elegant readable output
"""
import json
import sys
from datetime import datetime

def format_news(news_data, style="elegant"):
    """Format news into elegant readable format"""

    if isinstance(news_data, str):
        news_data = json.loads(news_data)

    if not news_data:
        return "暂无新闻数据"

    lines = []

    # Header
    if style == "elegant":
        lines.append("╔" + "═" * 58 + "╗")
        lines.append("║" + " " * 15 + "📰 实时热门新闻" + " " * 28 + "║")
        lines.append("╠" + "═" * 58 + "╣")
        lines.append(f"║  更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 33 + "║")
        lines.append("╚" + "═" * 58 + "╝")
        lines.append("")

    # News items
    for i, item in enumerate(news_data[:20], 1):
        if isinstance(item, dict):
            title = item.get('title', '无标题')
            source = item.get('source', '未知来源')
            hot = item.get('hot', '')
            url = item.get('url', '')
        else:
            title = str(item)
            source = ""
            hot = ""
            url = ""

        # Format hot number
        hot_str = f" 🔥{hot}" if hot else ""

        if style == "elegant":
            # Number with circle emoji for top 10
            if i <= 10:
                num_emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣",
                            "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"][i-1]
            else:
                num_emoji = f"{i}."

            lines.append(f"{num_emoji} {title}{hot_str}")
            if source:
                lines.append(f"   📍 {source}")
            if url:
                lines.append(f"   🔗 {url}")
            lines.append("")

        elif style == "compact":
            lines.append(f"{i}. {title}{hot_str}")

        elif style == "markdown":
            lines.append(f"**{i}.** {title}{hot_str}")
            if url:
                lines.append(f"   [查看原文]({url})")

    return "\n".join(lines)

def format_summary(news_data):
    """Generate a brief summary of top news"""

    if isinstance(news_data, str):
        news_data = json.loads(news_data)

    if not news_data:
        return "暂无新闻数据"

    top5 = news_data[:5]
    titles = []

    for item in top5:
        if isinstance(item, dict):
            title = item.get('title', '无标题')
        else:
            title = str(item)
        titles.append(title)

    summary = "📰 今日热点速览:\n\n"
    for i, title in enumerate(titles, 1):
        summary += f"{i}. {title}\n"

    return summary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python format_news.py <json_file> [style]", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)

    style = sys.argv[2] if len(sys.argv) > 2 else "elegant"

    if style == "summary":
        print(format_summary(data))
    else:
        print(format_news(data, style))
