# -*- coding: utf-8 -*-
"""journal：本次运行流水（journal/current.jsonl）。

记录类型（架构设计 §4.4）：
  run      账户级：本次扫描到的邮件数（含 0 封）
  fetched  scan fetch 每返回一封待处理邮件
  create   create --journal 写入成功
  duplicate create --journal 查重命中（跨账户/重复）
  skip     LLM 调 journal skip（含脚本自动的 SENDER_FILTERED）
  error    脚本（IMAP 失败等）或 LLM 调 journal error
"""
import json
import os
from datetime import datetime


def _journal_dir(root):
    return os.path.join(root, 'journal')


def _path(root):
    return os.path.join(_journal_dir(root), 'current.jsonl')


def append(root, record):
    os.makedirs(_journal_dir(root), exist_ok=True)
    record = dict(record)
    record.setdefault('ts', datetime.now().astimezone().isoformat(timespec='seconds'))
    with open(_path(root), 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def records(root):
    path = _path(root)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue  # 跳过损坏行，保证整体可用
    return out


def clear(root):
    os.makedirs(_journal_dir(root), exist_ok=True)
    with open(_path(root), 'w', encoding='utf-8') as f:
        f.write('')
