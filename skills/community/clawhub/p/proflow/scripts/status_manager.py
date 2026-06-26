#!/usr/bin/env python3
"""
Status Manager - 管理 proflow 各阶段状态标记
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

STATUS_DIR = Path('.opencode/status/proflow')
STAGES = ['brainstorm', 'plan', 'execute', 'spec']


def ensure_status_dir():
    STATUS_DIR.mkdir(parents=True, exist_ok=True)


def get_status_file(stage):
    return STATUS_DIR / f"{stage}.done"


def check_stage(stage):
    ensure_status_dir()
    fpath = get_status_file(stage)
    if not fpath.exists():
        return False, None
    try:
        data = json.loads(fpath.read_text(encoding='utf-8'))
        return True, data
    except Exception:
        return True, None


def mark_done(stage, output_path=None, requirement_id=None):
    ensure_status_dir()
    fpath = get_status_file(stage)
    data = {
        "stage": stage,
        "timestamp": datetime.now().isoformat(),
        "output_path": str(output_path) if output_path else None,
        "requirement_id": requirement_id,
    }
    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def reset_stage(stage):
    ensure_status_dir()
    fpath = get_status_file(stage)
    if fpath.exists():
        fpath.unlink()
        return True
    return False


def list_status():
    ensure_status_dir()
    for stage in STAGES:
        done, data = check_stage(stage)
        status = "DONE" if done else "PENDING"
        ts = data.get('timestamp', '') if data else ''
        print(f"{stage}: {status} {ts}")


def main():
    parser = argparse.ArgumentParser(description='Proflow Status Manager')
    sub = parser.add_subparsers(dest='command')

    p_check = sub.add_parser('check', help='检查阶段状态')
    p_check.add_argument('stage', choices=STAGES)

    p_done = sub.add_parser('done', help='标记阶段完成')
    p_done.add_argument('stage', choices=STAGES)
    p_done.add_argument('--output', help='输出路径')
    p_done.add_argument('--id', help='需求ID')

    p_reset = sub.add_parser('reset', help='重置阶段状态')
    p_reset.add_argument('stage', choices=STAGES + ['all'])

    p_list = sub.add_parser('list', help='列出所有阶段状态')

    args = parser.parse_args()

    if args.command == 'check':
        done, data = check_stage(args.stage)
        print(json.dumps({"done": done, "data": data}, ensure_ascii=False))
    elif args.command == 'done':
        mark_done(args.stage, args.output, args.id)
        print(f"Marked {args.stage} as done.")
    elif args.command == 'reset':
        if args.stage == 'all':
            for s in STAGES:
                reset_stage(s)
            print("Reset all stages.")
        else:
            reset_stage(args.stage)
            print(f"Reset {args.stage}.")
    elif args.command == 'list':
        list_status()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
