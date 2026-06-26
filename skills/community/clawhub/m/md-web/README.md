# MD Web

Turn any content into a web page with a shareable URL. Uploads Markdown to an S3-compatible storage bucket, rendered by Docsify.

[中文文档](README.zh.md)

## Installation

Pick whichever matches your agent / CLI:

```bash
# ClawHub / OpenClaw
clawhub install md-web

# skills.sh (Vercel skills CLI — Claude Code, Cursor, and more)
npx skills add rockbenben/aishort-skills
```

Or install manually — clone this repo into your agent's skills directory (e.g. `~/.claude/skills/md-web`).

## Quick Start

1. Install the skill (see above)
2. On first use, the AI will guide you through bucket configuration
3. After that, tell the AI "share as a link" whenever you want to publish content as a web page

## Bucket Setup

This skill requires an **S3-compatible object storage bucket** with public access enabled. The example below uses Cloudflare R2.

### Step 1: Create a Bucket

1. Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Select **R2 Object Storage** from the left menu
3. Click **Create bucket**, enter a name (e.g., `md-web`), use the default region
4. After creation, go to the bucket's **Settings** page
5. Find **Public Access**, click **Allow Access**, enable the **R2.dev subdomain**
6. Once enabled, a public URL will appear: `https://pub-XXXX.r2.dev`
   → This is the **public_url** in the config

### Step 2: Create an API Token

1. On the R2 page, click **Manage R2 API Tokens**
2. Click **Create API Token**
3. Set permissions to **Object Read & Write** (or **Admin Read & Write** if you want automatic file expiry — see `expire_days` below)
4. Optionally restrict scope to the specific bucket
5. After creation, you'll see:
   - **Access Key ID** → **access_key** in the config
   - **Secret Access Key** → **secret_key** in the config
   - **S3 Endpoint** in the format `https://ACCOUNT_ID.r2.cloudflarestorage.com`
     → Remove `https://`, the rest is the **endpoint**

### Step 3: Tell the AI

On first use, the AI will ask for these fields:

| Field       | Required | Description                                                               | Example                               |
| ----------- | -------- | ------------------------------------------------------------------------- | ------------------------------------- |
| access_key  | Yes      | API access key ID                                                         | `a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4`    |
| secret_key  | Yes      | API secret access key                                                     | `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6...` |
| endpoint    | Yes      | S3 endpoint (without `https://`)                                          | `ACCOUNT_ID.r2.cloudflarestorage.com` |
| bucket      | Yes      | Bucket name                                                               | `md-web`                              |
| public_url  | Yes      | Public access URL (custom domain recommended)                             | `https://pub-XXXX.r2.dev`             |
| region      | No       | S3 region (`auto` for R2, actual region for AWS S3, e.g., `us-east-1`)   | `auto`                                |
| expire_days | No       | Days before uploaded files auto-delete (default `30`, `0` = keep forever) | `30`                                  |

> **Tip**: R2.dev URLs have rate limits. For production use, bind a custom domain to your bucket and use that as `public_url`.

The AI will automatically save these to `~/.md-web/config.json`. No repeat setup needed.

## Usage

Uploaded content is **publicly accessible** via the generated URL. The skill only runs when you explicitly ask for it:

```text
show as a web page
publish this online
/md-web path/to/file.md
share as a link
```

The AI returns a link — click to view the rendered document in your browser.

> **Note**: Markdown image references (e.g., `![](image.png)`) are not uploaded — only the `.md` file itself. Use absolute image URLs if your document includes images.

## Security

- **Anything you upload is publicly accessible** at the returned URL — never upload secrets, API keys, PII, or other sensitive content.
- Your S3 credentials are stored **in plaintext** in `~/.md-web/config.json`. Keep this file private — don't commit it or share it.
- **Use a dedicated bucket.** Uploads are namespaced under the `md-web/` key prefix and the auto-expiry rule is scoped to it, so the skill only ever expires its own files — a dedicated bucket further guarantees it never touches your other objects or lifecycle rules.

## File Structure

```yaml
md-web/                     # Skill directory (managed by ClawHub, may be replaced on upgrade)
├── SKILL.md              # AI instruction file
├── upload.js             # Upload script (pure Node.js, zero dependencies)
├── README.md             # This document
├── README.zh.md          # Chinese documentation
└── docsify-server/       # Docsify server files (auto-deployed on first upload)
    ├── index.html
    ├── README.md
    ├── .nojekyll
    └── assets/           # JS/CSS assets (bundled locally, no CDN dependency)
        ├── docsify.min.js
        ├── vue.css
        └── ...

~/.md-web/                  # User data directory (preserved across upgrades)
├── config.json           # Bucket credentials & settings (created on first use)
└── .deployed             # Deploy fingerprint (tracks server deployment state)
```

## Other S3-Compatible Services

Besides Cloudflare R2, this skill works with any S3-compatible object storage:

- **AWS S3**: endpoint is `s3.REGION.amazonaws.com`
- **Backblaze B2**: endpoint is `s3.REGION.backblazeb2.com`
- **DigitalOcean Spaces**: endpoint is `REGION.digitaloceanspaces.com`
- **Wasabi**: endpoint is `s3.REGION.wasabisys.com`
- **Tencent Cloud COS**: endpoint is `cos.REGION.myqcloud.com`

Any service that provides an S3-compatible API and a public access URL will work.
