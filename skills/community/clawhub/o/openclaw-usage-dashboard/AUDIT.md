# OpenClaw Usage Dashboard v2.0 — Pre-Release Audit

**Auditor:** Quality Agent (Senior Developer)  
**Date:** 2026-03-27  
**Files audited:** `server.js`, `dashboard.html`  
**Verdict:** ✅ Ready to publish (after fixes applied below)

---

## Summary

Overall, this is well-built code with solid security fundamentals — no raw secrets exposed, proper HTML escaping, localhost-only binding, and good defensive limits. The audit found **9 issues** (2 critical, 3 moderate, 4 minor), all of which have been fixed in-place.

---

## Issues Found & Fixed

### 🔴 Critical

#### C1. `modelIds` ReferenceError in chart tooltip handler
**File:** `dashboard.html` (inside `drawChart`)  
**Problem:** The `canvas.onmousemove` tooltip handler referenced `modelIds`, but `drawChart` is a standalone function — `modelIds` is only a parameter of `renderTimeline`, not in `drawChart`'s scope. Hovering over the chart would throw a `ReferenceError` every time.  
**Fix:** Added `const chartModelIds = series.filter(s => !s.dashed && !s.id.startsWith('agent:')).map(s => s.id)` at the top of `drawChart`, and replaced `modelIds` with `chartModelIds` in the tooltip handler.

#### C2. `getAgentColor()` returns `undefined` for unknown agents
**File:** `dashboard.html`  
**Problem:** When `dashData` is null or an agent ID isn't in `agentStats`, `keys.indexOf(id)` returns `-1`. `AGENT_PALETTE[-1 % 8]` evaluates to `AGENT_PALETTE[-1]` which is `undefined`. This would render `style="color:undefined"` in CSS — invalid/broken.  
**Fix:** Added `if (idx < 0) return AGENT_PALETTE[0]` fallback.

### 🟡 Moderate

#### M1. XSS via single quotes in `esc()` function
**File:** `dashboard.html`  
**Problem:** `esc()` escaped `<`, `>`, `&`, `"` but NOT single quotes. Since legend items use `onclick="toggleSeries('...')"` with single-quoted IDs, a model ID containing `'` could break out of the handler — an XSS vector.  
**Fix:** Added `.replace(/'/g,'&#39;')` to `esc()`.

#### M2. CSP allows `unsafe-eval` unnecessarily
**File:** `server.js`  
**Problem:** Content-Security-Policy included `'unsafe-eval'`, but no code uses `eval()`, `Function()`, or `setTimeout(string)`. This unnecessarily weakens CSP.  
**Fix:** Removed `'unsafe-eval'` from the CSP directive. `'unsafe-inline'` is still needed for the inline `<script>` and `<style>`.

#### M3. Windows `wmic` deprecated/removed
**File:** `server.js`  
**Problem:** Disk free space on Windows used `wmic logicaldisk`, which is deprecated in Windows 10 and removed in Windows 11. Would silently fail.  
**Fix:** Added PowerShell `(Get-PSDrive C).Free` as the primary method, with `wmic` as fallback for older systems.

### 🟢 Minor

#### m1. `vm_stat` page size hardcoded to 16384
**File:** `server.js`  
**Problem:** Page size was hardcoded to 16384 (Apple Silicon). Intel Macs use 4096-byte pages. Memory calculation would be 4x too high on Intel.  
**Fix:** Parse page size from `vm_stat` output header (`page size of N bytes`), fall back to 16384.

#### m2. Double-escaped HTML in tooltip model breakdown
**File:** `dashboard.html`  
**Problem:** `modelBreakdown` was already built with `esc()` on each model name, then wrapped again with `esc(modelBreakdown)`. Characters like `&` would render as `&amp;amp;`.  
**Fix:** Removed the outer `esc()` since the inner values are already escaped.

#### m3. `openclaw version` shell command not Windows-compatible
**File:** `server.js`  
**Problem:** Used `||` and `2>/dev/null` (bash syntax) with `shell: true`, which on Windows invokes `cmd.exe` where these don't work.  
**Fix:** Split into two separate `try/catch` blocks, each calling one variant without shell redirection.

#### m4. Dead code cleanup
**Files:** `server.js`, `dashboard.html`  
- **`CHUNK_SIZE = 200`** (server.js) — defined but never used. Removed.
- **`const alpha`** (dashboard.html, `renderHeatmap`) — computed but never used. Removed.
- **`const labels = ''`** (dashboard.html, `renderHeatmap`) — assigned but never used. Removed.
- **Heatmap color ternary dead branch** — `pct > 0.4 ? '56,189,248' : '56,189,248'` — both branches identical. Simplified to just `'56,189,248'`.

---

## Issues Noted (Not Fixed — Acceptable for v2.0)

### N1. Synchronous file I/O on every API request
`getAllSessionFiles` and `parseSessionFile` use `fs.readFileSync`/`fs.readdirSync`. For a local single-user dashboard this is fine — the `MAX_SESSIONS` (2000) and `MEMORY_BUDGET_MB` (100) limits prevent catastrophic blocking. Consider async I/O for v3 if scaling to multi-user.

### N2. `parseInt()` without radix parameter
Multiple `parseInt()` calls omit the radix argument. All inputs are known decimal strings from regex captures of `\d+`, so this is functionally safe. Purely a lint-level concern.

### N3. `sanitizeEntry()` / `sanitizeText()` defined but unused
These functions exist as defensive code for future config sanitization. The current code only exposes numeric aggregates (never raw log content), so they're not needed today. Kept as defense-in-depth.

### N4. `configInfo` variable assigned but never read
Populated in `loadConfig()` but never referenced elsewhere. Presumably reserved for future features. Harmless.

### N5. Auto-refresh interval not configurable
The 5-minute auto-refresh is hardcoded in dashboard.html. Not a problem, but could be a `--refresh-interval` flag for power users.

---

## Checklist Results

| Category | Status |
|---|---|
| **macOS** | ✅ Works (with vm_stat page size fix) |
| **Linux** | ✅ Works (os.freemem fallback is fine) |
| **Windows** | ✅ Works (PowerShell + wmic fallback, separate version commands) |
| **Node 18/20** | ✅ All features compatible (optional chaining since v14, catch binding since v10) |
| **Port configurable** | ✅ `--port` CLI flag with clear error on EADDRINUSE |
| **No secrets leaked** | ✅ `getConfig()` extracts only model metadata, never keys/tokens |
| **XSS protection** | ✅ `esc()` covers all 5 HTML special chars; `textContent` used for error messages |
| **Path traversal** | ✅ No user-controlled file paths in serving logic |
| **CORS** | ✅ Restricted to `http://localhost:PORT` |
| **CSP** | ✅ Tightened (removed `unsafe-eval`) |
| **Error handling** | ✅ All file ops wrapped in try/catch, graceful fallbacks |
| **Edge cases** | ✅ 0 data, 1 bucket, null dashData all handled |

---

## Files Modified

- `server.js` — 5 surgical edits
- `dashboard.html` — 6 surgical edits
- `AUDIT.md` — this file (new)
