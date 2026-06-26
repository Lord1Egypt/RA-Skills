---
name: instagram-publish
description: Use when publishing images to Instagram via the Graph API from a Creator or Business account. Triggers when the user wants to automate Instagram posting, push an image with caption to their account, set up Instagram API access for the first time, or troubleshoot Instagram Graph API errors like "Media download has failed" or "Unsupported post request". Assumes one-time Meta App setup is complete and an Access Token is available.
---

# Instagram Publish

Publish images to Instagram through Meta's Graph API. Part 1 is one-time manual setup (browser clicks); Part 2 is the repeatable automated publish (this skill does it for you).

## When to use

- User wants to post an image to Instagram programmatically
- User has a public image URL and wants to attach a caption and publish
- User just registered a Meta App and needs the rest of the wiring done
- User is hitting "Media download has failed" or "Unsupported post request"

## When NOT to use

- Posting Reels, Stories, or Carousels (this skill handles single-image posts only)
- Local files (image must be a public URL — see error #1 below)
- Account is still a personal account (must be Creator or Business first)

## Quick Start (after Part 1 setup is done)

```bash
# 1. Put credentials in .env (one time)
cp .env.example .env
# edit .env with ACCESS_TOKEN (and optionally IG_USER_ID)

# 2. Publish
python3 scripts/publish.py \
  --image-url "https://example.com/photo.jpg" \
  --caption "Hello from Instagram API"
```

The script prints the new post ID on success. Done.

---

# Part 1: One-time manual setup (browser only)

These steps cannot be automated — they require human logins, email verification, and Meta's UI. Do them once, save the resulting `ACCESS_TOKEN`, and you never need to touch Meta's dashboard again unless permissions change.

## Step 1 — Switch Instagram to a Creator account

Visit <https://www.instagram.com/accounts/professional_account_settings/> and follow:

```
Settings
  ↓
Account Type
  ↓
Switch to Professional Account
  ↓
Creator
```

## Step 2 — Create a Meta Developer account

Visit <https://developers.facebook.com/> and sign in with your Facebook account, then:

```
Get Started
  ↓
Verify Email
  ↓
Accept Terms
```

## Step 3 — Create an App

Visit <https://developers.facebook.com/apps/>:

```
Create App
  ↓
Use cases: Manage messaging & content on Instagram
  ↓
Do NOT connect a Business portfolio
```

> ⚠️ Skipping the Business portfolio avoids the "insufficient developer permissions" error later.

## Step 4 — Finish App settings

In **App settings → Basic**:

- Upload an app icon
- Fill in Privacy Policy URL and Data Deletion URL
- Pick an app category
- (Optional) In **Use cases → Customize**, configure account linking at <https://accountscenter.instagram.com/connected_experiences/>
- Click **Publish** to make the app live

## Step 5 — Generate the Access Token

```
Use cases → Customize
  ↓
Left sidebar: API setup with Instagram login
  ↓
Add required messaging permissions
  ↓
Add account → authorize your Instagram account
  ↓
Generate token
  ↓
Check "I understand" → copy the token
```

The token starts with `IGAA...`. Save it to `.env` (next section).

## Credentials you should have after Part 1

| Field | Example | Lives in |
|---|---|---|
| `ACCESS_TOKEN` | `IGAAxxxxx...` | `.env` |
| `IG_USER_ID` | `2700xxxxxx` | `.env` (optional — script can auto-fetch) |
| `USERNAME` | `xxxxx` | reference only |

> ⚠️ Never commit `.env` to git. The token is the only thing that authenticates posts on your behalf.

---

# Part 2: Automated publishing (the skill does this)

The three Graph API calls below are bundled in `scripts/publish.py`. You run one command; the script runs all three.

```
[1] Validate token   →  GET /me?fields=id,username
       ↓
[2] Create container  →  POST /{ig_user_id}/media   (image_url + caption)
       ↓
[3] Publish           →  POST /{ig_user_id}/media_publish   (creation_id)
```

## Setting up `.env`

```bash
cp .env.example .env
```

`.env` contents:

```
ACCESS_TOKEN=IGAAxxxxxxxxxxxxxxxxxxxx
IG_USER_ID=2700xxxxxxxx        # optional — auto-detected if missing
```

The script reads `.env` from the skill directory. If you run it from elsewhere, pass `--env /path/to/.env`.

## Publishing an image

```bash
python3 scripts/publish.py \
  --image-url "https://example.com/photo.jpg" \
  --caption "Hello from Instagram API"
```

Optional flags:

| Flag | Default | Notes |
|---|---|---|
| `--image-url URL` | required | Must be publicly reachable by Meta's servers |
| `--caption TEXT` | empty | Instagram's caption, with hashtags and mentions |
| `--env PATH` | `./.env` | Path to a `.env` file |
| `--api-version` | `v24.0` | Graph API version |
| `--dry-run` | off | Validate token and build the container, but skip the final publish |

Successful output:

```
✓ Token valid — user: xxxxx (id: 2700xxxxxx)
✓ Container created: xxxxx
✓ Published: xxxxx
https://www.instagram.com/p/xxxxxxxxx
```

---

# Common errors

## "Media download has failed"

```json
{"error": {"message": "Media download has failed"}}
```

Meta's servers cannot reach your `image_url`. Fix:

- Host the image somewhere public: Alibaba Cloud OSS, AWS S3, GitHub Raw, any CDN
- Open the URL in a fresh browser *while logged out* — if you can't see it, Meta can't either
- Avoid `localhost`, `127.0.0.1`, and private network IPs

## "Unsupported post request"

```json
{"error": {"message": "Unsupported post request"}}
```

Almost always a token-permission issue. Fix:

- Back to **Use cases → Customize** in the App dashboard
- Confirm `instagram_content_publish` and `instagram_basic` are granted
- Re-generate the token and replace `ACCESS_TOKEN` in `.env`

## Token expired

Long-lived tokens still expire (default ~60 days). If `/me` returns an auth error, regenerate the token in the App dashboard and update `.env`.

---

# Files in this skill

```
instagram-publish/
├── SKILL.md            # this file
├── .env.example        # template for ACCESS_TOKEN and IG_USER_ID
├── .gitignore          # keeps .env out of git
└── scripts/
    └── publish.py      # the three-step publisher
```
