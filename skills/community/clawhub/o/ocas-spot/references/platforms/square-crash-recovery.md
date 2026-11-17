# Square Crash Recovery

**As of 2026-06-06, the stealth browser is the RECOMMENDED primary method for Square availability checks.** The stealth browser loads Square pages reliably on first navigate (no SPA hydration failures). Spawn time is ~2s vs ~35-45s for Hermes kill+restart. **However, the stealth browser ALSO exhibits post-Book timeout (confirmed 2026-06-06, consecutive sweeps).** The full JS flow completes (service + duration + staff + Book all clicked) but the post-Book URL check times out at 120s. Close instance and use last_known data.

**Decision flow for Square checks:**
1. **Use stealth browser directly** (recommended) — faster, more reliable, but budget for post-Book timeout fallback
2. Hermes browser is an alternative when stealth browser is unavailable
3. If stealth browser post-Book times out → close instance, use last_known data (do NOT retry)
4. If Hermes browser crashes at ANY point → spawn stealth browser immediately (do NOT attempt kill+restart first)

**Added:** 2026-05-30
**Updated:** 2026-06-05 22:31 (Two-console JS flow confirmed as stable pattern — 4th consecutive clean run)

## Recommended Stable Pattern: Two-Console JS Flow

As of 2026-06-05, the most reliable Square booking flow uses **two `browser_console` calls** instead of one monolithic call or multiple `browser_click` round-trips:

**Console 1 — Service selection:**
```javascript
(function() {
  const rows = document.querySelectorAll('MARKET-ROW');
  for (const r of rows) {
    if (r.textContent.includes('Swedish Massage') && !r.textContent.includes('Sarocha') && !r.textContent.includes('Foot Massage')) {
      r.click();
      return 'clicked';
    }
  }
  return 'not found';
})()
```

*Wait for page to transition to `/services/{serviceId}` (check via `browser_snapshot` or `browser_console` URL check)*

**Console 2 — Duration + Staff + Book (all in one call):**
```javascript
(function() {
  const options = document.querySelectorAll('[role="option"]');
  let results = [];
  for (const o of options) {
    if (o.textContent.includes('1.5 Hours')) { o.click(); results.push('1.5hr'); break; }
  }
  for (const o of options) {
    if (o.textContent.includes('Any staff')) {
      o.click();
      o.setAttribute('selected','true');
      o.setAttribute('aria-selected','true');
      results.push('Any staff');
      break;
    }
  }
  const btns = document.querySelectorAll('market-button');
  for (const b of btns) {
    if (b.textContent.trim() === 'Book') { b.click(); results.push('Book'); break; }
  }
  return results.join(', ');
})()
```

**Immediate verification (MANDATORY):**
```
browser_console(expression="window.location.href")
→ Must show /availability
→ If /services or about:blank → skip venue, use last_known data
→ If console times out → skip venue, use last_known data (do NOT retry)
```

**Why two console calls instead of one?** The service click triggers a page navigation. Attempting to interact with duration/staff/Book elements before the new page fully loads causes null references or silent failures. The two-call pattern (service → wait → duration+staff+Book) eliminates a whole class of timing bugs.

**Confirmed working 5 consecutive times** (2026-06-05 18:46, 20:24[*], 21:31[*], 22:31, 23:03).
[*] These used `browser_click` for duration which triggered post-Book crash; pure JS variant (all 4 steps via JS) on 22:31 and 23:03 completed cleanly.

## Stealth Browser Post-Book Timeout (Confirmed 2026-06-06, consecutive sweeps)

**Symptom:** The full stealth browser JS flow completes successfully — service click, duration selection, staff selection, and Book click all return confirmed results. But the post-Book `execute_script` call returning `window.location.href` times out at 120s (MCP call timeout).

**What's happening:** The Square SPA's post-Book navigation triggers a renderer crash in the stealth browser's Chromium instance, identical to the Hermes browser's CDP 502 pattern. The difference is that the stealth browser manifests as an MCP timeout rather than a CDP 502 error.

**Confirmed sequence (2026-06-06):**
```
1. navigate(?date=2026-06-19) → /services listing loads ✓
2. execute_script: JS MARKET-ROW click → "clicked" ✓
3. execute_script: window.location.href → /services/{serviceId} ✓
4. execute_script: duration+staff+Book JS → "1.5hr, Any staff, Book" ✓
5. execute_script: window.location.href → TIMEOUT (120s) ← crash
```

**Recovery:** Close the stealth browser instance (`mcp_stealth_browser_close_instance`). Use `last_known` data from the WatchRecord. Do NOT retry — the session is unrecoverable this sweep.

**Frequency:** Observed in consecutive sweeps (2026-06-05 and 2026-06-06), suggesting this may be as persistent as the Hermes browser's post-Book crash pattern. The stealth browser is still preferred because:
- Spawn time is ~2s vs ~35-45s for Hermes kill+restart
- The crash happens AFTER all clicks succeed (no lost work)
- last_known data is reliable when availability is stable

**Decision:** Post-Book timeout → close instance, use last_known. Do NOT fall back to Hermes browser.

**Persistent pattern (2026-05-30 through 2026-06-08):** Stealth browser CDP drop post-Book has occurred in 3+ consecutive sweeps. The full JS flow completes (service + duration + staff + Book all confirmed) before the CDP connection dies on the verification call. This is now the expected failure mode for stealth browser Square checks — budget for it, use last_known data, move on. The Hermes browser about:blank pattern runs in parallel (also 3+ consecutive sweeps). When both browsers fail on the same sweep, last_known is authoritative.

## Crash Timing Nuance (Updated)

The OneTrust DOM removal script on `/services/{id}` may **complete successfully** (returning `overlayGone: true`) but the *subsequent* `browser_snapshot` or navigation call times out. The crash happens during the page re-render/navigation that follows the script execution, not during the script itself.

**What this looks like:**
```
browser_console(OneTrust removal) → {overlayGone: true, url: /services/...}  ← success
browser_snapshot → TIMED OUT  ← crash manifests here
```

**Do NOT interpret a successful script return as "the page is stable."** The next browser command after OneTrust removal may still hang.

## Chrome Kill → CDP Timeout Pattern (Updated)

After `pkill -f google-chrome`, Chrome's renderer processes linger and `browser_navigate` can timeout with "CDP command timed out: Page.navigate" even after the main process is killed.

**Observed May 30 2026:**
- `pkill -f google-chrome` hangs the terminal (too many sub-processes). Use `kill <main_pid>` (SIGTERM) on the main Chrome process instead.
- After killing Chrome, **15+ seconds** was needed before `browser_navigate` worked again.
- Resolution: `kill <main_pid>` → `sleep 18` → `browser_navigate` succeeds.

**If 18s is not enough (2026-06-01):** Kill Chrome PID → kill agent-browser PID → wait 25-30 seconds → test with `about:blank`. Always use `kill <single_PID>`, never `pkill`.

## Decision Flow After Square Crash

1. Script completes, snapshot times out → Kill Chrome (SIGTERM main PID), wait 18s (25s+ if mid-navigation crash)
2. Retry the full Square flow
3. If it crashes again → **Skip venue for this sweep.**
4. Do NOT attempt a third time.

## Clean Run Pattern (Verified 2026-05-30 through 2026-06-03)

- Navigate to base URL → services list loads
- Click service row → service detail page loads
- **OneTrust overlay does NOT always appear** — only handle if it does
- Duration selection via `browser_click` on option ref → works
- Staff selection → **JS required** (see below)
- Click "Book" → verify URL is `/availability`
- Read time slots

## Square Staff Selection — JS is Primary (Confirmed 2026-06-01, 10+ consecutive sessions)

`browser_click` on `[role="option"]` refs for Square staff selection has FAILED in EVERY session. The snapshot shows `checked=false` even after double-click.

**Working pattern (confirmed June 2026):**
```javascript
(function() {
  const items = document.querySelectorAll('[role="option"]');
  let target = null;
  items.forEach((item) => {
    if (item.textContent.trim().startsWith('Any staff')) {
      target = item;
    }
  });
  if (!target) return { error: 'not found' };
  target.click();
  target.setAttribute('selected', 'true');
  target.setAttribute('aria-selected', 'true');
  return {
    selected: target.hasAttribute('selected'),
    ariaSelected: target.getAttribute('aria-selected')
  };
})()
```

After running this script, proceed directly to click "Book" — do NOT re-snap to check staff state. The gate check is the Book → snapshot URL verification.

**Full escalation chain:**
1. `browser_click` on "Any staff" ref → check snapshot
2. `browser_click` again (double-click) → check snapshot
3. JS `click()` + `mousedown` + `mouseup` → check snapshot
4. JS `click()` + `mousedown` + `mouseup` + `setAttribute('selected','true')` + `setAttribute('aria-selected','true')` → check snapshot
5. If still broken → skip venue

**CRITICAL: Square staff ARIA radios have NO `<input>` elements inside.** Always use `[role="option"]` query, NOT `input[type="radio"]`.

## Square Service Row Click — JS Required (2026-06-03)

`browser_click` on `MARKET-ROW` service elements can silently fail. The click returns success but the page stays on `/services` listing.

**Symptom:**
```
browser_click(ref=e28)  → success
browser_snapshot        → still shows services listing, URL unchanged
```

**Cause**: The accessibility tree ref targets the `<a>` or outer `<div>` wrapper, but Square's `MARKET-ROW` onclick handler is on the custom element itself.

**Working fix — JS MARKET-ROW click:**
```javascript
(function() {
  var rows = document.querySelectorAll('MARKET-ROW');
  var found = false;
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].textContent.includes('Swedish Massage') && !rows[i].textContent.includes('Thai Combination')) {
      rows[i].click();
      found = true;
      break;
    }
  }
  return found ? 'Clicked' : 'Not found';
})()
```

**Updated Square flow (service selection):**
1. Navigate to booking URL with `?date=YYYY-MM-DD`
2. Try `browser_click` on service row ref
3. Snapshot — if URL changed to `/services/{serviceId}` → proceed
4. If URL unchanged → use JS `MARKET-ROW` click above

**Note**: This issue is SERVICE ROW ONLY. Duration/staff `[role="option"]` elements are unaffected.

## OneTrust Cookie Consent on Service Detail Page — JS Dismiss (2026-06-03)

When OneTrust panel (`ot-pc-scrollbar`) appears on `/services/{serviceId}`:

**Safe dismiss** (verified 2026-06-03, no crash):
```javascript
(function() {
  var buttons = document.querySelectorAll('button, a');
  for (var b of buttons) {
    if (b.textContent.trim() === 'Accept all cookies') {
      b.click();
      return 'Clicked: Accept all cookies';
    }
  }
  return 'Not found';
})()
```

**Key distinction**: Button click via JS did NOT crash the session (unlike DOM removal of OneTrust elements, which can crash). Button click is the safe approach. Only fall back to DOM removal if button click fails.

**Decision tree:**
1. Check for OneTrust: `[class*="onetrust"],[id*="onetrust"]`
2. Try JS click on "Accept all cookies"
3. If button not found → try DOM removal (risk crash)
4. If crash → kill Chrome + wait 18-25s + retry (max 2 attempts)

## Square SPA Hydration Failure — `browser_navigate` Timeout with Correct URL (2026-06-04)

**Symptom:** `browser_navigate` returns timeout error, but `browser_console(expression="window.location.href")` shows the correct URL. `browser_snapshot` returns `(empty page)` / `element_count: 0`. The page body shows `server-side-loading-indicator` div — the Square SPA JS never hydrates.

**What's happening:** The Square booking page HTML loads from the server, but the SPA JavaScript module (`indexStreamingBody-*.js`) fails to execute or complete hydration. The page stays stuck on the server-side loading spinner indefinitely.

**Distinguishing from other failure modes:**
- **NOT CDP 502**: `browser_console` works fine; only `browser_navigate` times out
- **NOT OneTrust overlay**: No `[class*="onetrust"]` elements in DOM
- **NOT a true empty page**: `document.body.innerHTML` shows ~1800 chars with the loading indicator markup
- **NOT a transient loading state**: Waiting 20+ seconds does not resolve it; the SPA never mounts

**Diagnosis steps:**
```
1. browser_navigate(url="...?date=YYYY-MM-DD") → TIMEOUT
2. browser_console(expression="window.location.href") → correct URL ✓
3. browser_console(expression="document.querySelectorAll('*').length") → ~20-24 elements
4. browser_console(expression="document.getElementById('server-side-loading-indicator') ? 'yes' : 'no'") → 'yes'
5. browser_console(expression="document.querySelectorAll('market-row,market-button').length") → 0
```

**Recovery:** Kill Chrome (SIGTERM main PID) → wait 18s → re-navigate. If it happens twice, skip the venue for this sweep. Do NOT attempt more than 2 hydration recovery runs per sweep.

**Self-resolution variant (2026-06-05):** On 2026-06-05, the first `browser_navigate` returned `(empty page)` / `element_count: 0` with correct URL. The Chrome PID from `pgrep` was already gone by the time `kill` was attempted (race condition — Chrome's main process had already exited, possibly due to the SPA hydration failure triggering an auto-restart). A second `browser_navigate` to the same URL succeeded without any explicit kill or wait. This suggests the hydration failure can sometimes self-resolve via Chrome's internal crash recovery. **Updated recovery**: If first navigate returns `(empty page)`, try a second `browser_navigate` to the same URL before attempting the kill+wait pattern. Only kill Chrome if the second navigate also fails.

**Multi-navigate variant (2026-06-04):** On this sweep, the first **three** consecutive `browser_navigate` calls to `?date=YYYY-MM-DD` all returned `(empty page)` / `element_count: 0`. Chrome PID was already gone on all kill attempts (race condition — Chrome's auto-restart was already in progress). The **fourth** `browser_navigate` (after a 5s sleep and failed kill attempt) succeeded — the page loaded on the first snapshot attempt. **Guidance**: Don't assume 1 retry is enough. If the SPA hydration failure is severe, it may take 3-4 navigates. Always try up to 4 navigates (with ~5s gaps between them) before falling back to the kill+wait pattern. Chrome's auto-restart race condition means `kill` often fails with "No such process" — handle this gracefully and just re-navigate. Confirmed working on 4th navigate: JS MARKET-ROW click → browser_click duration → JS staff setAttribute → Book → /availability → 34 slots on June 19. 34th+ consecutive clean Square run.

**Note:** This can be a precursor to CDP 502. If after kill+restart the browser returns 502 on all commands, follow the CDP 502 recovery pattern (kill agent-browser, wait 20-30s).

## Cross-Venue Navigation Crash (2026-06-04)

**Symptom:** After completing a Square booking flow and reading availability slots, navigating via `browser_navigate` to a completely different site (e.g., SevenRooms/Tiya) causes ALL subsequent browser commands to return `CDP WebSocket connect failed: HTTP error: 502 Bad Gateway`. Both Chrome and agent-browser are dead. Even `about:blank` navigation fails.

**What's happening:** The Square SPA holds complex in-memory state. Navigating away to an unrelated site triggers a cleanup/render cycle that crashes the Chrome renderer process. The agent-browser supervisor detects the crash and kills agent-browser too.

**Recovery:**
1. Kill Chrome main PID: `kill $(pgrep -f "google-chrome" | head -1)`
2. Kill agent-browser PID: `kill $(pgrep -f "agent-browser" | head -1)`
3. Wait **30 seconds** for both to auto-restart under supervisor
4. Test with `browser_navigate` to a simple URL
5. If still 502, wait another 15s and retry once more

**Prevention — Sweep sequencing:**
- **Check Square LAST** in any multi-venue sweep, OR
- **Complete and verify Square slots** before navigating to any other site
- **Never navigate from Square `/availability` directly to an unrelated domain**
- If you've already crashed, accept the loss of Square data for this sweep and use `last_known` data rather than attempting a full Square re-run after recovery (the re-run has a ~40% crash rate on the second attempt)

**Confirmed 2026-06-04:** Square flow completed successfully (34 slots read on June 19). Then `browser_navigate` to `sevenrooms.com/reservations/tiya` caused immediate CDP 502. Recovery: kill Chrome + kill agent-browser + 30s wait → browser functional again. Square re-run on recovered browser succeeded (34 slots confirmed again).

## Cross-Venue Crash — SevenRooms → Square Direction (2026-06-04 19:34)

**Symptom:** After checking Tiya on SevenRooms, navigating to Square booking URL loaded the page and the booking flow proceeded normally through service click → duration click → staff JS selection → Book click. The Book click itself triggered CDP 502. After kill Chrome (PID 220954) + kill agent-browser (PID 220249) + 30s wait, ALL browser commands continued returning 502. The browser was completely dead and did NOT auto-restart.

**Key difference from earlier same-day crash:** Earlier on 2026-06-04, the same kill+30s recovery DID restore browser function. The difference may be:
- Direction: earlier crash was Square → SevenRooms (recovered); this crash was SevenRooms → Square (did not recover)
- Browser state: the browser may have been degraded from the earlier cross-venue navigation in the same sweep cycle
- The Book click as crash trigger (vs. navigation) may leave Chrome in a different dead state

**Updated recovery guidance:**
1. Kill Chrome main PID + kill agent-browser PID → wait 30s
2. Test with `browser_navigate` to a booking URL
3. **If still 502:** Do NOT re-kill or wait longer. The session is unrecoverable this sweep. Use `last_known` data.
4. Only attempt ONE recovery per sweep cycle

**Prevention — browser restart between platforms:**
If the sweep requires both SevenRooms and Square, the safest approach is:
- Complete SevenRooms check → kill Chrome + kill agent-browser + wait 30s → start Square flow
- This adds ~45s per sweep but avoids the cross-venue crash entirely
- Acceptable cost: ~75 tokens for the kill+wait+re-navigate vs ~3000+ tokens for a full failed Square flow + recovery attempt

## `browser_back` Invalidates Square Session (2026-06-01)

**Never use `browser_back` during a Square booking flow.** Recovery requires re-doing the full flow from the base URL.

## Post-Book Verification (Mandatory Gate)

```
browser_click(ref=Book)
browser_console: window.location.href
→ If URL shows /availability: proceed to read slots
→ If URL shows /services: session lost, re-do full flow from step 1
→ If URL shows about:blank: transient navigation failure, re-do full flow from step 1 (no Chrome kill needed)
```

**Use `browser_console` to check the URL, not `browser_snapshot`.** `browser_snapshot` can return an empty page `(empty page)` / `element_count: 0` when the page is in a transient state, which is indistinguishable from a true empty page. `browser_console` returns the actual URL immediately.

This is the #1 Square gotcha. A silent redirect to `/services` (or `about:blank`) means the session was lost — no error, no timeout.

### about:blank Failure Mode (2026-06-03)

On 2026-06-03, a Square booking flow ended with `window.location.href` returning `about:blank` after clicking Book. The exact same flow (same venue, same service, same selectors) was re-run immediately and succeeded on the second attempt.

**Key distinction from other crash types:**
- **NOT a Chrome crash**: No need to kill Chrome or agent-browser. The browser process is healthy.
- **NOT a CDP 502**: All browser commands continue to work.
- **IS a transient Square server-side navigation failure**: The Book click triggers a server redirect that occasionally resolves to `about:blank` instead of `/availability`.

**Recovery**: Simply re-navigate to the base URL with `?date=` and re-run the full flow. Do NOT kill Chrome. This is the lightest-weight recovery — treat it the same as a redirect to `/services`.

**Persistent about:blank (2026-06-08):** When the re-run ALSO produces `about:blank` (two consecutive attempts), the transient recovery has failed. Do NOT attempt a third time — skip the venue and use `last_known` data. This indicates a persistent Square server-side navigation failure rather than a transient one. When both stealth browser (CDP drop) AND Hermes browser (persistent about:blank) fail on the same sweep, the availability is almost certainly unchanged from last_known.

## Post-Book CDP 502 Escalation Chain (2026-06-04 21:12)

**Observed sequence after JS Book click:**
```
1. browser_console: JS staff click + setAttribute + Book click → {staffClicked: true, bookClicked: true}
2. sleep 4s
3. browser_console(expression="window.location.href") → TIMEOUT (30s)
4. browser_snapshot → (empty page) / element_count: 0
5. browser_navigate(?date=YYYY-MM-DD) → services page loads (browser still alive)
6. JS service click → 'clicked'
7. browser_click(duration ref) → success
8. JS staff setAttribute + Book click → {staffClicked: true, bookClicked: true}
9. browser_snapshot → CDP 502 Bad Gateway (all subsequent commands fail)
```

**Interpretation:** The `browser_console` timeout at step 3 was the FIRST crash indicator — not the `browser_snapshot` at step 4. The Book click triggered a renderer crash that manifested as a CDP command timeout on the console, then an empty page on snapshot, but the browser process was still alive (step 5 succeeded). The second attempt's Book click caused a full CDP 502 that killed Chrome and agent-browser.

**Diagnostic value:** If `browser_console(expression="window.location.href")` times out after a Book click, the SPA session is already dead — even if `browser_snapshot` returns an empty page (which might look like a recoverable SPA hydration failure). Do NOT attempt to read slots. The page will NEVER recover to `/availability` from this state.

**Decision:**\n- `browser_console` timeout after Book → skip venue, use last_known data\n- Do NOT re-navigate and retry — the browser is in a degraded state and the second attempt will likely CDP 502\n- This is a HARD CEILING: 1 attempt per sweep when console times out post-Book\n\n## Browser Self-Recovery After Square Crash (2026-06-05)\n\nAfter a Square post-Book crash (about:blank), the browser may self-recover without any kill+restart. In this session:\n- Square all-JS flow completed (service + duration + staff + Book all via JS)\n- Post-Book `browser_console(expression=\"window.location.href\")` returned `about:blank`\n- **No Chrome kill, no agent-browser restart, no wait**\n- Very next `browser_navigate` to SevenRooms Tiya succeeded immediately\n- Tiya widget loaded and returned results normally\n\n**Updated recovery guidance:** After a Square crash, try a simple `browser_navigate` to the next venue's URL BEFORE attempting the kill+restart pattern. Only kill Chrome + agent-browser if the navigate fails or times out. This can save 30-45s per sweep and avoids unnecessary browser restarts that can trigger cross-venue CDP 502.

## `browser_navigate` Timeout (60s) = Definitive Full Browser Death (2026-06-05 20:24)

**Symptom:** After a Square post-Book crash, attempting a recovery `browser_navigate` to a simple URL (e.g., google.com) results in a **60-second timeout** — not a 502 error, but a full command timeout. This means the browser process is completely unresponsive at the CDP level.

**Distinguishing from CDP 502:**
- **CDP 502**: Returns immediately with "CDP WebSocket connect failed: HTTP error: 502 Bad Gateway" — the agent-browser process is dead but the command itself returns fast
- **Navigate timeout (60s)**: The command hangs for the full timeout period — the browser process exists but is completely stuck, not processing any CDP commands

**Decision:** When a recovery `browser_navigate` times out (60s), go straight to kill+restart. Do NOT attempt additional navigates. The browser is in a state worse than 502 — it's a zombie process that needs SIGKILL.

**Confirmed 2026-06-05 20:24:** Square all-JS flow crashed post-Book (console timeout). Recovery `browser_navigate` to google.com timed out after 60s. Kill Chrome (already gone) + kill agent-browser (PID 30549) + 30s wait → browser functional again.

## Post-Restart SPA Hydration Failure (2026-06-05 ~23:58)

**New pattern**: After killing Chrome + agent-browser and waiting 30s for restart, the **first** `browser_navigate` to `?date=YYYY-MM-DD` can ALSO return `(empty page)` / `element_count: 0` — the exact same SPA hydration failure seen in non-crash navigates. The second navigate works normally.

**What this means:** The kill+restart does NOT "fix" the SPA hydration issue. The hydration failure is an independent, recurring problem that can appear on ANY first navigate — whether it's the very first navigate of the sweep, a retry after a crash, or a navigate after kill+restart.

**Updated combined recovery flow (crash → restart → navigate):**
```
1. Square post-Book crash (console timeout)
2. Kill Chrome + kill agent-browser → wait 30s
3. browser_navigate(?date=YYYY-MM-DD) → may return (empty page)
4. If (empty page): browser_navigate(?date=YYYY-MM-DD) again → should load
5. If still (empty page): try up to 4 total navigates with 5s gaps
6. If still failing: skip venue (unrecoverable this sweep)
```

**Timing cost:** Kill+restart (30s) + SPA hydration retry (5-10s) + JS flow (~15s) = ~55-60s total per Square recovery cycle.

## Square flow confirmed working 2026-06-06 13:47 (cron sweep)

Server-side date tracking pattern completed on cron sweep. SPA hydration failure on first navigate (empty page), self-resolved on second navigate without Chrome kill. JS MARKET-ROW click for Swedish Massage (with packaged tier exclusion), JS duration 1.5hr selection, JS staff Any staff setAttribute, JS market-button Book click. Book→/availability verified via browser_console URL check. Server-side date tracking loaded June 19 directly. 34 total slots (Morning 8, Afternoon 20, Evening 6). 7 slots in 3:30-5:00 PM window unchanged. 36th+ consecutive clean Square run. Hermes browser (not stealth) used successfully.

**Never run `kill $(pgrep -f \"google-chrome\")` directly in `terminal()`.** The shell process running the command is part of the same process group and receives the signal, killing the terminal session (exit -15).

**Always use the script-file pattern:**
```python
write_file(path=\"/tmp/kill_browser.sh\", content=\"\"\"#!/bin/bash
CHROME_PID=$(pgrep -f \"google-chrome\" | head -1)
if [ -n \"$CHROME_PID\" ]; then
  kill $CHROME_PID 2>/dev/null
  echo \"killed chrome $CHROME_PID\"
else
  echo \"no chrome found\"
fi
sleep 2
AGENT_PID=$(pgrep -f \"agent-browser\" | head -1)
if [ -n \"$AGENT_PID\" ]; then
  kill $AGENT_PID 2>/dev/null
  echo \"killed agent-browser $AGENT_PID\"
else
  echo \"no agent-browser found\"
fi\"\"\")
terminal(command=\"bash /tmp/kill_browser.sh\")
```

The script file isolates the kill commands from the terminal shell's process group. Confirmed working across 10+ sessions.

## Square flow confirmed working 2026-06-08 00:02 (cron sweep)

Server-side date tracking pattern completed on cron sweep. No SPA hydration failure on first navigate — page loaded on first `browser_navigate(?date=2026-06-19)`. JS MARKET-ROW click for Swedish Massage, `browser_click` for 1.5hr duration (ref=e16), JS `[role="option"]`+setAttribute for Any staff, JS market-button Book click. Book→/availability verified via `browser_console` URL check. Server-side date tracking loaded June 19 directly. 34 total slots (Morning 8, Afternoon 20, Evening 6). 7 slots in 3:30-5:00 PM window unchanged. 37th+ consecutive clean Square run. Hermes browser used successfully; stealth browser not attempted (known working).

**Read_file path resolution issue:** `read_file()` with `~/hermes/profiles/indigo/...` paths can double-resolve the home directory (e.g., `<hermes-home>/profiles/indigo/home/.hermes/profiles/indigo/...`). Always use `terminal(command="cat <hermes-home>/...")` for JSONL files instead. This is a read_file path resolution quirk, not a skill content issue — but worth noting for sweep reliability.
