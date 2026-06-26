#!/usr/bin/env python3
import json
import re
import sys

LIGHT_SKIP_PATTERNS = [
    r'^ok$', r'^好的$', r'^收到$', r'^嗯$', r'^hi$', r'^hello$', r'^1$', r'^2$', r'^3$'
]

WRITE_WORDS = ['记住', '以后', '默认', '不要', '改成', '更新记忆', '写进记忆', '记一下']
RECALL_WORDS = ['上次', '之前', '还记得', '继续', '回到', '沿用', '翻一下记忆', '查一下记忆']
REFLECT_WORDS = ['整理记忆', '反思记忆', '压缩记忆', '更新主题卡', '重整记忆']
COMMANDS = {
    '/remember': ('write',),
    '/recall': ('recall',),
    '/reflect': ('reflect',),
    '/memory': ('recall',),
    '/topic': ('write',),
    '/object': ('write',),
}


def contains_any(text, words):
    return any(word in text for word in words)


def main():
    text = sys.stdin.read().strip()
    normalized = text.lower().strip()

    if any(re.fullmatch(p, normalized, re.IGNORECASE) for p in LIGHT_SKIP_PATTERNS):
        result = {
            'should_process': False,
            'should_recall': False,
            'should_write': False,
            'should_reflect': False,
            'reason': 'lightweight-message-skip'
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    matched_command = None
    for command, actions in COMMANDS.items():
        if normalized.startswith(command):
            matched_command = (command, actions)
            break

    if matched_command:
        command, actions = matched_command
        result = {
            'should_process': True,
            'should_recall': 'recall' in actions,
            'should_write': 'write' in actions,
            'should_reflect': 'reflect' in actions,
            'reason': f'command:{command}'
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    should_write = contains_any(text, WRITE_WORDS)
    should_recall = contains_any(text, RECALL_WORDS)
    should_reflect = contains_any(text, REFLECT_WORDS)
    should_process = should_write or should_recall or should_reflect

    result = {
        'should_process': should_process,
        'should_recall': should_recall,
        'should_write': should_write,
        'should_reflect': should_reflect,
        'reason': 'triggered-by-keywords' if should_process else 'no-explicit-memory-trigger'
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
