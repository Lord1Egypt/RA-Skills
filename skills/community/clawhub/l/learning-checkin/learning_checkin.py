#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Check-in Skill
A skill to help users build daily learning habits through check-ins and reminders.
"""

import os
import sys

# Fix Windows console encoding for UTF-8
if sys.platform == "win32":
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

import json
import datetime
import locale


def get_user_language():
    """Detect user's preferred language based on system locale."""
    try:
        system_lang = locale.getdefaultlocale()[0] or "en_US"
        if system_lang.lower().startswith("zh"):
            return "zh"
        return "en"
    except Exception:
        return "en"


def get_environment_info():
    """Collect minimal environment information - only user_language is required."""
    # Only user_language is needed to display messages in the correct language
    # Other info is not collected to protect user privacy
    return {
        "user_language": get_user_language()
    }


# Configuration
VERSION = "3.1.0"

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Data will be stored in a 'data' subfolder next to the script
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
RULE_FILE = os.path.join(DATA_DIR, "rule.md")
RECORDS_FILE = os.path.join(DATA_DIR, "records.json")
VERSION_FILE = os.path.join(DATA_DIR, "version.txt")
REMINDER_LOG_FILE = os.path.join(DATA_DIR, "reminder_log.json")
CRON_STATUS_FILE = os.path.join(DATA_DIR, "cron_status.json")

# Default reminder times (24-hour format)
DEFAULT_REMINDER_TIMES = ["09:00", "17:00", "20:00"]

# English-only messages (Agent will translate based on user's language)
MESSAGES = {
    "welcome": """🎉 Welcome to Your Learning Journey!

I'm so glad you've decided to build a daily learning habit! That's a great decision 👏

🌟 How Simple It Is:
   Just tell me "I'm done" or "I finished my learning" when you're done for the day!

🔥 Streak Tracking:
   I'll help you track your consecutive learning days
   Miss a day, and the streak resets (but that's okay, just start again!)

⏰ Want Daily Reminders?
   I can remind you if you forget to check in! Just let me know your preferred time (e.g., morning, afternoon, or evening), and I'll help you set it up.

Ready? Let's start your first check-in!""",

    # Check-in success messages
    "checkin_first": "🎉 Awesome! First day check-in complete! Great start!",
    "checkin_week": "🌟 One week! 7 days in a row, you're amazing!",
    "checkin_month": "🏆 One month! 30 days of continuous learning, you're a superstar!",
    "checkin_100": "👑 100 days! You're the learning champion!",
    "checkin_success": [
        "✅ Check-in successful! {streak} days in a row! Keep it up! 💪",
        "✨ Today's learning complete! {streak} days streak, keep it going!",
        "🎯 Day {streak}! Every day of consistency deserves respect!"
    ],

    # Already checked in today
    "already_checked": [
        "You've already checked in today! Great job! Keep up the momentum! 🔥",
        "You're already done for today! See you tomorrow! 💪",
        "Another day completed! So proud of you! ⭐"
    ],

    # Status messages
    "status_done": "✅ You've checked in today!",
    "status_not_done": "⏳ Haven't checked in yet today~",
    "status_streak": " {streak} days in a row!",
    "status_no_streak": " Start your streak journey!",

    # Reminder messages
    "reminder_09": [
        "☀️ Good morning! Have you completed your learning today? Let's start!",
        "🌅 A new day! Remember to check in~",
        "📚 Morning reminder: Learning is a daily goal. Let me know when done!"
    ],
    "reminder_17": [
        "🌤️ Good afternoon! Finished your tasks today?",
        "💪 Half day passed! How's your learning going?",
        "⏰ Reminder: No check-in recorded yet today!"
    ],
    "reminder_20": [
        "🌙 Good evening! Don't forget today's check-in, the streak matters!",
        "🔥 Final reminder: Haven't checked in today. Don't break the streak!",
        "⭐ Did you learn today? Tell me 'done' to keep the streak going!"
    ]
}


def get_message(key, lang=None):
    """Get message by key. Agent should translate to user's language."""
    # Always return English message - Agent handles translation
    return MESSAGES.get(key, MESSAGES.get("en", {}).get(key, ""))


def get_reminder_message(time_slot, lang=None):
    """Get reminder message for specific time slot."""
    if lang is None:
        lang = get_user_language()

    rules = load_rules()
    lines = rules.split("\n")
    in_reminder_section = False
    custom_messages = []
    for line in lines:
        if line.strip() == "## Reminder Messages":
            in_reminder_section = True
            continue
        if in_reminder_section and line.startswith("## "):
            break
        if in_reminder_section and line.strip():
            custom_messages.append(line.strip())

    if custom_messages:
        import random
        return random.choice(custom_messages)

    time_key = f"reminder_{time_slot.split(':')[0]}"
    messages = MESSAGES.get(time_key, [])
    if not messages:
        messages = MESSAGES.get("reminder_20", [])

    import random
    return random.choice(messages) if messages else "Time to check in!"


def ensure_dir():
    """Ensure data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_records():
    """Load check-in records."""
    if not os.path.exists(RECORDS_FILE):
        return {"checkins": []}
    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"checkins": []}


def save_records(records):
    """Save check-in records."""
    ensure_dir()
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def load_rules():
    """Load user rules."""
    if not os.path.exists(RULE_FILE):
        return ""
    try:
        with open(RULE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except IOError:
        return ""


def load_reminder_log():
    """Load reminder log."""
    if not os.path.exists(REMINDER_LOG_FILE):
        return {}
    try:
        with open(REMINDER_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_reminder_log(log_data):
    """Save reminder log."""
    ensure_dir()
    with open(REMINDER_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def load_cron_status():
    """Load cron status."""
    if not os.path.exists(CRON_STATUS_FILE):
        return {"configured": False, "times": [], "last_check": None}
    try:
        with open(CRON_STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"configured": False, "times": [], "last_check": None}


def save_cron_status(status):
    """Save cron status."""
    ensure_dir()
    with open(CRON_STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def get_today():
    """Get today's date string."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def is_checked_in_today():
    """Check if user has already checked in today."""
    records = load_records()
    today = get_today()
    checkins = records.get("checkins", [])
    for checkin in checkins:
        # Support both old format (string) and new format (dict)
        if isinstance(checkin, dict):
            checkin_date = checkin.get("date")
        else:
            checkin_date = checkin
        if checkin_date == today:
            return True
    return False


def get_streak():
    """Calculate current check-in streak."""
    records = load_records()
    checkins = records.get("checkins", [])

    if not checkins:
        return 0

    # Convert to standard format (list of dicts) if needed
    normalized = []
    for c in checkins:
        if isinstance(c, dict):
            normalized.append(c)
        else:
            normalized.append({"date": c, "timestamp": ""})

    # Sort by date descending
    sorted_checkins = sorted(normalized, key=lambda x: x.get("date", ""), reverse=True)

    streak = 0
    today = datetime.datetime.now()
    expected_date = today.strftime("%Y-%m-%d")

    # Check if checked in today
    if sorted_checkins and sorted_checkins[0].get("date") == expected_date:
        streak = 1
        expected_date = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # Count consecutive days
    for checkin in sorted_checkins[1:]:
        checkin_date = checkin.get("date", "")
        if checkin_date == expected_date:
            streak += 1
            expected_date = (datetime.datetime.strptime(expected_date, "%Y-%m-%d") - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            break

    return streak


def do_checkin():
    """Perform check-in."""
    lang = get_user_language()

    if is_checked_in_today():
        streak = get_streak()
        messages = get_message("already_checked", lang)
        import random
        return {
            "success": False,
            "message": random.choice(messages),
            "streak": streak,
            "language": lang
        }

    now = datetime.datetime.now()
    checkin_record = {
        "date": now.strftime("%Y-%m-%d"),
        "timestamp": now.isoformat()
    }

    records = load_records()
    records["checkins"].append(checkin_record)
    save_records(records)

    streak = get_streak()

    # Return different celebration messages based on streak
    if streak == 1:
        message = get_message("checkin_first", lang)
    elif streak == 7:
        message = get_message("checkin_week", lang)
    elif streak == 30:
        message = get_message("checkin_month", lang)
    elif streak == 100:
        message = get_message("checkin_100", lang)
    else:
        messages = get_message("checkin_success", lang)
        import random
        message = random.choice(messages).format(streak=streak)

    return {
        "success": True,
        "message": message,
        "streak": streak,
        "date": checkin_record["date"],
        "note": "Version check is handled by Agent - check GitHub releases periodically"
    }


def get_status():
    """Get current check-in status."""
    today_checked = is_checked_in_today()
    streak = get_streak()
    records = load_records()
    total_checkins = len(records.get("checkins", []))
    lang = get_user_language()

    if today_checked:
        status_message = get_message("status_done", lang)
        status_message += get_message("status_streak", lang).format(streak=streak)
    else:
        status_message = get_message("status_not_done", lang)
        if streak > 0:
            status_message += get_message("status_streak", lang).format(streak=streak)
        else:
            status_message += get_message("status_no_streak", lang)

    return {
        "checked_in_today": today_checked,
        "streak": streak,
        "total_checkins": total_checkins,
        "today": get_today(),
        "message": status_message,
        "language": lang
    }


def get_version():
    """Return current version."""
    return VERSION
    """Get the friendly welcome message for first-time users."""
    return get_message("welcome", lang)


def update_cron_status(times):
    """Update cron status after Agent attempts to set up."""
    status = {
        "configured": True,
        "times": times,
        "last_check": datetime.datetime.now().isoformat()
    }
    save_cron_status(status)


def init_skill():
    """Initialize the skill - create data directory and default files."""
    ensure_dir()
    lang = get_user_language()

    # Create default rule.md if not exists
    if not os.path.exists(RULE_FILE):
        default_rule = get_welcome_message(lang)
        with open(RULE_FILE, "w", encoding="utf-8") as f:
            f.write(default_rule)

    # Create empty records if not exists
    if not os.path.exists(RECORDS_FILE):
        save_records({"checkins": []})

    # Save current version
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(VERSION)

    # Get environment info
    env_info = get_environment_info()

    # Reminder strategy - for documentation only, Agent handles cron setup
    cron_setup = {
        "note": "Agent uses cron skill to set up reminders at user's preferred time"
    }

    # Load existing cron status
    cron_status = load_cron_status()

    # Get welcome message
    welcome_msg = get_welcome_message(lang)

    # Reminder strategy - Agent handles the actual setup
    reminder_strategy = {
        "recommended_time": "20:00",
        "suggested_schedule": {
            "morning": "09:00",
            "afternoon": "17:00", 
            "evening": "20:00"
        },
        "note": "If user wants reminders, Agent should use the cron skill to set up a daily job at the user's preferred time. The Agent will check if user already checked in before sending reminders."
    }

    return {
        "success": True,
        "message": welcome_msg,
        "data_dir": DATA_DIR,
        "first_time": True,
        "language": lang,
        "environment": env_info,
        "reminder_strategy": reminder_strategy,
        "cron_status": cron_status,
        "skill_path": SCRIPT_DIR,
        "note": "Ask user if they want daily reminders. If yes, Agent uses cron skill to set up."
    }


def update_cron_command(times_str):
    """Update cron status from Agent after setting up."""
    times = [t.strip() for t in times_str.split(",") if t.strip()]
    update_cron_status(times)
    return {
        "success": True,
        "configured_times": times,
        "message": "Cron status updated successfully"
    }


def get_reminder_message_main(time_slot):
    """Get reminder message for specific time slot (CLI entry point)."""
    return get_reminder_message(time_slot, None)


def should_send_reminder(time_slot):
    """Check if reminder should be sent for this time slot today."""
    reminder_log = load_reminder_log()
    today = get_today()
    key = f"{today}_{time_slot}"

    # Already reminded today at this time
    if reminder_log.get(key):
        return False

    # Check if already checked in today
    if is_checked_in_today():
        return False

    return True


def log_reminder_sent(time_slot):
    """Log that reminder was sent."""
    reminder_log = load_reminder_log()
    today = get_today()
    key = f"{today}_{time_slot}"
    reminder_log[key] = {"timestamp": datetime.datetime.now().isoformat()}
    save_reminder_log(reminder_log)


# CLI Interface
def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python learning_checkin.py <command> [args]")
        print("Commands:")
        print("  init                  - Initialize the skill (first time setup)")
        print("  checkin               - Record a check-in")
        print("  status                - Get current status")
        print("  streak                - Get current streak")
        print("  version               - Get current version")
        print("  env                   - Get user language (for message display)")
        print("  cron-status           - Get reminder configuration status")
        print("  update-cron <times>   - Update reminder times (after user sets up)")
        print("  reminder <time>       - Check if reminder should be sent (e.g., 09:00)")
        print("  message <time>        - Get reminder message for time slot")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "init":
        result = init_skill()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "checkin":
        result = do_checkin()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "status":
        result = get_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "streak":
        print(json.dumps({"streak": get_streak()}, ensure_ascii=False, indent=2))

    elif command == "version":
        print(json.dumps({"version": VERSION}, ensure_ascii=False, indent=2))

    elif command == "env":
        result = get_environment_info()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "update-cron":
        if len(sys.argv) < 3:
            print("Usage: python learning_checkin.py update-cron <times>")
            print("Example: python learning_checkin.py update-cron 20:00")
            print("Example: python learning_checkin.py update-cron 09:00,20:00")
            sys.exit(1)
        times_str = sys.argv[2]
        result = update_cron_command(times_str)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "cron-status":
        status = load_cron_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))

    elif command == "setup-cron":
        setup_result = {
            "skill_path": SCRIPT_DIR,
            "cron_commands": {
                "09:00": f'<command> cron create --type agent --name "Learning Check-in Morning" --cron "0 9 * * *" --channel <channel> --target-user <user> --target-session <session> --text "python \\"{SCRIPT_DIR}\\learning_checkin.py\\" checkin"',
                "17:00": f'<command> cron create --type agent --name "Learning Check-in Afternoon" --cron "0 17 * * *" --channel <channel> --target-user <user> --target-session <session> --text "python \\"{SCRIPT_DIR}\\learning_checkin.py\\" checkin"',
                "20:00": f'<command> cron create --type agent --name "Learning Check-in Evening" --cron "0 20 * * *" --channel <channel> --target-user <user> --target-session <session> --text "python \\"{SCRIPT_DIR}\\learning_checkin.py\\" checkin"'
            },
            "note": "Replace <command>, <channel>, <user>, <session> with your actual values"
        }
        print(json.dumps(setup_result, ensure_ascii=False, indent=2))

    elif command == "reminder":
        if len(sys.argv) < 3:
            print("Usage: python learning_checkin.py reminder <time_slot>")
            sys.exit(1)
        time_slot = sys.argv[2]
        result = {
            "should_send": should_send_reminder(time_slot),
            "checked_in": is_checked_in_today()
        }
        if result["should_send"]:
            log_reminder_sent(time_slot)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "message":
        if len(sys.argv) < 3:
            print("Usage: python learning_checkin.py message <time_slot>")
            sys.exit(1)
        time_slot = sys.argv[2]
        message = get_reminder_message_main(time_slot)
        print(json.dumps({"message": message}, ensure_ascii=False, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()