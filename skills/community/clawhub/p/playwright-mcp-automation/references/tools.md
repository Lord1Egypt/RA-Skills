# Playwright MCP Tool Reference

Use this table when deciding which MCP tool to call. Only the most common tools are listed here—call `browser_snapshot` often to keep refs up to date.

| Tool | Typical Use | Key Params / Tips |
| --- | --- | --- |
| `browser_navigate` | Go to a URL. Always the first step after launch. | `url` must be absolute. Wait for load or call `browser_wait_for` if heavy.
| `browser_snapshot` | Get the accessibility tree (preferred over screenshots). | Use before every interaction; pass `filename` to persist Markdown logs.
| `browser_click` | Press a button/link. | Provide `ref` from snapshot + human `element` description. For double clicks, set `doubleClick=true`.
| `browser_type` | Type into an input. | Provide `ref`, text, optional `submit=true` to press Enter, `slowly=true` for JS listeners.
| `browser_fill_form` | Fill multiple inputs at once. | `fields` is an array of `{ element, ref, value }`. Great for checkout forms.
| `browser_select_option` | Choose a dropdown value. | Provide `values` array; still needs `ref` + `element`.
| `browser_hover` | Trigger hover states / tooltips / lazy menus. | Pair with `browser_wait_for` if hover spawns async content.
| `browser_press_key` | Send keyboard shortcut (`Enter`, `Meta+L`, etc.). | Use sparingly; combine modifier keys via `modifiers` array in `browser_click` or `browser_press_key`.
| `browser_wait_for` | Wait for text, disappearance, or fixed time. | Prefer waiting for text or `textGone` over blind sleeps. Example: `{"text": "Order submitted"}`.
| `browser_drag` | Drag-and-drop flows (sliders, Kanban). | Needs both `startRef` and `endRef` from snapshots.
| `browser_run_code` | Execute arbitrary Playwright JS. | Pass `async (page) => { ... }`. Use for fragile sequences (complex checkouts, interceptors). Return logs for transparency.
| `browser_console_messages` / `browser_network_requests` | Debug API calls / console errors. | Use when diagnosing login failures or CSR glitches.
| `browser_tabs` | Manage multiple tabs (list/create/select/close). | When a click opens a new tab, call `browser_tabs` → `action: "list"`, then `action: "select"` with index.
| `browser_take_screenshot` | Visual evidence (read-only). | Prefer after snapshots to document final state; `fullPage=true` for long receipts.
| `browser_pdf_save` (requires `--caps=pdf`) | Export page as PDF for audit logs. | Provide `filename` or default will be timestamped.
| `browser_mouse_*` (requires `--caps=vision`) | Coordinate-based fallback when accessibility tree lacks nodes. | Use only when semantic refs fail; coordinates depend on viewport! |
| `browser_install` | Install missing browser binary. | Call when you see `Executable doesn't exist` errors.
| `browser_close` | End the session neatly. | Use at the end of long autonomous runs to release resources.

## Common Patterns
- **Login sequences**: `browser_snapshot` → locate inputs → `browser_type` (username) → `browser_type` (password, `submit=true`) → `browser_wait_for` success text → call `browser_snapshot` to confirm.
- **Checkout**: Use `browser_fill_form` for shipping/billing blocks, `browser_select_option` for shipping method, double-check totals with `browser_snapshot` text search before final `browser_click`.
- **Retries**: If an action fails, grab a fresh snapshot, verify the element still exists, optionally re-issue the command with `browser_wait_for` preceding it.
