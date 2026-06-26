#!/usr/bin/env python3
"""mit.prompt — cron-time chat prompt text for the nightly MIT check-in."""

import json

PROMPT = (
    "MIT nightly check-in. In this same chat session:\n"
    "1) Run: python3 examples/mit/scripts/today_brief.py\n"
    "2) Read the JSON. If today's task is set, ask the user (in their language):\n"
    "     a) Did you finish today's MIT \"<task>\"? (yes/no)\n"
    "     b) What's tomorrow's MIT?\n"
    "   If today's task is unset, only ask (b).\n"
    "3) When the user replies, run:\n"
    "     python3 examples/mit/scripts/log.py --upsert --date <today> --task \"<today task>\" --completed <true|false>\n"
    "     python3 examples/mit/scripts/log.py --upsert --date <tomorrow> --task \"<tomorrow task>\" --completed false\n"
    "4) Confirm briefly. Do not skip silently."
)

if __name__ == "__main__":
    print(json.dumps({"component": "mit", "text": PROMPT}, ensure_ascii=False))
