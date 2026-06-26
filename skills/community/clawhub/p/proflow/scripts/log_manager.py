#!/usr/bin/env python3
"""
Log Manager - 记录 proflow 各阶段执行日志
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Windows 控制台编码兼容
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

LOGS_DIR = Path('docs/logs')


def ensure_logs_dir():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_log_file(requirement_id):
    today = datetime.now().strftime('%Y%m%d')
    return LOGS_DIR / f"cr-{requirement_id}-logs-{today}.log"


def log_message(requirement_id, message):
    ensure_logs_dir()
    fpath = get_log_file(requirement_id)
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {message}\n"
    with open(fpath, 'a', encoding='utf-8') as f:
        f.write(line)
    print(f"LOGGED: {message}")


def show_logs(requirement_id, tail=None):
    fpath = get_log_file(requirement_id)
    if not fpath.exists():
        print(f"No logs found for {requirement_id}")
        return
    lines = fpath.read_text(encoding='utf-8').splitlines()
    if tail:
        lines = lines[-tail:]
    for line in lines:
        print(line)


def main():
    parser = argparse.ArgumentParser(description='Proflow Log Manager')
    sub = parser.add_subparsers(dest='command')

    p_log = sub.add_parser('log', help='记录日志')
    p_log.add_argument('--id', required=True, help='需求ID')
    p_log.add_argument('--message', required=True, help='日志内容')

    p_show = sub.add_parser('show', help='查看日志')
    p_show.add_argument('--id', required=True, help='需求ID')
    p_show.add_argument('--tail', type=int, help='显示最后N行')

    args = parser.parse_args()

    if args.command == 'log':
        log_message(args.id, args.message)
    elif args.command == 'show':
        show_logs(args.id, args.tail)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
