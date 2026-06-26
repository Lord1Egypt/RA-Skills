#!/bin/bash
# send_email_smtp.sh — Send email via SMTP using curl
# Usage: bash send_email_smtp.sh <to> <subject> <body>
#
# Requires OTC_SMTP_* environment variables to be set.
# Does NOT source external files — credentials must be provided
# via environment variables or OpenClaw config injection.

set -euo pipefail

TO="$1"
SUBJECT="$2"
BODY="$3"

# Read SMTP configuration from environment only
SMTP_HOST="${OTC_SMTP_HOST:-smtp.gmail.com}"
SMTP_PORT="${OTC_SMTP_PORT:-587}"
SMTP_USER="${OTC_SMTP_USER:-}"
SMTP_PASS="${OTC_SMTP_PASS:-}"
SMTP_FROM="${OTC_SMTP_FROM:-${SMTP_USER}}"

if [ -z "$SMTP_USER" ] || [ -z "$SMTP_PASS" ]; then
  echo "Error: SMTP credentials not configured." >&2
  echo "Set OTC_SMTP_USER and OTC_SMTP_PASS environment variables," >&2
  echo "or configure them in openclaw.json under skills.entries.otc-confirmation.env" >&2
  exit 1
fi

# Build SMTP URL based on port
if [ "$SMTP_PORT" = "465" ]; then
  SMTP_URL="smtps://${SMTP_HOST}:${SMTP_PORT}"
else
  SMTP_URL="smtp://${SMTP_HOST}:${SMTP_PORT}"
fi

curl --silent --show-error \
  --url "${SMTP_URL}" \
  --ssl-reqd \
  --mail-from "${SMTP_FROM}" \
  --mail-rcpt "${TO}" \
  --user "${SMTP_USER}:${SMTP_PASS}" \
  -T - <<EOF
From: ${SMTP_FROM}
To: ${TO}
Subject: ${SUBJECT}
Content-Type: text/plain; charset=utf-8

${BODY}
EOF

if [ $? -eq 0 ]; then
  echo "Email sent successfully." >&2
else
  echo "Error: Failed to send email via SMTP." >&2
  exit 1
fi
