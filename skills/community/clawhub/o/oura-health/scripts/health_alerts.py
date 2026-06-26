#!/usr/bin/env /opt/homebrew/bin/python3.11
"""Oura Ring health alert checker. Outputs warnings, empty if nothing notable."""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta

CREDS_PATH = os.path.expanduser("~/.config/oura/credentials.json")


def load_credentials():
    try:
        with open(CREDS_PATH) as f:
            creds = json.load(f)
        token = creds.get("personal_access_token")
        base = creds.get("base_url", "https://api.ouraring.com/v2").rstrip("/")
        if not token:
            return None, None
        return token, base
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None


def api_get(token, base, path, params=None):
    url = f"{base}{path}"
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url += "?" + urllib.parse.urlencode(filtered)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def days_ago_str(n):
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


def main():
    token, base = load_credentials()
    if not token:
        # Silent exit — no credentials means no alerts
        sys.exit(0)

    alerts = []
    today = today_str()
    yesterday = days_ago_str(1)
    week_ago = days_ago_str(7)

    # ── Readiness check ─────────────────────────────────────────────────
    readiness = api_get(token, base, "/usercollection/daily_readiness",
                        {"start_date": today, "end_date": today})
    if readiness and readiness.get("data"):
        r = readiness["data"][-1]
        score = r.get("score")
        if score is not None and score < 70:
            alerts.append(f"🔴 Low readiness score: {score} (threshold: 70)")

        contribs = r.get("contributors", {})
        recovery = contribs.get("recovery_index")
        if recovery is not None and recovery < 30:
            alerts.append(f"🔴 Low recovery index: {recovery} (threshold: 30)")

    # ── Temperature check ───────────────────────────────────────────────
    if readiness and readiness.get("data"):
        r = readiness["data"][-1]
        temp_dev = r.get("temperature_deviation")
        if temp_dev is not None and abs(temp_dev) > 0.5:
            direction = "above" if temp_dev > 0 else "below"
            alerts.append(f"🔴 Body temp {direction} baseline: {temp_dev:+.2f}°C (threshold: ±0.5°C)")

    # ── Sleep duration check ────────────────────────────────────────────
    sleep_sessions = api_get(token, base, "/usercollection/sleep",
                             {"start_date": yesterday, "end_date": today})
    if sleep_sessions and sleep_sessions.get("data"):
        session = sleep_sessions["data"][-1]
        total_seconds = session.get("total_sleep_duration")
        if total_seconds is not None:
            hours = total_seconds / 3600
            if hours < 6:
                alerts.append(f"🔴 Short sleep: {hours:.1f}h (threshold: 6h)")

    # ── HRV trend check (3+ days declining) ─────────────────────────────
    week_sleep = api_get(token, base, "/usercollection/sleep",
                         {"start_date": week_ago, "end_date": today})
    if week_sleep and week_sleep.get("data"):
        hrvs = []
        for s in week_sleep["data"]:
            hrv = s.get("average_hrv")
            if hrv is not None:
                hrvs.append(hrv)

        if len(hrvs) >= 3:
            # Check if last 3+ readings are all declining
            consecutive_down = 0
            for i in range(len(hrvs) - 1, 0, -1):
                if hrvs[i] < hrvs[i - 1]:
                    consecutive_down += 1
                else:
                    break
            if consecutive_down >= 3:
                alerts.append(f"🔴 HRV declining for {consecutive_down} consecutive days "
                              f"({hrvs[-consecutive_down - 1]:.0f} → {hrvs[-1]:.0f} ms)")

    # ── Resting HR spike check ──────────────────────────────────────────
    week_readiness = api_get(token, base, "/usercollection/daily_readiness",
                             {"start_date": week_ago, "end_date": today})
    if week_sleep and week_sleep.get("data"):
        resting_hrs = []
        for s in week_sleep["data"]:
            hr = s.get("lowest_heart_rate")
            if hr is not None:
                resting_hrs.append(hr)

        if len(resting_hrs) >= 3:
            # Compare latest to 7-day average (excluding latest)
            avg_hr = sum(resting_hrs[:-1]) / len(resting_hrs[:-1])
            latest_hr = resting_hrs[-1]
            if latest_hr > avg_hr + 5:
                alerts.append(f"🔴 Resting HR spike: {latest_hr} bpm "
                              f"(7-day avg: {avg_hr:.0f} bpm, +{latest_hr - avg_hr:.0f} above)")

    # ── Output ──────────────────────────────────────────────────────────
    for alert in alerts:
        print(alert)

    # Always exit 0 — alerts are informational, not errors
    sys.exit(0)


if __name__ == "__main__":
    main()
