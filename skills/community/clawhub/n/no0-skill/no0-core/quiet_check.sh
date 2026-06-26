#!/bin/bash
cd "$(dirname "$0")"
python3 scripts/skill_launcher.py status --quiet > /dev/null 2>&1
exit 0
