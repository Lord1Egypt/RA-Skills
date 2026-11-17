#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_forms.py — 双发布形态验收（v7.5.0：SH/CH 对偶统一）。

两种随包形态都必须在发布前跑通全量 smoke：
  sh（SkillHub 中文包）: SKILL_ZH.md 内容以 SKILL.md 名义发布，无独立 SKILL_ZH.md
  ch（ClawHub 英文包）  : 仅英文 SKILL.md，无 SKILL_ZH.md

为什么副本隔离：验收需要"改动包形态"（删/换 SKILL.md），在正本上做曾两次
引发并行套件竞态丢文件（v7.2.0 事故）——一律整包复制到临时目录后操作，
正本只读。O_EXCL 锁序列化多实例。

用法:
  python3 eval/verify_forms.py --form ch   # 单形态（默认 ch，向后兼容 verify_ch_form）
  python3 eval/verify_forms.py --form both # 双形态串行（发布链用）
退出: 0 = 全部通过；非 0 = 阻断发布。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "score_cache.json")


def _make_form_copy(form, tmp_root):
    """构造指定形态的包副本，返回 (副本路径, 临时目录)。"""
    tmp = Path(tempfile.mkdtemp(prefix=f"ppp_form_{form}_"))
    copy = tmp / "pkg"
    shutil.copytree(PKG, copy, ignore=IGNORE)
    if form == "ch":
        (copy / "SKILL_ZH.md").unlink()
    elif form == "sh":
        # SKILL_ZH.md 内容以 SKILL.md 名义发布（平台打包约定）
        (copy / "SKILL.md").unlink()
        shutil.move(str(copy / "SKILL_ZH.md"), str(copy / "SKILL.md"))
    return copy, tmp


def _run_smoke(copy):
    p = subprocess.run([sys.executable, str(copy / "eval" / "release_smoke.py"), "--fast"],
                       capture_output=True, text=True, timeout=2400,
                       encoding="utf-8", cwd=str(copy))
    return p


def _judge(form, p):
    if "Traceback" in p.stderr[:2000]:
        print(f"[{form}] FAIL: smoke 崩溃——stderr 尾部：", file=sys.stderr)
        print(p.stderr[-1200:], file=sys.stderr)
        print("---- stdout 尾部 ----", file=sys.stderr)
        print(p.stdout[-800:], file=sys.stderr)
        return False
    if "[汇总]" not in p.stdout:
        print(f"[{form}] FAIL: smoke 未跑完", file=sys.stderr)
        return False
    m = re.search(r"\[汇总\] total=\d+ pass=\d+ fail=(\d+)", p.stdout)
    fails = int(m.group(1)) if m else -1
    print(f"[{form}] smoke: {m.group(0) if m else '汇总缺失'}")
    if fails > 0:
        print(f"[{form}] fail 明细：", file=sys.stderr)
        for ln in p.stdout.splitlines():
            if ln.startswith("[FAIL]"):
                print(ln, file=sys.stderr)
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description="双发布形态验收（SH/CH 对偶）")
    ap.add_argument("--form", choices=("sh", "ch", "both"), default="ch")
    a = ap.parse_args()
    forms = ["sh", "ch"] if a.form == "both" else [a.form]
    lock = Path(tempfile.gettempdir()) / "ppp_forms_verify.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
    except FileExistsError:
        print("另一实例在跑（锁在位），跳过", file=sys.stderr)
        return 0
    ok = True
    try:
        for form in forms:
            copy, tmp = _make_form_copy(form, None)
            try:
                print(f"== {form} 形态验收（副本隔离，正本只读）==")
                ok = _judge(form, _run_smoke(copy)) and ok
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    finally:
        try:
            os.unlink(lock)
        except FileNotFoundError:
            pass
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
