# lite-mode

OpenClaw skill for running on low-RAM machines (2-4 GB). Checks free memory before
heavy operations, caps conversation history at ~6,000 tokens, and throttles
browser/image tools when RAM is tight.

## Install

    openclaw skills install git:YOUR_GITHUB_USERNAME/openclaw-lite-mode

or, once published to ClawHub:

    openclaw skills install lite-mode

## Files

- `SKILL.md` — agent instructions
- `scripts/memcheck.js` — standalone memory check, no dependencies
- `openclaw-lite.json` — optional config snippet to lower baseline memory
