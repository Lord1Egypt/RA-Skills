---
name: oxypages-publish
description: Publish a static website (HTML, CSS, JS, images, or a ZIP) or a built framework app (React, Vue, Svelte, Vite, Astro, Next.js static export) to OxyPages and hand the user a live HTTPS link. Works with no account for a 30-minute unclaimed link, or with an OxyPages API key for a permanent site the user owns, including editing a site they already have.
version: 1.1.0
homepage: https://oxypages.com
metadata:
  openclaw:
    emoji: "\U0001F680"
    requires:
      bins:
        - curl
    primaryEnv: OXYPAGES_API_KEY
    envVars:
      - name: OXYPAGES_API_KEY
        required: false
        description: An OxyPages API key (starts with oxy_). Optional - without it the skill publishes an unclaimed 30-minute link. Create one at app.oxypages.com under Profile, API Keys. Free accounts include API keys.
---

# Publish a website to OxyPages

OxyPages is static website hosting. You hand it HTML (and any CSS, JS, images or fonts it uses), or the output folder of a framework build, and it is live on an HTTPS link in seconds, on a `*.myoxypages.com` subdomain. OxyPages does not build a no-account upload: for a framework app you run the build first.

There are two ways to publish, and you must choose based on whether the user has given you an API key. Without a key, also choose by what you are publishing: an HTML page or hand-written static files go to `POST /drops` (Path 1); a framework project (a `package.json` with a build script) is built locally and its output goes to `POST /drops/app` (Path 1b).

| | Unclaimed link (no key) | Owned site (API key) |
|---|---|---|
| Needs | nothing | `OXYPAGES_API_KEY` |
| Lives | 30 minutes, then gone unless claimed | permanently, on the user's account |
| Size | 3 MB, 10 files for a page or site; 25 MB, 500 files for a built app | the account's plan |
| Rate | a small hourly cap per address | a far higher hourly cap |
| Use it for | a quick preview, "show me what this looks like live" | anything the user wants to keep |

## Consent rule - read this first

Publishing puts content on the public internet under a URL anyone can open. Before you publish:

1. **The user must have asked for the content to be published or hosted.** Writing a page is not the same as asking for it to go live. If they said "make me a landing page", show them the file and ask whether to publish it. If they said "put this online", "host this", "give me a link" or "publish it", that is consent.
2. **Never publish content that impersonates a brand or asks for credentials.** OxyPages runs a moderation pass on every publish and refuses or removes phishing, brand impersonation, gambling funnels and illegal content. Do not try to route around a refusal.
3. **Tell the user what you published and where.** Always relay the URL, and for an unclaimed link always relay the claim link and the 30-minute expiry.

## Path 1 - unclaimed link, no account

Use this when there is no `OXYPAGES_API_KEY`. One `POST` with the file as multipart form data. The file may be a single `.html` page or a `.zip` whose top level contains `index.html`.

```bash
# A single page
curl -sS -X POST https://api.oxypages.com/drops \
  -H "X-Oxy-Agent: openclaw" \
  -F "file=@index.html"

# A folder, zipped first (index.html must be at the top level of the zip)
zip -r site.zip index.html css/ js/ images/
curl -sS -X POST https://api.oxypages.com/drops \
  -H "X-Oxy-Agent: openclaw" \
  -F "file=@site.zip"
```

Send the `X-Oxy-Agent` header naming your agent. It buys nothing except attribution, and it is how OxyPages knows the publish came from an agent rather than a person.

A successful response:

```json
{
  "ok": true,
  "url": "https://unclaimed-k3j9x2m1qa.myoxypages.com",
  "token": "…",
  "claim_url": "https://app.oxypages.com/claim/…",
  "expires_at": "2026-09-12T13:05:00.000Z",
  "note": "Published. This unclaimed website expires in 30 minutes unless it is claimed via claim_url. …",
  "signup_url": "https://app.oxypages.com/signup",
  "login_url": "https://app.oxypages.com/login"
}
```

Relay to the user, in this order:

- the live `url`
- that it expires in 30 minutes unless claimed
- the `claim_url`, which moves the site into a free account permanently (signing up takes a minute and the link stays valid for the 30 minutes)
- that a free account also gives them an API key so you can publish permanent sites for them next time

A `warnings` array, when present, lists files that were left out (for example `README.md` or `.env`). The site is live; say which files were skipped.

Refusals come back as `{"ok": false, "error": "…"}` with an HTTP 4xx. The common ones:

| Status | Meaning | What to do |
|---|---|---|
| 400 | no `index.html` at the top level, or a bad body | fix the file layout and retry once |
| 413 | over 3 MB or more than 10 files | trim the site, or ask the user for an API key (paid plans allow more) |
| 415 | a file type that is not hosted (binaries, executables) | remove it |
| 422 | the moderation pass refused the content | tell the user why; do not retry with small edits |
| 429 | the hourly cap is reached | relay `error` verbatim - it names the way past it, which is a free account and an API key. It does not state a number, so do not invent one |

## Path 1b - a built app, no account

Use this for a framework project (React, Vue, Svelte, Vite, Astro, a Next.js static export) when there is no `OXYPAGES_API_KEY`. OxyPages never builds it for you.

1. Run the project's build: `npm run build`, or the `build` script in `package.json` with the project's package manager.
2. Find the output folder, usually `dist/`, `build/` or `out/`. It must hold an `index.html`.
3. Send what is inside that folder. Never the source folder, `node_modules` or `package.json`: source is refused with `needs_build` (HTTP 422), and the fix is to build first.

```bash
npm run build
(cd dist && zip -r ../dist.zip .)
curl -sS -X POST https://api.oxypages.com/drops/app \
  -H "X-Oxy-Agent: openclaw" \
  -F "file=@dist.zip"

# Or as JSON: text as utf8, binaries as base64
curl -sS -X POST https://api.oxypages.com/drops/app \
  -H "X-Oxy-Agent: openclaw" \
  -H "Content-Type: application/json" \
  -d '{"files": [
        {"path": "index.html", "content": "<!doctype html>…"},
        {"path": "assets/index-3f9a1c2b.js", "content": "…"},
        {"path": "logo.png", "content": "iVBORw0KGgo…", "encoding": "base64"}
      ]}'
```

What applies: Single-Page App routing (unknown paths serve `index.html`), the build's `_redirects` and `_headers` files, up to 25 MB and 500 files, live for 30 minutes. `node_modules`, `.git` and source maps are left out and counted in `warnings`.

The reply has `ok`, `kind: "app"`, `url`, `claim_url`, `expires_at`, `root`, `files`, `bytes`, and `warnings` when something was left out. Relay the `url`, the 30-minute expiry and the `claim_url`, which keeps the app in a free account. Claiming turns it into a project in their account; after that, the keyed `deploy_app` tool (with `project`) deploys new versions of it.

Refusals specific to this path:

| Code | Meaning | What to do |
|---|---|---|
| `needs_build` (422) | you sent source code | run the build and send the output folder |
| `choose_root` (422) | no `index.html` at the top, several HTML files | send again with `root` set to one of `html_files`, or `"none"` |
| `too_large` / `too_many_files` (413) | over the cap | send only the output folder, without source maps |
| `bad_file_type` (415) | the multipart `file` is not a `.zip` | zip the output folder |

For a build too large for one request: `POST https://api.oxypages.com/drops/app/manifest` with `{"files": [{"path": "index.html", "size": 1234, "sha256": "<hex>"}, …]}`, PUT each file to the `url` in its `upload` entry with the `headers` given there, then `POST https://api.oxypages.com/drops/app/finalize` with `{"upload_id": "…", "token": "…"}` from the manifest reply.

## Path 2 - a permanent site on the user's account

Use this when `OXYPAGES_API_KEY` is set. Every request carries it as a bearer token. Keys start with `oxy_`; if the key is rejected with 401, tell the user to create a new one at app.oxypages.com, Profile, API Keys.

**1. Find or create the site.**

```bash
# Existing sites: id, name, subdomain, url, status
curl -sS https://api.oxypages.com/v1/sites \
  -H "Authorization: Bearer $OXYPAGES_API_KEY"

# A new site (the subdomain is generated; name is optional)
curl -sS -X POST https://api.oxypages.com/v1/sites \
  -H "Authorization: Bearer $OXYPAGES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme landing page"}'
```

Ask the user which site to deploy into when they already have one that fits. Do not create a new site for every publish. To make a CHANGE to a site they already have, use step 3 (edit only what changed) instead of redeploying every file.

**2. Deploy the files.** Either a ZIP or a JSON file list. A deploy replaces the whole site, so send every file each time.

```bash
# ZIP (index.html at the top level)
curl -sS -X POST "https://api.oxypages.com/v1/sites/$SITE_ID/deployments" \
  -H "Authorization: Bearer $OXYPAGES_API_KEY" \
  -F "zip=@site.zip"

# JSON: text files as utf8, binaries as base64
curl -sS -X POST "https://api.oxypages.com/v1/sites/$SITE_ID/deployments" \
  -H "Authorization: Bearer $OXYPAGES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"files": [
        {"path": "index.html", "content": "<!doctype html>…"},
        {"path": "css/style.css", "content": "body{…}"},
        {"path": "logo.png", "content": "iVBORw0KGgo…", "encoding": "base64"}
      ]}'
```

The response carries `ok`, `url`, `deployment_number`, `pages`, `bytes`, `files` and, when some files were skipped, `warnings`. Relay the `url`. Version history is at `GET /v1/sites/$SITE_ID/deployments`.

**3. Edit a site the user already has: change only some files.** Read the live files, edit the text files, then send back only what changed. Everything you do not send, including images and fonts, is kept, and the change is a new version.

```bash
# Live files: text files with "content", images and other binaries as "url"
curl -sS "https://api.oxypages.com/v1/sites/$SITE_ID/files" \
  -H "Authorization: Bearer $OXYPAGES_API_KEY"
# One file only
curl -sS "https://api.oxypages.com/v1/sites/$SITE_ID/files?path=css/style.css" \
  -H "Authorization: Bearer $OXYPAGES_API_KEY"

# Publish only the changed text files (and any deletions)
jq -n --rawfile c index.html '{files: [{path: "index.html", content: $c}], deletions: []}' |
  curl -sS -X POST "https://api.oxypages.com/v1/sites/$SITE_ID/files" \
    -H "Authorization: Bearer $OXYPAGES_API_KEY" \
    -H "Content-Type: application/json" --data-binary @-
```

This route takes text files only (HTML, CSS, JS, JSON, SVG, text); a binary file is refused with 415, so to replace an image deploy the whole site with step 2. The reply has the same `url` and `deployment_number` as a deploy.

## Limits, without guessing

Do not quote sizes from memory - they are tuned from the admin panel and this
file cannot keep up. Read them:

```bash
curl -sS https://api.oxypages.com/limits
```

It returns the per-page and per-asset ceilings, the ZIP upload ceiling, the
unclaimed-drop ceilings and each plan's storage. It does **not** carry the
hourly publish caps, and no number in this skill should either. It does not
carry the built-app drop's ceilings yet either; those are the 25 MB and 500
files stated in Path 1b, and a `413` refusal names the live one. A `429`
answer does not state a number at all - it explains in `error` that a free
account lifts the limit, and that sentence is what to relay.

## What a site needs

- `index.html` at the top level. That is the page visitors see at `/`.
- Relative links between files (`css/style.css`, not `/Users/me/site/css/style.css`).
- Only hostable types: HTML, CSS, JS, JSON, text, images, fonts, PDF. Anything else is skipped and reported in `warnings`.
- Nothing in the page that would break under a strict content policy: inline scripts are fine, but the page cannot load from unknown origins that the user has not asked for.

## MCP instead of curl

If your runtime speaks MCP, the same account operations are available as tools at `https://mcp.oxypages.com/mcp` (Streamable HTTP, bearer `OXYPAGES_API_KEY`): `list_sites`, `create_site`, `deploy_site` (the JSON file list above), `read_site_files` and `update_site_files` (step 3) and `list_deployments` (plus `deploy_app` on accounts with Web Apps turned on). With no `Authorization` header at all, the same URL offers the no-account paths: `publish_page` (Path 1) and `deploy_app` (Path 1b, a built app's output files). Both return `url` and `claim_url`.

## Phrases to use with the user

- After an unclaimed app deploy: "Your app is live at {url} for the next 30 minutes. To keep it, open this claim link and sign in or create a free OxyPages account: {claim_url}."
- After an unclaimed publish: "It's live at {url} for the next 30 minutes. To keep it, claim it here: {claim_url} - that puts it in a free OxyPages account, and you'll get an API key so I can publish permanent sites for you in future."
- After an owned deploy: "Deployed to {url} (version {deployment_number})."
- On a moderation refusal: "OxyPages declined to host this page: {error}. I can't publish it there."
