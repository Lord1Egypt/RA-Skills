#!/bin/bash
set -a
source /home/admin/.openclaw/workspace/skills/mapulse-prod/.env
set +a
cd /home/admin/.openclaw/workspace/skills/mapulse-prod/scripts
/usr/bin/python3 cron_briefing.py >> /tmp/mapulse_briefing.log 2>&1
