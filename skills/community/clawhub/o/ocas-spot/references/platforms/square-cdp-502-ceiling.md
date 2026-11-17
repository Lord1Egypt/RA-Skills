# Square — Persistent CDP 502 Kill+Restart Ceiling

**Added:** 2026-06-01

## Kill+restart ceiling — maximum 2 attempts

If `about:blank` still returns CDP 502 after the **second** kill+restart cycle, the browser session is unrecoverable for this sweep. Do NOT attempt a third cycle.

**Evidence (2026-06-01):** 5 consecutive kill+restart attempts all returned CDP 502 on `about:blank`. Each attempt: kill Chrome PID → kill agent-browser PID → wait 25-30s → test. All failed. The CDP WebSocket was in a persistent broken state that kill+restart could not fix within the sweep's time budget.

## Procedure

1. Kill Chrome main PID: `kill $(pgrep -f "google-chrome" | head -1)`
2. Kill agent-browser PID: `kill $(pgrep -f "agent-browser" | head -1)`
3. Wait 25-30 seconds
4. Test: `browser_navigate(url="about:blank")`
5. If success → proceed with full Square flow
6. If CDP 502 → repeat steps 1-4 **once more**
7. If still CDP 502 after 2nd attempt → **skip venue**, log `square_status: browser_crash`, use last_known data

## Staff double-click pattern (confirmed again 2026-06-01)

The double-click pattern for Square's "Any staff" selection was confirmed working:
1. `browser_click(ref=AnyStaff)` → snapshot shows `checked=false`
2. `browser_click(ref=AnyStaff)` again → snapshot shows `checked=true` AND `selected`
3. Proceed to click Book

This is now the 4th+ confirmation of this pattern. It is reliable. Always try double-click before escalating to JS fallback.

## Book click → mid-navigation CDP 502 pattern (confirmed 2026-06-01)

A CDP 502 can occur *after* the Book click succeeds, during navigation to `/availability`. Evidence:
1. Service selection: ✅ duration selected (1 Hour, checked=true)
2. Staff selection: ✅ "Any staff" selected (checked=true, selected) via double-click
3. `browser_click(ref=Book)` → returned success
4. `browser_snapshot` → CDP 502 Bad Gateway

The crash happens during the page transition, not during the click itself. After recovery failure, the full flow must be restarted (session state is lost). This is consistent with the "CDP 502 Mid-Navigation Crash" entry in the main crash-recovery doc.