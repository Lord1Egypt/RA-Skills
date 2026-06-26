#!/usr/bin/env python3
"""
setup.py — First-time setup validator for Homebase

Run this after filling in config.json and .env to verify everything works.
Usage: python3 setup.py
"""

import os
import sys
import json

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "

errors   = []
warnings = []

def check(label: str, condition: bool, error_msg: str = "", warn: bool = False):
    if condition:
        print(f"  {PASS} {label}")
    elif warn:
        print(f"  {WARN} {label}")
        warnings.append(error_msg or label)
    else:
        print(f"  {FAIL} {label}")
        errors.append(error_msg or label)

print("\n🏠 Homebase — Setup Check\n")

# ─── 1. Config file ───────────────────────────────────────────────────────────
print("1. Configuration")

config_path = os.path.join(SKILL_DIR, "config.json")
check("config.json exists", os.path.exists(config_path),
      "Run: cp config.example.json config.json && edit config.json")

if os.path.exists(config_path):
    with open(config_path) as f:
        cfg = json.load(f)

    check("whatsapp.group_id set",
          cfg.get("whatsapp", {}).get("group_id", "").endswith("@g.us") and
          "YOUR" not in cfg.get("whatsapp", {}).get("group_id", ""),
          "Set whatsapp.group_id in config.json")

    check("calendar.id set",
          bool(cfg.get("calendar", {}).get("id")) and
          "YOUR" not in cfg.get("calendar", {}).get("id", ""),
          "Set calendar.id in config.json")

    check("family.members configured",
          len(cfg.get("family", {}).get("members", [])) > 0 and
          "XXXXXXXXXX" not in str(cfg.get("family", {}).get("members", [])),
          "Set family.members with real phone numbers in config.json")

    check("family.kids configured",
          len(cfg.get("family", {}).get("kids", [])) > 0 and
          "Child" not in str([k["name"] for k in cfg.get("family", {}).get("kids", [])]),
          "Set family.kids with real names in config.json")

    check("location configured",
          cfg.get("location", {}).get("latitude", 0) != 0,
          "Set location.latitude and location.longitude in config.json")

    check("school configured",
          bool(cfg.get("school", {}).get("name")) and
          "Your School" not in cfg.get("school", {}).get("name", ""),
          "Set school.name in config.json", warn=True)


# ─── 2. Credentials ───────────────────────────────────────────────────────────
print("\n2. Credentials")

env_path = os.path.join(SKILL_DIR, ".env")
check(".env file exists", os.path.exists(env_path),
      "Run: cp .env.example .env && edit .env")

if os.path.exists(env_path):
    from dotenv import load_dotenv
    load_dotenv(env_path)

    check("GOOGLE_CLIENT_ID set",
          bool(os.environ.get("GOOGLE_CLIENT_ID")) and
          "your_client_id" not in os.environ.get("GOOGLE_CLIENT_ID", ""),
          "Set GOOGLE_CLIENT_ID in .env")

    check("GOOGLE_CLIENT_SECRET set",
          bool(os.environ.get("GOOGLE_CLIENT_SECRET")) and
          "your_client_secret" not in os.environ.get("GOOGLE_CLIENT_SECRET", ""),
          "Set GOOGLE_CLIENT_SECRET in .env")

    check("GOOGLE_REFRESH_TOKEN set",
          bool(os.environ.get("GOOGLE_REFRESH_TOKEN")) and
          "your_refresh_token" not in os.environ.get("GOOGLE_REFRESH_TOKEN", ""),
          "Run: python3 get_token.py to generate refresh token")


# ─── 3. Dependencies ──────────────────────────────────────────────────────────
print("\n3. Dependencies")

deps = [
    ("google.oauth2.credentials", "pip install google-auth"),
    ("googleapiclient.discovery", "pip install google-api-python-client"),
    ("dotenv",                    "pip install python-dotenv"),
]

for module, install_cmd in deps:
    try:
        __import__(module.split(".")[0])
        check(f"{module.split('.')[0]} installed", True)
    except ImportError:
        check(f"{module.split('.')[0]} installed", False,
              f"Run: {install_cmd}")


# Note: this skill does NOT call any LLM directly. The OpenClaw agent
# (whichever model is configured) provides all reasoning and vision. There
# is no Anthropic / OpenAI / Ollama key required by Homebase itself.

# ─── 4. Google Calendar ───────────────────────────────────────────────────────
print("\n4. Google Calendar")

if (os.path.exists(env_path) and os.path.exists(config_path) and
    os.environ.get("GOOGLE_REFRESH_TOKEN")):
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = Credentials(
            token="",
            refresh_token=os.environ.get("GOOGLE_REFRESH_TOKEN"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ.get("GOOGLE_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET")
        )
        creds.refresh(Request())
        service = build("calendar", "v3", credentials=creds)
        service.calendarList().list().execute()
        check("Google Calendar connected", True)
    except Exception as e:
        check("Google Calendar connected", False,
              f"Check credentials in .env. Error: {str(e)[:60]}")
else:
    check("Google Calendar connected", False,
          "Complete steps 1-2 first", warn=True)


# ─── 5. File permissions ─────────────────────────────────────────────────────
print("\n5. Security")

check(".env permissions (600)",
      oct(os.stat(env_path).st_mode)[-3:] == "600" if os.path.exists(env_path) else False,
      "Run: chmod 600 .env", warn=True)

check("config.json not in git",
      ".env" in open(os.path.join(SKILL_DIR, ".gitignore")).read()
      if os.path.exists(os.path.join(SKILL_DIR, ".gitignore")) else False,
      "Add .env and config.json to .gitignore", warn=True)


# ─── Summary ─────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
if errors:
    print(f"❌ {len(errors)} error(s) — fix before running:")
    for e in errors:
        print(f"   • {e}")
    sys.exit(1)
elif warnings:
    print(f"⚠️  Setup complete with {len(warnings)} warning(s):")
    for w in warnings:
        print(f"   • {w}")
    print("\n✅ Ready to run! Start OpenClaw and message your agent on WhatsApp.")
else:
    print("✅ Everything looks great — you're ready to go!")
    print("\nNext steps:")
    print("  1. Test: python3 tools.py get_todays_events")
    print("  2. Run: openclaw start")
    print("  3. Message your agent on WhatsApp!")
