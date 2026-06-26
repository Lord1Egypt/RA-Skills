#!/usr/bin/env python3
import json
import os
from collections import Counter
from datetime import datetime, timedelta

ROOT = os.environ.get('MEMORY_ROOT', os.path.join(os.getcwd(), 'memory'))
DAILY_DIR = os.path.join(ROOT, 'daily')
REFLECTIONS_DIR = os.path.join(ROOT, 'reflections')


def read_recent_daily(days=3):
    texts = []
    if not os.path.isdir(DAILY_DIR):
        return texts
    cutoff = datetime.now().date() - timedelta(days=days)
    for name in sorted(os.listdir(DAILY_DIR)):
        if not name.endswith('.md'):
            continue
        try:
            d = datetime.strptime(name[:-3], '%Y-%m-%d').date()
        except Exception:
            continue
        if d >= cutoff:
            with open(os.path.join(DAILY_DIR, name), 'r', encoding='utf-8') as f:
                texts.append((name[:-3], f.read()))
    return texts


def main():
    os.makedirs(REFLECTIONS_DIR, exist_ok=True)
    recent = read_recent_daily(3)
    counter = Counter()
    for _, text in recent:
        for keyword in ['技术', '职业', '投资', '理财', '论文', '科研', '记忆', '日报', '偏好']:
            counter[keyword] += text.count(keyword)
    day = datetime.now().astimezone().strftime('%Y-%m-%d')
    out = os.path.join(REFLECTIONS_DIR, f'{day}.md')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(f'# Reflection {day}\n\n')
        f.write('## Reviewed\n')
        for name, _ in recent:
            f.write(f'- {name}\n')
        f.write('\n## Keyword Signals\n')
        for k, v in counter.most_common():
            if v > 0:
                f.write(f'- {k}: {v}\n')
        f.write('\n## Suggested Actions\n')
        f.write('- Promote repeated preferences and decisions into durable objects\n')
        f.write('- Update topic summaries for recurring domains\n')
        f.write('- Merge duplicated objects if repeated references point to the same theme\n')
    print(json.dumps({'ok': True, 'reflection_path': out}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
