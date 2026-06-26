#!/usr/bin/env python3
"""MinerDetector billing/export utility.

This script does not scan or detect anything. It only:
1) checks billing balance,
2) creates a payment link,
3) charges 0.01 USDT for one export,
4) exports the 4 bundled text libraries.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict

BILLING_API_URL = os.environ.get("MINERDETECTOR_BILLING_API_URL", "https://skillpay.me").rstrip("/")
SKILL_ID = "82c878f5-1b74-4ee3-a32a-eeb878309ba5"
DEFAULT_CHARGE_AMOUNT = 0.01
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
INDICATOR_DIR = ROOT_DIR / "indicators"
LIB_FILES = {
    "mining_pool_websites.txt": INDICATOR_DIR / "mining_pool_websites.txt",
    "mining_software_filenames.txt": INDICATOR_DIR / "mining_software_filenames.txt",
    "mining_pool_public_ips.txt": INDICATOR_DIR / "mining_pool_public_ips.txt",
    "mining_pool_ports.txt": INDICATOR_DIR / "mining_pool_ports.txt",
}


class BillingError(RuntimeError):
    pass


def get_api_key(cli_api_key: str | None) -> str:
    api_key = cli_api_key or os.environ.get("MINERDETECTOR_API_KEY")
    if not api_key:
        raise BillingError(
            "Missing API key. Set MINERDETECTOR_API_KEY or pass --api-key. "
            "Apply here: https://x.com/MaZhenZi1/status/2034654798906269916"
        )
    return api_key


def _http_json(method: str, url: str, api_key: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    headers = {"X-API-Key": api_key}
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as json_exc:
            raise BillingError(f"HTTP {exc.code}: {body}") from json_exc
        raise BillingError(json.dumps(parsed, ensure_ascii=False)) from exc
    except urllib.error.URLError as exc:
        raise BillingError(f"Network error: {exc}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise BillingError(f"Invalid JSON response: {body}") from exc


def check_balance(user_id: str, api_key: str) -> Dict[str, Any]:
    query = urllib.parse.urlencode({"user_id": user_id})
    url = f"{BILLING_API_URL}/api/v1/billing/balance?{query}"
    return _http_json("GET", url, api_key)


def charge_user(user_id: str, api_key: str, amount: float = DEFAULT_CHARGE_AMOUNT) -> Dict[str, Any]:
    url = f"{BILLING_API_URL}/api/v1/billing/charge"
    return _http_json(
        "POST",
        url,
        api_key,
        {
            "user_id": user_id,
            "skill_id": SKILL_ID,
            "amount": amount,
        },
    )


def get_payment_link(user_id: str, api_key: str, amount: float) -> Dict[str, Any]:
    url = f"{BILLING_API_URL}/api/v1/billing/payment-link"
    return _http_json("POST", url, api_key, {"user_id": user_id, "amount": amount})


def load_libs() -> Dict[str, str]:
    result: Dict[str, str] = {}
    for name, path in LIB_FILES.items():
        if not path.exists():
            raise BillingError(f"Bundled library is missing: {path}")
        result[name] = path.read_text(encoding="utf-8", errors="replace")
    return result


def export_libs(output_dir: Path) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    exported: Dict[str, str] = {}
    for name, path in LIB_FILES.items():
        dest = output_dir / name
        shutil.copyfile(path, dest)
        exported[name] = str(dest)
    return exported


def cmd_balance(args: argparse.Namespace) -> int:
    api_key = get_api_key(args.api_key)
    data = check_balance(args.user_id, api_key)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def cmd_payment_link(args: argparse.Namespace) -> int:
    api_key = get_api_key(args.api_key)
    data = get_payment_link(args.user_id, api_key, args.amount)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    api_key = get_api_key(args.api_key)
    charge = charge_user(args.user_id, api_key, args.amount)

    success = bool(
        charge.get("success")
        or charge.get("ok")
        or charge.get("charged")
    )

    if not success:
        payload = {
            "success": False,
            "message": "Charge failed or balance is insufficient.",
            "billing": charge,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2

    libs = load_libs()
    payload: Dict[str, Any] = {
        "success": True,
        "charged_amount": args.amount,
        "skill_id": SKILL_ID,
        "billing": charge,
    }

    if args.json_only:
        payload["files"] = libs
    else:
        output_dir = Path(args.output_dir).resolve()
        payload["files"] = export_libs(output_dir)
        payload["output_dir"] = str(output_dir)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MinerDetector: bill-and-export utility for 4 bundled text libraries."
    )
    parser.add_argument("--api-key", help="SkillPay API key. Overrides MINERDETECTOR_API_KEY.")

    sub = parser.add_subparsers(dest="command", required=True)

    p_balance = sub.add_parser("balance", help="Check billing balance.")
    p_balance.add_argument("--user-id", required=True, help="Billing user identifier.")
    p_balance.set_defaults(func=cmd_balance)

    p_payment = sub.add_parser("payment-link", help="Generate a recharge/payment link.")
    p_payment.add_argument("--user-id", required=True, help="Billing user identifier.")
    p_payment.add_argument("--amount", type=float, default=5.0, help="Recharge amount in USDT.")
    p_payment.set_defaults(func=cmd_payment_link)

    p_fetch = sub.add_parser("fetch", help="Charge 0.01 USDT and export the 4 bundled files.")
    p_fetch.add_argument("--user-id", required=True, help="Billing user identifier.")
    p_fetch.add_argument("--amount", type=float, default=DEFAULT_CHARGE_AMOUNT, help="Charge amount in USDT.")
    p_fetch.add_argument(
        "--output-dir",
        default="./minerdetector-libs",
        help="Directory to write the 4 files into. Ignored when --json-only is used.",
    )
    p_fetch.add_argument(
        "--json-only",
        action="store_true",
        help="Return the 4 files in JSON instead of writing to disk.",
    )
    p_fetch.set_defaults(func=cmd_fetch)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except BillingError as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
