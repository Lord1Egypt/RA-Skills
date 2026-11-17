#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sync_contract_guard.py — 把 canonical contract_guard.py 同步/校验到算量技能。

canonical: lis-skill-bus/lib/contract_guard.py
副本:      <skill>/scripts/contract_guard.py

副本首行固定为：
    # VENDORED from lis-skill-bus/lib/contract_guard.py sha256:<canonical 哈希>

用法：
    python3 scripts/sync_contract_guard.py --check
    python3 scripts/sync_contract_guard.py --apply
    python3 scripts/sync_contract_guard.py --check --dest-root /tmp/sandbox
    python3 scripts/sync_contract_guard.py --apply --dest-root /tmp/sandbox

规则：
* --check 对缺失副本只打印 missing，不算失败；副本不一致才算失败（exit 1）。
* --apply 覆盖前先备份；无 vendored 头且内容与 canonical 不一致（疑似手改）
  默认拒写并 exit 1，只有显式 --force 才会备份后覆盖。
* 纯 stdlib，不联网。
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CANONICAL = REPO_ROOT / "lib" / "contract_guard.py"
DEFAULT_SKILLS_ROOT = Path.home() / ".codex" / "skills"
SKILL_SLUGS = (
    "gangjiegou-suanliang",
    "tujian-suanliang",
    "anzhuang-suanliang",
    "yuanlin-suanliang",
    "zhuangshi-suanliang",
)
HEADER_PREFIX = "# VENDORED from lis-skill-bus/lib/contract_guard.py sha256:"
HEADER_RE = re.compile(
    r"^# VENDORED from lis-skill-bus/lib/contract_guard\.py sha256:([0-9a-fA-F]{64})\s*$"
)
REL_TARGET = Path("scripts") / "contract_guard.py"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_canonical(path: Path):
    if not path.is_file():
        raise SystemExit("canonical 不存在: %s" % path)
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        data += b"\n"
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit("canonical 不是 UTF-8: %s（%s）" % (path, exc))
    return text, _sha256(data)


def _targets(args):
    if args.dest_root:
        root = Path(args.dest_root).expanduser().resolve()
        if not root.is_dir():
            raise SystemExit("--dest-root 不是目录: %s" % root)
        dirs = [
            p
            for p in sorted(root.iterdir())
            if p.is_dir() and not p.name.startswith(".") and p.name != "__pycache__"
        ]
        if args.skills:
            wanted = {s.strip() for s in args.skills.split(",") if s.strip()}
            dirs = [p for p in dirs if p.name in wanted]
        return [(p.name, p / REL_TARGET) for p in dirs]

    root = Path(args.skills_root).expanduser()
    slugs = SKILL_SLUGS
    if args.skills:
        slugs = tuple(s.strip() for s in args.skills.split(",") if s.strip())
    return [(slug, root / slug / REL_TARGET) for slug in slugs]


def _inspect(target: Path, canonical_text: str, canonical_hash: str):
    """返回 (status, detail)。status: missing/ok/stale/unmanaged-identical/hand-edited。"""
    if not target.exists():
        return "missing", ""
    try:
        text = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return "hand-edited", "读不了: %s" % exc

    if "\n" in text:
        first, rest = text.split("\n", 1)
    else:
        first, rest = text, ""
    match = HEADER_RE.match(first)
    if match:
        vendored_hash = match.group(1).lower()
        if vendored_hash == canonical_hash and rest == canonical_text:
            return "ok", vendored_hash
        return "stale", "vendored=%s canonical=%s" % (vendored_hash[:12], canonical_hash[:12])
    if text == canonical_text:
        return "unmanaged-identical", "内容一致但缺 vendored 头"
    return "hand-edited", "无 vendored 头且内容与 canonical 不一致"


def _backup(target: Path) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = target.with_name(target.name + ".bak." + stamp)
    counter = 1
    while backup.exists():
        backup = target.with_name(target.name + ".bak.%s-%d" % (stamp, counter))
        counter += 1
    shutil.copy2(target, backup)
    return backup


def _write(target: Path, canonical_text: str, canonical_hash: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    content = HEADER_PREFIX + canonical_hash + "\n" + canonical_text
    tmp = target.with_name(target.name + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(target)


def cmd_check(args, canonical_text: str, canonical_hash: str) -> int:
    ok = missing = bad = 0
    print("[check] canonical sha256=%s" % canonical_hash)
    for name, target in _targets(args):
        status, detail = _inspect(target, canonical_text, canonical_hash)
        if status == "ok":
            ok += 1
            print("ok        %-24s %s" % (name, target))
        elif status == "missing":
            missing += 1
            print("missing   %-24s %s" % (name, target))
        else:
            bad += 1
            print("MISMATCH  %-24s %s (%s: %s)" % (name, target, status, detail))
    print(
        "[check] ok=%d mismatch=%d missing=%d -> %s"
        % (ok, bad, missing, "FAIL" if bad else "PASS")
    )
    return 1 if bad else 0


def cmd_apply(args, canonical_text: str, canonical_hash: str) -> int:
    applied = uptodate = refused = 0
    print("[apply] canonical sha256=%s" % canonical_hash)
    for name, target in _targets(args):
        status, detail = _inspect(target, canonical_text, canonical_hash)
        if status == "ok":
            uptodate += 1
            print("up-to-date %-24s %s" % (name, target))
            continue
        if status == "hand-edited" and not args.force:
            refused += 1
            print(
                "REFUSE     %-24s %s (%s)；人工核对后用 --force（会先备份）"
                % (name, target, detail)
            )
            continue
        if target.exists():
            backup = _backup(target)
            print("backup     %-24s %s" % (name, backup))
        _write(target, canonical_text, canonical_hash)
        applied += 1
        print("apply      %-24s %s (%s)" % (name, target, status))
    print(
        "[apply] applied=%d up-to-date=%d refused=%d -> %s"
        % (applied, uptodate, refused, "FAIL" if refused else "PASS")
    )
    return 1 if refused else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="同步/校验 contract_guard.py 到算量技能（纯 stdlib）"
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true", help="只校验副本是否与 canonical 一致")
    action.add_argument("--apply", action="store_true", help="复制 canonical 并写 vendored 头")
    parser.add_argument("--canonical", default=str(DEFAULT_CANONICAL), help="canonical 文件路径")
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT), help="技能根目录，默认 $CODEX_HOME/skills")
    parser.add_argument("--dest-root", help="沙箱根目录：把其下每个一级子目录当作一个技能")
    parser.add_argument("--skills", help="逗号分隔的技能名过滤，例如 gangjiegou-suanliang")
    parser.add_argument("--force", action="store_true", help="--apply 时允许覆盖无 vendored 头的手改文件（先备份）")
    args = parser.parse_args(argv)

    canonical_text, canonical_hash = _load_canonical(Path(args.canonical).expanduser())
    if args.check:
        return cmd_check(args, canonical_text, canonical_hash)
    return cmd_apply(args, canonical_text, canonical_hash)


if __name__ == "__main__":
    sys.exit(main())
