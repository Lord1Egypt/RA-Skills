# openclaw-skill-podcast-manager

Podcast management skill for OpenClaw.

## Contents
- `SKILL.md` — skill instructions and behavior
- `scripts/feed_probe.py` — lightweight RSS/Atom feed probe utility for validation
- `SECURITY_REVIEW.md` — DD-style security/privacy checklist and verdict

## Quick check
```bash
python3 scripts/feed_probe.py https://feeds.simplecast.com/54nAGcIl
```

Expected output: compact JSON with feed title, link, and recent episode metadata.
