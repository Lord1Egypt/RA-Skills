#!/usr/bin/env python3
"""Sync Fitbit data to local storage."""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import httpx
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data" / "user_default"
TOKEN_FILE = BASE_DIR / "data" / "fitbit_token.json"
API_BASE = "https://api.fitbit.com"


def get_headers():
    """Get auth headers, refreshing token if needed."""
    if not TOKEN_FILE.exists():
        print("ERROR: No token found. Run fitbit_auth.py first.")
        sys.exit(1)
    with open(TOKEN_FILE) as f:
        tokens = json.load(f)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def fetch(endpoint, headers):
    """Fetch from Fitbit API with error handling."""
    url = f"{API_BASE}{endpoint}"
    resp = httpx.get(url, headers=headers, timeout=30)
    if resp.status_code == 401:
        print("Token expired. Re-run fitbit_auth.py or implement refresh.")
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


def sync_daily_summary(headers, start_date, end_date):
    """Sync daily activity, sleep, and heart rate summaries."""
    print(f"Syncing daily summaries: {start_date} to {end_date}")

    # Steps time series
    try:
        data = fetch(f"/1/user/-/activities/steps/date/{start_date}/{end_date}.json", headers)
        save("steps_daily.json", data)
    except Exception as e:
        print(f"  Steps failed: {e}")

    # Calories time series
    try:
        data = fetch(f"/1/user/-/activities/calories/date/{start_date}/{end_date}.json", headers)
        save("calories_daily.json", data)
    except Exception as e:
        print(f"  Calories failed: {e}")

    # Heart rate time series
    try:
        data = fetch(f"/1/user/-/activities/heart/date/{start_date}/{end_date}.json", headers)
        save("heart_rate_daily.json", data)
    except Exception as e:
        print(f"  Heart rate failed: {e}")

    # Sleep
    try:
        data = fetch(f"/1.2/user/-/sleep/date/{start_date}/{end_date}.json", headers)
        save("sleep_daily.json", data)
    except Exception as e:
        print(f"  Sleep failed: {e}")

    print("Daily summaries synced.")


def sync_hrv(headers, start_date, end_date):
    """Sync HRV data."""
    print("Syncing HRV data...")
    data = fetch(f"/1/user/-/hrv/date/{start_date}/{end_date}.json", headers)
    save("hrv_daily.json", data)


def sync_spo2(headers, start_date, end_date):
    """Sync SpO2 data."""
    print("Syncing SpO2 data...")
    data = fetch(f"/1/user/-/spo2/date/{start_date}/{end_date}.json", headers)
    save("spo2_daily.json", data)


def sync_breathing_rate(headers, start_date, end_date):
    """Sync breathing rate data."""
    print("Syncing breathing rate...")
    data = fetch(f"/1/user/-/br/date/{start_date}/{end_date}.json", headers)
    save("breathing_rate_daily.json", data)


def sync_skin_temp(headers, start_date, end_date):
    """Sync skin temperature data."""
    print("Syncing skin temperature...")
    data = fetch(f"/1/user/-/temp/skin/date/{start_date}/{end_date}.json", headers)
    save("skin_temp_daily.json", data)


def sync_profile(headers):
    """Sync user profile."""
    print("Syncing profile...")
    data = fetch("/1/user/-/profile.json", headers)
    save("profile.json", data)


def save(filename, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / filename
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 365
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    headers = get_headers()
    sync_profile(headers)
    sync_daily_summary(headers, start_date, end_date)
    for name, fn in [("HRV", sync_hrv), ("SpO2", sync_spo2), ("Breathing rate", sync_breathing_rate), ("Skin temp", sync_skin_temp)]:
        try:
            fn(headers, start_date, end_date)
        except Exception as e:
            print(f"  {name} failed: {e}")

    print(f"\nAll data synced to {DATA_DIR}")
    print(f"Date range: {start_date} to {end_date} ({days} days)")


if __name__ == "__main__":
    main()
