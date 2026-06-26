#!/usr/bin/env bash
# send.sh - simple msmtp wrapper for OpenClaw

if [ $# -lt 3 ]; then
  echo "Usage: $0 <to> <subject> <body>"
  exit 1
fi

TO="$1"
SUBJECT="$2"
BODY="$3"

{
  echo "To: $TO"
  echo "Subject: $SUBJECT"
  echo
  echo "$BODY"
} | msmtp -- "$TO"
