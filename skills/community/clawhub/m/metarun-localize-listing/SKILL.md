---
name: localize-listing
description: >-
  Localize or edit an App Store listing across languages through MetaRun:
  name, subtitle, description, keywords, What's New, promotional text, and
  URLs, per locale. YOU do the translating; MetaRun stages and applies.
  Trigger phrases: "translate my listing", "localize the app store page",
  "add German", "update the description in every language", "write What's
  New and translate it".
metadata:
  openclaw:
    homepage: https://metarun.dev/agents
    primaryEnv: METARUN_TOKEN
    envVars:
      - name: METARUN_TOKEN
        required: false
        description: MetaRun personal access token (Settings, MCP). Not needed after `npx metarun login`, which stores it in ~/.metarun/config.json.
    requires:
      anyBins:
        - npx
---

# Localize the listing: your words, every storefront

You are editing App Store listing copy through MetaRun. The division of
labor: **you (the agent) write and translate the copy**; MetaRun's tools
stage it per locale behind previews. There is no server-side translation in
this path, which means translation quality is yours to own: match the app's
tone, keep character budgets, and never machine-gloss idioms.

## Ground rules

- Tools run over MetaRun's MCP server or `npx metarun run <tool> '<json>'`.
  Fetch unfamiliar schemas with `npx metarun tools <tool-name> --json`.
- Two listing surfaces exist per locale, with different edit windows:
  **app-info localizations** (store name, subtitle, privacy URLs) and
  **version localizations** (description, keywords, What's New, promo text,
  support/marketing URLs). Check `apple_get_listing_editability` first: it
  says which surfaces are open and why others are locked.
- Character budgets are Apple law: name and subtitle 30, keywords 100,
  promotional text 170, description 4000. Count BEFORE staging; the preview
  will reject overruns, but a rejected preview is a wasted round trip.
- Every write previews first. Batch per-locale changes, show the user the
  set, then apply each with its confirmToken.

## The mission

### 1. Read what exists

- `apple_list_app_metadata` -> both surfaces in every current locale.
- `apple_list_version_localizations` -> the editable version's copy.
- `apple_get_listing_coverage` -> the same picture as flags instead of copy:
  filled/empty per language, plus `gaps` (field -> the languages missing it).
  Use it to scope the job before writing anything.
- Adding a language? `apple_list_supported_locales` names the valid codes.
  Creating an app-info localization REQUIRES the store name in the payload;
  a version localization needs only the locale.

### 2. Write the copy

- Translate from the primary locale yourself, locale by locale. Preserve
  meaning over word-for-word fidelity; keep brand terms untranslated; respect
  the budgets above (translations run long, subtitles especially).
- Keywords are not prose: comma-separated, no spaces after commas, no words
  already in the name/subtitle (Apple indexes those anyway). Run
  `aso_lint_metadata` on the result to catch violations and duplication.
- Cross-locale leverage: `aso_cross_locale_plan` shows which extra locales
  each storefront indexes (the US storefront reads NINE beyond en-US), so
  keyword sets can be packed without repeating words across them.

### 3. Stage and apply

- Version copy: `apple_preview_set_version_localization` per locale ->
  `apple_apply_set_version_localization`.
- Store name/subtitle/privacy URLs: `apple_preview_set_app_info_localization`
  -> `apple_apply_set_app_info_localization`.
- Promotional text goes live INSTANTLY with no review on a live app: treat
  it as a publish, not a draft, and say so when confirming. On an app that
  has never shipped it lands on the version in preparation instead.
- What's New exists only on updates. On a first release, do not write it
  anywhere; Apple rejects the field.

### 4. Verify

`apple_get_listing_coverage` is the check, not your own transcript: a
preview can be blocked, an apply can fail, a locale can be missed, and a
mission that reports itself complete with three languages empty is worse
than one that stops and says so. Read it back, and if `gaps` still names a
field the user asked for, stage the fixes now rather than announcing
completion. Then report the languages touched and remind them it is all in
change history, revertible per change.

## Beyond this mission

Screenshots per language (rendering, translation of slide copy, publishing)
are their own missions: discover with `npx metarun tools studio`.
