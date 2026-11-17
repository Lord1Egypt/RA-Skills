# Admin UI

SPA at `/admin`. Workspaces: dashboard, site (canvas editor), content, data, media, plugins, users, ai, account; each gated by capability. Cmd+K (Ctrl+K) Spotlight is global fuzzy action/search; registered commands behave exactly like built-ins.

## Site workspace (canvas)
- Design mode: several breakpoint frames side by side; editing the desktop frame reflows the mobile frame in the same view. Live mode: one full-size frame editing the real page in place.
- Canvas renders per-breakpoint iframes; selection rings distinguish hovered (pink), selected (green), matcher (orange).
- Tree panel + selectors panel per page; page/component/layout lists back the left rail; one outlet per template document is enforced at mutation points with explanatory toasts.
- Right properties panel is control-type driven: Input, Textarea, Number, Switch, Select, ColorInput, media picker, URL input, depending on the prop.
- Undo is patch-based; whole imports commit as a single undo.

## Content workspace
- Three panes: collection/entry explorer, document canvas, settings panel.
- Body is one Tiptap/ProseMirror document persisted as markdown; marks via bubble menu, blocks via slash menu and notch quick-actions.
- Write mode is the bare editor surface; live mode renders the entry inside its real template with site styles.
- The AI agent panel docks in the rail and operates the open draft, not a stale DB row.

## Data workspace
- Spreadsheet grid over any table: search, status filter chips, sort, selection, group collapse, column resize.
- Floating bulk action bar: publish, export, delete.
- Cell editing opens in an inspector; schema editor manages fields per table.

## Media workspace
- Folder tree plus smart folders (virtual predicate views like "unused"), usage tracking so you know where an asset appears, replace workflow preserving URLs, upload queue and viewer float windows, bulk operations.

## Users, roles, and account
- Role = set of capabilities; owner only exists from first-run setup; API refuses owner assignment and guards the last active owner. Create User button opens a dialog (Email, Display name, Initial password min 12 chars, Role select; Owner is filtered out of assignable roles) and asks for the acting user's password (step-up) on submit.
- Per-user TOTP MFA with recovery codes, device-labeled session list, step-up window preference.

## Dashboard and audit
- Widget surfaces: pages, posts, media, plugins, storage, publish lineup, activity feed; audit event stream is filterable via /audit.
