# instagram-publish

> EN | [中文](README.zh-cn.md)

Publish images to Instagram from the command line via Meta's Graph API.

- **One-time setup** in the Meta / Instagram web UI (5 manual steps)
- **Repeatable publishing** through a single Python command
- All credentials live in `.env` — never committed

## Requirements

- Python 3.7+
- An Instagram **Creator** or **Business** account
- A Meta Developer App with Instagram API access (see [Setup](#setup))
- A publicly hosted image URL (S3, OSS, GitHub Raw, any CDN)

## Install

```bash
git clone <this repo> ~/.claude/skills/instagram-publish
cd ~/.claude/skills/instagram-publish
cp .env.example .env
```

## Setup

The first-time setup is human-only — it requires logins, email verification, and clicking through Meta's UI. Follow the **Part 1** section in [`SKILL.md`](./SKILL.md) for the full step-by-step. The short version:

1. Switch your Instagram account to **Creator**
2. Create a Meta Developer account at <https://developers.facebook.com/>
3. Create an App → use case **"Manage messaging & content on Instagram"** → **do not** connect a Business portfolio
4. Finish the App's basic settings (icon, privacy policy URL, data deletion URL, category) and click **Publish**
5. In **Use cases → Customize → API setup with Instagram login**, grant permissions, add your Instagram account, and click **Generate token**

Save the resulting token (starts with `IGAA...`) to `.env`.

## Configuration

`.env` (copy from `.env.example`):

```ini
IG_USERNAME=your_handle_here        # reference only — shown in success output
ACCESS_TOKEN=IGAAxxxxxxxxxxxx        # required
IG_USER_ID=2700xxxxxxxxxxxxxxxxx        # optional — auto-detected from /me if blank
```

> ⚠️ **Never commit `.env`.** The token authenticates posts on your behalf. Rotate it immediately if it leaks.

## Usage

```bash
# Publish an image
python3 scripts/publish.py \
  --image-url "https://example.com/photo.jpg" \
  --caption "Hello from the Graph API"

# Validate token and build a container, but skip the final publish
python3 scripts/publish.py \
  --image-url "https://example.com/photo.jpg" \
  --caption "Just checking" \
  --dry-run

# Use a .env file from another location
python3 scripts/publish.py --image-url "..." --env /path/to/.env

# Pin a specific Graph API version
python3 scripts/publish.py --image-url "..." --api-version v23.0
```

Successful output:

```
✓ Token valid — user: @xxxxxxxxxx (id: 2700xxxxxxxxxxxxxxx)
✓ Container created: xxxxxxxxxxxxx
✓ Published: xxxxxxxxxxxxx
  https://www.instagram.com/p/xxxxxxxxxxxxxxx
```

## Troubleshooting

| Error message | Cause | Fix |
|---|---|---|
| `Media download has failed` | Meta's servers cannot reach your `image_url` | Host the image on a public URL — S3, OSS, GitHub Raw, or any CDN. Open the URL in a logged-out browser to confirm. |
| `Unsupported post request` | Token is missing publish permissions | Back in the App dashboard → **Use cases → Customize → API setup with Instagram login** → re-generate the token with all permissions. |
| HTTP 400 / OAuthException 190 on `/me` | Token expired or malformed | Re-generate the token in the App dashboard and update `ACCESS_TOKEN` in `.env`. |
| `ACCESS_TOKEN not found` | `.env` missing or empty | `cp .env.example .env` and fill in `ACCESS_TOKEN`. |

For deeper setup details and the full list of Graph API parameters, see [`SKILL.md`](./SKILL.md).

## Files

```
instagram-publish/
├── SKILL.md            # full reference for AI agents
├── README.md           # this file
├── README.zh-cn.md     # 中文说明
├── .env.example        # credential template
├── .gitignore          # keeps .env out of git
└── scripts/
    └── publish.py      # the three-step publisher (stdlib only)
```

## Security notes

- `.gitignore` excludes `.env` — keep it that way
- Long-lived tokens still expire (default ~60 days); re-generate when they do
- If you ever leak a token, treat it as compromised: revoke it in the App dashboard and re-issue
