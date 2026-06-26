#!/usr/bin/env python3
"""Fitbit data quality checks. Detects BMR-only, missing, and stale data.

Usage:
  uv run scripts/fitbit_data_quality.py
  
Returns a JSON report of data quality for each metric.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "user_default"


def load(filename):
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


def check_steps():
    data = load("steps_daily.json")
    if not data or "activities-steps" not in data:
        return {"status": "missing", "message": "No steps data. Run fitbit_sync.py first."}
    
    entries = data["activities-steps"]
    values = [int(e["value"]) for e in entries]
    nonzero = [v for v in values if v > 0]
    
    if not nonzero:
        return {
            "status": "no_real_data",
            "message": "All step counts are 0. Fitbit has not been worn recently.",
            "total_days": len(values),
            "active_days": 0,
        }
    
    last_active = None
    for e in reversed(entries):
        if int(e["value"]) > 0:
            last_active = e["dateTime"]
            break
    
    days_since = (datetime.now() - datetime.strptime(last_active, "%Y-%m-%d")).days if last_active else None
    
    return {
        "status": "ok" if days_since and days_since < 3 else "stale",
        "total_days": len(values),
        "active_days": len(nonzero),
        "avg_steps": sum(nonzero) // len(nonzero) if nonzero else 0,
        "last_active_date": last_active,
        "days_since_last_active": days_since,
        "message": f"Last active: {last_active} ({days_since} days ago)" if days_since else None,
    }


def check_calories():
    data = load("calories_daily.json")
    if not data or "activities-calories" not in data:
        return {"status": "missing", "message": "No calories data."}
    
    entries = data["activities-calories"]
    values = [int(e["value"]) for e in entries]
    
    # Detect BMR-only: all values identical or very close (within 5 cal)
    if values:
        unique = set(values)
        is_bmr_only = len(unique) <= 2 or (max(values) - min(values) < 10)
        
        if is_bmr_only:
            return {
                "status": "bmr_only",
                "message": f"All calorie values are ~{values[0]} (BMR estimate only). No real activity data. Fitbit not worn.",
                "bmr_estimate": values[0],
                "total_days": len(values),
            }
    
    return {
        "status": "ok",
        "total_days": len(values),
        "avg_calories": sum(values) // len(values) if values else 0,
    }


def check_heart_rate():
    data = load("heart_rate_daily.json")
    if not data or "activities-heart" not in data:
        return {"status": "missing", "message": "No heart rate data."}
    
    entries = data["activities-heart"]
    has_rhr = []
    has_active_zones = []
    
    for e in entries:
        val = e.get("value", {})
        if val.get("restingHeartRate"):
            has_rhr.append(e["dateTime"])
        zones = val.get("heartRateZones", [])
        active_mins = sum(z.get("minutes", 0) for z in zones if z["name"] != "Out of Range")
        if active_mins > 0:
            has_active_zones.append(e["dateTime"])
    
    if not has_rhr and not has_active_zones:
        return {
            "status": "no_real_data",
            "message": "No resting HR or active zone data. Fitbit not worn. HR zone data is default/empty.",
            "total_days": len(entries),
        }
    
    return {
        "status": "ok",
        "total_days": len(entries),
        "days_with_rhr": len(has_rhr),
        "days_with_active_zones": len(has_active_zones),
        "last_rhr_date": has_rhr[-1] if has_rhr else None,
    }


def check_sleep():
    data = load("sleep_daily.json")
    if not data:
        return {"status": "missing", "message": "No sleep data."}
    
    sleeps = data.get("sleep", [])
    if not sleeps:
        return {"status": "no_real_data", "message": "No sleep records. Fitbit not worn during sleep."}
    
    main_sleeps = [s for s in sleeps if s.get("isMainSleep")]
    return {
        "status": "ok",
        "total_records": len(sleeps),
        "main_sleep_records": len(main_sleeps),
    }


def check_hrv():
    data = load("hrv_daily.json")
    if not data:
        return {"status": "missing", "message": "No HRV data file."}
    entries = data.get("hrv", [])
    if not entries:
        return {"status": "no_real_data", "message": "No HRV data. Requires wearing Fitbit during sleep."}
    return {"status": "ok", "days": len(entries)}


def check_spo2():
    data = load("spo2_daily.json")
    if not data or (isinstance(data, list) and not data):
        return {"status": "no_real_data", "message": "No SpO2 data. Requires compatible Fitbit model worn during sleep."}
    return {"status": "ok", "entries": len(data) if isinstance(data, list) else "unknown"}


def check_breathing_rate():
    data = load("breathing_rate_daily.json")
    if not data:
        return {"status": "missing"}
    entries = data.get("br", [])
    if not entries:
        return {"status": "no_real_data", "message": "No breathing rate data. Requires wearing Fitbit during sleep."}
    return {"status": "ok", "days": len(entries)}


def check_skin_temp():
    data = load("skin_temp_daily.json")
    if not data:
        return {"status": "missing"}
    entries = data.get("tempSkin", [])
    if not entries:
        return {"status": "no_real_data", "message": "No skin temp data. Requires compatible Fitbit model worn during sleep."}
    return {"status": "ok", "days": len(entries)}


def main():
    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "steps": check_steps(),
            "calories": check_calories(),
            "heart_rate": check_heart_rate(),
            "sleep": check_sleep(),
            "hrv": check_hrv(),
            "spo2": check_spo2(),
            "breathing_rate": check_breathing_rate(),
            "skin_temp": check_skin_temp(),
        }
    }
    
    # Summary
    real_data = [k for k, v in report["metrics"].items() if v["status"] == "ok"]
    no_data = [k for k, v in report["metrics"].items() if v["status"] in ("no_real_data", "bmr_only", "missing")]
    
    report["summary"] = {
        "metrics_with_real_data": real_data,
        "metrics_without_real_data": no_data,
        "device_worn_recently": len(real_data) > 2,
    }
    
    if no_data:
        report["summary"]["warning"] = (
            f"⚠️ No real data for: {', '.join(no_data)}. "
            "These metrics show default/BMR values only. "
            "Wear your Fitbit to get actual health data."
        )
    
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
