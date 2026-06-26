---
name: musescore-mcp
description: Search MuseScore sheet music and read score metadata via MCP. Triggers on phrases like "find sheet music for", "search MuseScore for", "is there a free arrangement of", "what's the license on this MuseScore score", "how many pages is", or any request involving MuseScore scores, arrangements, or sheet-music metadata. Requires musescore-mcp installed and the fetchproxy extension active with a signed-in musescore.com tab (see Setup).
---

# musescore-mcp

MCP server for MuseScore — search sheet music and read score metadata. Routes
through your signed-in musescore.com tab via the fetchproxy browser extension,
so Cloudflare sees a real browser session instead of a Node process.

- **Source:** [github.com/chrischall/musescore-mcp](https://github.com/chrischall/musescore-mcp) (private)

> ⚠️ MuseScore has no public consumer API (the old one was shut down). This
> server reads the same server-rendered data the musescore.com web app
> hydrates from, dispatched through your own signed-in browser tab via the
> fetchproxy extension. Use at your own discretion.

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

### 2. Install the fetchproxy extension and sign in

Install the [fetchproxy](https://github.com/chrischall/fetchproxy) browser
extension and open **musescore.com** signed in, with the Cloudflare check
cleared. Every request rides that tab's session.

## Tools

- **`musescore_search`** — search scores. Defaults to MuseScore's
  "Free to view, play & download" facet (`free_only=true`); set
  `free_only=false` to search the whole catalog. Returns id, title, uploader,
  composer, instrumentation, difficulty, counts, and downloadability flags
  (`free`, `downloadable`, `publicDomain`, `purchased`, `official`).
- **`musescore_get_score`** — one score's metadata (title, license, measures,
  key, parts, duration, dates) by URL or `user_id` + `score_id`.
- **`musescore_download`** — resolve the official download URL (pdf/mid/mscz/mxl)
  for a free or entitled score, from the store's `type_download_list`. Returns
  the link to open in your browser (the MCP can't stream the file).
- **`musescore_score_to_pdf`** — resolve or create a PDF for a score. Returns
  the official PDF URL when MuseScore exposes one; otherwise fetches rendered
  SVG pages and stitches them into `output_path` via `rsvg-convert`.
- **`musescore_svg_to_pdf`** — convert local `.svg` / `.svgz` files already on
  disk into a PDF via `rsvg-convert`.
- **`musescore_healthcheck`** — verify the fetchproxy bridge end-to-end.

> **Downloads:** free scores (`is_free`) are downloadable; paid scores need
> PRO/purchase. `musescore_download` resolves the official download URL from the
> store's `type_download_list`, gated on `is_free` or `hasAccess`, and returns
> the link for you to open in your browser — the MCP can't stream the file
> itself (Cloudflare + cross-origin S3 redirect). `musescore_score_to_pdf`
> writes a local PDF only in the SVG fallback path.

## Notes

- Read-only. No credentials stored — auth lives in your browser tab.
- Optional env: `MUSESCORE_WS_PORT` (default 37149), `MUSESCORE_DEBUG=1`.
