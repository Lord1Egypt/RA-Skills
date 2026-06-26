#!/bin/bash
# Operation Quarantine — Email Scanner
# Usage: bash email-scan.sh <raw_email_content_file_or_stdin>
# Pipe email content: echo "$EMAIL" | bash email-scan.sh
# Or from file: bash email-scan.sh /path/to/email.txt

QUARANTINE_PORT=${QUARANTINE_PORT:-8085}
QUARANTINE_URL="http://localhost:$QUARANTINE_PORT/quarantine/email"

if [ -n "$1" ] && [ -f "$1" ]; then
  CONTENT=$(cat "$1")
elif [ ! -t 0 ]; then
  CONTENT=$(cat)
else
  echo '{"error": "No email content provided. Pipe content or pass a file path."}'
  exit 1
fi

if [ -z "$CONTENT" ]; then
  echo '{"error": "Empty content"}'
  exit 1
fi

echo "$CONTENT" | jq -Rs '{content: .}' | curl -s -X POST "$QUARANTINE_URL" \
  -H "Content-Type: application/json" -d @-
