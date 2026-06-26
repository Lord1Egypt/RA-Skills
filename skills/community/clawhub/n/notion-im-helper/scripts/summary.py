"""Monthly summary with LLM generation and auto-record to Notion."""
import os
import re
import sys
import random
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from notion_client import get_children, PAGE_ID


def extract_text(block):
    """Extract text content from a block."""
    block_type = block.get("type", "")
    content = block.get(block_type, {})
    rich = content.get("rich_text", [])
    text = ""
    for item in rich:
        text += item.get("text", {}).get("content", "")
    return text.strip()


def get_all_blocks():
    """Get all blocks from the page, paginating through all pages."""
    cursor = None
    all_blocks = []
    while True:
        result = get_children(page_size=100, start_cursor=cursor, silent=True)
        if not result or "results" not in result:
            break
        all_blocks.extend(result["results"])
        if result.get("has_more") and result.get("next_cursor"):
            cursor = result["next_cursor"]
        else:
            break
    return all_blocks


def get_month_records():
    """Extract all records for the current month."""
    blocks = get_all_blocks()
    if not blocks:
        return None, None

    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    day_records = {}

    for block in blocks:
        text = extract_text(block)
        block_type = block.get("type", "")

        # Skip structural blocks
        if block_type in ("divider", "heading_1", "heading_2", "heading_3",
                          "bulleted_list_item", "numbered_list_item"):
            continue
        if not text:
            continue

        # Determine type
        if "📅" in text:
            t = "日记"
        elif "💡" in text or "想法" in text:
            t = "想法"
        elif "📝" in text:
            t = "笔记"
        elif "📖" in text or "摘抄" in text:
            t = "摘抄"
        elif "❓" in text:
            t = "问题"
        elif block_type == "to_do":
            checked = block.get("to_do", {}).get("checked", False)
            t = "已完成" if checked else "待办"
        elif block_type == "bookmark":
            t = "链接"
        else:
            t = "其他"

        # Extract date
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
        if date_match:
            day_str = date_match.group(1)[:10]
        else:
            continue  # Skip records without date

        if day_str.startswith(current_month):
            if day_str not in day_records:
                day_records[day_str] = []
            day_records[day_str].append((t, text))

    if not day_records:
        return current_month, None

    return current_month, day_records


def generate_monthly_report():
    """Extract and return current month's records for LLM to summarize.

    Returns structured data for the agent to analyze and summarize.
    """
    current_month, day_records = get_month_records()

    if day_records is None:
        return f"ERROR|暂时无法获取记录，请稍后重试。"

    if not day_records:
        return f"INFO|{current_month} 月暂无记录~"

    sorted_days = sorted(day_records.keys(), reverse=True)
    total_count = sum(len(v) for v in day_records.values())

    lines = [
        f"📊 {current_month} 月记录（共 {total_count} 条，{len(day_records)} 天有记录）\n"
    ]

    for day in sorted_days:
        records = day_records[day]
        lines.append(f"\n## {day}（{len(records)}条）")
        for t, text in records:
            display = text.replace("\n", " ")[:200]
            lines.append(f"- [{t}] {display}")

    return "INFO|" + "\n".join(lines)


def generate_random_quote(count=1):
    """Randomly select historical entries."""
    blocks = get_all_blocks()
    if not blocks:
        return "📖 还没有摘抄呢，先去记点什么吧~"

    candidates = []
    for block in blocks:
        text = extract_text(block)
        if text and ("📖" in text or "📝" in text or "💡" in text or "📅" in text):
            clean = text.replace("\n", " ").strip()
            if clean:
                candidates.append(clean)

    if not candidates:
        return "📖 没有找到合适的摘抄内容~"

    selected = random.sample(candidates, min(count, len(candidates)))
    lines = ["📖 随机回忆~"]
    for i, text in enumerate(selected, 1):
        lines.append(f"{i}. {text[:80]}")
    return "\n".join(lines)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "monthly"

    if command in ("quote", "random", "随机摘抄", "摘抄"):
        count = 1
        if len(sys.argv) > 2:
            try:
                count = int(sys.argv[2])
            except ValueError:
                pass
        result = generate_random_quote(count)
    elif command in ("weekly", "周报", "monthly", "月报"):
        result = generate_monthly_report()
    else:
        result = generate_monthly_report()

    print(result)


if __name__ == "__main__":
    main()
