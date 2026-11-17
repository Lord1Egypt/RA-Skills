---
name: gists-page
description: Publish HTML/JS/CSS demos as GitHub Gists and share gists.page preview links. Use when the user wants to share or preview a demo online, publish a snippet to gist, get a shareable preview link, or mentions gists.page or gist preview.
---

# gists.page — Gist preview service

gists.page is a static site + Service Worker that previews GitHub Gists: the browser
intercepts requests, fetches gist content from the GitHub API/raw endpoints, and renders
it with correct MIME types. Publishing a demo means producing a gist id, then handing
out the preview link.

## Authoring: prefer one self-contained `index.html`

Inline CSS in `<style>` and JS in `<script>`, and ship a single `index.html`.
One file publishes in a single call on every path below, and none of the flat-gist
constraints (no directories, basename folding, rename conflicts) can bite.
Multi-file gists are fully supported — relative references resolve between files —
so publish an existing multi-file demo as-is rather than rewriting it; just don't
author new demos as multi-file when inlining is trivial.

## URL rules

- `https://gists.page/{gist_id}/` — renders `index.html` (or an HTML first file);
  otherwise a gist-page-style overview of all files
- `https://gists.page/{gist_id}/{file_name}` — renders a specific file (URL-encode the name)
- gist_id is 16–40 hex chars (modern gists: 32) or an old-style short numeric id;
  a missing trailing slash redirects to add it

## Publishing

Several ways to create a gist — use the first one available in this session:

**1. `gh` CLI** — if installed and authenticated (`gh auth status`; it also picks up
`GH_TOKEN`/`GITHUB_TOKEN` env vars):

```bash
# Creates a secret gist by default (link works, but unlisted/unsearchable)
gh gist create index.html
# Multi-file works too: gh gist create index.html app.js style.css
# Add --public for a public gist; the last path segment of the output URL is the gist_id
```

**2. GitHub MCP tools** — if the session has them, look for gist tools
(`create_gist` / `update_gist` on the official GitHub MCP server) and follow their
schemas. The official server's gist tools take one file per call — a single-file
demo publishes in one `create_gist` call; for multi-file, create the gist with the
entry file, then add each remaining file with `update_gist`.

**3. GitHub REST API via curl** — needs a token with the `gist` scope (classic PAT)
or Gists read/write (fine-grained). Check `$GH_TOKEN` / `$GITHUB_TOKEN` before asking
the user for one; anonymous gist creation is not supported by the API.

```bash
jq -n --rawfile h index.html '{public: false, files: {"index.html": {content: $h}}}' |
curl -sS -X POST https://api.github.com/gists \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d @- | jq -r '.id'
```

`--rawfile` handles JSON escaping (multi-file: one `--rawfile` and one `files` entry
per file); without jq, build the body with a python one-liner — never splice file
contents into a hand-assembled JSON string.

**4. None of the above** — ask the user to create the gist manually at
https://gist.github.com (paste the files there) and reply with the gist URL or id.

Preview link = `https://gists.page/<gist_id>/`.

### Updating an existing gist

- gh: `gh gist edit <id> --add <file>` uploads that file (adds or replaces). Bare
  `gh gist edit <id>` opens an interactive `$EDITOR` — avoid in agent sessions.
- MCP: `update_gist` (or equivalent), one file per call.
- API: `PATCH https://api.github.com/gists/<id>` with the same `files` body shape as
  creation; set a file's value to `null` to delete it.
- git: clone `https://gist.github.com/<id>.git`, commit, push (HTTPS auth: any
  username, token as password).

### Verifying

Verify uploads with `curl -s https://api.github.com/gists/<id>` (check the `files`
keys; add `-H "Authorization: Bearer $GITHUB_TOKEN"` if anonymously rate-limited) —
do NOT verify by curling the preview link (see below). If a browser tool is available,
open the preview link to confirm rendering.

## Hard limits (GitHub side)

The first three bullets only apply to multi-file demos.

- **Gists are flat — no directories.** Pushes containing them are rejected server-side
  (`Gist does not support directories`), and the web UI can't create them either.
  Flatten files before uploading.
- **Directory-style references in HTML need no edits**: the preview folds an
  unresolvable `./css/style.css` onto its basename `style.css` (flat names are
  unique in a gist, so the mapping is unambiguous).
- The one case folding can't cover: same-named files under different directories
  (`css/a.js` + `js/a.js`). A gist can hold only one `a.js` — rename and update
  references before publishing.
- Filenames are case-sensitive; only an exact `index.html` gets default-page treatment.
- Binary files (images etc.): the gist API only accepts UTF-8 text, so none of the
  API-based paths (gh, MCP, curl) can upload them. `git push` may work (the preview
  streams binaries fine); if push is also rejected, use external hosting or `data:` URIs.
- Large files: when the API truncates content, the preview automatically streams from
  the raw endpoint — nothing to handle.

## Preview service behavior

- **Requires a browser with Service Workers.** First visits and hard refreshes briefly
  flash a loading state before content appears — normal mechanics. curl, crawlers, and
  no-SW environments only ever receive the shell page; that is not a bug.
- **Edits take up to 5 minutes to show.** Gist metadata is cached in the visitor's
  browser with a 5-minute TTL. If a preview looks stale right after an edit, wait out
  the TTL before debugging anything.
- Navigating to a non-HTML text file (markdown, source, json, unknown extensions)
  opens an in-page viewer: GitHub-flavored markdown with syntax highlighting,
  mermaid diagrams, and KaTeX math (libraries CDN-loaded at view time). A multi-file gist
  with no HTML entry renders as an overview of every file; binary files show a
  preview-not-supported note (subresources still stream raw bytes). Only `.html`/`.htm`
  run as pages — app entry files must end in `.html`. Subresource fetches
  (`./app.js`, `fetch('./data.json')`) always get raw content with
  extension-mapped MIME types.
- Rate limits: content is fetched over the visitor's own connection; the anonymous
  GitHub API allows 60 requests/hour/IP. When the API is unavailable (rate limited,
  or the 502s it returns for very popular gists), the preview falls back to cached
  data, then to the quota-free raw endpoint (basename folding is limited there).
- Same-level relative references (`./app.js`, `fetch('./data.json')`) all work.

## Security & privacy

- Anyone with the link can view it (secret only means unlisted) — never put keys,
  tokens, or internal data in a gist.
- Gist JS executes on the gists.page origin; the domain is dedicated to previews and
  carries no cookies or accounts, but demos still must not ask visitors for sensitive input.

## Quick troubleshooting

| Symptom | Cause & fix |
|---|---|
| Push rejected: `does not support directories` | Gists are flat; `git mv` files to the root and retry — HTML references need no changes |
| Edited the gist but the preview didn't change | Visitor-side 5-minute metadata cache; wait for the TTL to expire |
| curl on a preview link returns a form page | Normal: content renders via the SW; verify through the GitHub API instead |
| 401/403/404 from `POST /gists` | Token missing, expired, or lacking the `gist` scope (classic) / Gists read-write (fine-grained) |
| A file shows rendered markdown/source instead of running | Non-HTML navigations open the viewer; name the entry file `.html` to run it as a page |
| 404 saying `gists are flat` | The file (even after basename folding) isn't in the gist; check the exact name |
