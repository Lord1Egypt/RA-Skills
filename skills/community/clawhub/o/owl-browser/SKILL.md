---
name: owl-browser
description: Drive Owl Browser as an agent. Read pages as compact, handle-addressable OwlMark and click/type by handle, not by screenshot or pixel coordinates.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - OWL_API_ENDPOINT
        - OWL_API_TOKEN
      bins:
        - curl
    primaryEnv: OWL_API_TOKEN
    envVars:
      - name: OWL_API_ENDPOINT
        required: true
        description: Base URL of the Owl Browser HTTP API, e.g. http://localhost:8080 (raw server) or http://localhost:80 (Docker/nginx).
      - name: OWL_API_TOKEN
        required: true
        description: Bearer token for the Owl Browser API (matches OWL_HTTP_TOKEN on the server).
    emoji: "🦉"
    homepage: https://www.owlbrowser.net
---

# Owl Browser (agent rendering)

Owl Browser is an AI-native browser. Instead of screenshots or raw HTML, it renders
each page as **OwlMark**: a compact, handle-addressable text view of what is actually
on screen. You **observe** the page, then **act on handles**. This is far cheaper than
a screenshot and removes pixel-coordinate guessing.

Every call is `POST $OWL_API_ENDPOINT/execute/<tool>` with a JSON body and
`Authorization: Bearer $OWL_API_TOKEN`. A reusable helper:

```bash
owl() { curl -s -X POST "$OWL_API_ENDPOINT/execute/$1" \
  -H "Authorization: Bearer $OWL_API_TOKEN" \
  -H "Content-Type: application/json" -d "$2"; }
```

## The loop (do this, keep it short)

```
create_context(render_mode=agent) -> navigate(url) -> observe
   -> click/type(handle) -> observe -> ... -> close_context
```

- Call `observe` after navigating and after every action. It is the only way you see the page.
- Act using the handle tokens `observe` prints (e.g. `l5`, `b12`, `x27`). No CSS selectors, no pixel coordinates.
- `observe` blocks until the page is ready. Do not add a separate wait step.
- Never screenshot to read text or find elements. Screenshot only to judge visual design or layout.

## Core tools

### browser_create_context
Creates a session. Returns `result.context_id` (use it in every later call). Do NOT pass `context_id` in.
```bash
owl browser_create_context '{"render_mode":"agent"}'
# use "both" if you will also screenshot; "pixel" is the legacy human render
```

### browser_navigate
```bash
owl browser_navigate '{"context_id":"ctx_...","url":"https://example.com"}'
```
Does NOT return the page. Call `observe` next.

### browser_observe  (your eyes)
Returns `render` (OwlMark text), `handles` (actionable elements), `metadata`, `token_estimate`.
```bash
owl browser_observe '{"context_id":"ctx_..."}'
owl browser_observe '{"context_id":"ctx_...","detail":"outline"}'   # headings-only map of a long page
```
Params: `detail` = `min` | `normal` (default) | `full` | `outline`; `region` = `main`/`nav`/`header`/`footer` or a handle; `max_tokens` = soft budget.

A handle in the render looks like: `- link "Pricing" [#l5]` or `textbox "Email" [#x27 val=""]`. Pass the token (`l5`, `x27`).

### browser_click / browser_type  (your hands)
Pass the handle token as `selector` (or `handle`). The response includes an `effect`:
`navigated`, `dom-changed`, or `no-effect`. Trust it, then re-observe.
```bash
owl browser_click '{"context_id":"ctx_...","selector":"l5"}'
owl browser_type  '{"context_id":"ctx_...","selector":"x27","text":"you@example.com"}'
```
Also: `browser_clear_input '{"context_id":"...","selector":"x27"}'` before re-typing,
and `browser_press_key '{"context_id":"...","key":"Enter"}'` to submit.

### browser_screenshot  (visual check only)
```bash
owl browser_screenshot '{"context_id":"ctx_..."}'
```

### browser_close_context
```bash
owl browser_close_context '{"context_id":"ctx_..."}'
```

## Drill-down tools (when observe collapsed something)

- `browser_expand '{"context_id":"...","handle":"R1"}'` re-serializes one collapsed region/template at higher detail.
- `browser_read_node '{"context_id":"...","handle":"M1"}'` returns the full text of a single node (e.g. an article body).

## Edge cases and recovery

Check `metadata.status` on every observe:
- `ready` — act on it.
- `pending` — the page has not rendered its content yet (a lazy client-rendered shell). The envelope has `reason` and `retry_after_ms`; re-observe after that delay. Do NOT treat a pending render as an empty page.
- `incomplete` — chrome rendered but main content did not; re-observe once, then use vision.

`metadata.dropped_surfaces` tells you what text could not capture:
- `canvas` / `webgl` / `image:N` — a visual surface. Use `render_mode:"both"` + `browser_screenshot` + your own vision.
- `sparse_main` / `shell_unhydrated` / `main_content_unrendered` — content is late or withheld; re-observe, then vision if still empty.
- `first_tree_timeout` — slow or bot-blocked; read it with a screenshot.

Other cases:
- **Handles are per-document.** After any navigation (a click whose `effect` is `navigated`, or a `browser_navigate`), re-observe to get fresh handles. Acting on a stale handle returns `STALE_HANDLE`; when you see that, re-observe.
- **Same-page anchors scroll, they do not navigate.** Clicking an `href="#section"` link returns `effect: "scrolled"` and moves the viewport. Expected, not a failure.
- **Rare click-nav crash:** on a few slow sites, a click that triggers a cross-document navigation can crash and auto-respawn the browser (~1s). If a context is lost right after such a click, recreate the context and `browser_navigate` directly to the destination URL instead of clicking.
- **PDF / embedded plugins:** read the content with a screenshot (`render_mode:"both"`); in-page plugin controls may not be actionable handles.

## Do and do not

- DO observe before acting and re-observe after every action.
- DO act on the exact handle tokens `observe` printed.
- DO read the `effect` of a click/type before assuming it worked.
- DO use `detail:"outline"` on long reference pages, then `expand`/`read_node` the part you need.
- DO NOT screenshot to read a page or find elements.
- DO NOT guess pixel coordinates. Owl gives you handles so you never have to.
- DO NOT pass `context_id` to `create_context`; it is returned to you.

## Minimal example: search and open a result

```bash
CTX=$(owl browser_create_context '{"render_mode":"agent"}' | jq -r .result.context_id)
owl browser_navigate "$(printf '{"context_id":"%s","url":"https://duckduckgo.com"}' "$CTX")"
owl browser_observe  "{\"context_id\":\"$CTX\"}"                 # find the search box, e.g. x4
owl browser_type     "{\"context_id\":\"$CTX\",\"selector\":\"x4\",\"text\":\"owl browser olib ai\"}"
owl browser_press_key "{\"context_id\":\"$CTX\",\"key\":\"Enter\"}"
owl browser_observe  "{\"context_id\":\"$CTX\"}"                 # results appear, pick a link, e.g. l31
owl browser_click    "{\"context_id\":\"$CTX\",\"selector\":\"l31\"}"
owl browser_observe  "{\"context_id\":\"$CTX\"}"                 # read the opened page
owl browser_close_context "{\"context_id\":\"$CTX\"}"
```

## Notes

- Over MCP, the Owl MCP server exposes this same loop and defaults to `render_mode=agent`; the toolset is profile-scoped via `OWL_MCP_PROFILE` (`agent`, `automation`, `webdev`, `full`).
- The full machine-readable tool reference is served at `GET $OWL_API_ENDPOINT/agent-skills.md`.
