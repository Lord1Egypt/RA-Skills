#!/usr/bin/env bash
set -euo pipefail

echo "==== agents ===="
openclaw agents list --json
echo

echo "==== bindings ===="
openclaw agents bindings --json
echo

echo "==== cron ===="
openclaw cron list --json
echo

echo "==== sessions ===="
openclaw sessions --agent main --json
