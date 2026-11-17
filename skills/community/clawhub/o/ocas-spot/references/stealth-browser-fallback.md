# Stealth Browser Fallback

When the Hermes browser is persistently broken (CDP 502 across multiple kill+restart cycles), the stealth browser MCP provides a reliable alternative.

## When to Use

- Hermes browser returns CDP 502 on ALL commands
- Kill Chrome + kill agent-browser + 30s wait did NOT restore function
- Mid-sweep browser death with remaining venues to check
- **Square availability checks (RECOMMENDED primary method as of 2026-06-06)** — stealth browser loads Square pages reliably on first navigate and avoids the persistent post-Book crash pattern that has affected 4+ consecutive Hermes browser sweeps
- Any Square interaction crash (service click, duration click, staff click, or post-Book) — spawn stealth browser immediately, do NOT attempt kill+restart first
- **Stealth browser CDP connection drop (2026-06-06)** — if stealth browser `click_element` fails with `[Errno 111] Connect call failed`, spawn a NEW stealth browser instance. Do NOT fall back to Hermes browser.

## Key Tools

| Tool | Purpose |
|------|---------|
| `mcp_stealth_browser_spawn_browser(headless=True)` | Create instance, returns instance_id |
| `mcp_stealth_browser_navigate(instance_id, url)` | Navigate to URL |
| `mcp_stealth_browser_query_elements(instance_id, selector)` | Find elements by CSS selector |
| `mcp_stealth_browser_click_element(instance_id, selector, text_match)` | Click element matching text |
| `mcp_stealth_browser_get_page_content(instance_id)` | Get page content (returns file path) |
| `mcp_stealth_browser_close_instance(instance_id)` | Clean up |

## Critical: execute_script Returns Null for ALL DOM Access (2026-06-07)

`execute_script` returns `{"success":true,"result":null}` for EVERY DOM access attempt — `window.location.href`, `document.querySelectorAll`, `document.title`, complex multi-step scripts, all return null despite `success:true`. This is NOT intermittent; it is consistent across all calls in a session.

**Do NOT use `execute_script` for any data extraction or DOM interaction in stealth browser.** The ONLY reliable interaction methods are:
- `query_elements(selector)` — read element attributes, text, visibility
- `click_element(selector, text_match)` — click elements
- `get_page_content()` → parse file path with Python — extract page text/data
- `take_screenshot()` → use `vision_analyze` for visual inspection

**Confirmed 2026-06-07**: 6+ consecutive `execute_script` calls all returned null. `query_elements` and `click_element` worked reliably throughout.

## Stealth Browser execute_script — Do NOT Use (Updated 2026-06-08)

`execute_script` is UNRELIABLE for stealth browser DOM access. It has returned `{"success":true,"result":null}` on 2026-06-07 and again on 2026-06-08 across multiple sessions and cron runs. The 2026-06-06 session where it worked appears to be the exception, not the rule.

**Do NOT use `execute_script` for any data extraction or DOM interaction in stealth browser.** The ONLY reliable interaction methods are:
- `query_elements(selector)` — read element attributes, text, visibility, bounding boxes
- `click_element(selector, text_match)` — click elements (works on all Square custom elements, including calendar navigation buttons)
- `get_page_content()` → parse file path with Python — extract page text/data
- `take_screenshot()` → use `vision_analyze` for visual inspection

**Confirmed 2026-06-08**: 3+ consecutive `execute_script` calls all returned null. Full Square flow (service select → duration → staff → Book → calendar navigation → date state reading → time slot extraction) completed using only `query_elements` + `click_element`.

The stealth browser `navigate` tool uses `wait_until` (not `wait`) for the wait condition parameter. The Hermes browser uses `wait`. This is a common source of validation errors when copy-pasting browser commands.

**Stealth browser:**
```
mcp_stealth_browser_navigate(instance_id, url="...", wait_until="networkidle")
```

**Hermes browser:**
```
browser_navigate(url="...")  # wait parameter not exposed the same way
```

Valid `wait_until` values: `"load"`, `"domcontentloaded"`, `"networkidle"`. Default is `"load"`.

## Square Flow via Stealth Browser (Verified 2026-06-06 — PRIMARY METHOD)

The stealth browser is now the RECOMMENDED primary method for Square availability checks. It loads Square pages reliably on the first navigate (no SPA hydration issues) and does not suffer from the Hermes browser's persistent post-Book crash pattern.

### Complete Workflow

```
1. mcp_stealth_browser_spawn_browser(headless=true, sandbox=false)
   → Returns instance_id

2. mcp_stealth_browser_navigate(instance_id, url="{booking_url}?date=YYYY-MM-DD")
   → Page loads on FIRST navigate (no SPA hydration failure)

3. mcp_stealth_browser_query_elements(instance_id, selector="market-row", limit=20)
   → Find service by text content — match EXACT service name

4. mcp_stealth_browser_click_element(instance_id, selector="market-row", text_match="Swedish Massage")
   → Page transitions to duration/staff selection

5. mcp_stealth_browser_query_elements(instance_id, selector="[role=\"option\"]", limit=20)
   → Read all duration and staff options with attributes

6. mcp_stealth_browser_click_element(instance_id, selector="[role=\"option\"]", text_match="1.5 Hours")

7. mcp_stealth_browser_click_element(instance_id, selector="[role=\"option\"]", text_match="Any staff")

8. mcp_stealth_browser_query_elements(instance_id, selector="[role=\"option\"]", limit=4)
   → Verify aria-selected="true" and selected attribute on both duration and staff

9. mcp_stealth_browser_click_element(instance_id, selector="market-button", text_match="Book")

10. mcp_stealth_browser_get_page_content(instance_id)
    → Returns file_path — parse with terminal Python
    → Verify URL contains "/availability"
    → Parse available time slots from text content

11. mcp_stealth_browser_close_instance(instance_id)
```

### Stealth Browser Behavior Notes

- `execute_script` returns structured key-value pairs (not null) — but `query_elements` + `click_element` remain the PRIMARY interaction method for Square because they provide better state verification (attributes, visibility). Use `execute_script` for complex multi-step JS that can't be done with `click_element` alone.
- `query_elements` works reliably for reading element attributes and text
- `click_element` with `text_match` works for all Square custom elements (MARKET-ROW, market-button, [role="option"])
- `get_page_content` returns a file path — parse with `terminal(command="python3 -c ...")`
- Always close with `close_instance` when done to avoid resource leaks
- Duration and staff options both use `[role="option"]` tagName `market-row` — use `text_match` to distinguish
- **Text match length matters** — use the shortest unique prefix; long strings that extend past the element's visible truncation point fail with "Element not found". See `references/stealth-text-match-length.md`.
- **Confirmed clean Square flow (2026-06-06)** — full end-to-end run with slot parsing. See `references/stealth-browser-square-flow-20260606.md`.
- **`get_page_content` can return very large files (~3MB) for Square availability pages** — the `/availability` page with all time slots rendered produces a ~2990 KB JSON file. This is parseable but large. Use terminal Python to extract the `data.text` field and parse slots with regex. If the file is >5MB, the transfer may time out — in that case, use last_known data.

- **Confirmed clean stealth browser Square flow (2026-06-06 19:21 PT)** — `is_clickable: false` on all elements; `click_element` + `text_match` worked on service/duration/staff/Book; 2.99MB `get_page_content` returned cleanly; 34 slots parsed. 6th+ consecutive clean stealth browser run.
- **Confirmed clean stealth browser Square flow (2026-06-06 19:37 PT)** — 7th+ consecutive clean run. Full flow: service click → duration click → staff click → verify aria-selected → Book → get_page_content (2.99MB) → parse 34 slots. No SPA hydration failure, no post-Book crash. `is_clickable: false` artifact persists; `click_element` + `text_match` unaffected.
- **Confirmed clean stealth browser Square flow (2026-06-06 20:56 PT)** — 9th+ consecutive clean run. Rapid sequential click variant (no intermediate verification) after CDP drop recovery. All 4 clicks returned `true`, `get_page_content` returned 2.99MB, 34 slots parsed. See "CDP Drop After Staff Click" section above.

## Reading Page Content

`get_page_content` returns a file path, not inline. Parse with terminal Python:

```python
terminal(command=\"python3 -c \\\"
import json
with open('<file_path>', 'r') as f:
    data = json.load(f)
d = data['data']
print('url:', d['url'])
for line in d['text'].split('\\\\n'):
    line = line.strip()
    if any(kw in line for kw in ['AM', 'PM', 'Jun', 'availability']):
        print(repr(line))
\\\"\")
```

**File size warning**: Square availability pages can produce files up to **~3MB**. If `get_page_content` times out (120s), the browser has crashed post-Book — use last_known data. For very large files, extract only the `data.text` field to minimize parsing time:

```python
terminal(command=\"python3 -c \\\"
import json, re
with open('<file_path>', 'r') as f:
    d = json.load(f)['data']
text = d['text']
slots = re.findall(r'\\d{1,2}:\\d{2}\\s*(?:AM|PM)', text)
print(f'{len(slots)} slots:', slots[:5], '...')
\\\"\")
```

## Stealth Browser MCP Server Unreachable — Full Transport Failure (2026-06-08)

The stealth browser MCP server can become entirely unreachable — not just a CDP connection drop within a browser instance, but the MCP transport itself refuses new browser spawns. This is a distinct failure mode from the CDP connection drop documented below.

**Symptom:**
```
mcp_stealth_browser_spawn_browser(headless=True)
→ "Failed to connect browser"
→ "One of the causes could be when you are running as root.
   In this case you need to pass no_sandbox=True"
```

**Attempted fixes that did NOT work:**
- `sandbox=False` → Pydantic validation error (`Unexpected keyword argument`)
- `browser_args=["--no-sandbox"]` → Still fails with same root/sandbox error
- Retry → After 3 consecutive failures, MCP server marked "unreachable" with ~49s auto-retry cooldown

**Root cause:** The stealth browser MCP server's `spawn_browser` tool does not properly expose the `no_sandbox` parameter at the schema level despite the error message suggesting it. When running as root (common in Docker/VM/cron deployments), Chromium's sandbox requirement causes spawn to fail.

**Fallback: Switch to Hermes browser immediately.** As of 2026-06-08, the Hermes browser (`browser_navigate` / `browser_click` / `browser_snapshot`) successfully executed the full Square booking flow end-to-end as a fallback:
- Square SPA hydrated on first navigate (no empty-page issue)
- All interactions (service select → duration → staff → Book → calendar → date click → slot reading) worked via `browser_click` on snapshot refs
- No post-Book crash observed
- Clean data returned (15 slots, 7 in target window)

**Decision rule for cron sweeps:** If `spawn_browser` fails once, switch to Hermes browser immediately. Do NOT retry stealth browser more than once per sweep.

**Hermes browser confirmed as full Square flow replacement (2026-06-08 21:08 PT cron sweep):** When the stealth browser MCP server is entirely unreachable (3 consecutive spawn failures → "MCP server unreachable"), the Hermes browser successfully executes the COMPLETE Square booking flow as a replacement:
- `browser_navigate` → Square services page loads (SPA hydrates on first navigate)
- `browser_snapshot` → service list with clickable refs
- `browser_click` service ref → duration/staff page
- `browser_click` duration ref → duration selected
- `browser_click` "Any staff" ref → staff selected (may require snapshot verification + re-click)
- `browser_click` Book button ref → calendar page loads
- `browser_snapshot` → find "Next week" button ref
- `browser_click` "Next week" → advance calendar (repeat until target date visible)
- `browser_click` target date ref (e.g., "Friday 19") → date selected
- `browser_snapshot` → time slot buttons rendered, grouped Morning/Afternoon/Evening
- No JS fallbacks, no `execute_script`, no stealth browser needed for ANY step
- Post-sweep: `browser_back` may fail with CDP 502 if browser process already expired — this is harmless, no data lost

This confirms the Hermes browser as a fully capable standalone Square automation tool, not just a fallback for individual steps.

**Spawn-succeeds-but-navigate-fails variant (2026-06-06):** `mcp_stealth_browser_spawn_browser` can return `{"state": "ready"}` successfully, but the subsequent `mcp_stealth_browser_navigate` call fails with `[Errno 111] Connect call failed ('127.0.0.1', <port>)`. This means the MCP transport itself is down — the spawn response was stale/cached or the transport died between spawn and navigate. **Treat this identically to a spawn failure: switch to Hermes browser immediately. Do NOT retry `spawn_browser` or `navigate`.** The stealth browser MCP server is unreachable for this sweep.

## Stealth Browser CDP Connection Drop (2026-06-06)

The stealth browser can suffer CDP connection drops mid-flow: `query_elements` succeeds but `click_element` fails with `[Errno 111] Connect call failed ('127.0.0.1', <port>)`. This is distinct from the Hermes browser's CDP 502 — it's a wholesale connection loss.

**Pattern:**
```
query_elements(selector="market-row") → success, returns elements
click_element(selector="market-row", text_match="...") → [Errno 111] Connect call failed
```

**Recovery**: Spawn a NEW stealth browser instance (don't try to reconnect to the old one). The spawn is fast (~2s) vs Hermes kill+restart (~35-50s).

```
mcp_stealth_browser_spawn_browser(headless=true, sandbox=false) → new instance_id
mcp_stealth_browser_navigate(new_instance_id, url) → re-navigate
...continue flow from step 3 (query_elements)...
```

**Do NOT fall back to Hermes browser** — just restart the stealth browser. It will load the page on the first navigate. The stealth browser's connection drops are transient; a new instance resolves the issue.

**Note**: This means the stealth browser is NOT more reliable than Hermes for CDP stability — it just fails differently (connection drop vs post-Book console timeout). However, recovery is much faster (spawn new instance: ~5s vs kill+restart: ~35-50s), so stealth browser remains the recommended primary for Square.

### CDP Drop After Staff Click (2026-06-06 20:56 PT)

A CDP connection drop was observed **after** the "Any staff" `[role='option']` click returned `true` but **before** the "Book" `market-button` click could be attempted. The sequence was:

```
click_element(selector="market-row", text_match="Swedish Massage") → true
click_element(selector="[role='option']", text_match="1.5 Hours") → true
click_element(selector="[role='option']", text_match="Any staff") → true
query_elements(selector="[role='option']") → [] (empty — page transitioning or CDP dropped)
get_page_content(instance_id) → [Errno 111] Connect call failed
```

**Recovery**: Closed dead instance, spawned new one, re-ran full flow. On the retry, the flow completed with rapid sequential clicks (service → duration → staff → Book without intermediate `query_elements` verification between each click). All 4 clicks returned `true`, and `get_page_content` succeeded (2.99MB file).

**Lesson**: The intermediate verification step (querying `[role='option']` to check `aria-selected` after each click) may widen the window for CDP drops. In cron mode, consider using the rapid sequential click pattern (click service → click duration → click staff → click Book → get_page_content) without intermediate verification. The post-Book `get_page_content` result is the ultimate verification — if it returns data, all clicks landed.

## Stealth Browser Post-Book Crash Variant (2026-06-06)

After clicking Book in the Square flow, `get_page_content()` can time out (120s) — this is the stealth browser's equivalent of the Hermes browser's post-Book crash. ALL Square interactions (service click, duration click, staff setAttribute, Book click) completed successfully via `execute_book` before the crash.

**Pattern:**
```
execute_script(click service + duration + staff + Book) → success, bookClicked: true
get_page_content(instance_id) → TimeoutError: MCP call timed out after 120.0s
navigate(instance_id, "about:blank") → TimeoutError (browser is dead)
close_instance(instance_id) → success
```

**Decision**: `get_page_content` timeout post-Book → use last_known data. Spawn a new stealth browser and re-navigate to confirm whether it's a browser death or transient.

**Recovery**: Close dead instance, spawn new one, test navigate. Do NOT attempt to reconnect to the old instance.

**Both browsers can exhibit post-Book crash patterns** — Hermes via CDP 502 / console timeout, stealth via `get_page_content` timeout. However, the stealth browser has completed consecutive clean sweeps without post-Book crashes (2026-06-06 18:50 PT — service click, duration, staff, Book, get_page_content all succeeded; 2.99MB page returned cleanly). The stealth browser's advantage is both speed of spawning a new instance (~5s vs ~45s for Hermes kill+restart) and apparently better post-Book stability in recent sessions.

## Key Differences from Hermes Browser

- `execute_script` returns structured key-value pairs (not null) — usable for multi-step JS, but `query_elements` + `click_element` remain primary for state verification
- Page content via file path, not inline
- `click_element` with `text_match` works on Square custom elements
- No SPA hydration failures observed — pages load reliably on first navigate
- Works as root with `sandbox=false`
- Can be spawned mid-sweep when Hermes browser crashes on a specific interaction (not just at sweep start)
- Faster recovery than Hermes browser kill+restart: spawn (~2s) + navigate (~3s) = ~5s vs kill+restart+wait = ~35-50s

## SevenRooms Pattern (Verified 2026-06-05)

SevenRooms widget pages (`sevenrooms.com/explore/<venue>/reservations/create/search`) embed availability state directly in the **initial HTML** — no SPA interaction needed.

**Pattern:** `navigate(url)` → wait for `networkidle` → `get_page_content()` → parse `text` field

The `text` field from `get_page_content` contains the full reservation state. For availability checks, simply search for:
- `"There is no availability that meets your search criteria."` = fully booked
- `"There is no additional availability at this time."` = no other dates either
- Time slot buttons rendered as text = available slots

This avoids all SPA JS interaction issues entirely. Only use `query_elements` + `click_element` when actually making a reservation (e.g., clicking "Book" on a specific slot).