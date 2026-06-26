#!/usr/bin/env bash
# email-health-check.sh — Verify email tool connectivity and skill setup
# Usage: bash email-assistant/scripts/email-health-check.sh
# Or: bash scripts/email-health-check.sh (from email-assistant/)

set -euo pipefail

# --- Workspace root detection ---
    # Skill directory detection (stay within skill boundary)
find_skill_root() {
  local dir
  dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  while [ "$dir" != "/" ]; do
    # Skill directory detection (stay within skill boundary)
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo ""
  return 1
}

SKILL_DIR="$(find_skill_root || true)"
if [ -z "$SKILL_DIR" ]; then
    # Skill directory detection (stay within skill boundary)
  echo "    Running checks without workspace context."
else
  echo "📁 Workspace root: $SKILL_DIR"
fi

echo ""
echo "=== Email Assistant Health Check ==="
echo ""

# --- 1. Check email tools ---
echo "1. Email Tool Availability"
TOOL_FOUND=false

if command -v himalaya &> /dev/null; then
  echo "   ✅ himalaya CLI found ($(himalaya --version 2>/dev/null || echo 'version unknown'))"
  if himalaya account list &> /dev/null; then
    echo "   ✅ himalaya accounts configured"
    TOOL_FOUND=true
  else
    echo "   ⚠️  himalaya installed but no accounts configured"
    echo "      Run: himalaya account configure"
  fi
elif command -v gog &> /dev/null; then
  echo "   ✅ gog CLI found (Google Workspace)"
  TOOL_FOUND=true
elif command -v neomutt &> /dev/null; then
  echo "   ✅ neomutt found"
  TOOL_FOUND=true
elif command -v mutt &> /dev/null; then
  echo "   ✅ mutt found"
  TOOL_FOUND=true
else
  echo "   ❌ No email tool found"
  echo "      Install one of: himalaya, gog, mutt/neomutt"
  echo "      Recommended: himalaya (https://github.com/pimalaya/himalaya)"
fi

echo ""

# --- 2. Check data directory ---
echo "2. Data Directory"
DATA_DIR=""
if [ -n "$SKILL_DIR" ] && [ -d "$SKILL_DIR/email-assistant" ]; then
  DATA_DIR="$SKILL_DIR/email-assistant"
elif [ -d "./email-assistant" ]; then
  DATA_DIR="./email-assistant"
fi

if [ -n "$DATA_DIR" ]; then
  echo "   ✅ Data directory found: $DATA_DIR"
  
  # Check subdirectories
  for subdir in data data/digests scripts; do
    if [ -d "$DATA_DIR/$subdir" ]; then
      perms=$(stat -f "%Lp" "$DATA_DIR/$subdir" 2>/dev/null || stat -c "%a" "$DATA_DIR/$subdir" 2>/dev/null || echo "???")
      echo "   ✅ $subdir/ (permissions: $perms)"
    else
      echo "   ❌ MISSING: $subdir/"
    fi
  done
  
  # Check files
  for file in data/email-config.json data/writing-style.json; do
    if [ -f "$DATA_DIR/$file" ]; then
      perms=$(stat -f "%Lp" "$DATA_DIR/$file" 2>/dev/null || stat -c "%a" "$DATA_DIR/$file" 2>/dev/null || echo "???")
      echo "   ✅ $file (permissions: $perms)"
    else
      echo "   ❌ MISSING: $file"
    fi
  done
else
  echo "   ❌ Data directory not found. Run SETUP-PROMPT.md first."
fi

echo ""

# --- 3. Check config validity ---
echo "3. Configuration"
CONFIG_FILE=""
if [ -n "$DATA_DIR" ] && [ -f "$DATA_DIR/data/email-config.json" ]; then
  CONFIG_FILE="$DATA_DIR/data/email-config.json"
fi

if [ -n "$CONFIG_FILE" ]; then
  if python3 - "$CONFIG_FILE" >/dev/null 2>&1 <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    json.load(f)
PY
  then
    echo "   ✅ email-config.json is valid JSON"

    # Extract config values using argv-based path passing for safe path handling.
    VIP_COUNT=$(python3 - "$CONFIG_FILE" 2>/dev/null <<'PY' || echo "0"
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    cfg = json.load(f)

print(len(cfg.get("vip_senders", [])))
PY
)
    echo "   📋 VIP senders configured: $VIP_COUNT"

    MODE=$(python3 - "$CONFIG_FILE" 2>/dev/null <<'PY' || echo "unknown"
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    cfg = json.load(f)

print(cfg.get("check_frequency", {}).get("mode", "unknown"))
PY
)
    echo "   📋 Check mode: $MODE"
  else
    echo "   ❌ email-config.json is invalid JSON — needs repair"
  fi
else
  echo "   ⚠️  No config file found"
fi

echo ""

# --- 4. Test email connectivity ---
echo "4. Email Connectivity Test"
if [ "$TOOL_FOUND" = true ]; then
  if command -v himalaya &> /dev/null; then
    if himalaya envelope list --page-size 1 &> /dev/null; then
      echo "   ✅ Successfully connected to inbox via himalaya"
    else
      echo "   ❌ Could not connect to inbox — check himalaya configuration"
    fi
  elif command -v gog &> /dev/null; then
    echo "   ℹ️  gog connectivity test: run 'gog gmail list' manually"
  fi
else
  echo "   ⏭️  Skipped — no email tool available"
fi

echo ""
echo "=== Health Check Complete ==="
