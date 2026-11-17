#!/usr/bin/env python3
"""
setup_check.py — First-time setup validator for Homebase

Run this after filling in config.json to verify everything works. There is no
.env: Google credentials come from Keychain through the gog CLI.
Usage: python3 setup_check.py
"""

import os
from datetime import datetime, timedelta
import subprocess
import shutil
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

    def _primary_wa_group(c):
        wa = c.get("whatsapp", {})
        groups = wa.get("groups") or []
        if isinstance(groups, list) and groups:
            return (groups[0] or {}).get("id", "")
        return wa.get("group_id", "")

    _primary = _primary_wa_group(cfg)
    check("whatsapp primary group set",
          _primary.endswith("@g.us") and "YOUR" not in _primary,
          "Set whatsapp.groups[0].id (or legacy whatsapp.group_id) in config.json")

    _wa_groups = cfg.get("whatsapp", {}).get("groups", [])
    if isinstance(_wa_groups, list) and len(_wa_groups) > 1:
        for i, g in enumerate(_wa_groups[1:], start=1):
            gid = (g or {}).get("id", "")
            check(f"whatsapp.groups[{i}] ({(g or {}).get('name', 'unnamed')}) has JID",
                  gid.endswith("@g.us") and "YOUR" not in gid,
                  f"Populate whatsapp.groups[{i}].id in config.json", warn=True)

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

# Credentials belong to the `gog` CLI since 2026-09-07. This section used to
# load GOOGLE_* from Keychain and check each one, which was itself a fix for an
# earlier version that read only .env and so reported three errors against a
# perfectly working Keychain install. Both are moot: homebase holds no Google
# credentials, so the only honest check is to ask gog about its own.
_gog = shutil.which(os.environ.get("GOG_BIN", "gog"))
check("gog installed", bool(_gog),
      "Run: brew install gogcli")

if _gog:
    try:
        _st = subprocess.run([_gog, "auth", "status", "--json", "--no-input"],
                             capture_output=True, text=True, timeout=30)
        _st_json = json.loads(_st.stdout or "{}") if _st.returncode == 0 else {}
        _acct = (_st_json.get("account") or {}).get("email")
        _backend = (_st_json.get("keyring") or {}).get("backend", "?")
        check("gog authenticated", bool(_acct),
              "Run: gog auth add <your-google-account> --services gmail,calendar")
        if _acct:
            print(f"     ↳ {_acct} (keyring: {_backend})")
    except Exception as e:
        check("gog authenticated", False, f"gog auth status failed: {str(e)[:60]}")


# ─── 3. Dependencies ──────────────────────────────────────────────────────────
print("\n3. Dependencies")

# The google-auth / google-api-python-client entries are gone with the client
# they checked for: Google access is the `gog` binary now, verified in step 2.
deps = [
    ("requests", "pip install requests"),
    ("pypdf", "pip install pypdf"),
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

# A live read through the same path the skill actually uses. The previous
# version built its own Credentials + service here, which meant it could pass
# while the code under test failed, or vice versa.
if os.path.exists(config_path):
    try:
        from core.config_loader import config as _cfg
        from core import gcal
        _now = datetime.now().astimezone()
        gcal.list_events(_cfg.calendar_id, _now.isoformat(),
                         (_now + timedelta(days=1)).isoformat())
        check("Google Calendar connected", True)
    except Exception as e:
        check("Google Calendar connected", False,
              f"Check `gog auth status`. Error: {str(e)[:80]}")
else:
    check("Google Calendar connected", False,
          "Complete steps 1-2 first", warn=True)


# ─── 5. File permissions ─────────────────────────────────────────────────────
print("\n5. Security")

# .env is gone: it was the fallback for Google credentials homebase no longer
# holds. Nothing reads one, so there is nothing here to harden.

# config.json holds the family group jid, phone numbers, kid names, the
# calendar id and school addresses — principle 9 treats it as PII exactly like
# .env, but only .env was ever checked. It shipped 0644.
check("config.json permissions (600)",
      oct(os.stat(config_path).st_mode)[-3:] == "600" if os.path.exists(config_path) else False,
      "Run: chmod 600 config.json", warn=True)

_gitignore_path = os.path.join(SKILL_DIR, ".gitignore")
_gitignore_text = open(_gitignore_path).read() if os.path.exists(_gitignore_path) else ""
# .env was removed on 2026-09-10: credentials come from Keychain via gog, and
# nothing reads a .env any more (SKILL.md "Secrets handling"). Checking for it
# here kept the concept alive next to a .env.example that named two deleted
# scripts.
check("config.json not in git",
      "config.json" in _gitignore_text,
      "Add config.json to .gitignore", warn=True)


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
    print("  1. Test: python3 tools.py get_morning_briefing")
    print("  2. Run: openclaw start")
    print("  3. Message your agent on WhatsApp!")
