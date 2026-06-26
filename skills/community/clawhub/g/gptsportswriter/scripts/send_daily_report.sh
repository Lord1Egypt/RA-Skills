#!/usr/bin/env bash
set -euo pipefail
cd /home/pi/.openclaw/workspace
set -a
source /home/pi/.openclaw/workspace/.env
set +a
python3 /home/pi/.openclaw/workspace/skills/gptsportswriter/scripts/generate_report.py --sports baseball_mlb basketball_nba > /tmp/gptsportswriter-report.txt
source /home/pi/.openclaw/workspace/.venv-agentmail/bin/activate
python /home/pi/.openclaw/workspace/skills/agentmail/scripts/send_email.py \
  --inbox 'njm.openclaw@agentmail.to' \
  --to 'normandmickey@gmail.com' \
  --subject 'GPTSportswriter daily betting report' \
  --text "$(cat /tmp/gptsportswriter-report.txt)"
