#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime

EVENT_PATTERNS = [
    ('preference_update', r'(以后|默认|不要|别|讨厌|喜欢).+'),
    ('decision_made', r'(决定|就用|改成|采用).+'),
    ('correction', r'(不是|不对|改一下|更正).+'),
    ('topic_activation', r'(技术|职业|投资|理财|论文|科研|日常|记忆).+'),
]


def infer_domains(text: str):
    domains = []
    mapping = {
        'technology': ['技术', '代码', '实现', 'plugin', 'skill', 'openclaw'],
        'career': ['职业', '岗位', '求职', '规划'],
        'investing': ['投资', '理财', '资产', '风险'],
        'research': ['论文', '科研', '研究', '文献'],
        'life': ['日常', '生活'],
        'meta': ['记忆', '日报', '文档', '飞书', '工作目录'],
    }
    for domain, words in mapping.items():
        if any(w.lower() in text.lower() for w in words):
            domains.append(domain)
    return domains


def main():
    text = sys.stdin.read().strip()
    if not text:
        print(json.dumps({'events': []}, ensure_ascii=False))
        return
    events = []
    for event_type, pattern in EVENT_PATTERNS:
        if re.search(pattern, text):
            events.append({
                'event_type': event_type,
                'text': text,
                'domains': infer_domains(text),
                'timestamp': datetime.now().astimezone().isoformat(timespec='seconds')
            })
    if not events and infer_domains(text):
        events.append({
            'event_type': 'topic_activation',
            'text': text,
            'domains': infer_domains(text),
            'timestamp': datetime.now().astimezone().isoformat(timespec='seconds')
        })
    print(json.dumps({'events': events}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
