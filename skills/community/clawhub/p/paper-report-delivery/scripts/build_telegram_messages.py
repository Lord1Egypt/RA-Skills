#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DATE = datetime.now().strftime('%Y-%m-%d')
READABLE_JSON = ROOT / 'output' / 'readable' / f'paper_report_readable_{DATE}.json'
OUT_DIR = ROOT / 'output' / 'telegram'
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    return json.loads(path.read_text())


def chunk_text(text: str, limit: int = 3500):
    parts = []
    current = ''
    for para in text.split('\n'):
        if len(current) + len(para) + 1 > limit and current:
            parts.append(current.strip())
            current = para + '\n'
        else:
            current += para + '\n'
    if current.strip():
        parts.append(current.strip())
    return parts


def build_item_block(item):
    lines = []
    lines.append(f"{item['label']}. {item['title']}")
    lines.append(f"来源：{item['source']}｜发布日期：{item['published_at']}")
    lines.append(f"中文摘要：{item['cn_summary']}")
    lines.append('创新点：')
    for idx, point in enumerate(item.get('innovation_points', []), start=1):
        lines.append(f"{idx}. {point}")
    if item.get('paper_url'):
        lines.append(f"论文链接：{item['paper_url']}")
    if item.get('code_url'):
        lines.append(f"代码链接：{item['code_url']}")
    return '\n'.join(lines)


def main():
    data = load_json(READABLE_JSON)
    items = data.get('items', [])
    header = (
        f"论文日报（Telegram 可读版）\n日期：{data.get('runDate', '')}\n"
        '论文条目使用更接近原文 abstract 的中文翻译，创新点采用分点详细解释。'
    )

    messages = [header]
    for group in ['A', 'B']:
        group_items = [item for item in items if item.get('group') == group]
        group_title = 'A 组' if group == 'A' else 'B 组'
        group_text = [group_title]
        for item in group_items:
            group_text.append(build_item_block(item))
            group_text.append('')
        messages.extend(chunk_text('\n'.join(group_text)))

    out = {'runDate': data.get('runDate', ''), 'count': len(messages), 'messages': messages}
    out_path = OUT_DIR / f'telegram_messages_{data.get("runDate", DATE)}.json'
    txt_path = OUT_DIR / f'telegram_messages_{data.get("runDate", DATE)}.txt'
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    txt_path.write_text('\n\n===== MESSAGE =====\n\n'.join(messages), encoding='utf-8')
    print(out_path)
    print(txt_path)
    print(f'messages={len(messages)}')


if __name__ == '__main__':
    main()
