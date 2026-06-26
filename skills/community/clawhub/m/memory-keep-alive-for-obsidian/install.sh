#!/usr/bin/env bash
set -euo pipefail

# OpenClaw Memory + Keep-Alive — Installer
# Installs the skill, sets up Obsidian vault, and adds 5 cron jobs.

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
VAULT_PATH=""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Usage ---
usage() {
  echo "Usage: ./install.sh --vault /path/to/your/Obsidian\\ Vault"
  echo ""
  echo "Options:"
  echo "  --vault PATH         Absolute path to your Obsidian vault (required)"
  echo "  --openclaw PATH      OpenClaw home directory (default: ~/.openclaw)"
  echo "  --help               Show this help"
  exit 1
}

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --vault)     VAULT_PATH="$2"; shift 2 ;;
    --openclaw)  OPENCLAW_DIR="$2"; shift 2 ;;
    --help)      usage ;;
    *)           echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$VAULT_PATH" ]]; then
  echo "Error: --vault is required."
  echo ""
  usage
fi

# --- Validate ---
if [[ ! -d "$OPENCLAW_DIR" ]]; then
  echo "Error: OpenClaw directory not found at $OPENCLAW_DIR"
  echo "Set --openclaw to your OpenClaw home directory."
  exit 1
fi

# --- 1. Install the skill ---
SKILL_DIR="$OPENCLAW_DIR/skills/memory-keep-alive-for-obsidian"
mkdir -p "$SKILL_DIR/templates" "$SKILL_DIR/prompts" "$SKILL_DIR/examples"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

# Copy supporting files into the skill directory
for file in templates/TEMPLATE.md templates/LOOP-STATE.md; do
  if [[ -f "$SCRIPT_DIR/$file" ]]; then
    cp "$SCRIPT_DIR/$file" "$SKILL_DIR/$file"
  fi
done
for file in prompts/*.md; do
  if [[ -f "$SCRIPT_DIR/$file" ]]; then
    cp "$SCRIPT_DIR/$file" "$SKILL_DIR/$file"
  fi
done
for file in examples/*.md; do
  if [[ -f "$SCRIPT_DIR/$file" ]]; then
    cp "$SCRIPT_DIR/$file" "$SKILL_DIR/$file"
  fi
done

echo "Installed skill to $SKILL_DIR/"

# --- 2. Set up Obsidian vault structure ---
TASKS_DIR="$VAULT_PATH/Tasks/Session-Resume-Workflow"
mkdir -p "$TASKS_DIR"

for file in LOOP-STATE.md TEMPLATE.md; do
  if [[ ! -f "$TASKS_DIR/$file" ]]; then
    cp "$SCRIPT_DIR/templates/$file" "$TASKS_DIR/$file"
    echo "Copied $file to $TASKS_DIR/"
  else
    echo "$file already exists, skipping."
  fi
done

if [[ ! -f "$TASKS_DIR/WORKFLOW-INDEX.md" ]]; then
  cp "$SCRIPT_DIR/examples/WORKFLOW-INDEX.md" "$TASKS_DIR/WORKFLOW-INDEX.md"
  echo "Copied WORKFLOW-INDEX.md to $TASKS_DIR/"
else
  echo "WORKFLOW-INDEX.md already exists, skipping."
fi

# --- 3. Add cron jobs ---
# Replace VAULT_PATH in prompts
WATCHDOG_PROMPT="$(sed "s|VAULT_PATH|$VAULT_PATH|g" "$SCRIPT_DIR/prompts/watchdog-prompt.md")"
REPLAYER_PROMPT="$(sed "s|VAULT_PATH|$VAULT_PATH|g" "$SCRIPT_DIR/prompts/replayer-prompt.md")"
ESCALATOR_PROMPT="$(sed "s|VAULT_PATH|$VAULT_PATH|g" "$SCRIPT_DIR/prompts/escalator-prompt.md")"
VALIDATOR_PROMPT="$(sed "s|VAULT_PATH|$VAULT_PATH|g" "$SCRIPT_DIR/prompts/validator-prompt.md")"
SMOKETEST_PROMPT="$(sed "s|VAULT_PATH|$VAULT_PATH|g" "$SCRIPT_DIR/prompts/smoke-test-prompt.md")"

# Try OpenClaw CLI first, fall back to jobs.json merge
if command -v openclaw &>/dev/null; then
  echo "Using OpenClaw CLI to add cron jobs..."

  add_job_if_missing() {
    local name="$1" cron="$2" prompt="$3"
    # Check if job already exists
    if openclaw cron list 2>/dev/null | grep -q "$name"; then
      echo "  Skipped (already exists): $name"
    else
      openclaw cron add \
        --name "$name" \
        --cron "$cron" \
        --session isolated \
        --message "$prompt" \
        --announce 2>/dev/null && echo "  Added job: $name" || echo "  Warning: failed to add $name via CLI"
    fi
  }

  add_job_if_missing "keep-alive-watchdog"    "*/15 * * * *" "$WATCHDOG_PROMPT"
  add_job_if_missing "keep-alive-replayer"    "*/30 * * * *" "$REPLAYER_PROMPT"
  add_job_if_missing "keep-alive-escalator"   "0 * * * *"    "$ESCALATOR_PROMPT"
  add_job_if_missing "memory-validator"        "5 * * * *"    "$VALIDATOR_PROMPT"
  add_job_if_missing "memory-smoke-test"       "0 */6 * * *"  "$SMOKETEST_PROMPT"

else
  echo "OpenClaw CLI not found. Merging jobs directly into jobs.json..."

  JOBS_FILE="$OPENCLAW_DIR/cron/jobs.json"
  mkdir -p "$OPENCLAW_DIR/cron"
  NOW="$(date -u +"%Y-%m-%dT%H:%M:%S.000000+00:00")"

  python3 - "$JOBS_FILE" "$NOW" \
    "$WATCHDOG_PROMPT" "$REPLAYER_PROMPT" "$ESCALATOR_PROMPT" \
    "$VALIDATOR_PROMPT" "$SMOKETEST_PROMPT" <<'PYEOF'
import json, sys, secrets, os

jobs_file = sys.argv[1]
now = sys.argv[2]

SKILL_NAME = "memory-keep-alive-for-obsidian"

prompts = {
    "keep-alive-watchdog":  {"prompt": sys.argv[3], "cron": "*/15 * * * *"},
    "keep-alive-replayer":  {"prompt": sys.argv[4], "cron": "*/30 * * * *"},
    "keep-alive-escalator": {"prompt": sys.argv[5], "cron": "0 * * * *"},
    "memory-validator":     {"prompt": sys.argv[6], "cron": "5 * * * *"},
    "memory-smoke-test":    {"prompt": sys.argv[7], "cron": "0 */6 * * *"},
}

# Load existing jobs
if os.path.exists(jobs_file):
    with open(jobs_file) as f:
        data = json.load(f)
else:
    data = {"jobs": []}

existing_names = {j["name"] for j in data["jobs"]}
added = []
skipped = []

for name, info in prompts.items():
    if name in existing_names:
        skipped.append(name)
        continue
    job = {
        "id": secrets.token_hex(6),
        "name": name,
        "prompt": info["prompt"],
        "skills": [SKILL_NAME],
        "skill": SKILL_NAME,
        "model": None,
        "provider": None,
        "base_url": None,
        "schedule": {
            "kind": "cron",
            "expression": info["cron"],
            "display": info["cron"]
        },
        "schedule_display": info["cron"],
        "repeat": {"times": None, "completed": 0},
        "enabled": True,
        "state": "scheduled",
        "paused_at": None,
        "paused_reason": None,
        "created_at": now,
        "next_run_at": now,
        "last_run_at": None,
        "last_status": None,
        "last_error": None,
        "deliver": "origin",
        "origin": None,
    }
    data["jobs"].append(job)
    added.append(name)

with open(jobs_file, "w") as f:
    json.dump(data, f, indent=2)

for name in added:
    print(f"  Added job: {name}")
for name in skipped:
    print(f"  Skipped (already exists): {name}")
PYEOF
fi

echo ""
echo "Done. Installed:"
echo "  - Skill:      $SKILL_DIR/"
echo "  - Vault:      $TASKS_DIR/"
echo "  - Cron jobs:  5 jobs configured"
echo ""
echo "Your agent will now automatically create task notes for every task."
echo "For long tasks, use /loop-start to arm the keep-alive loop."
echo "When done, /loop-stop to stop burning tokens."
