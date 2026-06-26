#!/usr/bin/env python3
"""
JobClaw Setup Wizard

Interactive first-run configuration. Generates config.json in JOBCLAW_DIR.

Usage:
    python3 setup.py
    python3 setup.py --non-interactive  (uses all defaults, prompts only for required fields)
"""

import json
import os
import subprocess
import sys
from pathlib import Path


# ── Defaults ──────────────────────────────────────────────────────────────────

DEFAULT_CODING_KEYWORDS = [
    "machine learning engineer", "deep learning engineer", "AI engineer",
    "LLM engineer", "MLOps engineer", "computer vision engineer",
    "NLP engineer", "data scientist", "applied scientist", "research scientist",
]

DEFAULT_NONCODING_KEYWORDS = [
    "wearable AI", "human activity recognition", "affective computing",
    "healthcare AI", "digital health machine learning", "health data scientist",
    "clinical AI", "fintech data scientist", "AI consultant",
    "research associate machine learning", "postdoctoral machine learning",
    "AI product manager",
]

DEFAULT_LOCATIONS = ["London, UK"]

CONFIG_TEMPLATE = {
    "user": {
        "name": "",
        "background": "",
        "target_roles": [],
        "skill_keywords": [],
        "cv_path": "",
    },
    "search": {
        "coding_keywords": DEFAULT_CODING_KEYWORDS,
        "noncoding_keywords": DEFAULT_NONCODING_KEYWORDS,
        "locations": DEFAULT_LOCATIONS,
        "min_score": 70,
        "hours_old": 48,
        "results_per_search": 10,
        "platforms": ["linkedin", "indeed"],
    },
    "notifications": {
        "enabled": False,
        "telegram_bot_token": "",
        "telegram_chat_id": "",
        "openclaw_channel": "",
        "openclaw_account": "",
    },
    "schedule": {
        "daily_time": "07:30",
        "weekdays_only": True,
        "timezone": "Europe/London",
    },
    "csv_filename": "jobs.csv",
    "version": "1.0",
}


def get_jobclaw_dir() -> Path:
    env_dir = os.environ.get("JOBCLAW_DIR")
    if env_dir:
        return Path(env_dir)
    return Path.home() / "Documents" / "JobClaw"


def prompt(message: str, default: str = "", required: bool = False) -> str:
    """Prompt user for input with an optional default."""
    if default:
        msg = f"  {message} [{default}]: "
    else:
        msg = f"  {message}: "

    while True:
        answer = input(msg).strip()
        if answer:
            return answer
        if default:
            return default
        if not required:
            return ""
        print("  (required — please enter a value)")


def prompt_yn(message: str, default: bool = False) -> bool:
    default_str = "Y/n" if default else "y/N"
    answer = input(f"  {message} [{default_str}]: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def check_pip_package(package: str) -> bool:
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        return False


def install_package(package: str) -> bool:
    print(f"  Installing {package}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package, "--break-system-packages"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"  ✅ {package} installed.")
        return True
    # Try without --break-system-packages
    result2 = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        capture_output=True, text=True,
    )
    if result2.returncode == 0:
        print(f"  ✅ {package} installed.")
        return True
    print(f"  ❌ Failed to install {package}. Install manually: pip install {package}")
    return False


def setup(non_interactive: bool = False):
    print("""
╔══════════════════════════════════════════╗
║           JobClaw Setup Wizard           ║
║   AI-powered job search for everyone    ║
╚══════════════════════════════════════════╝
""")

    jobclaw_dir = get_jobclaw_dir()
    config_path = jobclaw_dir / "config.json"

    # ── Check if already configured ──────────────────────────────────────────
    if config_path.exists() and not non_interactive:
        print(f"  Config already exists at: {config_path}")
        if not prompt_yn("Overwrite?", default=False):
            print("  Setup cancelled. Existing config preserved.")
            return

    # ── Create directories ────────────────────────────────────────────────────
    print(f"\n[1/6] Setting up directories in: {jobclaw_dir}")
    (jobclaw_dir / "data").mkdir(parents=True, exist_ok=True)
    (jobclaw_dir / "logs").mkdir(parents=True, exist_ok=True)
    print(f"  ✅ Directories ready.")

    # ── Check dependencies ────────────────────────────────────────────────────
    print("\n[2/6] Checking dependencies...")

    required_packages = ["jobspy", "openpyxl"]
    all_ok = True

    for pkg in required_packages:
        pkg_import = "jobspy" if pkg == "jobspy" else pkg
        if check_pip_package(pkg_import):
            print(f"  ✅ {pkg}")
        else:
            print(f"  ⚠️  {pkg} not found.")
            if not non_interactive:
                if prompt_yn(f"Install {pkg}?", default=True):
                    ok = install_package(pkg if pkg != "jobspy" else "python-jobspy")
                    if not ok:
                        all_ok = False
            else:
                install_package(pkg if pkg != "jobspy" else "python-jobspy")

    if not all_ok:
        print("\n  ⚠️  Some dependencies are missing. Search may not work until installed.")

    # ── User profile ──────────────────────────────────────────────────────────
    config = json.loads(json.dumps(CONFIG_TEMPLATE))  # deep copy

    print("\n[3/6] Your profile (used for job scoring)")

    if not non_interactive:
        config["user"]["name"] = prompt("Your name", required=True)
        config["user"]["background"] = prompt(
            "Brief background (e.g. 'ML PhD, LLM/NLP, wearable sensing')",
            default="ML researcher",
        )
        skill_str = prompt(
            "Key skills/domains (comma-separated, for scoring boost)",
            default="machine learning, deep learning, python, pytorch",
        )
        config["user"]["skill_keywords"] = [s.strip() for s in skill_str.split(",") if s.strip()]
        config["user"]["cv_path"] = prompt("Path to your CV (optional, for AI analysis)", default="")
    else:
        config["user"]["name"] = "User"
        print("  (Using defaults for non-interactive setup)")

    # ── Search settings ────────────────────────────────────────────────────────
    print("\n[4/6] Search settings")

    if not non_interactive:
        location_str = prompt(
            "Target locations (comma-separated, e.g. 'London, UK,Cambridge, UK,New York, NY')",
            default="London, UK",
        )
        # Parse: split on comma-space boundaries that look like "City, Country" pairs
        raw_locations = [loc.strip() for loc in location_str.split("|") if loc.strip()]
        if not raw_locations:
            # Try simple comma split as fallback
            parts = [p.strip() for p in location_str.split(",")]
            # Group pairs: "London" + " UK" → "London, UK"
            raw_locations = []
            i = 0
            while i < len(parts):
                if i + 1 < len(parts) and len(parts[i + 1]) <= 3:
                    raw_locations.append(f"{parts[i]}, {parts[i+1]}")
                    i += 2
                else:
                    raw_locations.append(parts[i])
                    i += 1
        config["search"]["locations"] = raw_locations or ["London, UK"]

        min_score = prompt("Minimum match score to save (0-100)", default="70")
        config["search"]["min_score"] = int(min_score) if min_score.isdigit() else 70

        hours_old = prompt("Only find jobs posted within (hours)", default="48")
        config["search"]["hours_old"] = int(hours_old) if hours_old.isdigit() else 48

        platforms_raw = prompt(
            "Platforms to search (comma-separated: linkedin,indeed)",
            default="linkedin,indeed",
        )
        config["search"]["platforms"] = [p.strip() for p in platforms_raw.split(",") if p.strip()]
    else:
        print("  (Using default search settings)")

    # ── Notifications ─────────────────────────────────────────────────────────
    print("\n[5/6] Notifications (optional)")

    if not non_interactive:
        # OpenClaw notifications (preferred if using within OpenClaw)
        if prompt_yn("Are you using JobClaw inside OpenClaw?", default=False):
            config["notifications"]["enabled"] = True
            config["notifications"]["openclaw_channel"] = prompt(
                "OpenClaw channel (e.g. telegram)", default="telegram"
            )
            config["notifications"]["openclaw_account"] = prompt(
                "OpenClaw account ID", default=""
            )
            config["notifications"]["telegram_chat_id"] = prompt(
                "Your Telegram chat ID (for target)", default=""
            )
        elif prompt_yn("Set up Telegram bot notifications?", default=False):
            config["notifications"]["enabled"] = True
            config["notifications"]["telegram_bot_token"] = prompt(
                "Telegram Bot Token (from @BotFather)", required=True
            )
            config["notifications"]["telegram_chat_id"] = prompt(
                "Your Telegram Chat ID", required=True
            )
        else:
            print("  Skipping notifications (you can add them to config.json later).")
    else:
        print("  (Notifications disabled — edit config.json to enable)")

    # ── Schedule ──────────────────────────────────────────────────────────────
    print("\n[6/6] Daily schedule")

    if not non_interactive:
        daily_time = prompt("Daily search time (HH:MM)", default="07:30")
        config["schedule"]["daily_time"] = daily_time

        weekdays = prompt_yn("Weekdays only (Mon-Fri)?", default=True)
        config["schedule"]["weekdays_only"] = weekdays

        timezone = prompt("Timezone", default="Europe/London")
        config["schedule"]["timezone"] = timezone
    else:
        print("  (Using default schedule: 07:30 weekdays, Europe/London)")

    # ── Save config ───────────────────────────────────────────────────────────
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Config saved to: {config_path}")

    # ── Print cron setup instructions ─────────────────────────────────────────
    skill_dir = Path(__file__).parent.parent
    daily_script = skill_dir / "scripts" / "run_daily.sh"

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                     Setup Complete! 🎉                       ║
╚══════════════════════════════════════════════════════════════╝

Config:  {config_path}
Data:    {jobclaw_dir / 'data' / 'jobs.csv'}
Logs:    {jobclaw_dir / 'logs' / 'daily.log'}

To run a search now:
    python3 {skill_dir}/scripts/search.py --mode all

To set up daily automation with OpenClaw cron, say:
    "Set up JobClaw to run daily at {config['schedule']['daily_time']}"

Manual commands:
    python3 {skill_dir}/scripts/search.py --mode coding
    python3 {skill_dir}/scripts/search.py --mode noncoding
    python3 {skill_dir}/scripts/search.py --mode coding --dry-run
    python3 {skill_dir}/scripts/tracker.py stats
    python3 {skill_dir}/scripts/tracker.py top
""")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="JobClaw setup wizard")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Use defaults without interactive prompts")
    args = parser.parse_args()
    setup(non_interactive=args.non_interactive)
