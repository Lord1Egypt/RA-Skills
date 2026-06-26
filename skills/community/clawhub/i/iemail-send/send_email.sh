#!/bin/bash

if [ $# -lt 3 ]; then
  echo "Usage: send_email.sh <to> <subject> <content>"
  exit 1
fi

TO="$1"
SUBJECT="$2"
CONTENT="$3"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 "$SCRIPT_DIR/send_email.py" --to "$TO" --subject "$SUBJECT" --content "$CONTENT"
