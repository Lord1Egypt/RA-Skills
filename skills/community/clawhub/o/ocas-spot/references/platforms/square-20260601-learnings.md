# Square — 2026-06-01 Sweep Learnings

## `browser_console` JS click on `[role="option"]` WORKS

**Contradicts earlier skill note:** The SKILL.md gotcha "`browser_console` cannot traverse Square's Shadow DOM" is overly broad. In this session (2026-06-01), the following JS pattern worked:

```javascript
(function() {
  const items = document.querySelectorAll('[role="option"]');
  let durTarget = null;
  let staffTarget = null;
  items.forEach((item) => {
    const text = item.textContent.trim();
    if (text.includes('1 Hour') && text.includes('$100')) durTarget = item;
    if (text.startsWith('Any staff')) staffTarget = item;
  });
  const clickItem = (item) => {
    if (!item) return false;
    item.click();
    item.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
    item.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
    item.setAttribute('selected', 'true');
    item.setAttribute('aria-selected', 'true');
    return true;
  };
  return { durClicked: clickItem(durTarget), staffClicked: clickItem(staffTarget) };
})()
```

**Result:** Both returned true. Subsequent snapshot showed checked=true AND selected on both options, with no "Please select" alerts.

**Lesson:** document.querySelectorAll('[role="option"]') DOES find Square's duration and staff options on the service detail page. The JS click+setAttribute pattern works. However, browser_click on snapshot refs still does NOT work reliably. The escalation chain should be:
1. browser_click on snapshot ref
2. browser_click again (double-click)
3. JS querySelectorAll('[role="option"]') + click+setAttribute (THIS WORKS, use it earlier than step 4)
4. If all fail - skip venue

**Caveat:** May not work on all Square configurations. Tested on Russamee's Square booking page (May-June 2026).

## "Next week" click triggers CDP 503/502

**New crash point:** After successfully reaching the availability page via Book, clicking "Next week" to advance the calendar week triggered a CDP 503 (Service Unavailable) followed by persistent CDP 502 (Bad Gateway) after browser restart.

**Sequence:**
- browser_snapshot - availability page loaded (week of June 1-6) OK
- browser_click(ref="Next week") - CDP 503
- browser_snapshot - CDP 502 (all subsequent commands fail)
- kill Chrome + agent-browser, wait 30s - still CDP 502

**This is distinct from other crash points:**
- Not OneTrust overlay related
- Not Book click related
- Specific to the "Next week" / calendar navigation interaction

## URL date jump confirmed failing (again)

Navigating to /availability?date=YYYY-MM-DD after the full flow silently redirects back to services listing. The only reliable date navigation after Book is:
1. Click day buttons directly (e.g., click "Friday 19" if visible in current week)
2. Click "Next week" buttons (risk of CDP crash)
3. Use server-side date tracking flow (see square-date-targeted-flow.md)

## Kill pattern note

When killing agent-browser + Chrome for CDP 502 recovery, sleep 20 is insufficient - need 30s minimum for CDP WebSocket to re-establish. After restart, Chrome auto-reconnects to agent-browser, but CDP WebSocket takes longer than process startup.