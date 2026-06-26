#!/usr/bin/env python3
"""mood.prompt — emits the cron-time chat prompt text.

The openclaw cron payload calls this in the agent prompt: it should ask the
user how they feel and, when they reply in the same session, run
`scripts/log.py --raw "<reply>"`.
"""

import json

PROMPT = (
    "It is time for the hourly mood check-in. In this same chat session:\n"
    "1) Ask the user briefly how they feel right now (in their preferred language).\n"
    "2) When they reply, immediately run:\n"
    "     python3 examples/mood/scripts/log.py --raw \"<their full reply>\"\n"
    "3) Confirm with a one-line ack (e.g. \"记下了 ✓\").\n"
    "Do not summarize previous moods. Do not skip silently."
)

if __name__ == "__main__":
    print(json.dumps({"component": "mood", "text": PROMPT}, ensure_ascii=False))
