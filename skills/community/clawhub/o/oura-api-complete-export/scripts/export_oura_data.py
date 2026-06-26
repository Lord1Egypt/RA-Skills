#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

import requests

BASE_URL = "https://api.ouraring.com"
TOKEN_URL = "https://api.ouraring.com/oauth/token"
CONFIG_PATH = Path.home() / ".config" / "oura-oauth" / "config.json"

ENDPOINTS = [
    {"name": "personal_info", "path": "/v2/usercollection/personal_info", "kind": "single"},
    {"name": "daily_activity", "path": "/v2/usercollection/daily_activity", "kind": "date"},
    {"name": "daily_readiness", "path": "/v2/usercollection/daily_readiness", "kind": "date"},
    {"name": "daily_sleep", "path": "/v2/usercollection/daily_sleep", "kind": "date"},
    {"name": "daily_spo2", "path": "/v2/usercollection/daily_spo2", "kind": "date"},
    {"name": "daily_stress", "path": "/v2/usercollection/daily_stress", "kind": "date"},
    {"name": "daily_resilience", "path": "/v2/usercollection/daily_resilience", "kind": "date"},
    {"name": "sleep", "path": "/v2/usercollection/sleep", "kind": "date"},
    {"name": "workout", "path": "/v2/usercollection/workout", "kind": "date"},
    {"name": "session", "path": "/v2/usercollection/session", "kind": "date"},
    {"name": "tag", "path": "/v2/usercollection/tag", "kind": "date"},
    {"name": "heartrate", "path": "/v2/usercollection/heartrate", "kind": "datetime"},
]


def load_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise RuntimeError(f"Missing OAuth config: {CONFIG_PATH}. Run auth_oura_oauth.py first.")
    return json.loads(CONFIG_PATH.read_text())


def save_config(cfg: Dict[str, Any]):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n")
    os.chmod(CONFIG_PATH, 0o600)


def refresh_if_needed(cfg: Dict[str, Any], force: bool = False) -> Dict[str, Any]:
    token = cfg.get("token", {})
    now = int(time.time())
    expires_at = int(cfg.get("token_expires_at", 0))
    if not force and expires_at and now < (expires_at - 120):
        return cfg

    refresh_token = token.get("refresh_token")
    if not refresh_token:
        return cfg

    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
        },
        timeout=30,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Token refresh failed: {r.status_code} {r.text[:500]}")

    tk = r.json()
    cfg["token"] = tk
    cfg["saved_at"] = now
    cfg["token_expires_at"] = now + int(tk.get("expires_in", 3600))
    save_config(cfg)
    return cfg


def req_json(session: requests.Session, path: str, params: Optional[Dict[str, Any]] = None):
    r = session.get(BASE_URL + path, params=params, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"{r.status_code} {r.reason}: {r.text[:400]}")
    return r.json()


def fetch_endpoint(session: requests.Session, ep: Dict[str, Any], start: str, end: str):
    kind = ep["kind"]
    if kind == "single":
        data = req_json(session, ep["path"])
        return {"endpoint": ep["name"], "path": ep["path"], "count": 1, "data": data}

    params: Dict[str, Any] = {"limit": 100}
    if kind == "date":
        params["start_date"] = start
        params["end_date"] = end
    elif kind == "datetime":
        params["start_datetime"] = f"{start}T00:00:00+00:00"
        params["end_datetime"] = f"{end}T23:59:59+00:00"

    items: List[Any] = []
    next_token = None

    while True:
        if next_token:
            params["next_token"] = next_token
        payload = req_json(session, ep["path"], params=params)

        data = payload.get("data")
        if isinstance(data, list):
            items.extend(data)
        elif data is not None:
            items.append(data)

        next_token = payload.get("next_token")
        if not next_token:
            break
        time.sleep(0.1)

    return {"endpoint": ep["name"], "path": ep["path"], "count": len(items), "data": items}


def main():
    ap = argparse.ArgumentParser(description="Export all available Oura data using stored OAuth tokens")
    ap.add_argument("--start", default="2020-01-01")
    ap.add_argument("--end", default=dt.date.today().isoformat())
    ap.add_argument("--out", default="./oura_export")
    args = ap.parse_args()

    cfg = refresh_if_needed(load_config())
    access_token = cfg.get("token", {}).get("access_token")
    if not access_token:
        raise SystemExit("Missing access token. Run auth_oura_oauth.py again.")

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {access_token}"})

    summary = {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "start": args.start,
        "end": args.end,
        "results": [],
        "errors": [],
    }

    for ep in ENDPOINTS:
        name = ep["name"]
        print(f"Fetching {name}...")
        try:
            payload = fetch_endpoint(s, ep, args.start, args.end)
            (out / f"{name}.json").write_text(json.dumps(payload, indent=2) + "\n")
            summary["results"].append({"endpoint": name, "count": payload.get("count", 0)})
        except Exception as e:
            err = str(e)
            if "401" in err or "unauthorized" in err.lower():
                cfg = refresh_if_needed(cfg, force=True)
                access_token = cfg.get("token", {}).get("access_token")
                s.headers.update({"Authorization": f"Bearer {access_token}"})
                try:
                    payload = fetch_endpoint(s, ep, args.start, args.end)
                    (out / f"{name}.json").write_text(json.dumps(payload, indent=2) + "\n")
                    summary["results"].append({"endpoint": name, "count": payload.get("count", 0)})
                    continue
                except Exception as e2:
                    err = str(e2)
            print(f"  ! {name} failed: {err}")
            summary["errors"].append({"endpoint": name, "error": err})

    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"Export complete: {out}")


if __name__ == "__main__":
    main()
