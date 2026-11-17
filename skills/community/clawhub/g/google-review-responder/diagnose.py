#!/usr/bin/env python3
"""
Review Responder — VPS Diagnostic
---------------------------------
Run this ON the VPS where OpenClaw/DaClaw lives. It checks every link in the
chain between "a review exists" and "Chris gets a Telegram ping," and tells you
exactly which link is broken.

Usage:
    python3 diagnose.py
    python3 diagnose.py --send-test-telegram   # also fires a real test message

It does NOT post anything to Google and does NOT change any config.
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

OK = "\033[92m[ OK ]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
WARN = "\033[93m[WARN]\033[0m"
INFO = "\033[96m[ -- ]\033[0m"

results = []


def report(status, label, detail=""):
    print(f"{status} {label}" + (f"  ->  {detail}" if detail else ""))
    results.append((status, label, detail))


def find_install_dir():
    """Locate the live review-responder folder on the VPS."""
    candidates = [
        Path.home() / "review-responder",
        Path.home() / ".openclaw" / "workspace" / "review-responder",
        Path("/root/review-responder"),
        Path(__file__).parent.resolve(),
    ]
    for c in candidates:
        try:
            if (c / "gbp_reviews.py").exists():
                return c
        except (PermissionError, OSError):
            continue
    return None


def check_dependencies():
    missing = []
    for mod in ("requests", "google.oauth2.credentials", "google.auth.transport.requests"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        report(FAIL, "Python dependencies", f"missing: {', '.join(missing)} — run: pip install google-auth google-auth-oauthlib requests")
        return False
    report(OK, "Python dependencies", "google-auth + requests present")
    return True


def check_config(install_dir):
    """review-responder.config.json holds the telegram_chat_id + approval channel."""
    cfg_path = install_dir / "review-responder.config.json"
    if not cfg_path.exists():
        report(FAIL, "review-responder.config.json", f"NOT FOUND at {cfg_path} — Telegram chat id lives here. No config = no pings.")
        return None
    try:
        cfg = json.loads(cfg_path.read_text())
    except Exception as e:
        report(FAIL, "review-responder.config.json", f"exists but won't parse: {e}")
        return None

    channel = cfg.get("approval_channel", "")
    report(OK if channel else WARN, "approval_channel", channel or "(empty)")

    if channel == "telegram":
        chat_id = cfg.get("telegram_chat_id", "")
        if not chat_id:
            report(FAIL, "telegram_chat_id", "EMPTY — agent has nowhere to send the ping. This alone explains zero notifications.")
        else:
            report(OK, "telegram_chat_id", str(chat_id))
    return cfg


def check_openclaw_telegram():
    """The bot token lives in openclaw.json under channels.telegram.botToken."""
    candidates = [
        Path.home() / ".openclaw" / "openclaw.json",
        Path.home() / "openclaw.json",
        Path("/root/.openclaw/openclaw.json"),
    ]
    path = next((p for p in candidates if p.exists()), None)
    if not path:
        report(WARN, "openclaw.json", "not found in usual spots — locate it and confirm channels.telegram.botToken is set")
        return None
    try:
        oc = json.loads(path.read_text())
    except Exception as e:
        report(FAIL, "openclaw.json", f"won't parse: {e}")
        return None

    token = (oc.get("channels", {}).get("telegram", {}) or {}).get("botToken", "")
    if not token:
        report(FAIL, "telegram botToken", f"channels.telegram.botToken empty in {path} — bot was never wired up. (Your 3/20 note: 'Telegram connection in progress.')")
    else:
        report(OK, "telegram botToken", "present (BotFather token set)")

    # heartbeat interval
    hb = (oc.get("agent", {}).get("heartbeat", {}) or {}).get("every", "")
    report(OK if hb else WARN, "heartbeat interval", hb or "not set — agent may never run the check")
    return oc


def check_clients(install_dir):
    clients_dir = install_dir / "clients"
    files = [f for f in glob.glob(str(clients_dir / "*.json")) if not f.endswith("_template.json")]
    if not files:
        report(FAIL, "client configs", f"no real client .json in {clients_dir} (only _template.json). Nothing to check = nothing to ping about.")
    else:
        report(OK, "client configs", f"{len(files)} found: {', '.join(Path(f).stem for f in files)}")
    return files


def check_oauth_and_api(client_file):
    """The #1 silent killer: expired refresh token (Testing-mode = 7-day expiry)."""
    name = Path(client_file).stem
    try:
        import requests
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
    except ImportError:
        return
    try:
        cfg = json.loads(Path(client_file).read_text())
    except Exception as e:
        report(FAIL, f"[{name}] config parse", str(e))
        return

    for field in ("refresh_token", "oauth_client_id", "oauth_client_secret", "account_id", "location_id"):
        if not cfg.get(field) or str(cfg.get(field)).startswith("YOUR_"):
            report(FAIL, f"[{name}] {field}", "missing or still a placeholder")
            return

    # 1) Can we exchange the refresh token for an access token?
    try:
        creds = Credentials(
            token=None,
            refresh_token=cfg["refresh_token"],
            client_id=cfg["oauth_client_id"],
            client_secret=cfg["oauth_client_secret"],
            token_uri="https://oauth2.googleapis.com/token",
        )
        creds.refresh(Request())
        token = creds.token
        report(OK, f"[{name}] OAuth refresh", "refresh token still valid")
    except Exception as e:
        msg = str(e)
        hint = ""
        if "invalid_grant" in msg:
            hint = " -> invalid_grant = refresh token EXPIRED/REVOKED. Most likely cause if it worked then died. Fix: set OAuth consent screen to 'In production' (Testing mode kills tokens after 7 days), then re-run get_client_token.py."
        report(FAIL, f"[{name}] OAuth refresh", msg + hint)
        return

    # 2) Does the reviews endpoint actually answer?
    acct, loc = cfg["account_id"], cfg["location_id"]
    acct = acct.split("/")[-1]
    loc = loc.split("/")[-1]
    url = f"https://mybusiness.googleapis.com/v4/accounts/{acct}/locations/{loc}/reviews"
    try:
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"},
                         params={"pageSize": 5, "orderBy": "updateTime desc"}, timeout=30)
    except Exception as e:
        report(FAIL, f"[{name}] reviews API call", str(e))
        return

    if r.status_code == 200:
        n = len(r.json().get("reviews", []))
        report(OK, f"[{name}] reviews API", f"200 OK — {n} review(s) returned. Pipeline to Google is healthy.")
    elif r.status_code == 403:
        report(FAIL, f"[{name}] reviews API", "403 — project not allowlisted for the legacy Google My Business API, OR the API is disabled. Request access in Cloud console / enable the API.")
    elif r.status_code == 404:
        report(FAIL, f"[{name}] reviews API", "404 — account_id/location_id likely wrong. Re-pull them (see SETUP.md step 2).")
    elif r.status_code == 429:
        report(WARN, f"[{name}] reviews API", "429 — rate limited / quota. Transient.")
    else:
        report(FAIL, f"[{name}] reviews API", f"{r.status_code}: {r.text[:300]}")


def send_test_telegram(install_dir):
    cfg_path = install_dir / "review-responder.config.json"
    oc_candidates = [Path.home() / ".openclaw" / "openclaw.json", Path.home() / "openclaw.json", Path("/root/.openclaw/openclaw.json")]
    if not cfg_path.exists():
        report(FAIL, "test telegram", "no config file, can't find chat id")
        return
    cfg = json.loads(cfg_path.read_text())
    chat_id = cfg.get("telegram_chat_id", "")
    oc_path = next((p for p in oc_candidates if p.exists()), None)
    token = ""
    if oc_path:
        oc = json.loads(oc_path.read_text())
        token = (oc.get("channels", {}).get("telegram", {}) or {}).get("botToken", "")
    if not (chat_id and token):
        report(FAIL, "test telegram", "need both botToken (openclaw.json) and telegram_chat_id (config) to send a test")
        return
    import requests
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": "Review Responder diagnostic: Telegram path is working."}, timeout=20)
    if r.status_code == 200:
        report(OK, "test telegram", "message sent — check your phone. If it arrives, the notification path is fine.")
    else:
        report(FAIL, "test telegram", f"{r.status_code}: {r.text[:300]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send-test-telegram", action="store_true", help="fire a real test message through the bot")
    args = ap.parse_args()

    print("\n=== Review Responder Diagnostic ===\n")
    install_dir = find_install_dir()
    if not install_dir:
        report(FAIL, "install dir", "could not find gbp_reviews.py — run this from inside the review-responder folder on the VPS")
        sys.exit(1)
    report(INFO, "install dir", str(install_dir))

    check_dependencies()
    check_config(install_dir)
    check_openclaw_telegram()
    clients = check_clients(install_dir)
    for cf in clients:
        check_oauth_and_api(cf)
    if args.send_test_telegram:
        send_test_telegram(install_dir)

    print("\n=== Summary ===")
    fails = [r for r in results if r[0] == FAIL]
    if not fails:
        print(f"{OK} Everything the script can see is healthy. If you still get no pings, the issue is the OpenClaw agent loop itself (is DaClaw running? check the process / systemctl status).")
    else:
        print(f"{FAIL} {len(fails)} problem(s) found — fix these first:")
        for _, label, detail in fails:
            print(f"   - {label}: {detail}")
    print()


if __name__ == "__main__":
    main()
