---
name: md-web
version: 1.1.0
description: Render a markdown file as a beautiful, shareable web page in the browser instead of dumping long text in chat. Use when the user wants to preview, view, share, export, or publish markdown as a web page, wants a shareable link to content, or when you need to present long markdown without flooding the conversation. Uploads the file to the user's own S3-compatible storage bucket; the rendered page is publicly accessible via the returned URL.
tags: [markdown, web, docsify, s3, preview, share, publish, export]
homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/md-web

metadata:
  clawdbot:
    emoji: "🌐"
    requires:
      bins: ["node"]
    files:
      - upload.js
      - "docsify-server/**"
---

# MD Web - Markdown to Web Page

Upload raw `.md` files to an S3-compatible storage bucket, where a pre-deployed Docsify server automatically renders them as web pages. This avoids sending long text in the conversation.

## When to use this skill

**Uploaded content is publicly accessible.** Only use this skill when the user explicitly requests it:

- User wants to **show or preview content as a web page** in a browser
- User wants to **generate, export, or publish** content as a web page
- User wants a **shareable link** to content
- User wants output **delivered as a web page** rather than as long text in chat
- User wants to **compile or organize content and present it as a web page**
- User invokes this skill by name (e.g., `/md-web`)

## How to use this skill

### Step 1: Check configuration

Check if `~/.md-web/config.json` exists (cross-platform: use the user's home directory). If it does NOT exist or has empty fields, follow the **Configuration** section below first.

### Step 2: Prepare the markdown file

Either use an existing `.md` file, or write the content to a temporary file. Choose the temp path based on the current platform (e.g., `/tmp/` on Linux/macOS, system temp dir on Windows). Use whichever path works in the current shell environment.

### Step 3: Upload via upload.js

```bash
node {SKILL_DIR}/upload.js <local-file> <remote-key>
```

- `{SKILL_DIR}`: the base directory of this skill (shown at the top when skill is loaded)
- `<remote-key>`: a descriptive lowercase name with hyphens (e.g., `api-docs.md`, `project-guide.md`). A timestamp is prepended automatically to avoid filename collisions.
- On first run, the script auto-detects and deploys Docsify server files. No manual setup needed.

### Step 4: Return the result

- **On success**: the script prints the URL. Reply with only the filename and clickable link. Do NOT paste the markdown content into the chat.
- **On failure** (non-zero exit code): report the error to the user, then fall back to sending the markdown content as text directly in the chat.

Example success output:
> `api-docs` - https://example.r2.dev/index.html#/md-web/20260305-091500-api-docs

## Configuration

This only needs to happen once. On subsequent runs, `config.json` already exists.

1. Tell the user this skill needs an S3-compatible storage bucket with public access. Point them to `{SKILL_DIR}/README.md` for detailed setup instructions (Cloudflare R2 / AWS S3 / other S3-compatible services).
2. Ask the user to provide these 5 required fields:
   - **access_key**: API access key ID
   - **secret_key**: API secret access key
   - **endpoint**: S3 endpoint hostname, without `https://` (e.g., `ACCOUNT_ID.r2.cloudflarestorage.com`)
   - **bucket**: bucket name
   - **public_url**: public access URL. If the user has a custom domain bound to the bucket, use that (e.g., `https://docs.example.com`); otherwise use the default R2.dev URL (e.g., `https://pub-XXXX.r2.dev`). **Recommend custom domain** for production use — R2.dev URLs have rate limits.
3. Ask about optional settings:
   - **region**: S3 region. Use `auto` for Cloudflare R2, or the actual region for AWS S3 (e.g., `us-east-1`). Default is `auto`.
   - **expire_days**: how many days before uploaded markdown files are automatically deleted from the bucket. Default is `30`. Set to `0` to keep files forever. The script sets an S3 lifecycle rule **scoped to the `md-web/` key prefix**, so only this skill's own uploads are affected — Docsify server files and any other objects in the bucket are never touched. **Note**: this requires the API token to have **Admin Read & Write** permission (not just Object Read & Write). If the token lacks permission, the script will warn but still upload normally — the user can set the lifecycle rule manually in the Cloudflare Dashboard instead.
4. Write the config to `~/.md-web/config.json` (create the `~/.md-web/` directory if it doesn't exist). Use the user's home directory (`$HOME` on Unix, `%USERPROFILE%` on Windows):

```json
{
  "access_key": "...",
  "secret_key": "...",
  "endpoint": "...",
  "bucket": "...",
  "region": "auto",
  "public_url": "...",
  "expire_days": 30
}
```

5. Then proceed with the upload.

## Important notes

- Do NOT generate HTML. Just upload the raw `.md` file — Docsify handles rendering.
- Do NOT send markdown content to the chat unless upload fails.
- `upload.js` uses only Node.js built-in modules (zero dependencies).
- All Docsify assets (JS/CSS) are bundled locally — no external CDN dependency at runtime.

## External endpoints

This skill connects only to the S3 endpoint configured by the user in `config.json`. No data is sent to the skill author or any third-party service.

| Endpoint | Purpose | Data sent |
|----------|---------|-----------|
| User's S3 endpoint (`config.json → endpoint`) | Upload .md files and Docsify server assets | File content, S3 auth headers |

## Security & privacy

- **Anything you upload becomes publicly accessible** at the returned URL — never upload secrets, credentials, PII, or other sensitive content.
- Credentials (`access_key`, `secret_key`) are stored **in plaintext** in `~/.md-web/config.json` (outside the skill directory, safe from upgrades) and only sent to the user's own S3 endpoint for authentication. Protect this file — don't commit it or share it.
- **Use a dedicated bucket.** Uploads live under the `md-web/` key prefix and the auto-expiry rule is scoped to it, but `expire_days: 0` clears the bucket's lifecycle config entirely — a dedicated bucket guarantees the skill never affects unrelated objects or lifecycle rules you set yourself.
- No telemetry, analytics, or data collection by the skill itself.
- `upload.js` uses only Node.js built-in modules — no third-party dependencies.

By using this skill, markdown content is uploaded to **your own** S3-compatible storage bucket and made publicly accessible. No data is sent to the skill author or any third-party service. Only install if you trust the storage provider you configure.
