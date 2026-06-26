#!/usr/bin/env python3
"""Proactive insight generation engine for Fitbit health data.

Generates personalized, actionable insights without the user asking.
Runs anomaly detection, trend analysis, correlations, goal tracking,
streaks, and recommendations.

Usage:
  uv run scripts/fitbit_insights.py                 # Full insights report
  uv run scripts/fitbit_insights.py --type anomaly   # Just anomalies
  uv run scripts/fitbit_insights.py --type trend      # Just trends
  uv run scripts/fitbit_insights.py --type goal       # Just goal tracking
  uv run scripts/fitbit_insights.py --type streak     # Just streaks
  uv run scripts/fitbit_insights.py --type correlation # Just correlations
  uv run scripts/fitbit_insights.py --type recommendation # Just recommendations
  uv run scripts/fitbit_insights.py --days 7          # Analyze last 7 days (default 30)
  uv run scripts/fitbit_insights.py --brief           # Just the briefing summary
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "user_default"
PROFILE_PATH = BASE_DIR / "data" / "user_profile.json"

# Add scripts dir for imports
sys.path.insert(0, str(Path(__file__).parent))
from fitbit_analyze import prepare_dataframes
from fitbit_data_quality import main as run_data_quality, check_steps, check_calories, check_heart_rate, check_sleep, check_hrv


def load_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH) as f:
            return json.load(f)
    return {}


def make_insight(insight_type, priority, title, message, data_points=None, recommendation=None):
    return {
        "type": insight_type,
        "priority": priority,
        "title": title,
        "message": message,
        "data_points": data_points or {},
        "recommendation": recommendation,
        "generated_at": datetime.now().isoformat(),
    }


# ---------------------------------------------------------------------------
# Anomaly Detection
# ---------------------------------------------------------------------------

def detect_anomalies(dfs, days=30):
    insights = []
    today = pd.Timestamp.now().normalize()
    cutoff = today - pd.Timedelta(days=days)

    # Steps anomalies
    if "df_steps" in dfs:
        df = dfs["df_steps"]
        df = df[df["date"] >= cutoff]
        active = df[df["steps"] > 0]
        if len(active) >= 7:
            mean = active["steps"].mean()
            std = active["steps"].std()
            if std > 0:
                recent = active.tail(3)
                for _, row in recent.iterrows():
                    z = (row["steps"] - mean) / std
                    if z > 2:
                        insights.append(make_insight(
                            "anomaly", "medium",
                            "🏃 Unusually high step count",
                            f"On {row['date'].strftime('%b %d')}, you walked {row['steps']:,.0f} steps — "
                            f"that's {z:.1f} standard deviations above your average of {mean:,.0f}. Nice burst of activity!",
                            {"date": str(row["date"].date()), "steps": int(row["steps"]),
                             "avg": round(mean), "z_score": round(z, 2)},
                        ))
                    elif z < -2:
                        insights.append(make_insight(
                            "anomaly", "medium",
                            "📉 Unusually low step count",
                            f"On {row['date'].strftime('%b %d')}, you only walked {row['steps']:,.0f} steps — "
                            f"well below your average of {mean:,.0f}. Rest day or just didn't get out?",
                            {"date": str(row["date"].date()), "steps": int(row["steps"]),
                             "avg": round(mean), "z_score": round(z, 2)},
                        ))

    # Resting HR anomalies
    if "df_hr" in dfs:
        df = dfs["df_hr"]
        df = df[df["date"] >= cutoff]
        hr_valid = df[df["resting_hr"].notna() & (df["resting_hr"] > 0)]
        if len(hr_valid) >= 7:
            mean = hr_valid["resting_hr"].mean()
            std = hr_valid["resting_hr"].std()
            if std > 0:
                recent = hr_valid.tail(3)
                for _, row in recent.iterrows():
                    z = (row["resting_hr"] - mean) / std
                    if z > 2:
                        insights.append(make_insight(
                            "anomaly", "high",
                            "❤️‍🔥 Elevated resting heart rate",
                            f"On {row['date'].strftime('%b %d')}, your resting HR was {row['resting_hr']:.0f} bpm — "
                            f"above your baseline of {mean:.0f} bpm. Could indicate stress, poor sleep, illness, or dehydration.",
                            {"date": str(row["date"].date()), "resting_hr": round(row["resting_hr"]),
                             "avg_hr": round(mean), "z_score": round(z, 2)},
                            "Monitor over the next few days. If consistently elevated, consider: Are you stressed? Getting enough sleep? Coming down with something?"
                        ))
                    elif z < -2:
                        insights.append(make_insight(
                            "anomaly", "low",
                            "💚 Unusually low resting heart rate",
                            f"On {row['date'].strftime('%b %d')}, your resting HR dropped to {row['resting_hr']:.0f} bpm — "
                            f"below your baseline of {mean:.0f} bpm. This often indicates good recovery and fitness.",
                            {"date": str(row["date"].date()), "resting_hr": round(row["resting_hr"]),
                             "avg_hr": round(mean)},
                        ))

    # Sleep duration anomalies
    if "df_sleep" in dfs:
        df = dfs["df_sleep"]
        df = df[df["date"] >= cutoff]
        main_sleep = df[df.get("is_main", True) if "is_main" in df.columns else True]
        if len(main_sleep) >= 5:
            mean = main_sleep["duration_hrs"].mean()
            std = main_sleep["duration_hrs"].std()
            if std > 0:
                latest = main_sleep.tail(1).iloc[0]
                z = (latest["duration_hrs"] - mean) / std
                if abs(z) > 1.5:
                    direction = "short" if z < 0 else "long"
                    emoji = "😴" if z < 0 else "🛏️"
                    insights.append(make_insight(
                        "anomaly", "medium",
                        f"{emoji} Unusually {direction} sleep",
                        f"On {latest['date'].strftime('%b %d')}, you slept {latest['duration_hrs']:.1f} hours — "
                        f"your average is {mean:.1f} hours.",
                        {"date": str(latest["date"].date()), "duration_hrs": round(latest["duration_hrs"], 1),
                         "avg_hrs": round(mean, 1), "z_score": round(z, 2)},
                    ))

    return insights


# ---------------------------------------------------------------------------
# Trend Analysis
# ---------------------------------------------------------------------------

def analyze_trends(dfs, days=30):
    insights = []
    today = pd.Timestamp.now().normalize()
    cutoff = today - pd.Timedelta(days=days)

    def trend_direction(series_7d, series_30d):
        """Compare 7-day avg to 30-day avg, return pct change and direction."""
        if series_30d == 0:
            return 0, "flat"
        pct = ((series_7d - series_30d) / series_30d) * 100
        if pct > 10:
            return pct, "improving"
        elif pct < -10:
            return pct, "declining"
        return pct, "stable"

    # Steps trend
    if "df_steps" in dfs:
        df = dfs["df_steps"]
        df = df[(df["date"] >= cutoff) & (df["steps"] > 0)]
        if len(df) >= 14:
            avg_30d = df["steps"].mean()
            avg_7d = df.tail(7)["steps"].mean()
            pct, direction = trend_direction(avg_7d, avg_30d)
            if direction != "stable":
                emoji = "📈" if direction == "improving" else "📉"
                insights.append(make_insight(
                    "trend", "medium" if direction == "declining" else "low",
                    f"{emoji} Steps {direction}",
                    f"Your 7-day average is {avg_7d:,.0f} steps vs {avg_30d:,.0f} over 30 days ({pct:+.0f}%).",
                    {"avg_7d": round(avg_7d), "avg_30d": round(avg_30d), "pct_change": round(pct, 1)},
                    "Keep pushing!" if direction == "improving" else
                    "Try adding a 15-minute walk after lunch to get your numbers back up."
                ))

    # Resting HR trend
    if "df_hr" in dfs:
        df = dfs["df_hr"]
        df = df[(df["date"] >= cutoff) & df["resting_hr"].notna() & (df["resting_hr"] > 0)]
        if len(df) >= 14:
            avg_30d = df["resting_hr"].mean()
            avg_7d = df.tail(7)["resting_hr"].mean()
            # For HR, lower is generally better
            pct = ((avg_7d - avg_30d) / avg_30d) * 100
            if abs(pct) > 3:  # HR changes are subtler
                if pct > 3:
                    insights.append(make_insight(
                        "trend", "medium",
                        "❤️ Resting HR trending up",
                        f"7-day avg: {avg_7d:.0f} bpm vs 30-day avg: {avg_30d:.0f} bpm ({pct:+.1f}%). "
                        "Rising resting HR can signal stress, overtraining, or poor recovery.",
                        {"avg_7d": round(avg_7d), "avg_30d": round(avg_30d), "pct_change": round(pct, 1)},
                        "Focus on sleep quality and recovery. Consider lighter workouts if you've been pushing hard."
                    ))
                else:
                    insights.append(make_insight(
                        "trend", "low",
                        "💚 Resting HR trending down",
                        f"7-day avg: {avg_7d:.0f} bpm vs 30-day avg: {avg_30d:.0f} bpm ({pct:+.1f}%). "
                        "Improving cardiovascular fitness!",
                        {"avg_7d": round(avg_7d), "avg_30d": round(avg_30d), "pct_change": round(pct, 1)},
                    ))

    # Sleep trend
    if "df_sleep" in dfs:
        df = dfs["df_sleep"]
        df = df[df["date"] >= cutoff]
        if "is_main" in df.columns:
            df = df[df["is_main"]]
        if len(df) >= 10:
            avg_all = df["duration_hrs"].mean()
            avg_recent = df.tail(5)["duration_hrs"].mean()
            pct = ((avg_recent - avg_all) / avg_all) * 100
            if abs(pct) > 10:
                direction = "improving" if pct > 0 else "declining"
                emoji = "📈" if pct > 0 else "📉"
                insights.append(make_insight(
                    "trend", "medium" if direction == "declining" else "low",
                    f"{emoji} Sleep duration {direction}",
                    f"Recent average: {avg_recent:.1f} hrs vs overall: {avg_all:.1f} hrs ({pct:+.0f}%).",
                    {"avg_recent": round(avg_recent, 1), "avg_overall": round(avg_all, 1)},
                    "Aim for 7-9 hours consistently. Set a bedtime alarm 30 minutes before your target."
                    if direction == "declining" else None
                ))

    return insights


# ---------------------------------------------------------------------------
# Correlations
# ---------------------------------------------------------------------------

def find_correlations(dfs, days=30):
    insights = []
    today = pd.Timestamp.now().normalize()
    cutoff = today - pd.Timedelta(days=days)

    # Steps vs Sleep
    if "df_steps" in dfs and "df_sleep" in dfs:
        steps = dfs["df_steps"][dfs["df_steps"]["date"] >= cutoff].copy()
        sleep = dfs["df_sleep"][dfs["df_sleep"]["date"] >= cutoff].copy()
        if "is_main" in sleep.columns:
            sleep = sleep[sleep["is_main"]]

        steps["date_key"] = steps["date"].dt.date
        sleep["date_key"] = sleep["date"].dt.date
        merged = pd.merge(steps, sleep, on="date_key", suffixes=("_steps", "_sleep"))
        merged = merged[merged["steps"] > 0]

        if len(merged) >= 10:
            corr = merged["steps"].corr(merged["duration_hrs"])
            if abs(corr) > 0.3:
                direction = "more" if corr > 0 else "fewer"
                quality = "longer" if corr > 0 else "shorter"
                insights.append(make_insight(
                    "correlation", "medium",
                    "🔗 Steps ↔ Sleep connection",
                    f"Days with {direction} steps tend to have {quality} sleep (correlation: {corr:.2f}). "
                    f"Based on {len(merged)} days of overlapping data.",
                    {"correlation": round(corr, 3), "sample_size": len(merged)},
                    f"{'Physical activity helps sleep quality!' if corr > 0 else 'You might be overexerting — listen to your body.'}"
                ))

    # Steps vs Resting HR
    if "df_steps" in dfs and "df_hr" in dfs:
        steps = dfs["df_steps"][dfs["df_steps"]["date"] >= cutoff].copy()
        hr = dfs["df_hr"][(dfs["df_hr"]["date"] >= cutoff) & dfs["df_hr"]["resting_hr"].notna()].copy()

        steps["date_key"] = steps["date"].dt.date
        hr["date_key"] = hr["date"].dt.date
        merged = pd.merge(steps, hr[["date_key", "resting_hr"]], on="date_key")
        merged = merged[(merged["steps"] > 0) & (merged["resting_hr"] > 0)]

        if len(merged) >= 10:
            corr = merged["steps"].corr(merged["resting_hr"])
            if abs(corr) > 0.3:
                insights.append(make_insight(
                    "correlation", "low",
                    "🔗 Activity ↔ Heart Rate pattern",
                    f"Your steps and resting HR have a {corr:.2f} correlation over {len(merged)} days. "
                    f"{'More active days = lower resting HR — your heart is responding to exercise!' if corr < 0 else 'Active days show slightly higher resting HR — normal if you exercise in the evening.'}",
                    {"correlation": round(corr, 3), "sample_size": len(merged)},
                ))

    # Weekday vs Weekend patterns
    if "df_steps" in dfs:
        df = dfs["df_steps"][(dfs["df_steps"]["date"] >= cutoff) & (dfs["df_steps"]["steps"] > 0)].copy()
        if len(df) >= 14:
            df["is_weekend"] = df["date"].dt.dayofweek >= 5
            weekday_avg = df[~df["is_weekend"]]["steps"].mean()
            weekend_avg = df[df["is_weekend"]]["steps"].mean()
            if weekday_avg > 0 and weekend_avg > 0:
                diff_pct = ((weekend_avg - weekday_avg) / weekday_avg) * 100
                if abs(diff_pct) > 20:
                    more_when = "weekends" if diff_pct > 0 else "weekdays"
                    insights.append(make_insight(
                        "correlation", "low",
                        f"📅 You're more active on {more_when}",
                        f"Weekday avg: {weekday_avg:,.0f} steps, Weekend avg: {weekend_avg:,.0f} steps ({diff_pct:+.0f}%).",
                        {"weekday_avg": round(weekday_avg), "weekend_avg": round(weekend_avg)},
                        f"{'Try adding walks during work breaks to balance it out.' if more_when == 'weekends' else 'Great weekday routine! Try to stay active on weekends too.'}"
                    ))

    return insights


# ---------------------------------------------------------------------------
# Goal Tracking
# ---------------------------------------------------------------------------

def track_goals(dfs, profile, days=30):
    insights = []
    today = pd.Timestamp.now().normalize()
    cutoff = today - pd.Timedelta(days=days)

    step_goal = profile.get("step_goal", 10000)
    sleep_target = profile.get("sleep_target_hrs", 8)

    # Step goal tracking
    if "df_steps" in dfs:
        df = dfs["df_steps"][(dfs["df_steps"]["date"] >= cutoff) & (dfs["df_steps"]["steps"] > 0)]
        if len(df) > 0:
            days_hit = (df["steps"] >= step_goal).sum()
            total = len(df)
            pct = (days_hit / total) * 100
            avg = df["steps"].mean()
            emoji = "🎯" if pct >= 50 else "💪"
            priority = "low" if pct >= 50 else "medium"

            insights.append(make_insight(
                "goal", priority,
                f"{emoji} Step goal: {pct:.0f}% hit rate",
                f"You hit your {step_goal:,}-step goal on {days_hit}/{total} active days. "
                f"Average: {avg:,.0f} steps/day.",
                {"goal": step_goal, "days_hit": int(days_hit), "total_days": total,
                 "hit_rate_pct": round(pct, 1), "avg_steps": round(avg)},
                None if pct >= 70 else
                f"You need ~{step_goal - avg:,.0f} more steps/day to consistently hit your goal. "
                f"That's about a {(step_goal - avg) / 100:.0f}-minute walk."
            ))

    # Sleep target tracking
    if "df_sleep" in dfs:
        df = dfs["df_sleep"][dfs["df_sleep"]["date"] >= cutoff]
        if "is_main" in df.columns:
            df = df[df["is_main"]]
        if len(df) > 0:
            days_hit = (df["duration_hrs"] >= sleep_target).sum()
            total = len(df)
            pct = (days_hit / total) * 100
            avg = df["duration_hrs"].mean()

            insights.append(make_insight(
                "goal", "low" if pct >= 50 else "medium",
                f"😴 Sleep goal: {pct:.0f}% hit rate",
                f"You hit your {sleep_target}-hour sleep target on {days_hit}/{total} nights. "
                f"Average: {avg:.1f} hours.",
                {"goal_hrs": sleep_target, "days_hit": int(days_hit), "total_nights": total,
                 "avg_hrs": round(avg, 1)},
                None if pct >= 70 else
                f"Try getting to bed {(sleep_target - avg) * 60:.0f} minutes earlier to hit your target."
            ))

    return insights


# ---------------------------------------------------------------------------
# Streaks & Achievements
# ---------------------------------------------------------------------------

def find_streaks(dfs, profile, days=30):
    insights = []
    today = pd.Timestamp.now().normalize()
    cutoff = today - pd.Timedelta(days=days)
    step_goal = profile.get("step_goal", 10000)

    if "df_steps" not in dfs:
        return insights

    df = dfs["df_steps"][(dfs["df_steps"]["date"] >= cutoff) & (dfs["df_steps"]["steps"] > 0)].copy()
    df = df.sort_values("date")

    if len(df) < 3:
        return insights

    # Current streak of hitting step goal
    hit_goal = (df["steps"] >= step_goal).values
    current_streak = 0
    for v in reversed(hit_goal):
        if v:
            current_streak += 1
        else:
            break

    if current_streak >= 3:
        insights.append(make_insight(
            "streak", "low",
            f"🔥 {current_streak}-day step goal streak!",
            f"You've hit your {step_goal:,}-step goal {current_streak} days in a row. Keep it going!",
            {"streak_days": current_streak, "goal": step_goal},
        ))

    # Best single day
    best = df.loc[df["steps"].idxmax()]
    insights.append(make_insight(
        "streak", "low",
        "🏆 Personal best",
        f"Your best day was {best['date'].strftime('%b %d')} with {best['steps']:,.0f} steps.",
        {"date": str(best["date"].date()), "steps": int(best["steps"])},
    ))

    # Best week
    df_weekly = df.set_index("date").resample("W")["steps"].sum()
    if len(df_weekly) >= 2:
        best_week = df_weekly.idxmax()
        best_week_total = df_weekly.max()
        this_week = df_weekly.iloc[-1] if len(df_weekly) > 0 else 0
        if this_week >= best_week_total * 0.9 and this_week > 0:
            insights.append(make_insight(
                "streak", "low",
                "⭐ Near your best week ever!",
                f"This week: {this_week:,.0f} steps. Your record: {best_week_total:,.0f} steps "
                f"(week of {best_week.strftime('%b %d')}). You're {best_week_total - this_week:,.0f} steps away!",
                {"this_week": int(this_week), "best_week": int(best_week_total)},
            ))

    return insights


# ---------------------------------------------------------------------------
# Actionable Recommendations
# ---------------------------------------------------------------------------

def generate_recommendations(dfs, profile, days=30):
    insights = []
    today = pd.Timestamp.now().normalize()
    cutoff = today - pd.Timedelta(days=days)
    goals = profile.get("goals", [])

    # Sleep consistency check
    if "df_sleep" in dfs:
        df = dfs["df_sleep"][dfs["df_sleep"]["date"] >= cutoff]
        if "is_main" in df.columns:
            df = df[df["is_main"]]
        if len(df) >= 7:
            std = df["duration_hrs"].std()
            if std > 1.5:
                insights.append(make_insight(
                    "recommendation", "medium",
                    "🎯 Inconsistent sleep schedule",
                    f"Your sleep varies by ±{std:.1f} hours night to night. "
                    "Consistent sleep timing improves both sleep quality and daytime energy.",
                    {"sleep_std_hrs": round(std, 1)},
                    "Try setting a consistent bedtime alarm. Even 30 minutes more consistency helps."
                ))

    # Weekday vs weekend sleep gap
    if "df_sleep" in dfs:
        df = dfs["df_sleep"][dfs["df_sleep"]["date"] >= cutoff].copy()
        if "is_main" in df.columns:
            df = df[df["is_main"]]
        if len(df) >= 10:
            df["is_weekend"] = df["date"].dt.dayofweek >= 5
            weekday_sleep = df[~df["is_weekend"]]["duration_hrs"].mean()
            weekend_sleep = df[df["is_weekend"]]["duration_hrs"].mean()
            gap = weekend_sleep - weekday_sleep
            if gap > 1:
                insights.append(make_insight(
                    "recommendation", "medium",
                    "📅 Social jet lag detected",
                    f"You sleep {gap:.1f} hours more on weekends ({weekend_sleep:.1f}h) than weekdays ({weekday_sleep:.1f}h). "
                    "This 'social jet lag' disrupts your circadian rhythm.",
                    {"weekday_avg": round(weekday_sleep, 1), "weekend_avg": round(weekend_sleep, 1), "gap_hrs": round(gap, 1)},
                    "Try adding 30 minutes to weekday sleep rather than oversleeping on weekends."
                ))

    # Low activity warning
    if "df_steps" in dfs:
        df = dfs["df_steps"][(dfs["df_steps"]["date"] >= cutoff) & (dfs["df_steps"]["steps"] > 0)]
        if len(df) >= 7:
            avg = df["steps"].mean()
            if avg < 5000:
                insights.append(make_insight(
                    "recommendation", "high",
                    "🚶 Activity level below recommended",
                    f"Your average of {avg:,.0f} steps/day is below the CDC-recommended minimum of 7,000-8,000 for health benefits.",
                    {"avg_steps": round(avg)},
                    "Start small: a 10-minute walk after each meal adds ~3,000 steps. That alone could change your numbers."
                ))

    # Device not worn recently
    if "df_steps" in dfs:
        df = dfs["df_steps"].sort_values("date")
        active = df[df["steps"] > 0]
        if len(active) > 0:
            last_active = active.iloc[-1]["date"]
            days_since = (today - last_active).days
            if days_since > 3:
                insights.append(make_insight(
                    "recommendation", "high",
                    "⌚ Fitbit not worn recently",
                    f"Your last activity was {days_since} days ago ({last_active.strftime('%b %d')}). "
                    "Put your Fitbit back on to keep tracking!",
                    {"last_active": str(last_active.date()), "days_since": days_since},
                    "Even wearing it just during the day gives valuable step, HR, and activity data."
                ))

    # Resting HR in high range
    if "df_hr" in dfs:
        df = dfs["df_hr"][(dfs["df_hr"]["date"] >= cutoff) & dfs["df_hr"]["resting_hr"].notna()]
        if len(df) >= 7:
            avg_hr = df["resting_hr"].mean()
            if avg_hr > 80:
                insights.append(make_insight(
                    "recommendation", "medium",
                    "❤️ Resting HR on the higher side",
                    f"Your average resting HR is {avg_hr:.0f} bpm. While normal range is 60-100, "
                    "a lower resting HR generally indicates better cardiovascular fitness.",
                    {"avg_resting_hr": round(avg_hr)},
                    "Regular cardio exercise (even brisk walking) can lower resting HR over weeks."
                ))

    return insights


# ---------------------------------------------------------------------------
# Briefing Summary
# ---------------------------------------------------------------------------

def generate_briefing(all_insights, profile):
    """Create a natural language 2-3 sentence summary of the most important findings."""
    high = [i for i in all_insights if i["priority"] == "high"]
    medium = [i for i in all_insights if i["priority"] == "medium"]

    if not all_insights:
        return "No significant health insights to report. Your data looks stable. Keep it up! 💪"

    parts = []

    # Lead with high priority
    if high:
        titles = [i["title"] for i in high[:2]]
        parts.append(f"⚠️ Attention needed: {'; '.join(titles)}.")

    # Add medium priority context
    if medium:
        titles = [i["title"] for i in medium[:2]]
        parts.append(f"Worth noting: {'; '.join(titles)}.")

    # Add a positive note if there are achievements
    streaks = [i for i in all_insights if i["type"] == "streak" and "streak" in i.get("title", "").lower()]
    if streaks:
        parts.append(streaks[0]["message"])
    elif not high:
        parts.append("Overall looking good — keep up the healthy habits! 💪")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Proactive Fitbit health insights")
    parser.add_argument("--type", choices=["anomaly", "trend", "goal", "streak", "correlation", "recommendation"],
                        help="Filter to specific insight type")
    parser.add_argument("--days", type=int, default=30, help="Analysis window in days (default 30)")
    parser.add_argument("--brief", action="store_true", help="Output only the briefing summary")
    args = parser.parse_args()

    # Load data
    dfs = prepare_dataframes()
    if not dfs:
        print(json.dumps({"error": "No Fitbit data found. Run fitbit_sync.py first."}, indent=2))
        sys.exit(1)

    profile = load_profile()

    # Run requested insight generators
    all_insights = []
    generators = {
        "anomaly": lambda: detect_anomalies(dfs, args.days),
        "trend": lambda: analyze_trends(dfs, args.days),
        "correlation": lambda: find_correlations(dfs, args.days),
        "goal": lambda: track_goals(dfs, profile, args.days),
        "streak": lambda: find_streaks(dfs, profile, args.days),
        "recommendation": lambda: generate_recommendations(dfs, profile, args.days),
    }

    if args.type:
        all_insights = generators[args.type]()
    else:
        for gen in generators.values():
            try:
                all_insights.extend(gen())
            except Exception as e:
                all_insights.append(make_insight(
                    "error", "low", "Analysis error",
                    f"Failed to generate some insights: {str(e)}"
                ))

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    all_insights.sort(key=lambda x: priority_order.get(x["priority"], 3))

    briefing = generate_briefing(all_insights, profile)

    if args.brief:
        print(briefing)
    else:
        report = {
            "generated_at": datetime.now().isoformat(),
            "analysis_window_days": args.days,
            "profile_loaded": bool(profile),
            "briefing_summary": briefing,
            "insight_count": len(all_insights),
            "insights": all_insights,
        }
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
