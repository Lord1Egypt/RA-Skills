---
name: hermes-desktop-customization
description: "Use when patching Hermes Desktop source (titlebar, fonts)."
version: 1.0.0
author: Hermes Agent
license: MIT-0
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
  hermes:
    tags: [hermes, desktop, electron, source, customization, titlebar]
    related_skills: [hermes-desktop-plugins, hermes-agent]
---

# Hermes Desktop Source Customization

Hermes Desktop is an Electron app built **from source** at
`~/.hermes/hermes-agent/apps/desktop/`. Customizing it means editing that
source tree and rebuilding — it is NOT the same as the plugin system
(see `hermes-desktop-plugins`, which covers runtime JS plugins that need no
rebuild). This skill covers the source-patching class of work.

## When to Use

- Titlebar / window-chrome changes (height, padding, control buttons).
- Font family/size changes (UI fonts, mono fonts, Arabic font size).
- Zoom / density complaints ("too much vertical space", "too small").
- Launcher icon, app metadata, or any "change the desktop app itself" ask.
- Answering "what custom changes have we applied to the desktop?" — verify
  against git, not memory (see Verification).

## Key Facts About the Source Tree

- Renderer entry: `apps/desktop/src/main.tsx`; app shell/layout lives in
  `apps/desktop/src/app/` (contrib shell = `app/contrib/controller.tsx`).
- Design tokens: `apps/desktop/src/styles.css` (CSS custom properties).
- UI atoms (Button variants, etc.): `apps/desktop/src/components/ui/`.
- Electron main process (window flags, titleBarOverlay, frameless config):
  `apps/desktop/electron/main.ts` — rebuilt to `release/linux-unpacked/Hermes`.

## Sizing/Chrome Knobs (verified anatomy)

The titlebar is NOT one component. Its sizes live in **several independent
places** that must change in lockstep:

| Knob | Location |
|------|----------|
| Bar height constant `TITLEBAR_HEIGHT` (34) + `TITLEBAR_CONTROL_HEIGHT` (22) | `src/app/shell/titlebar.ts` |
| Visible bar height — **hardcoded** `h-[34px]` | `src/app/contrib/controller.tsx` (does NOT read the constant!) |
| Button box size `--titlebar-control-size` / `--titlebar-control-height` | `src/styles.css` |
| Icon size inside buttons (`icon-titlebar` variant, codicon 0.875rem) | `src/components/ui/button.tsx` |
| `--titlebar-height` fallbacks hardcoded `34px` | `src/app/floating-hud.ts`, `src/components/notifications.tsx` |

`--titlebar-height` has **no global CSS default** — it is set inline
(`overlay-view.tsx`, `panes.tsx` set it from `TITLEBAR_HEIGHT`; the contrib
shell zeroes it in `controller.tsx`). The chat header
(`src/app/chat/index.tsx`) and a legacy header path consume it via
`h-(--titlebar-height)`, so scaling the bar requires touching both the
constant AND the hardcoded `h-[34px]` in `controller.tsx`.

See `references/titlebar-sizing.md` for the full map + the planned shrink.

## Procedure

1. **Plan first, get approval before touching source.** The owner's standing
   preference for this class of work: research the anatomy, present a plan,
   WAIT. He explicitly steered: "we're just planning and researching, make a
   plan when you finish." Never apply desktop source edits mid-research.
2. Inspect the real source before proposing values — grep the knob locations
   above; lines drift between updates.
3. Scale proportionally: when reducing bar height, reduce control height +
   control size + icon size together so layout and hit-testing stay intact.
4. Rebuild: `hermes desktop --build-only`, then relaunch (`hermes desktop`).
5. Verify visually (screenshot) after the build — zoom factor (e.g. 125%)
   amplifies padding complaints.

## Verification — "what have we customized?"

Never answer from session memory. The repo is ground truth:

```bash
cd ~/.hermes/hermes-agent
git branch --show-current          # main, or a personal branch (desktop-custom)
git status -s                      # live uncommitted edits
git diff -- apps/desktop/          # exact current edits
git log --oneline --all --grep fira   # was a change ever committed?
```

Pattern to remember: a customization may be **planned-but-never-landed** —
check the diff before claiming something is applied. Landed customizations
live on the `desktop-custom` branch (e.g. `ef94c674b` leads chat `--dt-font-mono`
with `terminal.font_family`, so chat code/diff text follows the Terminal Font
setting).

Update survival: plain `hermes update` would park/switch away from a
non-main branch, and `hermes update --branch desktop-custom` FAILS for a
local-only branch (`couldn't find remote ref`). The working setup is
`updates.parked_branch_strategy: update_in_place` in config.yaml (set):
plain `hermes update` then merges origin/main into desktop-custom in place,
behind a `pre-update-<stamp>` safety tag, stopping cleanly on conflict.

Verified pitfalls from a real run (2026-08-22):
- A DIRTY tree (uncommitted OR untracked files inside the checkout)
  blocks the whole update with "CODE UPDATE SKIPPED" — commit stray
  edits first (`git status -s` must be empty); hide legit-but-local
  paths via `.git/info/exclude`.
- `hermes update` itself rebuilds the packaged desktop app
  (`app.asar` timestamp advances past the merge) — no manual
  `hermes desktop --build-only` needed afterwards; just relaunch.
- The fleet restart mid-update kills any agent session driving the
  update from inside Hermes — expect the turn to be interrupted;
  verify state with git afterwards instead of re-running blindly.

## Update Survival

- `hermes update` / `hu` **auto-stashes uncommitted local changes and
  restores them after pulling** — source edits survive updates, but can
  conflict if upstream touches the same lines.
- For durable multi-edit customization, commit to a personal branch
  (`desktop-custom`) and `hermes update --branch desktop-custom`; rebase onto
  `origin/main` to pull upstream.
- After any update, re-verify with `git status -s` that stashed edits
  reapplied cleanly.

## Pitfalls

- The hardcoded `h-[34px]` in `app/contrib/controller.tsx` is the bar you
  actually see — changing `TITLEBAR_HEIGHT` alone appears to do nothing.
- `rg`/`search_files` treats a pattern starting with `--` (like
  `--titlebar-height`) as a flag. Use `grep -rn -- "--titlebar-height" .`
  or search for `titlebar-height\s*:` instead.
- Two titlebar code paths exist (contrib shell bar + legacy chat header);
  if the bar still looks tall after scaling, the other path is the suspect.
- Sizes in `rem` are zoomed by the user's window zoom (125% in one tested case)
  — a 34px bar renders ~42px physical. Complaints about "too much padding"
  at high zoom are usually the 34px bar vs 22px buttons gap, not real padding.
