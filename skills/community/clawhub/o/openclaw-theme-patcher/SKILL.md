---
name: openclaw-theme-patcher
description: Add, refine, calibrate, or migrate OpenClaw Control UI themes by patching the installed bundled frontend assets in dist/control-ui/assets. Use when a user wants a new WebUI theme, wants colors matched to a reference theme such as VSCode, wants chat/component styling tuned inside a custom theme, or wants an existing custom theme preserved across an OpenClaw upgrade.
---

# OpenClaw Theme Patcher

Add a new OpenClaw Control UI theme directly into the installed frontend bundle.

This skill also covers **theme migration across OpenClaw upgrades**. When a user already has a custom theme on an older installed bundle and wants to keep it after updating OpenClaw, preserve the old theme first, then migrate it into the new bundle using structural comparison rather than heuristic string injection.

## Scope

Use this skill for installed bundle patching, not upstream source development.

Default rule: add a new theme from the user's requested palette. Do not overwrite built-in themes unless the user explicitly asks.

For migrations, use a stricter rule set:
- preserve the user's old custom theme first
- treat the old and new bundles as potentially different structures
- never assume previous patch points still exist after an upgrade
- prefer restoring the UI to a known-good stock state over leaving a half-migrated broken theme live

## Files to patch

Patch the active OpenClaw install only:
- `dist/control-ui/assets/index-*.js`
- `dist/control-ui/assets/index-*.css`

Resolve the active install first. Do not assume the workspace copy is the live one.

## Workflow

For token design and live bundle patch locations, read as needed:
- `references/token-mapping.md`
- `references/patch-points.md`
- `references/theme-migration-checklist.md` when doing a version-to-version preserve/rebuild of an existing custom theme

Bundled helper script:
- `scripts/backup_theme_bundle.py` — backs up the active live JS/CSS bundles for a given theme id, extracts `:root[data-theme=<id>]` / `:root[data-theme=<id>-light]`, and saves JS snippets for the allowed set, alias map, resolver, and theme card when found

If the task is an upgrade or migration, follow the migration workflow below before any new patching. For day-of execution, prefer using `references/theme-migration-checklist.md` as the short operational checklist and this file as the fuller policy/guidance layer.

### 0. Migration workflow for existing custom themes

Use this when the user already has a custom theme on an older OpenClaw version and wants to keep it across an update.

#### Phase A. Snapshot the old theme before upgrade

Before updating OpenClaw:
- resolve the active install and active bundle files
- extract and save the old theme's CSS selectors from the live CSS bundle
- save a copy of the old JS and CSS bundles for offline comparison
- record the old theme id, visible label, description, and any resolver behavior you can confirm

Preferred method:

```bash
python3 scripts/backup_theme_bundle.py <theme-id> --output-dir /path/to/backups
```

Use manual extraction only if the helper script cannot capture enough of the live theme.

Leave the backup in the workspace, for example:

```text
backups/openclaw-<theme-id>-theme/
  report.json
  <theme-id>.dark.css
  <theme-id>.light.css
  bundle-js.txt
  bundle-css.txt
```

Minimum capture:
- old JS bundle path
- old CSS bundle path
- `:root[data-theme=<theme-id>]`
- `:root[data-theme=<theme-id>-light]` if present
- old JS snippets containing:
  - allowed theme id set
  - theme alias/default map
  - theme card list
  - resolver branch for the theme family

#### Phase B. Upgrade first, then rediscover structure

After the OpenClaw update:
- re-resolve the active install and the new hashed bundle filenames
- do **not** assume the old JS patch points are still valid
- inspect the new bundle's current theme structures fresh

#### Phase C. Compare old vs new structures

Compare the saved old bundle snippets to the new live bundle and answer these questions before editing:
- Does the new bundle still use an explicit allowed-theme set?
- Does it still use an alias/default map?
- Does it still use a visible theme card list?
- Does it still have a resolver that maps theme family + mode to selector id?
- Are any of those names, array shapes, or branches materially different?

Only patch after those answers are clear.

#### Phase D. Patch by exact structure, not guesswork

Migration rule:
- copy the old theme's CSS token values
- re-register the theme in the new bundle **using the new bundle's actual structures**
- keep edits surgical and reversible

Hard prohibition:
- never use broad or heuristic replacements like replacing the first `return e` or first matching `new Set(...)` unless you have first confirmed that exact snippet is the theme resolver or set you intend to patch
- never claim success just because the theme card appears; card presence alone is not proof of a correct migration

#### Phase E. Verify and, if broken, stop the bleeding first

If the migrated theme appears but looks wrong, or if unrelated UI behavior breaks:
1. identify whether the break is in CSS selectors, card registration, alias/default map, or resolver logic
2. if the UI is visibly degraded, first remove the broken migrated entry and revert residual bad injections so the UI returns to stock behavior
3. only then attempt a second migration pass

Preferred recovery order:
- restore normal UI first
- then rebuild the migrated theme from verified structures

### 1. Confirm the active install

Run:

```bash
which openclaw
readlink -f "$(which openclaw)"
openclaw status
```

Then locate candidate bundles:

```bash
find ~/.npm-global/lib/node_modules /usr/lib/node_modules /usr/local/lib/node_modules \
  -path '*/openclaw/dist/control-ui/assets/index-*.js' -o \
  -path '*/openclaw/dist/control-ui/assets/index-*.css'
```

If multiple installs exist, patch only the one that matches the active CLI path.

### 2. Define the theme

Collect the theme from one of:
- a named reference theme
- a local config file such as VSCode settings or theme JSON
- explicit palette colors
- a screenshot plus user guidance

Decide before patching:
- theme id: lowercase, short, stable
- theme label shown in Appearance
- dark palette
- light palette if the theme should work with the existing light/dark toggle

If the theme should support the toggle, implement both dark and light selectors.

For both new themes and migrations, define not only the palette but also the intended component feel:
- primary chrome and panel feel
- assistant bubble feel
- user bubble feel
- code/pre/blockquote feel
- border strength expectations

Do not assume token changes alone will always reproduce the intended message-bubble look in newer bundles.

### 3. Add CSS selectors

Add:

```css
:root[data-theme=<theme-id>]{...}
:root[data-theme=<theme-id>-light]{...}
```

Use an existing theme block as the structure template. Keep token names unchanged and only change values.

Use `references/token-mapping.md` to translate the user's palette into OpenClaw tokens.

At minimum define:
- `--bg`, `--bg-elevated`, `--panel`, `--card`
- `--text`, `--text-strong`, `--muted`
- `--border`, `--border-strong`, `--border-hover`
- `--accent`, `--accent-hover`, `--ring`, `--focus`

Also define the usual supporting tokens already used by existing themes, including input, secondary, accent-2, state colors, and shadow/subtle variants.

If the desired result depends on specific chat bubble behavior, it is acceptable to add small **theme-scoped component overrides** after the root selectors, for example only under:

```css
:root[data-theme=<theme-id>] .chat-line.user .chat-bubble{...}
:root[data-theme=<theme-id>] .chat-line.assistant .chat-bubble{...}
```

In newer OpenClaw bundles, verify which chat layout branch is actually live before calibrating. There may be more than one branch in the bundled CSS, commonly including `.chat-group...` and `.chat-line...` families. If both exist, inspect both and override the one that actually renders in the current UI; if needed, cover both branches under the same theme-scoped override.

Rules for component overrides:
- scope them to the theme selector only
- prefer chat/message/component overrides only when token-only theming is insufficient
- do not change built-in themes while adding overrides for the custom theme
- keep overrides as narrow as possible
- when multiple chat layout branches exist, confirm the active branch instead of assuming the first matching selector is live

### 4. Register the theme in bundled JS

Patch the bundled JS so the theme appears in Appearance settings and mode switching resolves correctly.

Use `references/patch-points.md` to locate the smallest reliable JS change points.

Update all relevant structures that actually exist in the current bundle:
- allowed theme id set
- Appearance theme card list
- resolver mapping theme family + light/dark mode to CSS selector ids
- alias/default map if present

Required behavior:
- dark mode resolves to `<theme-id>`
- light mode resolves to `<theme-id>-light`

If the bundle already contains an unused hidden theme id that matches the intended use, it is acceptable to expose and complete it instead of inventing another id.

For migrations, mirror the old theme's confirmed behavior, but express it through the new bundle's real structures. Do not port old JS fragments blindly into a new version.

### 5. Refresh and verify

After patching:
- tell the user to hard refresh: `Ctrl+F5`
- restart gateway if needed: `openclaw gateway restart`

Success means:
1. the new theme label appears in Appearance settings
2. selecting it visibly changes the UI
3. the top-right light/dark toggle switches between the new theme's variants if both were added
4. built-in themes remain unchanged unless the user requested otherwise
5. chat bubbles, code blocks, blockquotes, and key chrome surfaces match the intended look closely enough for the user

For chat-focused themes, explicitly verify both of these:
- user bubble color and border treatment
- assistant bubble color and border treatment

## Debugging

If the theme does not appear:
- theme id missing from JS allowed set
- theme card list not patched
- stale cached JS
- wrong install path edited

If the theme appears but looks unchanged:
- CSS selectors missing
- resolver maps to the wrong selector id
- only dark or only light selector was added
- wrong CSS bundle edited

If the light/dark toggle does not work:
- resolver was not updated for both variants
- `<theme-id>-light` is missing or misspelled

If the theme appears but looks wrong or breaks unrelated UI text/layout after a migration:
- assume the JS patch hit the wrong structure before assuming the CSS palette is wrong
- inspect the exact current resolver/card/alias snippets again
- remove any bad migration residue and restore stock behavior before retrying
- do not keep a visibly broken migrated theme live just because the theme card exists

If the theme is structurally correct but some surfaces still feel off:
- treat it as a component-level calibration pass, not a failed migration
- inspect the exact CSS rules for chat bubbles, code blocks, and other visible components in the current version
- prefer theme-scoped overrides over destabilizing global token changes
- if a component override appears correct in CSS but has no visual effect, check whether a later duplicate branch (for example `.chat-group...` vs `.chat-line...`) is the one actually rendering

## Working style

- Use exact-text edits for bundled assets
- Change the smallest possible amount of JS needed
- Keep built-in themes intact unless the user asked otherwise
- Do not claim success until the user confirms the live UI changed
- For migrations, create reversible workspace backups before editing live bundles
- Prefer exact known snippets over heuristic replacements in minified JS
- If a first migration attempt fails, document the failure mode and switch to compare-and-rebuild, not more guessing
- For new themes too, verify real rendered components after token work; if necessary, do one small theme-scoped calibration pass instead of pretending token-only theming always covers chat surfaces

## Deliverables

Leave behind:
- patched JS bundle path
- patched CSS bundle path
- theme id and label
- dark/light CSS selectors added
- any theme-scoped component overrides added

For migrations also leave behind:
- backup directory path
- old bundle paths used for comparison
- whether stock UI was restored at any point during recovery
- the exact structures patched in the new version (allowed set / card list / alias map / resolver)
- whether the helper backup script was used, and if not, what had to be collected manually
