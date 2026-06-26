#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import sys

import yaml


BASE_DIR = pathlib.Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config.yaml"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize obsidian-sync-kb for a specific Obsidian vault")
    parser.add_argument("--vault-root", required=True, help="Absolute path to the Obsidian vault root")
    parser.add_argument("--inbox-dir", default="笔记同步助手", help="Inbox directory relative to the vault root")
    parser.add_argument("--research-dir", default="Research/同步助手主题卡片", help="Research cards directory relative to the vault root")
    parser.add_argument("--topic-updates-dir", default="Research/同步助手主题更新日志", help="Topic update log directory relative to the vault root")
    parser.add_argument("--daily-digest-dir", default="Research/同步助手今日变更摘要", help="Daily digest directory relative to the vault root")
    parser.add_argument("--enable-network", dest="enable_network", action="store_true", help="Enable source fetching and limited public search")
    parser.add_argument("--disable-network", dest="enable_network", action="store_false", help="Disable network reads during build")
    parser.set_defaults(enable_network=True)
    parser.add_argument("--full-rescan-days", type=int, default=7, help="How often a full backscan should run")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing config.yaml")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    vault_root = pathlib.Path(args.vault_root).expanduser().resolve()
    if not vault_root.exists() or not vault_root.is_dir():
        print(f"vault root not found: {vault_root}", file=sys.stderr)
        return 2
    if DEFAULT_CONFIG_PATH.exists() and not args.force:
        existing = yaml.safe_load(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8")) or {}
        if str(existing.get("vault_root") or "").strip() == str(vault_root):
            print(f"config already initialized: {DEFAULT_CONFIG_PATH}")
            return 0
        print(f"config exists: {DEFAULT_CONFIG_PATH} (use --force to overwrite)", file=sys.stderr)
        return 2

    config = {
        "vault_root": str(vault_root),
        "inbox_dir": args.inbox_dir,
        "research_dir": args.research_dir,
        "topic_updates_dir": args.topic_updates_dir,
        "daily_digest_dir": args.daily_digest_dir,
        "artifacts_dir": "artifacts",
        "state_dir": "state",
        "exclude_bad_capture": True,
        "chunking": {
            "target_min_chars": 400,
            "target_max_chars": 800,
            "overlap_chars": 100,
        },
        "promotion": {
            "min_quality": 0.55,
            "min_docs": 3,
        },
        "research": {
            "min_chars": 220,
            "max_external_sources": 3,
            "network_timeout": 10,
            "enable_network": bool(args.enable_network),
        },
        "scan": {
            "full_rescan_days": args.full_rescan_days,
        },
    }
    DEFAULT_CONFIG_PATH.write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    inbox_path = vault_root / args.inbox_dir
    print(f"wrote config: {DEFAULT_CONFIG_PATH}")
    print(f"vault: {vault_root}")
    if inbox_path.exists():
        print(f"inbox: {inbox_path}")
    else:
        print(f"warning: inbox does not exist yet: {inbox_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
