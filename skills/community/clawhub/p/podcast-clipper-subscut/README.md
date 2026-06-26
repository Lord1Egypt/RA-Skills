# Podcast Clipper Skill

Standalone OpenClaw/ClawHub skill package for Subscut's podcast clipping API.

## Repo Scope

This repo contains only the marketplace skill package:

- `SKILL.md`
- `package.json`
- `scripts/generate-podcast-clips.js`
- `examples/`

The Subscut app and API live in the separate `subscut_web` repo.

## Usage

```bash
export SUBSCUT_API_KEY="subscut_your_api_key"
export SUBSCUT_API_BASE_URL="https://subscut.com"

npm run generate-podcast-clips -- \
  --video-url "https://example.com/podcast.mp4" \
  --max-clips 5 \
  --clip-style viral \
  --captions true
```

## Publish

```bash
clawhub login
clawhub whoami
clawhub skill publish .
```

## Notes

- Keep this repo versioned independently from the app repo.
- Treat the API contract as external and stable for skill consumers.
- Publish a new skill version whenever the runtime behavior or docs change.
