# htmlhoster-upload

Publish HTML pages, images, PDFs, ZIP archives and Markdown to
[htmlhoster.com](https://htmlhoster.com) and get back a public URL — from the
command line, or straight from an AI agent.

No browser. No CAPTCHA. No API key. Just a pure-standard-library Python script
(and an optional agent-skill wrapper) that works with any CLI agent:
Claude Code, Codex, WorkBuddy, or plain shell.

> **Docs:** full human/agent-readable API reference lives at
> [https://htmlhoster.com/agent/](https://htmlhoster.com/agent/).

---

## Why

- **Zero dependencies** — `upload.py` uses only the Python standard library.
- **Agent-friendly** — ships as a drop-in skill for Claude Code / Codex /
  WorkBuddy, plus a standalone CLI.
- **Everything in one call** — upload files, get `entryUrl` (public link),
  `files` (per-file URLs) and `deleteToken` (for later removal).
- **Markdown rendering** — GFM, task lists, KaTeX / Mermaid / CDN content is
  rendered to HTML before hosting.
- **ZIP unzip hosting** — upload a built site as a zip and each entry gets
  hosted; an inner `index.html` becomes the entry URL.
- **You keep control** — every upload returns a scoped `deleteToken` so the
  page can be removed later.

## Quick start

```bash
python scripts/upload.py --mode html --file index.html
```

On success it prints the API JSON — grab `entryUrl`:

```json
{
  "entryUrl": "https://htmlhoster.com/p/8F3K9Q2A/index.html",
  "files": { "index.html": "https://htmlhoster.com/p/8F3K9Q2A/index.html" },
  "deleteToken": "abc123..."
}
```

## Install as an agent skill

Copy `SKILL.md` to your agent's skill directory (e.g.
`~/.claude/skills/htmlhoster-upload/` or `~/.codex/skills/htmlhoster-upload/`)
and `scripts/upload.py` next to it under `scripts/`. The skill instructs the
agent when and how to use the API. Alternatively, just copy `scripts/upload.py`
anywhere on your `PATH` and drive it from the CLI.

## Usage

### HTML / images / PDF

```bash
# Single file
python scripts/upload.py --mode html --file index.html

# Multiple files with a custom relative path
python scripts/upload.py --mode html --file index.html --file logo.png --path . --path assets/logo.png

# Unzip a zip and host its contents
python scripts/upload.py --mode html --file dist.zip --unzip
```

HTML gets a `nofollow` + floating report widget injected automatically;
images and PDFs are served as-is.

### Markdown

```bash
# Zip package mode (contains .md + assets)
python scripts/upload.py --mode markdown --package doc.zip

# Single .md + assets
python scripts/upload.py --mode markdown --file doc.md --asset img1.png --asset img2.png
```

### Delete an upload

```bash
python scripts/upload.py --mode delete --id 8F3K9Q2A --token <deleteToken>
```

The `deleteToken` from the upload response is the **only** way to remove that
page — keep it somewhere safe. It cannot be re-derived or looked up later.

## Environment

| Variable | Description | Default |
|----------|-------------|---------|
| `HTMLHOSTER_API_BASE` | API base URL | `https://api.htmlhoster.com` |
| `HTMLHOSTER_UPLOAD_EXTRA_HEADERS` | Extra request headers, `k1:v1;k2:v2` | *(none)* |

## API endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/agent/upload` | POST | HTML / images / PDF / ZIP (unzip) |
| `/agent/markdown` | POST | Markdown rendering & hosting |
| `/api/uploads/{uploadId}` | DELETE | Remove a page (`X-Delete-Token` header) |

All endpoints take `multipart/form-data`. Successful uploads return JSON with
`entryUrl`, `files` and `deleteToken`. Exit code `0` on success, non-zero on
failure (error body goes to stderr).

## Rate limits & acceptable use

- **50 uploads per day per IP** (both upload endpoints share the quota).
  Exceeding returns HTTP `429` — stop, don't retry in a loop, and don't try to
  work around it. The interactive web tools at https://htmlhoster.com have no
  daily quota.
- Upload only content you created or are authorised to publish. Prohibited:
  phishing and brand-impersonation pages, credential-harvesting forms,
  malware, crypto-mining or hidden scripts, spam / SEO link farms, anything
  illegal.
- Pages are served from a shared public domain and may be removed without
  notice; abusive clients may be blocked. **Never upload secrets or personal
  data** — anyone holding the URL can access every uploaded file.

## Safety: pre-upload secret scan

Because htmlhoster is a **public** site, `upload.py` scans every file for
likely secrets / credentials **before uploading** and aborts (exit non-zero) if
it finds one — private keys, API keys (AWS / GCP / GitHub / OpenAI / Cloudflare /
Stripe …), `.env` / SSH keys, database connection strings with embedded
passwords, and other people's personal data. Matched values are never printed,
only the file, the kind of match, and a line number.

The scan is a guardrail, **not** a substitute for your own judgement. Before
uploading, an agent should read the file(s) it is about to publish and eyeball
them for sensitive material the scanner may miss — obfuscated credentials,
personal data (emails, phone numbers, internal hostnames), or anything you
wouldn't paste into a public chat. If the scan aborts, review the flagged file
before publishing. Pass `--no-check` only when you are certain the content is
safe. Never upload real credentials or personal data, even with `--no-check`.

## License

[MIT](./LICENSE)
