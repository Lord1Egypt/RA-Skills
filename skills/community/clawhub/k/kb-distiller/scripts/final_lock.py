#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""final_lock.py — 终稿锁定检查（validate.md「终稿锁定（前置门槛）」的脚本化）。

三种模式：

  1. 快照   python final_lock.py <产物目录> --snapshot -o lock.json
  2. 比对   python final_lock.py <产物目录> --check lock.json
  3. 稳定   python final_lock.py <产物目录> --stable [--interval 300]

  --snapshot : 记录产物全部 .md 文件的 mtime/size/行数（splitlines 口径）为 JSON 快照。
  --check    : 当前状态与快照比对——任何文件 mtime/size 漂移即失败（行数漂移仅提示，
               供与 agent 回报核对规模指标）。
  --stable   : 双采样稳定性检查——间隔 --interval 秒（默认 300）两次采样，全文件
               mtime/size 无变化即「终稿稳定」（validate.md 门槛 2 的自动化）。

输出同时打印各文件行数（splitlines 总行数口径），供与 agent 回报的规模指标核对。

退出码: 0 = 锁定成立/比对一致；1 = 漂移/不稳定；2 = 用法/目录/文件错误。
"""

import argparse
import json
import sys
import time
from pathlib import Path


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8", errors="replace"))


def snapshot(root: Path):
    """采样产物目录全部 .md 文件：path -> {mtime_ns, size, lines}。"""
    snap = {}
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        st = md.stat()
        with open(md, "r", encoding="utf-8", errors="replace") as f:
            lines = len(f.read().splitlines())
        snap[rel] = {"mtime_ns": st.st_mtime_ns, "size": st.st_size, "lines": lines}
    return snap


def print_lines(snap, title):
    safe_print("")
    safe_print("== {} | 文件 {} 份（行数为 splitlines 总行数口径）==".format(title, len(snap)))
    for rel, st in snap.items():
        safe_print("  {:<40} {:>6} 行  {:>7} B".format(rel, st["lines"], st["size"]))


def diff(old: dict, new: dict):
    """返回 (漂移列表, 行数变化列表)。漂移 = mtime/size 变化或增删文件。"""
    drift, line_changes = [], []
    for rel in sorted(set(old) | set(new)):
        if rel not in new:
            drift.append("已删除: {}".format(rel))
        elif rel not in old:
            drift.append("新增: {}".format(rel))
        else:
            if old[rel]["mtime_ns"] != new[rel]["mtime_ns"] or old[rel]["size"] != new[rel]["size"]:
                drift.append("已修改: {}".format(rel))
            if old[rel]["lines"] != new[rel]["lines"]:
                line_changes.append("{}: {} -> {} 行".format(rel, old[rel]["lines"], new[rel]["lines"]))
    return drift, line_changes

def report(drift, line_changes):
    if drift:
        safe_print("== 漂移文件 {} 处 ==".format(len(drift)))
        for d in drift:
            safe_print("  " + d)
    else:
        safe_print("== 比对一致：无 mtime/size 漂移 ==")
    if line_changes:
        safe_print("行数变化（供与 agent 回报核对）:")
        for c in line_changes:
            safe_print("  " + c)
    return len(drift)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="终稿锁定检查（mtime 快照/比对/稳定）")
    ap.add_argument("target", help="产物目录（如 output/ai-docgen-expert）")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--snapshot", action="store_true", help="记录 mtime/size/行数快照")
    mode.add_argument("--check", metavar="LOCK_JSON", help="与快照比对")
    mode.add_argument("--stable", action="store_true", help="双采样稳定性检查")
    ap.add_argument("-o", "--output", help="快照输出 JSON 路径（--snapshot 必填）")
    ap.add_argument("--interval", type=float, default=300, help="--stable 双采样间隔秒（默认 300）")
    args = ap.parse_args()

    root = Path(args.target)
    if not root.is_dir():
        safe_print("[ERROR] 目录不存在: {}".format(root))
        return 2

    if args.snapshot:
        if not args.output:
            safe_print("[ERROR] --snapshot 需要 -o <lock.json>")
            return 2
        snap = snapshot(root)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"target": str(root), "taken_at": time.strftime("%Y-%m-%d %H:%M:%S"), "files": snap}, f, ensure_ascii=False, indent=1)
        safe_print("== 快照已写入 {} | 文件 {} 份 | {} ==".format(args.output, len(snap), time.strftime("%Y-%m-%d %H:%M:%S")))
        print_lines(snap, "快照")
        return 0

    if args.check:
        lock_path = Path(args.check)
        if not lock_path.is_file():
            safe_print("[ERROR] 快照文件不存在: {}".format(lock_path))
            return 2
        with open(lock_path, "r", encoding="utf-8") as f:
            lock = json.load(f)
        old = lock["files"]
        new = snapshot(root)
        drift, line_changes = diff(old, new)
        n = report(drift, line_changes)
        return 1 if n else 0

    if args.stable:
        safe_print("== 稳定性检查：双采样间隔 {} 秒（validate.md 终稿锁定门槛 2）==".format(args.interval))
        first = snapshot(root)
        safe_print("第一次采样完成（{} 份），等待 {} 秒...".format(len(first), args.interval))
        time.sleep(args.interval)
        second = snapshot(root)
        drift, line_changes = diff(first, second)
        n = report(drift, line_changes)
        if n == 0:
            print_lines(second, "终稿稳定")
            safe_print("结果: 终稿锁定成立，可进入终态校验。")
        else:
            safe_print("结果: 产物仍在变化——agent 可能未完成，禁止进入终态校验。")
        return 1 if n else 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
