#!/usr/bin/env python3
"""Query Fitbit data from local cache or API.

Usage:
  uv run scripts/fitbit_query.py sleep [days]
  uv run scripts/fitbit_query.py steps [days]
  uv run scripts/fitbit_query.py heart_rate [days]
  uv run scripts/fitbit_query.py hrv [days]
  uv run scripts/fitbit_query.py spo2 [days]
  uv run scripts/fitbit_query.py skin_temp [days]
  uv run scripts/fitbit_query.py breathing_rate [days]
  uv run scripts/fitbit_query.py profile
  uv run scripts/fitbit_query.py all [days]
"""

import json
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
    if not TOKEN_FILE.exists():
        print("ERROR: No Fitbit token. Run: uv run scripts/fitbit_auth.py")
        sys.exit(1)
    with open(TOKEN_FILE) as f:
        tokens = json.load(f)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def load_local(filename):
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


def fetch_api(endpoint, headers):
    resp = httpx.get(f"{API_BASE}{endpoint}", headers=headers, timeout=30)
    if resp.status_code == 401:
        print("Token expired. Run: uv run scripts/fitbit_auth.py")
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


def query_data(metric, days=7):
    """Query a specific metric, preferring local cache."""
    file_map = {
        "sleep": "sleep_daily.json",
        "steps": "steps_daily.json",
        "heart_rate": "heart_rate_daily.json",
        "hrv": "hrv_daily.json",
        "spo2": "spo2_daily.json",
        "skin_temp": "skin_temp_daily.json",
        "breathing_rate": "breathing_rate_daily.json",
        "calories": "calories_daily.json",
        "profile": "profile.json",
    }

    if metric == "profile":
        data = load_local("profile.json")
        if data:
            return data
        headers = get_headers()
        return fetch_api("/1/user/-/profile.json", headers)

    filename = file_map.get(metric)
    if not filename:
        print(f"Unknown metric: {metric}")
        print(f"Available: {', '.join(file_map.keys())}")
        sys.exit(1)

    # Try local cache first
    data = load_local(filename)
    if data:
        return data

    # Fall back to API
    headers = get_headers()
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    api_map = {
        "sleep": f"/1.2/user/-/sleep/date/{start}/{end}.json",
        "steps": f"/1/user/-/activities/steps/date/{start}/{end}.json",
        "heart_rate": f"/1/user/-/activities/heart/date/{start}/{end}.json",
        "hrv": f"/1/user/-/hrv/date/{start}/{end}.json",
        "spo2": f"/1/user/-/spo2/date/{start}/{end}.json",
        "skin_temp": f"/1/user/-/temp/skin/date/{start}/{end}.json",
        "breathing_rate": f"/1/user/-/br/date/{start}/{end}.json",
        "calories": f"/1/user/-/activities/calories/date/{start}/{end}.json",
    }

    return fetch_api(api_map[metric], headers)


def main():
    if len(sys.argv) < 2:
        print("Usage: fitbit_query.py <metric> [days]")
        print("Metrics: sleep, steps, heart_rate, hrv, spo2, skin_temp, breathing_rate, calories, profile, all")
        sys.exit(1)

    metric = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7

    if metric == "all":
        for m in ["profile", "steps", "calories", "heart_rate", "sleep", "hrv", "spo2", "breathing_rate", "skin_temp"]:
            print(f"\n{'='*40}")
            print(f"  {m.upper()}")
            print(f"{'='*40}")
            try:
                data = query_data(m, days)
                print(json.dumps(data, indent=2)[:2000])
            except Exception as e:
                print(f"  Error: {e}")
    else:
        data = query_data(metric, days)
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
