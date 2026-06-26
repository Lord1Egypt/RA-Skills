#!/usr/bin/env python3
"""Execute Python analysis code on Fitbit data.

Usage:
  uv run scripts/fitbit_analyze.py "code_string"
  uv run scripts/fitbit_analyze.py --file analysis.py

The code has access to:
  - pandas (pd), numpy (np), matplotlib (plt), json, datetime
  - DATA_DIR: path to local Fitbit JSON data
  - CHARTS_DIR: path to save charts
  - load(filename): helper to load JSON from data dir
  - All Fitbit data pre-loaded as DataFrames: df_steps, df_calories, df_hr, df_sleep, df_hrv, etc.
"""

import io
import json
import sys
import contextlib
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "user_default"
CHARTS_DIR = BASE_DIR / "data" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def load(filename):
    """Load a JSON file from the data directory."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


def prepare_dataframes():
    """Pre-load all Fitbit data as pandas DataFrames."""
    import pandas as pd

    dfs = {}

    # Steps
    data = load("steps_daily.json")
    if data and "activities-steps" in data:
        df = pd.DataFrame(data["activities-steps"])
        df["dateTime"] = pd.to_datetime(df["dateTime"])
        df["value"] = pd.to_numeric(df["value"])
        df = df.rename(columns={"dateTime": "date", "value": "steps"})
        dfs["df_steps"] = df

    # Calories
    data = load("calories_daily.json")
    if data and "activities-calories" in data:
        df = pd.DataFrame(data["activities-calories"])
        df["dateTime"] = pd.to_datetime(df["dateTime"])
        df["value"] = pd.to_numeric(df["value"])
        df = df.rename(columns={"dateTime": "date", "value": "calories"})
        dfs["df_calories"] = df

    # Heart rate
    data = load("heart_rate_daily.json")
    if data and "activities-heart" in data:
        rows = []
        for entry in data["activities-heart"]:
            row = {"date": entry["dateTime"]}
            val = entry.get("value", {})
            row["resting_hr"] = val.get("restingHeartRate")
            for zone in val.get("heartRateZones", []):
                name = zone["name"].lower().replace(" ", "_")
                row[f"{name}_minutes"] = zone.get("minutes", 0)
                row[f"{name}_calories"] = zone.get("caloriesOut", 0)
            rows.append(row)
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        dfs["df_hr"] = df

    # Sleep
    data = load("sleep_daily.json")
    if data and "sleep" in data and data["sleep"]:
        rows = []
        for s in data["sleep"]:
            row = {
                "date": s.get("dateOfSleep"),
                "duration_hrs": s.get("duration", 0) / 3600000,
                "efficiency": s.get("efficiency"),
                "minutes_asleep": s.get("minutesAsleep"),
                "minutes_awake": s.get("minutesAwake"),
                "time_in_bed": s.get("timeInBed"),
                "is_main": s.get("isMainSleep", False),
            }
            levels = s.get("levels", {}).get("summary", {})
            for stage in ["deep", "light", "rem", "wake"]:
                if stage in levels:
                    row[f"{stage}_minutes"] = levels[stage].get("minutes", 0)
            rows.append(row)
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        dfs["df_sleep"] = df

    # HRV
    data = load("hrv_daily.json")
    if data and "hrv" in data and data["hrv"]:
        rows = []
        for entry in data["hrv"]:
            row = {"date": entry.get("dateTime")}
            val = entry.get("value", {})
            row["daily_rmssd"] = val.get("dailyRmssd")
            row["deep_rmssd"] = val.get("deepRmssd")
            rows.append(row)
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        dfs["df_hrv"] = df

    # SpO2
    data = load("spo2_daily.json")
    if data and isinstance(data, list) and data:
        df = pd.DataFrame(data)
        if "dateTime" in df.columns:
            df["date"] = pd.to_datetime(df["dateTime"])
        dfs["df_spo2"] = df

    # Breathing rate
    data = load("breathing_rate_daily.json")
    if data and "br" in data and data["br"]:
        rows = []
        for entry in data["br"]:
            row = {"date": entry.get("dateTime")}
            val = entry.get("value", {})
            row["breathing_rate"] = val.get("breathingRate")
            rows.append(row)
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        dfs["df_br"] = df

    # Skin temp
    data = load("skin_temp_daily.json")
    if data and "tempSkin" in data and data["tempSkin"]:
        rows = []
        for entry in data["tempSkin"]:
            row = {"date": entry.get("dateTime")}
            val = entry.get("value", {})
            row["skin_temp_deviation"] = val.get("nightlyRelative")
            rows.append(row)
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        dfs["df_skin_temp"] = df

    # Profile
    data = load("profile.json")
    if data:
        dfs["profile"] = data.get("user", {})

    return dfs


def main():
    if len(sys.argv) < 2:
        print("Usage: fitbit_analyze.py 'code' OR fitbit_analyze.py --file script.py")
        sys.exit(1)

    if sys.argv[1] == "--file":
        with open(sys.argv[2]) as f:
            code = f.read()
    else:
        code = sys.argv[1]

    # Prepare namespace
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Apply Google-style theme
    from fitbit_chart import apply_google_theme
    apply_google_theme()

    dfs = prepare_dataframes()

    namespace = {
        "pd": pd,
        "np": np,
        "plt": plt,
        "json": json,
        "datetime": datetime,
        "timedelta": timedelta,
        "DATA_DIR": str(DATA_DIR),
        "CHARTS_DIR": str(CHARTS_DIR),
        "load": load,
        "Path": Path,
        **dfs,
    }

    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, namespace)
        output = stdout.getvalue()
        if output:
            print(output)
        else:
            print("Code executed successfully (no output).")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
