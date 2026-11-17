# MD Web

> Turn any content into a web page with a shareable URL. Uploads Markdown to an S3-compatible storage bucket, rendered by Docsify.

[中文文档](README.zh.md)

## Installation

Pick whichever matches your agent / CLI:

```bash
# ClawHub / OpenClaw
clawhub install md-web

# skills.sh (Vercel skills CLI — Claude Code, Cursor, and more)
npx skills@1.7.2 add rockbenben/aishort-skills
```

Pin the CLI version as shown. An unpinned `npx skills add …` resolves whatever the
registry serves at install time, so the installer you review is not the installer that
runs.

That pins the **installer**, not the **content**. The fetched skill is still whatever the
repository serves at install time; what pins the content is the skill's own released
version, so install a release you have read and re-run the install after an upgrade —
the version is in `skills/md-web/SKILL.md`. Reviewing the installer does not review the
skill: read the skill before you install it.

Or install manually — clone this repo and copy (or symlink) the `skills/md-web/` folder
into the skills directory your agent reads from. A single folder named `md-web` is all
it needs; use whichever path your agent documents.

## Quick Start

1. Install the skill (see above)
2. On first use, the AI will guide you through bucket configuration
3. The AI then provisions the viewer once — a separate step that writes the page shell
   and its assets to your bucket, and again after an upgrade of the viewer. This
   requires authorization covering the shared files at the bucket root.
4. After that, ask the AI to publish that document to your public bucket

## What this touches

The complete list of what this skill does. Nothing outside it happens.

- **Publishing one document** writes **exactly one object** — `md-web/<timestamp>-<slug>-<suffix>.md`
  — under the `md-web/` prefix of your bucket. It writes nothing else and deletes nothing.
- **Provisioning the viewer** (`--setup --confirm-shared-writes`) is a **separate command**, never a side effect of
  publishing. It uploads `assets/<bundle-hash>/`, updates root `README.md`, then
  conditionally replaces root `index.html`. These are shared viewer files; old
  assets remain available to cached pages and existing document URLs stay unchanged.
- **`expire_days`** is the only bucket administration, and it is **off unless you set it**.
  With it set, the setup step **reads** your bucket's lifecycle configuration and writes
  back **one rule of its own**, scoped to the `md-web/` prefix; `0` removes that rule
  again. Every other rule and every bucket-wide setting is preserved, and the uploads
  under that prefix are **auto-deleted after N days**.
- **Local files:** it reads `~/.md-web/config.json` (your credentials and bucket settings)
  and writes `~/.md-web/.deployed` (a deploy fingerprint hint). Before publishing,
  it also reads remote `index.html` through your configured S3 endpoint.
- **Nothing else.** No other bucket, no other key prefix, no other skill's files, no
  startup entry, no scheduled job, no background service, no third-party service, no
  telemetry.

Scope in one line: it runs `node` locally, reads `~/.md-web/config.json` (or
`MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY`), makes HTTPS requests **only** to the S3
endpoint you configured, writes the uploaded `.md` plus the viewer assets, may write one
lifecycle rule scoped to the `md-web/` prefix, creates and deletes at most one temporary
file, touches no other skill, and installs nothing.

A request for a public share link authorizes uploading that document, including a
retry. The AI explains the public access before uploading. Viewer setup overwrites
shared bucket-root files, and retention changes edit bucket policy. Each needs
authorization covering that operation, which can be provided in the original request.

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
3. Set permissions to **Object Read & Write** (or **Admin Read & Write** only if you set `expire_days`, which manages a bucket lifecycle rule — see below)
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
| expire_days | No       | Auto-delete uploaded files after N days. Unset = this skill never touches the bucket's lifecycle (default) | `30` |

> **Tip**: R2.dev URLs have rate limits. For production use, bind a custom domain to your bucket and use that as `public_url`.

The AI will automatically save these to `~/.md-web/config.json`. No repeat setup needed.

Prefer not to keep a long-lived secret in a file? Leave `access_key` and `secret_key` out
of the config and set `MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY` in the environment
instead. The config file wins when both are set, so an existing setup keeps working.

## Usage

Uploaded content is **publicly accessible** via the generated URL. The skill only runs when you explicitly ask for it, and the AI tells you the link is public before it uploads anything:

```text
publish this Markdown to my public bucket
create a public web link for this document
/md-web path/to/file.md
```

A generic request to share an existing URL, create a private link, or preview locally does not authorize a public upload. If the sharing destination or public scope is unclear, clarify it before uploading.

The AI returns a link — click to view the rendered document in your browser.

> **Note**: Markdown image references (e.g., `![](image.png)`) are not uploaded — only the `.md` file itself. Use absolute image URLs if your document includes images.

## Auto-expiry (`expire_days`)

Left unset, this skill never sends a bucket-level request — an **Object Read & Write**
token is all you need, and your bucket's lifecycle configuration is untouched.

Set a number of days and the skill maintains exactly one rule, scoped to the `md-web/`
key prefix; set `0` and it removes that rule again. Either way the viewer files at the
bucket root and any unrelated object are never touched, and **rules you set yourself are
preserved**: the script reads the bucket's lifecycle configuration, drops only its own
rule, and writes the rest back unchanged.

Managing it needs an **Admin Read & Write** token. With a narrower token the setup
step still succeeds and a warning goes by in the output — set the rule in the dashboard
instead. Re-run the one-time setup step after changing it.

Lifecycle changes must be serialized with other administrators: S3 replaces the whole
configuration and offers no atomic per-rule update. Setup checks for concurrent edits
with a second read, rejects unsupported/incomplete XML or a conflicting rule ID, and
does not replay failed policy writes. A race remains between that final read and write.
A warning means retention needs verification; the viewer can still be used.

## Security

- **Anything you upload is publicly accessible** at the returned URL, and there is no un-publish step (unless `expire_days` is set, which auto-deletes the uploaded file after N days) — never upload secrets, API keys, PII, or other sensitive content.
- Credentials live in **plaintext** in `~/.md-web/config.json`, or in `MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY` if you prefer to keep them out of a file. On macOS and Linux the script tightens the config file to owner-only access; protect it either way — don't commit it or share it.
- **No elevated privileges.** That owner-only tightening is the only permission change the skill makes: a user-scoped change to a file in your own home directory, made by the script running as you. It never asks for root, never runs an elevated command, and touches no file outside your home directory and the bucket you configured.
- **Use a dedicated bucket.** Uploads and any expiry rule are namespaced under `md-web/`, but a dedicated bucket keeps this skill's bucket-administration rights away from anything you actually care about.
- **The viewer runs your Markdown as HTML on the page.** GFM, tables, `<details>` and inline HTML all render. Two things keep that in bounds: a route guard that only loads same-origin paths under `md-web/` (a crafted link cannot make the viewer fetch a document from another origin), and a Content-Security-Policy without `'unsafe-inline'`, so HTML inside a document cannot run script. What the policy does **not** stop is a document *inserting elements* into the page — so review unfamiliar Markdown and inline HTML before publishing; source authorship alone is not a safety check. Readers should treat the page as public and untrusted: anyone who can write to the bucket can put content there.
- Documents keep their original language. The viewer interface is English; the word counter follows the document content.

## File Structure

```yaml
md-web/                     # Skill directory (managed by ClawHub, may be replaced on upgrade)
├── SKILL.md              # AI instruction file
├── upload.js             # Upload script (pure Node.js, zero dependencies)
├── README.md             # This document
├── README.zh.md          # Chinese documentation
└── docsify-server/       # Viewer files (uploaded by the one-time setup step)
    ├── index.html
    ├── README.md
    └── assets/           # JS/CSS assets (bundled locally, no CDN dependency)
        ├── config.js     # Viewer configuration + document-route guard
        ├── docsify.min.js
        ├── vue.css
        └── ...

~/.md-web/                  # User data directory (preserved across upgrades)
├── config.json           # Bucket credentials & settings (created on first use)
└── .deployed             # Local deployment hint, checked against the remote entry point
```

`upload.js` snapshots and fingerprints `docsify-server/` (dot-files are ignored), puts
assets in `assets/<bundle-hash>/`, and switches `index.html` only after all files upload.
The local hint plus a read of the active remote entry point detects viewer upgrades,
deletion or another installation replacing it. Publishing stops with `SETUP_REQUIRED`
until an explicit setup. Old document links and the landing README path remain valid.

Setup uses an ETag precondition (`If-Match`, or `If-None-Match: *` on first deployment).
`SETUP_CONFLICT` stops a competing replacement; inspect the active viewer before
retrying. A provider must support conditional object writes and return ETags; there is
no unconditional fallback. This follows [S3 conditional writes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html)
and [R2's S3 compatibility](https://developers.cloudflare.com/r2/api/s3/api/).
The first upgrade from the old flat-asset layout needs setup once. Old flat assets and
version directories are retained, including files left by interrupted uploads; this
tool does not perform automatic cleanup or change lifecycle scope to remove them.

## Other S3-Compatible Services

Besides Cloudflare R2, this skill works with any S3-compatible object storage:

- **AWS S3**: endpoint is `s3.REGION.amazonaws.com`
- **Backblaze B2**: endpoint is `s3.REGION.backblazeb2.com`
- **DigitalOcean Spaces**: endpoint is `REGION.digitaloceanspaces.com`
- **Wasabi**: endpoint is `s3.REGION.wasabisys.com`
- **Tencent Cloud COS**: endpoint is `cos.REGION.myqcloud.com`

The provider also needs object reads, ETags and conditional object writes for safe
viewer setup. Check those capabilities when using an S3-compatible service.
