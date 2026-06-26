#!/usr/bin/env python3
"""SkillPay.me billing — charge / balance / payment-link."""

import json, sys, argparse, os
import urllib.request, urllib.error

API = "https://skillpay.me/api/v1"
SKILL_ID = "015eae56-90e7-4ac8-bece-47349663f9d7"


def _key(override=None):
    return override or os.environ.get("SKILLPAY_API_KEY")


def _post(path, body, api_key):
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-API-Key": api_key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def _get(path, api_key):
    req = urllib.request.Request(f"{API}{path}", headers={"X-API-Key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def charge(user_id, amount=0.001, api_key=None):
    k = _key(api_key)
    if not k:
        return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    data = _post("/billing/charge", {
        "user_id": user_id,
        "skill_id": SKILL_ID,
        "amount": amount,
        "currency": "USDT",
        "description": "Podcast Generator",
    }, k)
    if data.get("success"):
        return {"success": True, "charged": amount, "data": data}
    return {
        "success": False,
        "needs_payment": bool(data.get("payment_url")),
        "payment_url": data.get("payment_url", ""),
        "balance": data.get("balance", 0),
        "message": data.get("message", "charge failed"),
    }


def balance(user_id, api_key=None):
    k = _key(api_key)
    if not k:
        return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    return {"success": True, "data": _get(f"/billing/balance?user_id={user_id}", k)}


def payment_link(user_id, amount=5.0, api_key=None):
    k = _key(api_key)
    if not k:
        return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    data = _post("/billing/payment-link", {
        "user_id": user_id,
        "skill_id": SKILL_ID,
        "Amount": amount,
    }, k)
    return {"success": True, "data": data}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--user-id", required=True)
    p.add_argument("--amount", type=float, default=0.001)
    p.add_argument("--api-key", default=None)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--charge", action="store_true", default=True)
    g.add_argument("--balance", action="store_true")
    g.add_argument("--payment-link", action="store_true")
    a = p.parse_args()

    if a.balance:
        r = balance(a.user_id, a.api_key)
    elif a.payment_link:
        r = payment_link(a.user_id, a.amount or 5.0, a.api_key)
    else:
        r = charge(a.user_id, a.amount, a.api_key)

    print(json.dumps(r, indent=2, ensure_ascii=False))
    sys.exit(0 if r.get("success") else 1)
