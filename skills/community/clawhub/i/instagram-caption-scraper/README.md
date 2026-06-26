# 📸 Instagram Caption Scraper — OpenClaw Skill

Extracts captions and metadata from public Instagram posts and reels using Instaloader.

## Files
```
instagram-caption/
├── SKILL.md               ← OpenClaw skill definition
├── instagram_scraper.py   ← Python scraper script
└── README.md              ← This file
```

## Installation

### Step 1 — Copy skill to OpenClaw skills directory
```bash
cp -r instagram-caption ~/.openclaw/skills/
```

### Step 2 — Install Python dependency
```bash
pip3 install instaloader==4.14.1
```

### Step 3 — Restart OpenClaw gateway
```bash
pm2 restart openclaw
# or
systemctl restart openclaw
```

### Step 4 — Verify in OpenClaw UI
Go to **Settings → Skills** and confirm `instagram-caption` appears in the list.

## Usage
Just paste an Instagram URL in the OpenClaw chat:
> "Get the caption from https://www.instagram.com/p/DRiFkfoiIuC/"

## Notes
- Only works on **public** posts and reels
- Does not require Chrome or any browser
- Python 3.8+ compatible
- If you get 403 errors, add login credentials to the script (see scraper comments)

## Requirements
- Python 3.8+
- instaloader==4.14.1
