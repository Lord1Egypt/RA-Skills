---
name: litehost-connect
version: 4.2.0
author: Litehost
license: MIT
description: >
  Publish files and websites as shareable links on litehost.io and manage them through the
  Connect API. Use when the user asks to deploy, host, publish, share, upload, update, list,
  delete, archive or manage a site, file, project or custom domain on Litehost, send work to a
  client as one link, get a QR code for a link, or check their Litehost plan or quota.
user-invocable: true
argument-hint: "[file-or-folder]"
metadata:
  hermes:
    tags: [Hosting, Deployment, Web, Static Sites, API]
    related_skills: []
    requires_tools: [terminal]
  openclaw:
    requires:
      bins: [bash, curl]
required_environment_variables:
  - name: LITEHOST_API_KEY
    prompt: "Your Litehost API key (format: lh_live_...). Optional."
    help: "Optional. Without it the skill publishes with no sign-in, or signs in once and saves the key to ~/.config/litehost/credentials.json. Permanent keys: https://litehost.io/dashboard → Integrations."
    required_for: "Managing existing projects. Not needed to publish (POST /v1/projects/temp)."
---

# Litehost Connect

Base URL: `https://connect.litehost.io` · Agent guide: https://connect.litehost.io/llms.txt

Helper: `scripts/litehost.sh` (in this skill's folder). Use it whenever you can run bash: it keeps
the API key in a file between commands and never prints it.

---

## Step 0 — Can this environment reach Litehost?

This skill runs `curl` against `https://connect.litehost.io`. That works in Claude Code, Cursor and
other agents on the user's own computer. In a sandbox (the claude.ai or Claude desktop chat, ChatGPT,
hosted agents) outbound traffic is often limited to a list of allowed domains.

If `scripts/litehost.sh session` returns `NETWORK_BLOCKED`, or any call fails with a proxy error,
`host_not_allowed`, `403 Forbidden` before reaching Litehost, or "Could not resolve host":

- Stop. Do not retry, do not sign in, and do not try other URLs.
- Tell the user, in plain words: "This chat can't reach Litehost. The easiest fix is the Litehost
  connector: in Claude go to Settings → Connectors → Add custom connector and paste
  `https://connect.litehost.io/mcp`, then sign in once. It works in any chat, with nothing else to
  set up."
- Only if they want to keep using this skill: they add `connect.litehost.io` to the allowed domains
  in their code execution settings and start a **new chat** (the setting does not apply to a chat
  that is already open).

---

## Step 1 — Pick the path (do this before anything else)

Run `scripts/litehost.sh session` first.

| Result | Path |
|---|---|
| `"status":"success"` | **A. Signed in.** Use `scripts/litehost.sh api …` for every call. Never sign in again. |
| `NO_SAVED_KEY` and the user just wants a link | **B. Publish without signing in.** Follow `actions/temp-project.md`. |
| `NO_SAVED_KEY` and the user wants you to manage their projects | **C. Sign in once.** Follow `actions/otp-sign-in.md`, then path A. |
| `API_KEY_INVALID` / `API_KEY_EXPIRED` | Run `scripts/litehost.sh forget`, then B or C. |

Rules that prevent the "asked for a code again" problem:

- **Never start a sign-in because a command failed.** Read the error `code` and follow its
  `nextStep`. Only `API_KEY_INVALID` / `API_KEY_EXPIRED` (after `forget`) lead to signing in.
- **Never rely on `export LITEHOST_API_KEY=…`.** Each command usually runs in a new shell, so the
  variable is gone on the next call and every request fails with 401. The helper reads the key
  from `~/.config/litehost/credentials.json` on every call.
- **Request a code once per sign-in.** If you request again while a code is open, nothing new is
  sent. A wrong code (`OTP_INVALID`) means the user mistyped: ask them to re-check, never request
  a new one.
- A key from sign-in renews while in use. Once saved, it keeps working across sessions.

No bash (e.g. Windows without WSL)? Use the curl examples in the action files, read the key from
`LITEHOST_API_KEY` or the credentials file in **every** command, and follow the same rules.

---

## Step 2 — Do the task

Map the user's intent to one action file, read it, and follow it. Every curl example in the action
files maps to the helper: `curl -X METHOD https://connect.litehost.io/PATH -H "Authorization: …" ARGS`
becomes `scripts/litehost.sh api METHOD /PATH ARGS` (same `-F` / `-d` / `-H "Content-Type…"` args).

| User says | Action file |
|---|---|
| "share this", "quick link", "preview this", "publish this" (no key) | `actions/temp-project.md` |
| "sign in", "log in", "connect my account" | `actions/otp-sign-in.md` |
| "deploy this", "host this", "publish this" (signed in) | `actions/create-project.md` |
| "update my site", "push new version", "redeploy", "replace content" | `actions/replace-project.md` |
| "rename", "change slug", "make private", "set password", "set expiry", "SEO" | `actions/update-project.md` |
| "list my projects", "what do I have hosted" | `actions/list-projects.md` |
| "project details", "project status" | `actions/get-project.md` |
| "QR code", "print it on the menu / flyer" | `actions/qr-code.md` |
| "did my client open it?", "who opened the link" | `actions/link-opens.md` |
| "deploy history", "versions" | `actions/deployment-history.md` |
| "delete project" | `actions/delete-project.md` |
| "archive", "free up a slot" | `actions/archive-project.md` |
| "unarchive", "restore" | `actions/unarchive-project.md` |
| "domains", "custom domain" | `actions/domains.md` |
| "workspaces", "organize projects" | `actions/workspaces.md` |
| "my plan", "quota", "how much space" | `actions/get-user.md` |

When the user asks for changes to something already shared ("change the price", "send the new
version"), update the same project with `actions/replace-project.md` instead of creating a new one:
the link they already sent, and any printed QR code, keep working. Find it with
`actions/list-projects.md`.

Before creating, claiming or restoring a project while signed in, call `GET /v1/user` and check
quotas (`utils/quotas.md`).

---

## Plans

New accounts get Pro free for 7 days. On Free, the API allows: listing, viewing, creating and
deleting projects, claiming temp projects, and `GET /v1/user`. Pushing new versions, changing
settings, QR codes, link opens, archive/unarchive, domains and workspaces need a paid plan
(`FREE_TIER_RESTRICTED` or `FEATURE_LOCKED`).
That error means the key is fine: tell the user and link https://litehost.io/dashboard?upgrade=plans.
Do not sign in again.

---

## File detection

1. Single HTML file, or a folder with HTML → static site
2. ZIP with one HTML file → static site (that file is the homepage)
3. ZIP with several HTML files → set `zipIndexHtmlPath`. Try `index.html`, then `dist/index.html`; if
   still ambiguous, ask the user (the error lists `htmlPaths`).
4. ZIP without HTML, or PDFs, images, documents → file bundle
5. Force file-bundle mode with `asFileBundle=true`

---

## Output

After every publish or update, give the user:
1. The live `url`
2. For temp projects, the `claimUrl` and that it expires in 15 minutes unless they open it
3. The `projectId` (needed for later updates)

---

## Errors

Every error response has `code`, `error` and `nextStep`. Follow `nextStep`. Full table:
`utils/errors.md`.

---

## When NOT to use this skill

- General web development questions unrelated to hosting
- Other hosting providers (Vercel, Netlify, AWS, …)
- Local development servers
- DNS outside Litehost custom domains
- Billing: send the user to https://litehost.io/dashboard
- A chat that cannot reach connect.litehost.io (see Step 0): point the user to the Litehost
  connector (`https://connect.litehost.io/mcp`) instead
