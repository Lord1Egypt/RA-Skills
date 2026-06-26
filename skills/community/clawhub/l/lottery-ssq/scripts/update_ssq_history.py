#!/usr/bin/env python3
import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'data' / 'ssq_history.csv'
SOURCE_URL = 'https://datachart.500.com/ssq/history/newinc/history.php?start=03001&end=99999'
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ISSUE_RE = re.compile(r'^\d{5,7}$')
BALL_RE = re.compile(r'^\d{2}$')


def fetch_html():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://datachart.500.com/ssq/history/history.shtml',
    }
    r = requests.get(SOURCE_URL, headers=headers, timeout=30)
    r.raise_for_status()
    r.encoding = 'gb2312'
    return r.text


def normalized_lines(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text('\n').replace('\xa0', '')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines


def parse_rows(lines):
    rows = []
    i = 0
    while i < len(lines):
        if not ISSUE_RE.fullmatch(lines[i]):
            i += 1
            continue
        issue = lines[i]
        # 期号后面应该连续跟 7 个两位数：6红 + 1蓝
        if i + 7 >= len(lines):
            break
        balls = lines[i + 1:i + 8]
        if not all(BALL_RE.fullmatch(x) for x in balls):
            i += 1
            continue
        # 从后面窗口里找最近的开奖日期
        draw_date = None
        for j in range(i + 8, min(i + 20, len(lines))):
            if DATE_RE.fullmatch(lines[j]):
                draw_date = lines[j]
                i = j + 1
                break
        if not draw_date:
            i += 1
            continue

        reds = sorted(int(x) for x in balls[:6])
        blue = int(balls[6])
        rows.append({
            'draw_id': issue,
            'draw_date': draw_date,
            'red_1': reds[0],
            'red_2': reds[1],
            'red_3': reds[2],
            'red_4': reds[3],
            'red_5': reds[4],
            'red_6': reds[5],
            'blue_1': blue,
        })

    unique = {}
    for row in rows:
        unique[row['draw_id']] = row
    return sorted(unique.values(), key=lambda x: x['draw_id'])


def save_csv(rows):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ['draw_id', 'draw_date', 'red_1', 'red_2', 'red_3', 'red_4', 'red_5', 'red_6', 'blue_1']
    with open(DATA_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    html = fetch_html()
    lines = normalized_lines(html)
    rows = parse_rows(lines)
    if not rows:
        raise SystemExit('未解析到双色球历史开奖数据')
    save_csv(rows)
    print(f'规范化文本行数: {len(lines)}')
    print(f'已写入 {len(rows)} 期历史数据 -> {DATA_PATH}')
    print('首期:', rows[0])
    print('最新一期:', rows[-1])


if __name__ == '__main__':
    main()
