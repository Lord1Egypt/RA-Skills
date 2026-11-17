---
name: musescore
description: Search MuseScore sheet music and read score metadata via MCP. Triggers on phrases like "find sheet music for", "search MuseScore for", "is there a free arrangement of", "what's the license on this MuseScore score", "how many pages is", or any request involving MuseScore scores, arrangements, or sheet-music metadata. Requires musescore-mcp installed and the ContextMint Bridge browser extension active with a signed-in musescore.com tab (see Setup).
---

# musescore-mcp

MCP server for MuseScore — search sheet music and read score metadata. Routes
through your signed-in musescore.com tab via the ContextMint Bridge extension,
so Cloudflare sees a real browser session instead of a Node process.

- **Source:** [github.com/chrischall/musescore-mcp](https://github.com/chrischall/musescore-mcp) (private)

> ⚠️ MuseScore has no public consumer API (the old one was shut down). This
> server reads the same server-rendered data the musescore.com web app
> hydrates from, dispatched through your own signed-in browser tab via the
> ContextMint Bridge extension. Use at your own discretion.

## Setup

### 1. Install musescore-mcp

`.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "musescore": {
      "command": "node",
      "args": ["/absolute/path/to/musescore-mcp/dist/bundle.js"]
    }
  }
}
```

### 2. Install ContextMint Bridge and sign in

Install **ContextMint Bridge** from its [releases page](https://github.com/nullnet-app/contextmint-bridge/releases)
(Chrome: load the chrome zip unpacked; Safari is not available yet: it will ship inside the
ContextMint app, which has no public download, so use Chrome for now), then open **musescore.com** signed in, with the Cloudflare check
cleared. Every request rides that tab's session.

ContextMint Bridge is the fetchproxy extension under its new name, from the same
maintainer; its source is public at
https://github.com/nullnet-app/contextmint-bridge — build it yourself, or check
a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.

## Tools

- **`musescore_search`** — search scores. Defaults to MuseScore's
  "Free to view, play & download" facet (`free_only=true`); set
  `free_only=false` to search the whole catalog. Returns id, title, uploader,
  composer, instrumentation, difficulty, counts, and MuseScore's catalogue
  flags (`listedFree`, `listedDownloadable`, `publicDomain`, `purchased`,
  `official`). `listedFree`/`listedDownloadable` do **not** promise a free PDF:
  a non-Premium account can still hit a purchase paywall, which only shows at
  download time as `status: "gated"`.
- **`musescore_get_score`** — one score's metadata (title, license, measures,
  key, parts, duration, dates) by URL or `user_id` + `score_id`.
- **`musescore_download`** — resolve the official download URL (pdf/mid/mscz/mxl)
  for a free or entitled score; with `output_path` (local bridge) the browser
  downloads it and the MCP moves it there.
- **`musescore_score_to_pdf`** — best obtainable PDF: official PDF → page-1 SVG
  render → page-1 PNG → `gated`. Read `status` first: `complete`, `partial`
  (page 1 only — not the full score), `gated` (`requiresPurchase: true`), or
  `open_in_browser` (open `downloadUrl` in your signed-in browser).
- **Remote bridge (hosted MCP):** files can't be written where you can reach
  them, so `output_path` is ignored and the render PDF comes back as a download
  link (`fileUrl`; embedded inline only when the host has no blob store);
  official files come back as `open_in_browser` + URL.
- **`musescore_fetch_svgs`** — the page-1 render SVG; locally into `output_dir`,
  hosted as `files[]` with a download `url` and a `blobKey` per page.
- **`musescore_svg_to_pdf`** — stitch `.svg` / `.svgz` pages into a PDF (pure JS).
  Pass exactly one of `svg_paths` (local files), `svg_blob_keys` (the blobKeys
  `musescore_fetch_svgs` returned, hosted) or `svg_files` (inline base64).
- **`musescore_healthcheck`** — verify the ContextMint Bridge connection end-to-end.

> **Downloads:** free scores (`is_free`) are downloadable; paid scores need
> PRO/purchase. `musescore_download` resolves the official download URL from the
> store's `type_download_list`, gated on `is_free` or `hasAccess`, and returns
> the link for you to open in your browser — the MCP can't stream the file
> itself (Cloudflare + cross-origin S3 redirect). `musescore_score_to_pdf`
> writes a local PDF only in the SVG fallback path.

## In context groups

musescore is a member of the **family** group (each tool's `_meta.mint`).
It answers no what's-new / what's-due / what's-on question, so it has **no
canonical read** and no subjects: a group ask like "what's on for the family
this week?" skips it. It joins a compound ask only by name — "…and find
piano sheet music for the recital piece" routes to `musescore_search`
(a `lookup`); the file tools are writes (`other`), the session pair `change`.
It is browser-bridged, so when the ContextMint Bridge is not connected the
group answers "musescore needs your browser open" rather than an error.

## Notes

- Read-only. No credentials stored — auth lives in your browser tab.
- Optional env: `MUSESCORE_WS_PORT` (default 37149), `MUSESCORE_OUTPUT_DIR` (default `~/Downloads`),
  `MUSESCORE_DELIVERY` (`auto`|`file`|`inline`, default `auto`), `MUSESCORE_INLINE_MAX_BYTES` (default 4 MiB).
