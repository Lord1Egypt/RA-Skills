#!/usr/bin/env python3
"""User health profile management for personalized insights.

Usage:
  uv run scripts/fitbit_onboarding.py create                    # Print onboarding questions template
  uv run scripts/fitbit_onboarding.py create --goals "fitness,sleep" --activity "moderately active" --step-goal 10000
  uv run scripts/fitbit_onboarding.py show                      # Show current profile
  uv run scripts/fitbit_onboarding.py update --step-goal 12000  # Partial update
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
PROFILE_PATH = BASE_DIR / "data" / "user_profile.json"

VALID_GOALS = [
    "fitness", "weight_loss", "better_sleep", "heart_health",
    "stress_management", "general_wellness", "step_count", "active_minutes"
]

VALID_ACTIVITY_LEVELS = [
    "sedentary", "lightly active", "moderately active", "very active"
]

VALID_BRIEFINGS = ["daily", "weekly", "anomaly_only", "none"]

ONBOARDING_TEMPLATE = {
    "questions": [
        {
            "field": "goals",
            "question": "What health goals are most important to you?",
            "options": VALID_GOALS,
            "type": "multi_select",
            "hint": "Pick 1-3 that matter most. Examples: fitness, better_sleep, heart_health"
        },
        {
            "field": "activity_level",
            "question": "How would you describe your current activity level?",
            "options": VALID_ACTIVITY_LEVELS,
            "type": "single_select",
            "hint": "Be honest — this sets your baseline for personalized targets"
        },
        {
            "field": "step_goal",
            "question": "What's your daily step goal?",
            "type": "number",
            "default": 10000,
            "hint": "Leave blank to use your Fitbit default or 10,000"
        },
        {
            "field": "sleep_target_hrs",
            "question": "How many hours of sleep do you aim for?",
            "type": "number",
            "default": 8,
            "hint": "CDC recommends 7-9 hours for adults"
        },
        {
            "field": "bedtime_goal",
            "question": "What's your ideal bedtime? (e.g., 22:30)",
            "type": "time",
            "default": "23:00",
            "hint": "Consistent bedtime improves sleep quality"
        },
        {
            "field": "wake_goal",
            "question": "What's your ideal wake time? (e.g., 7:00)",
            "type": "time",
            "default": "07:00",
            "hint": "Used for sleep consistency tracking"
        },
        {
            "field": "briefing_preference",
            "question": "How often do you want proactive health updates?",
            "options": VALID_BRIEFINGS,
            "type": "single_select",
            "default": "daily",
            "hint": "daily = morning briefing, weekly = Sunday summary, anomaly_only = alerts when something unusual happens"
        },
        {
            "field": "health_conditions",
            "question": "Any health conditions the agent should be aware of? (optional)",
            "type": "free_text",
            "default": "",
            "hint": "E.g., 'high blood pressure', 'sleep apnea'. Helps contextualize your data. Stored locally only."
        }
    ],
    "instructions": "Ask the user these questions conversationally. Save their answers using: uv run scripts/fitbit_onboarding.py create --goals '<goals>' --activity '<level>' ..."
}


def load_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH) as f:
            return json.load(f)
    return None


def save_profile(profile):
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)


def build_profile(args, existing=None):
    profile = existing or {}

    if args.goals:
        goals = [g.strip() for g in args.goals.split(",")]
        profile["goals"] = goals

    if args.activity:
        profile["activity_level"] = args.activity

    if args.step_goal is not None:
        profile["step_goal"] = args.step_goal

    if args.sleep_target is not None:
        profile["sleep_target_hrs"] = args.sleep_target

    if args.bedtime:
        profile["bedtime_goal"] = args.bedtime

    if args.wake:
        profile["wake_goal"] = args.wake

    if args.briefing:
        profile["briefing_preference"] = args.briefing

    if args.conditions is not None:
        profile["health_conditions"] = args.conditions

    now = datetime.now().isoformat()
    if "created_at" not in profile:
        profile["created_at"] = now
    profile["updated_at"] = now

    return profile


def main():
    parser = argparse.ArgumentParser(description="Fitbit user health profile management")
    parser.add_argument("command", choices=["create", "show", "update"],
                        help="create: new profile, show: display, update: modify")
    parser.add_argument("--goals", help="Comma-separated health goals")
    parser.add_argument("--activity", help="Activity level")
    parser.add_argument("--step-goal", type=int, help="Daily step goal")
    parser.add_argument("--sleep-target", type=float, help="Sleep target in hours")
    parser.add_argument("--bedtime", help="Bedtime goal (HH:MM)")
    parser.add_argument("--wake", help="Wake time goal (HH:MM)")
    parser.add_argument("--briefing", choices=VALID_BRIEFINGS, help="Briefing frequency")
    parser.add_argument("--conditions", help="Health conditions (free text)")

    args = parser.parse_args()

    if args.command == "show":
        profile = load_profile()
        if profile:
            print(json.dumps(profile, indent=2))
        else:
            print("No profile found. Run 'create' first.")
            print("\nOnboarding template:")
            print(json.dumps(ONBOARDING_TEMPLATE, indent=2))
        return

    if args.command == "create":
        # If no flags provided, print the onboarding template for the agent
        has_flags = any([args.goals, args.activity, args.step_goal is not None,
                         args.sleep_target is not None, args.bedtime, args.wake,
                         args.briefing, args.conditions is not None])
        if not has_flags:
            print(json.dumps(ONBOARDING_TEMPLATE, indent=2))
            return

        if load_profile():
            print("⚠️  Profile already exists. Use 'update' to modify, or delete data/user_profile.json to start fresh.")
            sys.exit(1)

        profile = build_profile(args)
        save_profile(profile)
        print("✅ Profile created!")
        print(json.dumps(profile, indent=2))
        return

    if args.command == "update":
        existing = load_profile()
        if not existing:
            print("No profile found. Use 'create' first.")
            sys.exit(1)

        profile = build_profile(args, existing)
        save_profile(profile)
        print("✅ Profile updated!")
        print(json.dumps(profile, indent=2))
        return


if __name__ == "__main__":
    main()
