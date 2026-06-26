---
name: instagram-posting-pipeline
description: End-to-end Instagram automation pipeline using the official Meta Graph API. Generates promotional creatives and publishes directly to Instagram Business accounts without third-party automation tools. Completely free — no Zapier, no Make, no paid schedulers. Requires user-provided credentials (no shared app or tokens). Triggers on: "post to Instagram", "autopost Instagram", "auto Instagram poster free", "automate Instagram posts", "schedule Instagram post free", "post to IG automatically", "create and post Instagram promo", "free Instagram automation", "Instagram bulk poster", "auto post to Instagram from website", "AI Instagram poster", "post promo image to Instagram", "generate and post course promo", "automate Instagram for gym/salon/course/restaurant/shop". Works for any business: gyms, salons, courses, restaurants, e-commerce, local shops, agencies. Just provide business name and details, or paste your website URL and AI auto-extracts your business info to generate the post.

env:
  IG_ACCESS_TOKEN: "Required — Page Access Token with instagram_content_publish and pages_read_engagement permissions"
  IG_BUSINESS_ACCOUNT_ID: "Required — Instagram Business Account ID (numeric)"
  CLOUDINARY_CLOUD_NAME: "Required — Cloud name from your Cloudinary dashboard"
  CLOUDINARY_UPLOAD_PRESET: "Required — Unsigned upload preset from Cloudinary dashboard"
  CLOUDINARY_FOLDER: "Optional — Target folder name for uploads"
---

# Instagram Posting Pipeline

End-to-end Instagram automation pipeline. Generate professional promotional images and publish them automatically to any Instagram Business account — no third-party automation tools needed.

## Skill Scope

- Generate promotional images (text + branding overlays, 1080×1350)
- Upload images to Cloudinary for public hosting
- Publish to Instagram via Meta Graph API
- Optional: extract business info from a public website URL

**Not in scope:** scraping private/internal networks, storing credentials externally, third-party data sharing.

## Install Model

**Instruction-driven skill** — all scripts are bundled in the package. No external binaries, installers, or runtime dependencies beyond Python 3.8+ and Pillow. Place the `scripts/` folder alongside the skill and configure env vars to use.

## Pipeline Flow

```
Business info (name, details, website URL)
    → scrape_business.py (optional — auto-extract from website)
    → generate_course_promo.py
    → upload_cloudinary.py
    → post_to_instagram.py
    → Instagram post URL
```

## Data Extraction (Optional)

`scrape_business.py` fetches a **user-provided public URL** to extract business info — name, tagline, services, contact — for auto-generating content.

**What it does:**
- Makes an outbound HTTP(S) request to the provided URL
- Parses the HTML response using Python's built-in `html.parser`
- Extracts title, meta description, H1 tags, paragraphs, and contact patterns
- Returns structured data to populate the image generation prompt
- May extract email and phone if publicly available

**What it does NOT do:**
- Does not follow redirects to third-party domains (all 3xx responses are blocked)
- Does not access internal/private networks
- Does not store or retransmit scraped data

> Do not provide internal/private URLs (e.g. `localhost`, `192.168.x.x`, `10.x.x.x`). SSRF protections enforced: DNS resolution + private-IP blocking (via `ipaddress` module), SSL certificate verification, scheme/hostname allowlist, and **all redirects are explicitly blocked** (no following 3xx responses to any destination).

## Environment Setup

Before using, set these environment variables:

```bash
# Meta Graph API (required)
export IG_ACCESS_TOKEN="your_page_access_token"
export IG_BUSINESS_ACCOUNT_ID="your_ig_business_account_id"
export IG_DEFAULT_CAPTION="Your default caption"

# Cloudinary (required — create your own free account)
# No default credentials are used — you must set up your own
export CLOUDINARY_CLOUD_NAME="your_cloud_name"
export CLOUDINARY_UPLOAD_PRESET="your_unsigned_preset"
export CLOUDINARY_FOLDER="mybusiness"

# Image output (optional)
export IG_PIPELINE_OUTPUT_DIR="./output"
```

## Security & Credentials

**Your credentials stay yours.**

- Tokens are **user-provided at runtime** (environment variables)
- Tokens are **never stored externally** or sent to any third-party service
- Tokens are **used only during execution** and never persisted
- SSL/TLS verification is enforced on all outbound requests
- Use least-privilege and test accounts during evaluation
- Never log tokens — only non-sensitive metadata is logged

**Cloudinary hardening recommendation:**
Prefer signed upload presets, or restrict unsigned presets by folder/origin in your Cloudinary dashboard.

### Getting Credentials

**Access Token:**
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your Facebook App (must have `instagram_content_publish` and `pages_read_engagement` permissions)
3. Generate token for your Page
4. Grant `pages_read_engagement`, `instagram_content_publish`

**IG Business Account ID:**
- Found in Meta Business Suite → Instagram settings → Account ID

## Step-by-Step Usage

### Step 1: Generate Image

```python
from generate_course_promo import generate_course_promo

path = generate_course_promo(
    course_name="Diploma in Artificial Intelligence",
    institution="CADDESK Centre",
    duration="90 Weeks",
    bullets=[
        "Machine Learning & Data Science",
        "Building Intelligent Systems",
        "Algorithm Development",
        "Real-World AI Projects",
    ],
    hook_lines=["Your Future in AI", "Starts Here."],
    cta_text="Ready to shape the future with AI?",
    handle="@caddeskcentre",
    output_filename="course_promo.png"
)
```

CLI:
```bash
python scripts/generate_course_promo.py
```

### Step 2: Upload to Cloudinary

```bash
python scripts/upload_cloudinary.py <image_path> [folder]
```

Returns a public URL like `https://res.cloudinary.com/image/upload/xyz.png`

### Step 3: Post to Instagram

```bash
python scripts/post_to_instagram.py <image_url> <caption>
```

Or programmatically:

```python
from post_to_instagram import post_to_instagram

success, post_id, ig_url = post_to_instagram(
    image_url="https://res.cloudinary.com/image/upload/xyz.png",
    caption="Your caption with #hashtags"
)
```

## Caption Structure

```
[HOOK - bold claim or question, 1-2 lines]
[VALUE - what they'll learn/achieve]
[CTA - link in bio / DM to enroll / visit website]
[8-15 hashtags - mix of broad + niche]
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| `401 Invalid OAuth` | Token expired — regenerate at Graph API Explorer |
| `IG token format error` | Use Page Access Token, not IG-only token |
| `image_url required` | Image not publicly accessible — upload to Cloudinary first |
| `403 Forbidden` | App not in Live mode or `instagram_content_publish` permission not approved |
| `Cloudinary 400` | Image too large (>10MB), unsupported format, or credentials not configured |
| `IG account not found` | Account not set as Business/Creator mode in Meta |
| Scrape returns None | Website uses JS rendering — provide details manually |

## Multiple Accounts

To switch between IG accounts, update environment variables before each post:

```bash
export IG_ACCESS_TOKEN="token_for_account_a"
export IG_BUSINESS_ACCOUNT_ID="ig_id_account_a"
python scripts/post_to_instagram.py <url> <caption>
```
