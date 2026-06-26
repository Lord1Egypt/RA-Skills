# Page Fetch Strategy

## Default flow

1. Fetch raw HTML with `requests` first.
2. If the HTML does not contain a usable body, inspect embedded data such as `__NEXT_DATA__`, JSON-LD, or other hydration payloads.
3. If the page is JS-heavy and the first two steps fail, use `scripts/render_page.py` as the browser-render escalation path.
4. If browser rendering is unavailable locally, report that dependency gap explicitly and then fall back to alternate accessible sources when appropriate.
5. If the page is blocked by login, region locks, or anti-bot controls, say so clearly and fall back to alternate accessible sources when appropriate.

## Why this flow exists

- It is fast.
- It is cheaper than browser rendering.
- It is reproducible across models.
- It keeps simple news, blog, and docs pages off the heavy path.

## Output expectations

Return the following when possible:

- title
- author
- publish/update time
- body text or a concise body summary
- extraction method used
- known limitations or missing sections

## Failure handling

Map failures to next actions instead of retrying blindly:

- Timeout or transient network error -> retry once with a reasonable timeout.
- `403` / `401` / `429` -> mention access limits; consider header changes or alternate sources.
- HTML present but body missing -> inspect embedded data.
- Body only appears after JS execution -> escalate to browser rendering.
- Login wall / CAPTCHA / region block -> stop pretending and tell the user what is blocked.
