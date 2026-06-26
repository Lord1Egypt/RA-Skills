# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## X/Twitter Posting
- Script: `scripts/social-poster.mjs --platform x --file /tmp/post.txt`
- Profile: `~/.openclaw/browser/openclaw/user-data/Default` (Playwright persistent context)
- Login: `node scripts/social-poster.mjs --platform x --login` (manual login, 120s window)
- Thread replies: use Playwright script to navigate to tweet URL → click tweetTextarea_0 → paste → Cmd+Enter
- Account: @Rockwood_Ray (clawlite)

## Secrets (no plaintext)

- Tavily API key is stored in **macOS Keychain** item:
  - account: `openclaw`
  - service: `OPENCLAW_TAVILY_API_KEY`
- Retrieve when needed:
  - `security find-generic-password -a openclaw -s OPENCLAW_TAVILY_API_KEY -w`

- Supabase Management token is stored in **macOS Keychain** item:
  - account: `openclaw`
  - service: `SUPABASE_MANAGEMENT_TOKEN`
- Retrieve when needed:
  - `security find-generic-password -a openclaw -s SUPABASE_MANAGEMENT_TOKEN -w`

- Rule: never store API keys directly in markdown or git-tracked files.

## Examples

```markdown
### X / Twitter
- Account: @Rockwood_Ray (clawlite official)
- Can login via browser and post/reply
- Rule: 发帖时可以 @ mention @Rockwood_Ray（增加曝光）。不要 @ mention @Rockwood_XRay。

### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
