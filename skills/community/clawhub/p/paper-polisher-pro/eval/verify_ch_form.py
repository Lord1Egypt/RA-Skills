#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_ch_form.py — CH 英文包形态验收（v7.2.0 从单测套件摘出为独立脚本）。

为什么独立：该验收需要"在无 SKILL_ZH 的包副本上跑全量 smoke"（约 20 分钟，
独占型），混在并行单测套件里曾两次引发全局文件竞态（SKILL_ZH.md 被从正本
删丢的真实事故）。发布前由发布链**串行独占**调用本脚本，不进入 discover 套件。

用法: python3 eval/verify_ch_form.py          # 在 trunk 副本上验收 CH 形态
退出: 0 = 验收通过；非 0 = 阻断发布。
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent


def main():
    lock = Path(tempfile.gettempdir()) / "ppp_chform_verify.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
    except FileExistsError:
        print("另一实例在跑（锁在位），跳过", file=sys.stderr)
        return 0
    try:
        copy = Path(tempfile.mkdtemp(prefix="ppp_chform_")) / "pkg"
        shutil.copytree(PKG, copy,
                        ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                      "*.pyc", "score_cache.json"))
        (copy / "SKILL_ZH.md").unlink()
        print("== CH 英文包形态验收（副本隔离，正本只读）==")
        p = subprocess.run([sys.executable, str(copy / "eval" / "release_smoke.py"),
                            "--fast"],
                           capture_output=True, text=True, timeout=2400,
                           encoding="utf-8", cwd=str(copy))
        if "Traceback" in p.stderr[:2000]:
            print("FAIL: CH 形态下 smoke 崩溃——stderr 尾部：", file=sys.stderr)
            print(p.stderr[-1200:], file=sys.stderr)
            print("---- stdout 尾部（崩前进度）----", file=sys.stderr)
            print(p.stdout[-800:], file=sys.stderr)
            return 1
        if "[汇总]" not in p.stdout:
            print("FAIL: CH 形态下 smoke 未跑完", file=sys.stderr)
            return 1
        import re
        m = re.search(r"\[汇总\] total=\d+ pass=\d+ fail=(\d+)", p.stdout)
        fails = int(m.group(1)) if m else -1
        print(f"CH 形态 smoke: {m.group(0) if m else '汇总缺失'}")
        if fails > 0:
            print("CH 形态 fail 明细：", file=sys.stderr)
            for ln in p.stdout.splitlines():
                if ln.startswith("[FAIL]"):
                    print(ln, file=sys.stderr)
        return 0 if fails == 0 else 1
    finally:
        try:
            os.unlink(lock)
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(copy, ignore_errors=True)  # v7.2.0 收尾：副本用完即清（此前路径写错未清）
        except NameError:
            pass


if __name__ == "__main__":
    sys.exit(main())
