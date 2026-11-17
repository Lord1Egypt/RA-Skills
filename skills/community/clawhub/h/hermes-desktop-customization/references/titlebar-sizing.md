# Titlebar sizing map + planned shrink (Aug 2026 session)

Verified against the source tree at
`~/.hermes/hermes-agent/apps/desktop/` during a research-only session
(titlebar vertical-space reduction, user at 125% window zoom).

## The anatomy — sizes live in 5 independent places

| # | Knob | Location | Value (at time of writing) |
|---|------|----------|----------------------------|
| 1 | `TITLEBAR_HEIGHT` | `src/app/shell/titlebar.ts:3` | `34` |
| 2 | `TITLEBAR_CONTROL_HEIGHT` | `src/app/shell/titlebar.ts:7` | `22` |
| 3 | Visible bar height | `src/app/contrib/controller.tsx:763` | **hardcoded `h-[34px]`** — does NOT read the constant |
| 4 | `--titlebar-control-size` / `--titlebar-control-height` | `src/styles.css:471-472` | `1.25rem` (20px) / `1.375rem` (22px) |
| 5 | Icon size in titlebar buttons | `src/components/ui/button.tsx:53` | `[&_.codicon]:text-[0.875rem]` (14px) via `icon-titlebar` variant |

Related derived values:

- `TITLEBAR_CONTROLS_TOP = (TITLEBAR_HEIGHT - TITLEBAR_CONTROL_HEIGHT) / 2`
  (`titlebar.ts:8`) — auto-recomputes when the two constants change.
- `controlsTranslateY = 2` in `src/app/contrib/wiring.tsx:973`; the fixed
  button clusters are positioned with
  `'--titlebar-controls-top': `${controlsPos.top - controlsTranslateY}px``
  (`wiring.tsx:998`).
- `--titlebar-height` has **no global CSS default**. It is set inline:
  - `app/overlays/overlay-view.tsx:94` and `app/contrib/panes.tsx:97` set
    it to `${TITLEBAR_HEIGHT}px`;
  - `app/contrib/controller.tsx:750` zeroes it (`'0px'`) for the contrib
    shell.
  Consumers that rely on the var: the chat header
  (`app/chat/index.tsx:143` via `titlebarHeaderBaseClass` in
  `app/shell/titlebar.ts:22`), right-rail tabs (`app/chat/right-rail/preview.tsx:97`),
  sidebar spacing, overlay clearances.
- Hardcoded `34px` fallbacks elsewhere: `app/floating-hud.ts:12`
  (`var(--titlebar-height,34px)`) and `components/notifications.tsx:122`
  — must be updated in lockstep or they drift.

## The window-control removal (already applied, separate patch)

`apps/desktop/electron/main.ts` has an uncommitted local change:
- `getTitleBarOverlayOptions()`: skip Electron's window-control overlay on
  ANY non-Windows (`if (!IS_WINDOWS) return false` — was previously only
  Windows+WSL). Niri/DMS tiling compositor draws no SSD and keyboard-driven
  close/maximize makes the buttons useless.
- `getNativeOverlayWidth()`: returns `0` unless Windows.

This is the ONLY live customization as of Aug 2026 (`git status -s` shows
`M apps/desktop/electron/main.ts`).

## Planned-but-NOT-executed: proportional titlebar shrink

User asked to reduce the vertical space the titlebar takes at 125% zoom
(~6px dead padding around the 22px buttons in a 34px bar). Proposed plan,
presented for approval — NOT applied:

1. `titlebar.ts`: `TITLEBAR_HEIGHT` 34 → 26; `TITLEBAR_CONTROL_HEIGHT`
   22 → 18 (`TITLEBAR_CONTROLS_TOP` auto → 4px).
2. `controller.tsx:763`: hardcoded `h-[34px]` → `h-[26px]` (the visible bar).
3. `styles.css`: `--titlebar-control-size` 1.25rem → 1.0625rem;
   `--titlebar-control-height` 1.375rem → 1.125rem.
4. `button.tsx`: codicon `0.875rem` → `0.75rem`.
5. Fallbacks: `floating-hud.ts` + `notifications.tsx` 34px → 26px.

Rationale: scale bar + control + icon together (proportional ~24% shrink)
so layout and hit-testing stay intact. Verification: `hermes desktop
--build-only`, relaunch, screenshot before/after.

Open question from the session: two titlebar code paths exist (contrib
shell bar in `controller.tsx` vs legacy header sized by `--titlebar-height`
in `chat/index.tsx`). The contrib bar is believed to be the visible one;
Edits 1+2 cover both paths regardless.

## Pitfall hit during research

`rg`/`search_files` errors with "unrecognized flag" for patterns starting
with `--` (e.g. `--titlebar-height`). Workaround:
`grep -rn -- "--titlebar-height" .` or search `titlebar-height\s*:`.
