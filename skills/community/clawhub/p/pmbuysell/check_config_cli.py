"""
Validate pmbuysell account configuration for agents/users.

Usage:
  python -m pmbuysell.skills.check_config_cli
  python -m pmbuysell.skills.check_config_cli --account ACC1
  python -m pmbuysell.skills.check_config_cli --require-redeem
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from .local_config import (
    get_account,
    list_account_ids,
    get_relayer_settings,
    get_builder_api_creds_for_account,
)


_RE_HEX_ADDR = re.compile(r"^0x[0-9a-fA-F]{40}$")


def _is_probably_eth_address(s: str | None) -> bool:
    if not s:
        return False
    return bool(_RE_HEX_ADDR.match(str(s).strip()))


def _is_probably_private_key(s: str | None) -> bool:
    if not s:
        return False
    v = str(s).strip()
    # allow 0x-prefixed or raw 64 hex
    if v.startswith("0x"):
        v = v[2:]
    return bool(re.fullmatch(r"[0-9a-fA-F]{64}", v))


def _check_one_account(account_id: str, require_redeem: bool) -> dict[str, Any]:
    acc = get_account(account_id)
    if not acc:
        return {
            "account": account_id,
            "ok": False,
            "missing": ["account_config"],
            "message": "未找到账号配置（检查 PM_ACCOUNT_IDS 或 PM_ACCOUNTS_JSON）",
        }

    missing: list[str] = []
    pk = acc.get("private_key")
    funder = acc.get("funder")

    if not pk:
        missing.append("private_key")
    elif not _is_probably_private_key(str(pk)):
        missing.append("private_key_format")

    if not funder:
        missing.append("funder")
    elif not _is_probably_eth_address(str(funder)):
        missing.append("funder_format")

    if require_redeem:
        relayer_url, chain_id = get_relayer_settings()
        if not relayer_url:
            missing.append("RELAYER_URL")
        if not chain_id:
            missing.append("CHAIN_ID")

        k, s, p = get_builder_api_creds_for_account(account_id)
        if not k:
            missing.append(f"{account_id.upper()}_BUILDER_API_KEY")
        if not s:
            missing.append(f"{account_id.upper()}_BUILDER_SECRET")
        if not p:
            missing.append(f"{account_id.upper()}_BUILDER_PASSPHRASE")

    ok = len(missing) == 0
    return {
        "account": account_id,
        "ok": ok,
        "missing": missing,
        "message": None if ok else "配置不完整/格式异常",
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Check pmbuysell .env/account config")
    p.add_argument("--account", default="", help="只检查某个账号，如 ACC1；不填则检查全部")
    p.add_argument("--require-redeem", action="store_true", help="额外检查 auto_redeem 所需 relayer/builder 配置")
    args = p.parse_args()

    if args.account.strip():
        accounts = [args.account.strip().upper()]
    else:
        accounts = list_account_ids()

    if not accounts:
        result = {
            "ok": False,
            "message": "未发现任何账号配置（PM_ACCOUNT_IDS 或 PM_ACCOUNTS_JSON 为空）",
            "accounts": [],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    checks = [_check_one_account(a, require_redeem=bool(args.require_redeem)) for a in accounts]
    ok_all = all(c.get("ok") for c in checks)
    result = {"ok": ok_all, "message": None if ok_all else "存在账号配置缺失/异常", "accounts": checks}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()

