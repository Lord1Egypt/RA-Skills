#!/usr/bin/env python3
"""reminder.prompt — cron-time chat prompt text."""

import json

PROMPT = (
    "Morning reminder digest time. In this same chat session:\n"
    "1) Run: python3 examples/reminder/scripts/digest.py\n"
    "2) Forward the stdout markdown verbatim to the user.\n"
    "3) Do not add commentary unless the user asks."
)

if __name__ == "__main__":
    print(json.dumps({"component": "reminder", "text": PROMPT}, ensure_ascii=False))
