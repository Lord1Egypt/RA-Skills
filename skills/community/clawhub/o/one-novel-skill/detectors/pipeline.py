#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 自动化管线编排器

将 检测→追踪→报告 流程自动化，填补 SKILL.md 描述的"自动触发"缺口。

用法:
  python pipeline.py --book "小说目录" [--chapter 1] [--mode fast] [--safety]

流程:
  1. 定位正文文件 → 自动确定章号
  2. 检测正文（run_all_detectors）
  3. 更新追踪文件（update_tracker）
  4. 输出摘要报告

注意：只编排检测+追踪部分。章节生成和 spec 规划仍由 LLM 对话完成。
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def find_latest_chapter(book_dir):
    text_dir = book_dir / "正文"
    if not text_dir.exists():
        return 0
    max_n = 0
    for f in text_dir.iterdir():
        if f.suffix in (".txt", ".md"):
            try:
                n = int(''.join(c for c in f.stem if c.isdigit()))
                max_n = max(max_n, n)
            except ValueError:
                continue
    return max_n


def run_detector(chapter_path, genre="general", fast_mode=False, safety=False):
    """运行检测，默认进程内（直接 import），回退到子进程"""
    try:
        from detectors.run_all_detectors import run_all as run_all_fn
        text = open(chapter_path, encoding="utf-8", errors="ignore").read()
        result = run_all_fn(text, chapter_path.stem, genre, safety, fast_mode)
        return f"\n{'='*50}\n  进程内检测完成\n{'='*50}\n  判定: {result['classification']}\n  问题数: {result['total_issues']}\n"
    except Exception as e:
        import traceback
        inner_err = traceback.format_exc()
        import sys as _sys
        print(f"  [WARN] 进程内检测失败，回退到子进程:\n  {inner_err.split(chr(10))[-3]}", file=_sys.stderr)
    # 回退到子进程
    detector = Path(__file__).parent / "run_all_detectors.py"
    cmd = [
        sys.executable, str(detector),
        "--input", str(chapter_path),
        "--genre", genre,
        "--mode", "fast" if fast_mode else "polish",
    ]
    if safety:
        cmd.append("--safety")
    cmd.append("--json")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return f"[ERR] 检测进程返回码 {result.returncode}\n{result.stderr}"
        import json as _json
        try:
            parsed = _json.loads(result.stdout)
            return f"判定: {parsed['classification']} | 问题: {parsed['total_issues']} 处"
        except (_json.JSONDecodeError, KeyError):
            return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] 检测超时（30秒）"
    except Exception as e:
        return f"[ERR] 检测异常: {e}\n进程内错误: {inner_err}"


def run_tracker(book_dir, chapter_num):
    """运行追踪更新，直接 import，回退到子进程"""
    try:
        from detectors.update_tracker import read_spec, update_tracker as ut_fn
        spec_path = Path(book_dir) / "规格" / ("第%03d章.json" % chapter_num)
        if spec_path.exists():
            spec = read_spec(spec_path)
            tracker_dir = Path(book_dir) / "追踪"
            tracker_dir.mkdir(parents=True, exist_ok=True)
            ut_fn(tracker_dir, spec)
        return "[OK] 进程内追踪更新完成\n"
    except Exception as e:
        import traceback
        inner_err = traceback.format_exc()
    # 回退到子进程
    tracker = Path(__file__).parent / "update_tracker.py"
    cmd = [
        sys.executable, str(tracker),
        "--book", str(book_dir),
        "--chapter", str(chapter_num),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return f"[ERR] 追踪进程返回码 {result.returncode}\n{result.stderr}"
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] 追踪更新超时"
    except Exception as e:
        return f"[ERR] 追踪异常: {e}\n进程内错误: {inner_err}"


def check_consistency(book_dir):
    tracker_dir = book_dir / "追踪"
    text_dir = book_dir / "正文"
    issues = []
    if not tracker_dir.exists():
        issues.append("追踪/ 目录不存在")
        return issues
    char_file = tracker_dir / "角色状态.md"
    if not char_file.exists():
        issues.append("追踪/角色状态.md 不存在")
    else:
        cnt = char_file.read_text(encoding="utf-8", errors="ignore").count("## ")
        if cnt == 0:
            issues.append("角色状态.md 中无角色条目")
    hook_file = tracker_dir / "伏笔.md"
    if not hook_file.exists():
        issues.append("追踪/伏笔.md 不存在")
    if not text_dir.exists() or not list(text_dir.iterdir()):
        issues.append("正文/ 目录为空")
    if not issues:
        issues.append("状态校验通过")
    return issues


def print_report(book_dir, ch_num, det_out, trk_out, consistency):
    print(f"\n{'='*55}")
    print(f"  管线报告 — {book_dir.name} 第{ch_num}章")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}")
    print(f"\n--- 检测结果 ---")
    for line in det_out.split('\n'):
        if any(kw in line for kw in ["判定:", "加权投票:", "GREEN", "YELLOW", "RED", "[OK]", "[!]"]):
            print(f"  {line.strip()}")
    print(f"\n--- 追踪更新 ---")
    for line in trk_out.split('\n'):
        s = line.strip()
        if s and not s.startswith('=') and not s.startswith('---') and s != '':
            print(f"  {s}")
    print(f"\n--- 一致性 ---")
    for i in consistency:
        print(f"  {i}")
    print(f"\n{'='*55}\n")


def main():
    p = argparse.ArgumentParser(description="one-novel-skill 管线编排器")
    p.add_argument("--book", "-b", required=True)
    p.add_argument("--chapter", "-c", type=int, default=0)
    p.add_argument("--mode", default="polish", choices=["fast","polish"])
    p.add_argument("--genre", "-g", default="general")
    p.add_argument("--safety", action="store_true")
    a = p.parse_args()
    book_dir = Path(a.book)
    if not book_dir.exists():
        print(f"[ERR] 目录不存在: {book_dir}"); sys.exit(1)
    ch = a.chapter if a.chapter else find_latest_chapter(book_dir)
    if ch == 0:
        print("[ERR] 未找到正文"); sys.exit(1)
    ch_path = book_dir / "正文" / f"第{ch:03d}章.txt"
    if not ch_path.exists():
        ch_path = book_dir / "正文" / f"第{ch:03d}章.md"
    if not ch_path.exists():
        print(f"[ERR] 第{ch}章不存在"); sys.exit(1)
    print(f"  启动: {book_dir.name} 第{ch}章 ({a.mode})")
    print(f"  [1/3] 检测...")
    det_out = run_detector(ch_path, a.genre, a.mode=="fast", a.safety)
    print(f"  [2/3] 追踪...")
    trk_out = run_tracker(book_dir, ch)
    print(f"  [3/3] 一致性检查...")
    cons = check_consistency(book_dir)
    print_report(book_dir, ch, det_out, trk_out, cons)


if __name__ == "__main__":
    main()
