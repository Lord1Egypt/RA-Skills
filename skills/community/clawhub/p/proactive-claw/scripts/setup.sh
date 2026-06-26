#!/bin/bash
# Proactive Claw — One-time setup
# Supports: Google Calendar API | Nextcloud CalDAV
#
# SECURITY NOTE:
# - No curl/wget. No eval of remote code. No sudo. No root.
# - This script does NOT auto-install Python packages.
# - If required libraries are missing, it prints explicit install commands and exits.

set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/proactive-claw"
CONFIG="$SKILL_DIR/config.json"
CREDS="$SKILL_DIR/credentials.json"

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/setup.sh
  bash scripts/setup.sh --doctor
  bash scripts/setup.sh --print-install-cmd google|nextcloud

Modes:
  default                 Validate deps + run backend setup (OAuth/CalDAV)
  --doctor                Run local readiness checks only (no network writes)
  --print-install-cmd X   Print one install command for backend X
USAGE
}

print_install_cmd() {
  local backend="${1:-}"
  case "$backend" in
    google)
      echo "python3 -m pip install -r \"$SKILL_DIR/requirements-google.txt\""
      ;;
    nextcloud)
      echo "python3 -m pip install -r \"$SKILL_DIR/requirements-nextcloud.txt\""
      ;;
    *)
      echo "Unknown backend: $backend" >&2
      return 1
      ;;
  esac
}

ensure_python() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 not found. Install Python 3.8+ first."
    return 1
  fi
  if ! python3 - <<'PYEOF'
import sys
raise SystemExit(0 if sys.version_info >= (3, 8) else 1)
PYEOF
  then
    echo "ERROR: Python 3.8+ required."
    return 1
  fi
  return 0
}

detect_backend() {
  if [ -f "$CONFIG" ]; then
    python3 - <<PYEOF
import json
from pathlib import Path
p = Path("$CONFIG")
try:
    d = json.loads(p.read_text())
    b = str(d.get("calendar_backend", "google")).strip().lower()
    print(b if b in ("google", "nextcloud") else "google")
except Exception:
    print("google")
PYEOF
  else
    echo "google"
  fi
}

ensure_config_exists() {
  mkdir -p "$SKILL_DIR"
  mkdir -p "$SKILL_DIR/outcomes"
  if [ -f "$CONFIG" ]; then
    return 0
  fi

  echo "Creating default config.json (safe defaults — all features OFF)..."
  cat > "$CONFIG" << 'JSONEOF'
{
  "calendar_backend": "google",
  "max_autonomy_level": "confirm",
  "daemon_enabled": false,
  "proactivity_mode": "balanced",
  "pre_checkin_offset_default": "1 day",
  "pre_checkin_offset_same_day": "1 hour",
  "post_checkin_offset": "30 minutes",
  "conversation_threshold": 5,
  "calendar_threshold": 6,
  "feature_conversation": false,
  "feature_calendar": false,
  "feature_daemon": false,
  "feature_memory": false,
  "feature_conflicts": false,
  "feature_rules": false,
  "feature_intelligence_loop": false,
  "feature_policy_engine": false,
  "feature_orchestrator": false,
  "feature_energy": false,
  "feature_cal_editor": false,
  "feature_relationship": false,
  "feature_adaptive_notifications": false,
  "feature_proactivity_engine": false,
  "feature_interrupt_controller": false,
  "feature_explainability": false,
  "feature_health_check": false,
  "feature_simulation": false,
  "feature_export": false,
  "feature_behaviour_report": false,
  "feature_config_wizard": false,
  "feature_policy_conflict_detection": false,
  "default_user_calendar": "",
  "timezone": "UTC",
  "user_email": "",
  "notes_destination": "local",
  "notes_path": "~/.openclaw/workspace/skills/proactive-claw/outcomes/",
  "scan_days_ahead": 7,
  "scan_cache_ttl_minutes": 30,
  "openclaw_cal_id": "",
  "action_cleanup_days": 30,
  "memory_decay_half_life_days": 90,
  "max_nudges_per_day": 12,
  "quiet_hours": {
    "weekdays": "22:00-07:00",
    "weekends": "21:00-09:00"
  },
  "nextcloud": {
    "url": "",
    "username": "",
    "password": "",
    "openclaw_calendar_url": "",
    "caldav_path": "/remote.php/dav"
  }
}
JSONEOF
  echo "config.json created at $CONFIG"
}

check_google_deps() {
  if python3 - <<'PYEOF'
import importlib.util
mods = ["google.oauth2", "google_auth_oauthlib.flow", "googleapiclient.discovery"]
missing = []
for m in mods:
    try:
        if importlib.util.find_spec(m) is None:
            missing.append(m)
    except Exception:
        missing.append(m)
raise SystemExit(1 if missing else 0)
PYEOF
  then
    echo "Google dependencies: OK"
    return 0
  fi
  echo "Google dependencies: MISSING"
  echo "Install with:"
  print_install_cmd google
  return 1
}

check_nextcloud_deps() {
  if python3 - <<'PYEOF'
import importlib.util
mods = ["caldav", "icalendar"]
missing = []
for m in mods:
    try:
        if importlib.util.find_spec(m) is None:
            missing.append(m)
    except Exception:
        missing.append(m)
raise SystemExit(1 if missing else 0)
PYEOF
  then
    echo "Nextcloud dependencies: OK"
    return 0
  fi
  echo "Nextcloud dependencies: MISSING"
  echo "Install with:"
  print_install_cmd nextcloud
  return 1
}

check_nextcloud_config_fields() {
  python3 - <<PYEOF
import json
from pathlib import Path
p = Path("$CONFIG")
try:
    cfg = json.loads(p.read_text())
except Exception:
    raise SystemExit(1)
nc = cfg.get("nextcloud", {})
needed = ["url", "username", "password"]
missing = [k for k in needed if not str(nc.get(k, "")).strip()]
if missing:
    print("Missing nextcloud config fields: " + ", ".join(missing))
    raise SystemExit(1)
raise SystemExit(0)
PYEOF
}

run_doctor() {
  echo "Proactive Claw Doctor"
  echo "======================"

  local failures=0
  if ensure_python; then
    echo "Python: OK"
  else
    failures=1
  fi

  if [ -f "$CONFIG" ]; then
    echo "Config file: OK ($CONFIG)"
  else
    echo "Config file: MISSING ($CONFIG)"
    echo "  Run: python3 scripts/config_wizard.py --defaults"
  fi

  local backend
  backend="$(detect_backend)"
  echo "Backend: $backend"

  if [ "$backend" = "nextcloud" ]; then
    if ! check_nextcloud_deps; then
      failures=1
    fi
    if ! check_nextcloud_config_fields; then
      echo "Nextcloud config: MISSING REQUIRED FIELDS"
      failures=1
    else
      echo "Nextcloud config: OK"
    fi
  else
    if [ ! -f "$CREDS" ]; then
      echo "Google credentials: MISSING ($CREDS)"
      echo "Create OAuth Desktop credentials in Google Cloud Console and place credentials.json at:"
      echo "  $CREDS"
      failures=1
    else
      echo "Google credentials: OK"
    fi
    if ! check_google_deps; then
      failures=1
    fi
  fi

  echo ""
  if [ "$failures" -eq 0 ]; then
    echo "Doctor result: PASS"
    return 0
  fi
  echo "Doctor result: FAIL"
  return 1
}

run_nextcloud_setup() {
  echo "Setting up Nextcloud backend..."
  check_nextcloud_deps

  python3 - <<'PYEOF'
import json
import sys
from pathlib import Path

SKILL_DIR = Path.home() / ".openclaw/workspace/skills/proactive-claw"
CONFIG_FILE = SKILL_DIR / "config.json"

with open(CONFIG_FILE) as f:
    config = json.load(f)

nc = config.get("nextcloud", {})
url = nc.get("url", "").strip()
username = nc.get("username", "").strip()
password = nc.get("password", "").strip()
caldav_path = nc.get("caldav_path", "/remote.php/dav").strip() or "/remote.php/dav"

if not all([url, username, password]):
    print("ERROR: Nextcloud credentials not set in config.json")
    print("Set nextcloud.url, nextcloud.username, nextcloud.password")
    sys.exit(1)

try:
    import caldav
    client = caldav.DAVClient(
        url=f"{url.rstrip('/')}{caldav_path}",
        username=username,
        password=password,
    )
    principal = client.principal()
    calendars = principal.calendars()
    print(f"Connected to Nextcloud. Found {len(calendars)} calendar(s).")

    openclaw_url = None
    for cal in calendars:
        if cal.name in ("Proactive Claw - Actions", "Proactive Claw — Actions", "OpenClaw"):
            openclaw_url = str(cal.url)
            print(f"Action Calendar exists: {openclaw_url}")
            break

    if not openclaw_url:
        new_cal = principal.make_calendar(name="Proactive Claw - Actions")
        openclaw_url = str(new_cal.url)
        print(f"Action Calendar created: {openclaw_url}")

    config["openclaw_cal_id"] = openclaw_url
    config["nextcloud"]["openclaw_calendar_url"] = openclaw_url

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print("openclaw_cal_id saved to config.json")

except Exception as e:
    print(f"Nextcloud connection failed: {e}")
    sys.exit(1)
PYEOF
}

run_google_setup() {
  echo "Setting up Google backend..."

  if [ ! -f "$CREDS" ]; then
    echo "ERROR: credentials.json not found at $CREDS"
    echo "To create it:"
    echo "  1. Go to https://console.cloud.google.com"
    echo "  2. Create project 'OpenClaw' and enable Google Calendar API"
    echo "  3. Create OAuth 2.0 credentials (Desktop app)"
    echo "  4. Move file to: $CREDS"
    return 1
  fi

  check_google_deps

  python3 - <<'PYEOF'
import json
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SKILL_DIR = Path.home() / ".openclaw/workspace/skills/proactive-claw"
CREDS_FILE = SKILL_DIR / "credentials.json"
TOKEN_FILE = SKILL_DIR / "token.json"
CONFIG_FILE = SKILL_DIR / "config.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None
if TOKEN_FILE.exists():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            creds = None
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
        creds = flow.run_local_server(port=0)
    TOKEN_FILE.write_text(creds.to_json())

service = build("calendar", "v3", credentials=creds)
calendars = service.calendarList().list().execute().get("items", [])
openclaw_id = None
for cal in calendars:
    if cal.get("summary") in ("Proactive Claw - Actions", "Proactive Claw — Actions", "OpenClaw"):
        openclaw_id = cal["id"]
        print(f"Action Calendar exists (id: {openclaw_id})")
        break

if not openclaw_id:
    cal = service.calendars().insert(body={"summary": "Proactive Claw - Actions"}).execute()
    openclaw_id = cal["id"]
    print(f"Action Calendar created (id: {openclaw_id})")

with open(CONFIG_FILE) as f:
    config = json.load(f)
config["openclaw_cal_id"] = openclaw_id

try:
    profile = service.calendars().get(calendarId="primary").execute()
    email = profile.get("id", "")
    if email and not config.get("user_email"):
        config["user_email"] = email
        print(f"user_email set to: {email}")
except Exception:
    pass

with open(CONFIG_FILE, "w") as f:
    json.dump(config, f, indent=2)

try:
    service.events().list(calendarId="primary", maxResults=1).execute()
    print("Calendar API read verified")
except Exception as e:
    print(f"Warning: could not read primary calendar: {e}")

print("Google setup complete")
PYEOF
}

main() {
  local mode="setup"
  local backend_arg=""

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --doctor)
        mode="doctor"
        shift
        ;;
      --print-install-cmd)
        if [ "$#" -lt 2 ]; then
          echo "Missing backend for --print-install-cmd" >&2
          usage
          exit 1
        fi
        mode="print_install"
        backend_arg="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown argument: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  if [ "$mode" = "print_install" ]; then
    if [ -z "$backend_arg" ]; then
      echo "Missing backend for --print-install-cmd" >&2
      usage
      exit 1
    fi
    print_install_cmd "$backend_arg"
    exit 0
  fi

  if [ "$mode" = "doctor" ]; then
    run_doctor
    exit $?
  fi

  echo "Proactive Claw Setup"
  echo "===================="

  ensure_python
  ensure_config_exists

  local backend
  backend="$(detect_backend)"
  echo "Calendar backend: $backend"

  if [ "$backend" = "nextcloud" ]; then
    run_nextcloud_setup
  else
    run_google_setup
  fi

  echo ""
  echo "Setup complete."
  echo "Next steps:"
  echo "  1. Run quickstart: bash scripts/quickstart.sh"
  echo "  2. Customize config: python3 scripts/config_wizard.py"
  echo "  3. Run once: python3 scripts/daemon.py"
}

main "$@"
