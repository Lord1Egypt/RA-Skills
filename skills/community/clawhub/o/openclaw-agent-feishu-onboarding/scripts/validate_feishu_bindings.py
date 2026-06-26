#!/usr/bin/env python3
"""
Validate Feishu routing bindings in an OpenClaw config file.

Default behavior is strict for this skill:
- every Feishu route binding must include match.peer.kind and match.peer.id
- accountId must be a configured Feishu account key (e.g. "main")
- accountId must never look like a Feishu group/session id (oc_xxx)
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
from typing import Any


def _load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"[ERROR] config not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[ERROR] invalid JSON at {path}: {exc}") from exc


def _resolve_config_path(user_path: str | None) -> pathlib.Path:
    if user_path:
        return pathlib.Path(user_path).expanduser().resolve()
    env_path = os.environ.get("OPENCLAW_CONFIG_PATH")
    if env_path:
        return pathlib.Path(env_path).expanduser().resolve()
    return pathlib.Path.home().joinpath(".openclaw", "openclaw.json").resolve()


def _extract_feishu_accounts(cfg: dict[str, Any]) -> set[str]:
    accounts = (
        cfg.get("channels", {})
        .get("feishu", {})
        .get("accounts", {})
    )
    if not isinstance(accounts, dict):
        return set()
    # "default" is a pointer, not a real account definition.
    return {k for k, v in accounts.items() if k != "default" and isinstance(v, dict)}


def _validate_binding(
    binding: dict[str, Any],
    index: int,
    feishu_accounts: set[str],
    allow_account_only: bool,
) -> list[str]:
    errors: list[str] = []
    match = binding.get("match")
    if not isinstance(match, dict):
        return errors

    if match.get("channel") != "feishu":
        return errors

    account_id = match.get("accountId")
    if not isinstance(account_id, str) or not account_id.strip():
        errors.append(f"bindings[{index}]: missing or invalid match.accountId")
    else:
        if account_id.startswith("oc_"):
            errors.append(
                f'bindings[{index}]: match.accountId="{account_id}" looks like a Feishu group id; '
                "use account key (e.g. main) and put group id in match.peer.id"
            )
        if feishu_accounts and account_id not in feishu_accounts and account_id != "*":
            errors.append(
                f'bindings[{index}]: match.accountId="{account_id}" is not in channels.feishu.accounts '
                f"({sorted(feishu_accounts)})"
            )

    peer = match.get("peer")
    if peer is None:
        if not allow_account_only:
            errors.append(f"bindings[{index}]: missing match.peer (peer structure is required)")
        return errors

    if not isinstance(peer, dict):
        errors.append(f"bindings[{index}]: match.peer must be an object")
        return errors

    peer_kind = peer.get("kind")
    peer_id = peer.get("id")
    if not isinstance(peer_kind, str) or not peer_kind.strip():
        errors.append(f"bindings[{index}]: missing or invalid match.peer.kind")
    if not isinstance(peer_id, str) or not peer_id.strip():
        errors.append(f"bindings[{index}]: missing or invalid match.peer.id")

    if isinstance(peer_id, str) and peer_id.startswith("oc_") and peer_kind != "group":
        errors.append(
            f'bindings[{index}]: match.peer.id="{peer_id}" looks like Feishu group id; '
            'match.peer.kind should be "group"'
        )
    if peer_kind == "group" and isinstance(peer_id, str) and not peer_id.startswith("oc_"):
        errors.append(
            f'bindings[{index}]: match.peer.kind="group" should use group id like "oc_xxx", got "{peer_id}"'
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Feishu bindings in openclaw.json"
    )
    parser.add_argument(
        "--config",
        help="Path to openclaw.json (default: OPENCLAW_CONFIG_PATH or ~/.openclaw/openclaw.json)",
    )
    parser.add_argument(
        "--allow-account-only",
        action="store_true",
        help="Allow Feishu bindings without match.peer (account-level fallback).",
    )
    args = parser.parse_args()

    cfg_path = _resolve_config_path(args.config)
    cfg = _load_json(cfg_path)

    bindings = cfg.get("bindings", [])
    if not isinstance(bindings, list):
        print("[ERROR] top-level bindings must be an array", file=sys.stderr)
        return 2

    feishu_accounts = _extract_feishu_accounts(cfg)
    all_errors: list[str] = []
    feishu_binding_count = 0

    for i, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            continue
        match = binding.get("match")
        if isinstance(match, dict) and match.get("channel") == "feishu":
            feishu_binding_count += 1
        all_errors.extend(
            _validate_binding(
                binding=binding,
                index=i,
                feishu_accounts=feishu_accounts,
                allow_account_only=args.allow_account_only,
            )
        )

    if all_errors:
        print(f"[FAIL] Found {len(all_errors)} issue(s) in Feishu bindings:")
        for msg in all_errors:
            print(f"- {msg}")
        return 1

    print(
        "[OK] Feishu bindings are valid "
        f"(checked {feishu_binding_count} binding(s), config={cfg_path})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
