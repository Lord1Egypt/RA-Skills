---
name: htmlhoster-upload
description: >-
  Publish HTML pages, images, PDFs, ZIP (unzip hosting) and Markdown documents to
  htmlhoster.com and get back a public URL. Use this whenever an agent needs to
  host generated web pages, static assets, or rendered markdown and return a
  shareable link. Works for WorkBuddy, Claude Code, Codex, and any CLI agent.
---

# htmlhoster-upload

Host generated content on **htmlhoster.com** through its programmatic Agent upload
API and receive a public URL (`entryUrl`). No browser, no CAPTCHA, no API key
required (rate-limited per IP instead).

## When to use
- You produced an `.html` page (or a set of HTML + assets) and need a public link.
- You have images / PDFs to host.
- You have a `.zip` whose contents should be hosted (e.g. a built site).
- You have Markdown (`.md` + assets, or a zip package) to render into HTML and host.

## Before you upload: scan for sensitive info
htmlhoster is a **public** site — every uploaded file is reachable by anyone who
has the URL, with no authentication. Treat every upload as publishing to the
world.

**Step 1 — the agent reviews the content itself (mandatory, do not skip).**
Before you call the upload, you (the agent) must actually *read* the file(s) you
are about to publish and eyeball them for sensitive material. Do **not** rely on
the script's scan alone — the scan is mechanical and will miss things like:
- credentials in unusual or obfuscated forms (split strings, base64, env lookups)
- personal data that isn't a literal "key" pattern (emails, phone numbers,
  addresses, internal hostnames, real names of third parties)
- anything you generated that you would not paste into a public chat
If you spot something sensitive, stop and ask the user before publishing.

**Step 2 — the script's automatic scan (defence in depth).**
The bundled `scripts/upload.py` also runs a secret scan **before every upload**
and aborts (non-zero exit) if it detects a likely secret. If it aborts, do **not**
blindly re-run with `--no-check` to push the content through — review the flagged
file with the user first. Only pass `--no-check` when the user has explicitly
confirmed the content is safe to publish. Even with `--no-check`, never upload
real credentials or personal data: the final responsibility is yours, not the
script's.

## Endpoint
- Base: `https://api.htmlhoster.com` (override with env `HTMLHOSTER_API_BASE`)
- `POST /agent/upload`    — HTML / images / PDF / ZIP
- `POST /agent/markdown`  — Markdown rendering & hosting

- `DELETE /api/uploads/{uploadId}` — remove a page you uploaded (see *Deleting*)

Both upload endpoints return JSON containing `entryUrl` (the public page), `files`
(per-file URLs) and `deleteToken` (see *Deleting* below).

## Supported formats
| Mode | Endpoint | Notes |
|------|----------|-------|
| HTML | `/agent/upload` | HTML gets automatic `nofollow` + floating report widget injected. |
| Images (png/jpg/gif/webp/svg/...) | `/agent/upload` | Served as-is. |
| PDF | `/agent/upload` | Served as-is. |
| ZIP (unzip) | `/agent/upload` with `--unzip` | Each entry hosted; inner `index.html` becomes the entry URL. |
| Markdown | `/agent/markdown` | Rendered to HTML (GFM + task lists + KaTeX/Mermaid/CDN), then hosted. |

## Rate limit
Single client IP: **50 uploads per day** (both endpoints share the quota). Exceeding
returns HTTP `429`.

On `429`: stop and tell the user the daily quota is exhausted. Do **not** retry in a
loop, and do **not** attempt to work around the limit. Suggest the user upload
manually in the browser at https://htmlhoster.com — the web tools have no daily
quota — or wait for the quota to reset. A login / API-key system is planned to
lift the quota for identified users.

## Acceptable use
Upload only content you created or are authorised to publish. Prohibited: phishing and
brand-impersonation pages, credential-harvesting forms, malware, crypto-mining or other
hidden scripts, spam / SEO link farms, and anything illegal. Pages are served from a
shared public domain and may be removed without notice; abusive clients may be blocked.
Never upload secrets, credentials, or personal data — every uploaded file is reachable
by anyone holding the URL. If you are unsure whether content is allowed, ask the user
before uploading.

## How to upload (recommended: the bundled script)
This skill ships `scripts/upload.py` — **pure standard library, zero dependencies**.

```bash
# HTML / images / PDF, optionally unzip a zip
python scripts/upload.py --mode html --file index.html --file logo.png --unzip

# Markdown via zip package (contains .md + assets)
python scripts/upload.py --mode markdown --package doc.zip

# Markdown via single .md + assets
python scripts/upload.py --mode markdown --file doc.md --asset img1.png --asset img2.png
```

Environment:
- `HTMLHOSTER_API_BASE` (optional): API base, default `https://api.htmlhoster.com`.
- `HTMLHOSTER_UPLOAD_EXTRA_HEADERS` (optional): extra request headers, `k1:v1;k2:v2`.

On success it prints the JSON (grab `entryUrl`). Exit code `0` on success, non-zero on
failure (the error body is printed to stderr).

## Deleting an upload
Every successful upload returns a `deleteToken`. It is scoped to that one `uploadId`
and is the **only** way for you to remove the page. The token is a random value stored
server-side on htmlhoster (under a non-public prefix, not derivable from the id) — so
keep it safe. You cannot re-derive or look it up later.

```bash
python scripts/upload.py --mode delete --id A1B2C3D4 --token <deleteToken>
```

Or directly: `DELETE /api/uploads/{uploadId}` with header `X-Delete-Token: <token>`.

Guidance for agents:
- Report `entryUrl` to the user, and **keep `deleteToken` in your working notes** for
  the rest of the session so a mistaken upload can be undone.
- If the user asks to remove something you uploaded earlier in the session, use the
  token you saved. If you no longer have it, say so plainly — you cannot recover it,
  but the site owner can still take the page down if necessary.
- Deletion can take a while (object listing + CDN purge); the script waits up to 180s.
  If it times out, the deletion has usually still succeeded server-side — verify by
  fetching `entryUrl` (a deleted page returns `404`) instead of retrying blindly.
- Once a page is deleted its token is destroyed, so re-running delete on the same id
  returns `401`, not `200`. Treat `401` after a confirmed delete as "already gone".
- Never publish the `deleteToken` alongside the public link (e.g. in a shared doc or
  chat message) — anyone holding it can delete the page.

## Porting to other agents (Claude Code / Codex)
The script is self-contained. To use it elsewhere:
1. Copy `scripts/upload.py` to the agent's working directory (or anywhere on PATH).
2. Run it with the same CLI shown above.
3. No API key needed; respect the 50/day per-IP limit.

A full human/agent-readable doc page lives at `https://htmlhoster.com/agent/`, and the
raw script is downloadable at `https://htmlhoster.com/agent/upload.py`.
