#!/usr/bin/env bash
set -euo pipefail

out="$(bash "$(dirname "$0")/../scripts/speak.sh" --list-voices)"
printf '%s
' "$out" | grep -q 'en-us-Jasper:MAI-Voice-1'
printf '%s
' "$out" | grep -q 'en-us-Iris:MAI-Voice-1'
echo ok
