# Browser Runtime Notes

## What the browser fallback does

`render_page.py` uses Node Playwright with headless Chromium to render pages that do not expose usable content in raw HTML.

Use this path for:

- JS-heavy news or blog pages
- client-rendered documentation sites
- pages where the first-pass extractor only returns fragments or metadata

## Runtime expectations

The browser fallback expects:

- Node.js available in `PATH`
- global or otherwise resolvable `playwright` package
- Chromium installed via Playwright
- required system shared libraries for headless Chromium

## Failure modes

### `browser-render:unavailable`

The script could not find a usable Playwright runtime.

Typical causes:

- `playwright` not installed
- Chromium not installed
- `NODE_PATH` does not include the global npm module path

### `browser-render:failed`

Playwright was found, but page rendering or browser launch failed.

Typical causes:

- missing system libraries for Chromium
- TLS / certificate / network issues
- hard anti-bot defenses, login walls, or CAPTCHA
- site-specific rendering failures

## Operational guidance

- Prefer `fetch_page.py` first; it is faster and cheaper.
- Use browser rendering only when the lightweight path is incomplete.
- If browser rendering still fails, report the exact limitation and do not claim full page access.
