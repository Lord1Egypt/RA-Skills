---
name: indexnow-setup
description: Set up IndexNow for any website to enable real-time URL submission to Bing, Yandex, Seznam, and other search engines. Use when the user needs to (1) configure IndexNow for a website, (2) generate and place an IndexNow key file, (3) create a URL submission script, (4) integrate IndexNow into a build/deploy pipeline, or (5) fix Google/Bing indexing delays by pushing URLs proactively.
---

# IndexNow Setup

## Overview

IndexNow is a protocol that lets websites notify search engines about new, updated, or deleted URLs in real time. Instead of waiting for crawlers, you push URLs directly to `api.indexnow.org`, and participating search engines (Bing, Yandex, Seznam, Naver) pick them up.

## Workflow

### Step 1: Generate and place the key file

Generate a random 32-character hex key:

```bash
node -e "console.log(require('crypto').randomBytes(16).toString('hex'))"
```

Place a `.txt` file named `<key>.txt` containing only the key string into the site's public root:

- **Next.js App Router** -- `public/<key>.txt`
- **Next.js Pages Router** -- `public/<key>.txt`
- **Plain static site** -- root directory (e.g., `dist/` or `public/`)
- **Vite / CRA** -- `public/<key>.txt`
- **Nuxt** -- `public/<key>.txt`

After deploy, the file must be accessible at `https://<domain>/<key>.txt` with a `200` response containing only the key string.

### Step 2: Create the submission script

Copy `scripts/submit-indexnow.mjs` from this skill into the project (e.g., `scripts/submit-indexnow.mjs`).

If the project already has `package.json`, add an npm script:

```json
"indexnow": "node scripts/submit-indexnow.mjs"
```

Or add a `site_url` and `key` pair inline:

```json
"indexnow": "node scripts/submit-indexnow.mjs https://example.com abcd1234..."
```

### Step 3: Ensure a sitemap exists

The script reads URLs from `/sitemap.xml`. Ensure the site generates a valid sitemap at that path. For Next.js App Router, this is typically `app/sitemap.ts`.

### Step 4: Submit URLs

Run after every deploy or content update:

```bash
npm run indexnow
```

The script:
1. Fetches `sitemap.xml` from the site
2. Extracts all `<loc>` URLs
3. POSTs them to `https://api.indexnow.org/IndexNow`

For non-Node projects, invoke the script directly:

```bash
node scripts/submit-indexnow.mjs https://example.com <key>
```

### Step 5: Verify

Use [Bing Webmaster Tools](https://www.bing.com/webmasters) to confirm URLs are being received. Check the URL inspection tool for submission history.

## Environment Variables

The script accepts arguments or environment variables:

| Priority | Source |
|----------|--------|
| 1st | CLI args: `node submit-indexnow.mjs <url> <key>` |
| 2nd | `SITE_URL` + `INDEXNOW_KEY` env vars |

## HTTP Response Codes

| Status | Meaning |
|--------|---------|
| 200 | URLs submitted successfully |
| 400 | Invalid request format |
| 403 | Key not found or invalid |
| 422 | URLs don't belong to the host |
| 429 | Rate limited (spam protection) |
