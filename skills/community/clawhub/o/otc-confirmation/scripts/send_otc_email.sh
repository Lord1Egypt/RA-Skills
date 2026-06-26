#!/bin/bash
# send_otc_email.sh — Send OTC confirmation email
# Usage: bash send_otc_email.sh <operation> [session] [lang]
#
# Reads the code from the secure state file (written by generate_code.sh).
# The code is NEVER printed to stdout or included in any output.
# If email sending fails, the script exits with error — no silent fallback.

set -euo pipefail

OPERATION="$1"
SESSION="${2:-current session}"
LANG_PREF="${3:-auto}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="${OTC_STATE_DIR:-${TMPDIR:-/tmp}/otc_state_$(id -u)}"
STATE_FILE="$STATE_DIR/pending"

# Read code from state file
if [ ! -f "$STATE_FILE" ]; then
  echo "Error: No pending OTC code found. Run generate_code.sh first." >&2
  exit 1
fi

CODE=$(cat "$STATE_FILE")

if [ -z "$CODE" ]; then
  echo "Error: State file is empty. Run generate_code.sh first." >&2
  exit 1
fi

# Auto-detect language if not specified
if [ "$LANG_PREF" = "auto" ]; then
  if LC_ALL=C grep -q '[一-龥]' <<< "$OPERATION$SESSION" 2>/dev/null || \
     python3 -c "import sys; sys.exit(0 if any('\u4e00' <= c <= '\u9fff' for c in '''$OPERATION$SESSION''') else 1)" 2>/dev/null; then
    LANG_PREF="zh"
  else
    LANG_PREF="en"
  fi
fi

# Read configuration
EMAIL_RECIPIENT="${OTC_EMAIL_RECIPIENT:-}"
EMAIL_BACKEND="${OTC_EMAIL_BACKEND:-smtp}"

if [ -z "$EMAIL_RECIPIENT" ]; then
  echo "Error: OTC_EMAIL_RECIPIENT not configured." >&2
  exit 1
fi

# Load email template based on language
TEMPLATE_FILE="${SCRIPT_DIR}/../templates/email_template_${LANG_PREF}.txt"
if [ ! -f "$TEMPLATE_FILE" ]; then
  TEMPLATE_FILE="${SCRIPT_DIR}/../templates/email_template.txt"
  if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: Email template not found." >&2
    exit 1
  fi
fi

# Replace variables in template (use | as delimiter for safety)
EMAIL_BODY=$(cat "$TEMPLATE_FILE" | \
  sed "s|{code}|${CODE}|g" | \
  sed "s|{operation}|${OPERATION}|g" | \
  sed "s|{session}|${SESSION}|g")

SUBJECT="OTC Confirmation Code"

# Send via configured backend — failure is FATAL, never fallthrough
case "$EMAIL_BACKEND" in
  smtp)
    bash "${SCRIPT_DIR}/send_email_smtp.sh" "$EMAIL_RECIPIENT" "$SUBJECT" "$EMAIL_BODY"
    ;;
  send-email)
    if ! command -v send-email &> /dev/null; then
      echo "Error: send-email command not found. Install send-email skill or use smtp backend." >&2
      exit 1
    fi
    send-email --to "$EMAIL_RECIPIENT" --subject "$SUBJECT" --body "$EMAIL_BODY"
    ;;
  himalaya)
    if ! command -v himalaya &> /dev/null; then
      echo "Error: himalaya command not found. Install himalaya or use smtp backend." >&2
      exit 1
    fi
    echo "$EMAIL_BODY" | himalaya send --to "$EMAIL_RECIPIENT" --subject "$SUBJECT"
    ;;
  custom)
    CUSTOM_SCRIPT="${OTC_CUSTOM_EMAIL_SCRIPT:-}"
    if [ -z "$CUSTOM_SCRIPT" ]; then
      echo "Error: OTC_CUSTOM_EMAIL_SCRIPT not set." >&2
      exit 1
    fi
    if [ ! -f "$CUSTOM_SCRIPT" ]; then
      echo "Error: Custom email script not found: $CUSTOM_SCRIPT" >&2
      exit 1
    fi
    if [ ! -x "$CUSTOM_SCRIPT" ]; then
      echo "Error: Custom email script is not executable: $CUSTOM_SCRIPT" >&2
      exit 1
    fi
    bash "$CUSTOM_SCRIPT" "$EMAIL_RECIPIENT" "$SUBJECT" "$EMAIL_BODY"
    ;;
  *)
    echo "Error: Unknown email backend: $EMAIL_BACKEND" >&2
    exit 1
    ;;
esac

# Check exit status of the email backend
if [ $? -ne 0 ]; then
  echo "Error: Failed to send OTC email. Operation BLOCKED." >&2
  exit 1
fi

echo "OTC email sent successfully." >&2
