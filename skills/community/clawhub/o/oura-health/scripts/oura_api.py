#!/usr/bin/env /opt/homebrew/bin/python3.11
"""Oura Ring API v2 client. Stdlib only. Human-readable output."""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta, timezone

# ── Config ──────────────────────────────────────────────────────────────────

CREDS_PATH = os.path.expanduser("~/.config/oura/credentials.json")
TZ_OFFSET = timezone(timedelta(hours=-7))  # PDT; adjust or use dateutil if needed
TZ_NAME = "America/Los_Angeles"


def load_credentials():
    try:
        with open(CREDS_PATH) as f:
            creds = json.load(f)
        token = creds.get("personal_access_token")
        base = creds.get("base_url", "https://api.ouraring.com/v2").rstrip("/")
        if not token:
            die("No personal_access_token in credentials file")
        return token, base
    except FileNotFoundError:
        die(f"Credentials file not found: {CREDS_PATH}\n"
            f"Create it with: {{\"personal_access_token\": \"...\", \"base_url\": \"https://api.ouraring.com/v2\"}}")
    except json.JSONDecodeError:
        die(f"Invalid JSON in {CREDS_PATH}")


def die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


# ── API helpers ─────────────────────────────────────────────────────────────

def api_get(path, params=None):
    token, base = load_credentials()
    url = f"{base}{path}"
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url += "?" + urllib.parse.urlencode(filtered)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            die("Unauthorized — check your personal access token")
        elif e.code == 404:
            die(f"Not found: {path}")
        elif e.code == 429:
            die("Rate limited by Oura API — try again in a minute")
        else:
            body = e.read().decode() if e.fp else ""
            die(f"HTTP {e.code}: {body[:200]}")
    except urllib.error.URLError as e:
        die(f"Connection error: {e.reason}")


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def yesterday_str():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def days_ago_str(n):
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


def score_emoji(score):
    if score is None:
        return "⚪"
    if score >= 85:
        return "🟢"
    if score >= 70:
        return "🟡"
    return "🔴"


def fmt_duration(seconds):
    """Format seconds into Xh Ym."""
    if seconds is None:
        return "N/A"
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"


def fmt_hours(seconds):
    """Format seconds as decimal hours."""
    if seconds is None:
        return "N/A"
    return f"{seconds / 3600:.1f}h"


def safe_get(d, *keys, default=None):
    """Safely traverse nested dicts."""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d if d is not None else default


# ── Commands ────────────────────────────────────────────────────────────────

def cmd_status():
    data = api_get("/usercollection/personal_info")
    print("✅ Connected to Oura API v2\n")
    print(f"  Age:    {data.get('age', 'N/A')}")
    print(f"  Sex:    {data.get('biological_sex', 'N/A')}")
    print(f"  Email:  {data.get('email', 'N/A')}")
    print(f"  Weight: {data.get('weight', 'N/A')} kg")
    print(f"  Height: {data.get('height', 'N/A')} m")


def cmd_briefing():
    date = today_str()
    yesterday = yesterday_str()

    # Fetch all three
    readiness = api_get("/usercollection/daily_readiness", {"start_date": date, "end_date": date})
    sleep = api_get("/usercollection/daily_sleep", {"start_date": yesterday, "end_date": date})
    activity = api_get("/usercollection/daily_activity", {"start_date": date, "end_date": date})

    print(f"📊 Daily Briefing — {date}\n")

    # Readiness
    r_data = readiness.get("data", [])
    if r_data:
        r = r_data[-1]
        score = r.get("score")
        print(f"  {score_emoji(score)} Readiness: {score or 'N/A'}")
        contribs = r.get("contributors", {})
        if contribs:
            temp = contribs.get("body_temperature")
            hrv = contribs.get("hrv_balance")
            recovery = contribs.get("recovery_index")
            print(f"     HRV Balance: {hrv or 'N/A'}  |  Recovery: {recovery or 'N/A'}  |  Temp: {temp or 'N/A'}")
    else:
        print("  ⚪ Readiness: No data yet today")

    print()

    # Sleep
    s_data = sleep.get("data", [])
    if s_data:
        s = s_data[-1]
        score = s.get("score")
        contribs = s.get("contributors", {})
        print(f"  {score_emoji(score)} Sleep Score: {score or 'N/A'}")
        total = contribs.get("total_sleep")
        efficiency = contribs.get("efficiency")
        deep = contribs.get("deep_sleep")
        print(f"     Total: {total or 'N/A'}  |  Efficiency: {efficiency or 'N/A'}  |  Deep: {deep or 'N/A'}")
    else:
        print("  ⚪ Sleep: No data yet")

    print()

    # Activity
    a_data = activity.get("data", [])
    if a_data:
        a = a_data[-1]
        score = a.get("score")
        steps = a.get("steps", 0)
        cal = a.get("total_calories", 0)
        active = a.get("active_calories", 0)
        print(f"  {score_emoji(score)} Activity: {score or 'N/A'}")
        print(f"     Steps: {steps:,}  |  Calories: {cal:,} (active: {active:,})")
    else:
        print("  ⚪ Activity: No data yet today")


def cmd_sleep(date=None):
    if date is None:
        # Sleep data for "last night" — use yesterday as start
        start = yesterday_str()
        end = today_str()
    else:
        start = date
        end = date

    # Daily sleep summary
    daily = api_get("/usercollection/daily_sleep", {"start_date": start, "end_date": end})
    # Detailed sleep sessions
    sessions = api_get("/usercollection/sleep", {"start_date": start, "end_date": end})

    d_data = daily.get("data", [])
    s_data = sessions.get("data", [])

    if not d_data and not s_data:
        print(f"No sleep data for {start}")
        return

    if d_data:
        d = d_data[-1]
        score = d.get("score")
        contribs = d.get("contributors", {})
        print(f"😴 Sleep Report — {d.get('day', start)}\n")
        print(f"  {score_emoji(score)} Score: {score or 'N/A'}\n")
        print("  Contributors:")
        for key in ["total_sleep", "efficiency", "restfulness", "rem_sleep", "deep_sleep", "latency", "timing"]:
            val = contribs.get(key)
            if val is not None:
                label = key.replace("_", " ").title()
                print(f"    {score_emoji(val)} {label}: {val}")

    if s_data:
        session = s_data[-1]
        print(f"\n  Session Details:")
        bedtime = session.get("bedtime_start", "N/A")
        wakeup = session.get("bedtime_end", "N/A")
        if bedtime != "N/A":
            bedtime = bedtime.replace("T", " ")[:16]
        if wakeup != "N/A":
            wakeup = wakeup.replace("T", " ")[:16]
        print(f"    Bedtime:    {bedtime}")
        print(f"    Wake-up:    {wakeup}")
        print(f"    Total:      {fmt_duration(session.get('total_sleep_duration'))}")
        print(f"    Awake:      {fmt_duration(session.get('awake_time'))}")
        print(f"    Light:      {fmt_duration(session.get('light_sleep_duration'))}")
        print(f"    Deep:       {fmt_duration(session.get('deep_sleep_duration'))}")
        print(f"    REM:        {fmt_duration(session.get('rem_sleep_duration'))}")
        print(f"    Efficiency: {session.get('efficiency', 'N/A')}%")
        print(f"    Avg HRV:    {session.get('average_hrv', 'N/A')} ms")
        print(f"    Lowest HR:  {session.get('lowest_heart_rate', 'N/A')} bpm")
        temp = session.get("readiness", {}).get("temperature_deviation") if isinstance(session.get("readiness"), dict) else None
        if temp is None:
            temp = session.get("temperature_deviation")
        if temp is not None:
            print(f"    Temp Dev:   {temp:+.1f}°C")


def cmd_readiness(date=None):
    date = date or today_str()
    data = api_get("/usercollection/daily_readiness", {"start_date": date, "end_date": date})
    items = data.get("data", [])
    if not items:
        print(f"No readiness data for {date}")
        return

    r = items[-1]
    score = r.get("score")
    print(f"💪 Readiness — {r.get('day', date)}\n")
    print(f"  {score_emoji(score)} Score: {score or 'N/A'}\n")

    contribs = r.get("contributors", {})
    if contribs:
        print("  Contributors:")
        labels = {
            "activity_balance": "Activity Balance",
            "body_temperature": "Body Temperature",
            "hrv_balance": "HRV Balance",
            "previous_day_activity": "Previous Day Activity",
            "previous_night": "Previous Night",
            "recovery_index": "Recovery Index",
            "resting_heart_rate": "Resting Heart Rate",
            "sleep_balance": "Sleep Balance",
        }
        for key, label in labels.items():
            val = contribs.get(key)
            if val is not None:
                print(f"    {score_emoji(val)} {label}: {val}")

    temp_dev = r.get("temperature_deviation")
    if temp_dev is not None:
        emoji = "🟢" if abs(temp_dev) < 0.5 else ("🟡" if abs(temp_dev) < 1.0 else "🔴")
        print(f"\n  {emoji} Temperature Deviation: {temp_dev:+.2f}°C")

    trend = r.get("temperature_trend_deviation")
    if trend is not None:
        print(f"  Temperature Trend: {trend:+.2f}°C")


def cmd_activity(date=None):
    date = date or today_str()
    data = api_get("/usercollection/daily_activity", {"start_date": date, "end_date": date})
    items = data.get("data", [])
    if not items:
        print(f"No activity data for {date}")
        return

    a = items[-1]
    score = a.get("score")
    print(f"🏃 Activity — {a.get('day', date)}\n")
    print(f"  {score_emoji(score)} Score: {score or 'N/A'}\n")

    print(f"  Steps:            {a.get('steps', 0):,}")
    print(f"  Total Calories:   {a.get('total_calories', 0):,}")
    print(f"  Active Calories:  {a.get('active_calories', 0):,}")
    print(f"  Equivalent Walk:  {fmt_duration(a.get('equivalent_walking_distance'))}" if isinstance(a.get('equivalent_walking_distance'), (int, float)) else "")

    # Movement breakdown
    high = a.get("high_activity_time", 0)
    med = a.get("medium_activity_time", 0)
    low = a.get("low_activity_time", 0)
    sedentary = a.get("sedentary_time", 0)
    rest = a.get("resting_time", 0)

    print(f"\n  Movement Breakdown:")
    print(f"    High Activity:  {fmt_duration(high)}")
    print(f"    Medium:         {fmt_duration(med)}")
    print(f"    Low:            {fmt_duration(low)}")
    print(f"    Sedentary:      {fmt_duration(sedentary)}")
    print(f"    Resting:        {fmt_duration(rest)}")

    contribs = a.get("contributors", {})
    if contribs:
        print(f"\n  Contributors:")
        for key in ["meet_daily_targets", "move_every_hour", "recovery_time", "stay_active", "training_frequency", "training_volume"]:
            val = contribs.get(key)
            if val is not None:
                label = key.replace("_", " ").title()
                print(f"    {score_emoji(val)} {label}: {val}")


def cmd_heartrate(hours=4):
    try:
        hours = int(hours)
    except (ValueError, TypeError):
        hours = 4

    now = datetime.now()
    start = now - timedelta(hours=hours)
    # Oura expects ISO 8601 with timezone for heartrate
    start_str = start.strftime("%Y-%m-%dT%H:%M:%S-07:00")
    end_str = now.strftime("%Y-%m-%dT%H:%M:%S-07:00")

    data = api_get("/usercollection/heartrate", {"start_datetime": start_str, "end_datetime": end_str})
    items = data.get("data", [])

    if not items:
        print(f"No heart rate data in the last {hours} hours")
        return

    bpms = [item["bpm"] for item in items if "bpm" in item]
    if not bpms:
        print(f"No heart rate readings in the last {hours} hours")
        return

    avg_bpm = sum(bpms) / len(bpms)
    min_bpm = min(bpms)
    max_bpm = max(bpms)
    latest = bpms[-1]
    sources = {}
    for item in items:
        src = item.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1

    # Color the latest reading
    if latest < 60:
        emoji = "🟢"  # Low resting
    elif latest < 100:
        emoji = "🟢"  # Normal
    else:
        emoji = "🟡"  # Elevated

    print(f"❤️ Heart Rate — Last {hours} hours ({len(bpms)} readings)\n")
    print(f"  {emoji} Latest:  {latest} bpm")
    print(f"     Average: {avg_bpm:.0f} bpm")
    print(f"     Min:     {min_bpm} bpm")
    print(f"     Max:     {max_bpm} bpm")

    if len(sources) > 1 or list(sources.keys()) != ["unknown"]:
        print(f"\n  Sources: {', '.join(f'{k}: {v}' for k, v in sources.items())}")


def cmd_trends(days=7):
    try:
        days = int(days)
    except (ValueError, TypeError):
        days = 7

    start = days_ago_str(days)
    end = today_str()

    readiness = api_get("/usercollection/daily_readiness", {"start_date": start, "end_date": end})
    sleep = api_get("/usercollection/daily_sleep", {"start_date": start, "end_date": end})
    activity = api_get("/usercollection/daily_activity", {"start_date": start, "end_date": end})

    r_data = {d["day"]: d for d in readiness.get("data", [])}
    s_data = {d["day"]: d for d in sleep.get("data", [])}
    a_data = {d["day"]: d for d in activity.get("data", [])}

    all_days = sorted(set(list(r_data.keys()) + list(s_data.keys()) + list(a_data.keys())))

    if not all_days:
        print(f"No data for the last {days} days")
        return

    print(f"📈 Trends — Last {days} days\n")
    print(f"  {'Date':<12} {'Readiness':>10} {'Sleep':>10} {'Activity':>10} {'Steps':>8}")
    print(f"  {'─' * 12} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 8}")

    r_scores, s_scores, a_scores = [], [], []

    for day in all_days:
        r_score = safe_get(r_data.get(day, {}), "score")
        s_score = safe_get(s_data.get(day, {}), "score")
        a_score = safe_get(a_data.get(day, {}), "score")
        steps = safe_get(a_data.get(day, {}), "steps", default=0)

        r_str = f"{score_emoji(r_score)} {r_score}" if r_score else "  —"
        s_str = f"{score_emoji(s_score)} {s_score}" if s_score else "  —"
        a_str = f"{score_emoji(a_score)} {a_score}" if a_score else "  —"
        steps_str = f"{steps:,}" if steps else "—"

        print(f"  {day:<12} {r_str:>10} {s_str:>10} {a_str:>10} {steps_str:>8}")

        if r_score:
            r_scores.append(r_score)
        if s_score:
            s_scores.append(s_score)
        if a_score:
            a_scores.append(a_score)

    print()
    if r_scores:
        avg_r = sum(r_scores) / len(r_scores)
        print(f"  {score_emoji(avg_r)} Avg Readiness: {avg_r:.0f}")
    if s_scores:
        avg_s = sum(s_scores) / len(s_scores)
        print(f"  {score_emoji(avg_s)} Avg Sleep:     {avg_s:.0f}")
    if a_scores:
        avg_a = sum(a_scores) / len(a_scores)
        print(f"  {score_emoji(avg_a)} Avg Activity:  {avg_a:.0f}")

    # Trend direction
    if len(r_scores) >= 3:
        recent = sum(r_scores[-3:]) / 3
        older = sum(r_scores[:3]) / 3
        if recent > older + 3:
            print(f"\n  📈 Readiness trending UP (+{recent - older:.0f})")
        elif recent < older - 3:
            print(f"\n  📉 Readiness trending DOWN ({recent - older:.0f})")


# ── Main ────────────────────────────────────────────────────────────────────

COMMANDS = {
    "status": (cmd_status, 0),
    "briefing": (cmd_briefing, 0),
    "sleep": (cmd_sleep, 1),
    "readiness": (cmd_readiness, 1),
    "activity": (cmd_activity, 1),
    "heartrate": (cmd_heartrate, 1),
    "trends": (cmd_trends, 1),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("Usage: oura_api.py <command> [args]")
        print(f"\nCommands: {', '.join(COMMANDS.keys())}")
        print("\nExamples:")
        print("  oura_api.py status")
        print("  oura_api.py briefing")
        print("  oura_api.py sleep 2026-03-08")
        print("  oura_api.py readiness")
        print("  oura_api.py activity 2026-03-07")
        print("  oura_api.py heartrate 6")
        print("  oura_api.py trends 14")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        die(f"Unknown command: {cmd}\nAvailable: {', '.join(COMMANDS.keys())}")

    func, max_args = COMMANDS[cmd]
    args = sys.argv[2:2 + max_args] if max_args > 0 else []

    # Pass None for optional args not provided
    if max_args == 1:
        func(args[0] if args else None)
    else:
        func()


if __name__ == "__main__":
    main()
