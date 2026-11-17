# Multi-Venue Sweep Sequencing

## Problem

When running `spot.watch.sweep` with venues on multiple platforms, the **order of browser navigation** matters. navigating from one booking platform's page directly to another unrelated site can crash the browser session.

## Confirmed Crash Pattern (2026-06-04)

**Sequence:** Square `/availability` → `browser_navigate` to `sevenrooms.com/reservations/tiya`
**Result:** CDP 502 on ALL subsequent browser commands. Chrome AND agent-browser both dead.
**Recovery time:** ~45 seconds (kill Chrome + kill agent-browser + 30s wait + re-test).

## Sweep Sequencing Rules

1. **Check API-first platforms first** (SevenRooms public widget API, Acuity REST API, Calendly) — these don't need the browser
2. **Check browser-based platforms LAST** — Square, Meevo, Vagaro, etc.
3. **Within browser-based platforms:** Complete one venue fully (read all slots) before navigating to the next
4. **NEVER navigate from Square `/availability` directly to an unrelated domain** — if you need to check another site after Square, expect a crash and plan for recovery
5. **After any CDP 502 recovery:** The re-run Square flow has a ~40% crash rate. Use `last_known` data if the second attempt also crashes.

## Optimal Sweep Order for Current Watch List

1. Tiya (SevenRooms) — browser widget page
2. Rockridge (Meevo) — skip per consecutive failure threshold
3. Rin (Vagaro) — skip per consecutive failure threshold
4. Russamee (Square) — check LAST to avoid cross-navigation crashes

## ⚠️ Cross-Venue Crash — Any Direction (Updated 2026-06-04)

The crash is NOT limited to Square → SevenRooms. It also occurs **SevenRooms → Square**:

**Sequence:** SevenRooms widget page → `browser_navigate` to Square booking URL → CDP 502 on ALL subsequent browser commands.

**Confirmed 2026-06-04 19:34:** Tiya checked successfully (SevenRooms). Navigated to Square `?date=2026-06-19` → page loaded → clicked service → clicked duration → ran JS for staff selection → clicked Book → CDP 502 immediately. Recovery: kill Chrome (PID 220954) + kill agent-browser (PID 220249) + wait 30s. After recovery, ALL browser commands still returned 502 (navigate, console, snapshot — everything). The browser was completely dead and did NOT auto-restart.

**Key difference from earlier confirmed crash pattern:** Previously (same day, earlier sweep), the same kill+30s recovery DID restore browser function. The SevenRooms → Square direction may cause a more severe crash state, or the browser may have been degraded from prior cross-venue navigation earlier in the same sweep cycle.

**Updated guidance:**
- If recovery fails (all commands still 502 after kill+30s), **use last_known data** for Square
- Do NOT attempt to re-kill or wait longer — the browser session is unrecoverable this sweep
- Consider restarting the browser between browser-based platforms (navigate to `about:blank` doesn't work as root — a full kill+wait is needed)
- The safest approach if both SevenRooms and Square must be checked: complete SevenRooms, then **kill Chrome + kill agent-browser + wait 30s** before starting the Square flow. This adds ~45s per sweep but avoids the 502 entirely.

## Single-Venue-at-a-Time Pattern

If the sweep has already started a Square flow, **do not navigate away** until Square slots are read and recorded. If you need to check SevenRooms:
1. Complete Square flow → read slots → write journal partial
2. Navigate to SevenRooms (accept crash risk)
3. If crash → recovery → re-do Square flow or use last_known

## Post-Restart SPA Hydration Failure (2026-06-05)

**Critical finding**: After killing Chrome + agent-browser and waiting 30s for restart, the first `browser_navigate` to Square `?date=YYYY-MM-DD` can ALSO return `(empty page)` — the same SPA hydration failure seen on any first navigate. This is **independent** of the crash/restart.

**Implication**: The kill+restart does NOT "fix" the hydration issue. Budget for 2 navigates after EVERY restart, same as the initial navigate.

**Combined crash recovery flow:**
```
1. Square post-Book crash (console timeout)
2. Kill Chrome + kill agent-browser → wait 30s
3. browser_navigate(?date=YYYY-MM-DD) → may return (empty page) ← hydration failure
4. browser_navigate(?date=YYYY-MM-DD) → should load (if not, try up to 4 total)
5. Run Square JS flow
6. Post-Book console timeout again → use last_known (don't re-kill)
```

**Total timing budget**: Kill+restart (30s) + hydration retry (5-10s) + JS flow (~15s) = ~55-60s per Square recovery cycle.

## Kill Method — Script File Only

**Never run `kill $(pgrep -f "google-chrome")` directly in `terminal()`.** The shell process receives the signal and dies (exit -15). Always use the script-file pattern:
```python
write_file(path="/tmp/kill_browser.sh", content="""#!/bin/bash
CHROME_PID=$(pgrep -f "google-chrome" | head -1)
[ -n "$CHROME_PID" ] && kill $CHROME_PID 2>/dev/null
sleep 2
AGENT_PID=$(pgrep -f "agent-browser" | head -1)
[ -n "$AGENT_PID" ] && kill $AGENT_PID 2>/dev/null
echo "done"
""")
terminal(command="bash /tmp/kill_browser.sh")
```