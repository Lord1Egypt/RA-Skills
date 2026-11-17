# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/), and this
project adheres to [Semantic Versioning](https://semver.org/).

## [1.6.0] - 2026-09-22

### Fixed

- **Watchdog 12-day silent failure due to path encoding bug.** When the watchdog task was
  registered (v1.5.2), non-ASCII characters in the repo path were corrupted by Windows
  `Register-ScheduledTask` / `schtasks /create` (both convert UTF-8 path bytes to GBK,
  producing mojibake). The task ran every 15 minutes but `conhost.exe` could never find
  the script, so the log stayed empty for 12 days after the last healthy entry
  (2026-09-10). After an OpenClaw upgrade wiped `dist/` on ~Sep 22, the enhancement
  disappeared and the watchdog could not self-heal.

  **Fix**: the `-Install` path now resolves the script directory to its **8.3 short path**
  (e.g. `MODELS~1`) before passing it to the task action, which contains only ASCII
  characters and survives any encoding conversion. The short path is obtained via
  `Scripting.FileSystemObject.ShortPath` with a graceful fallback.

### Changed

- Version bump to 1.6.0 (the watchdog fix is a meaningful reliability improvement).

## [1.5.3] - 2026-09-11

### Fixed

- ClawHub artifact now includes `scripts/` directory (the publish-core filter was too
  aggressive and excluded the `scripts/` folder from the ClawHub package).

## [1.5.2] - 2026-09-11

### Changed

- Watchdog launcher switched from VBScript (`pcl-run-hidden.vbs`) to `conhost.exe --headless`
  (Windows 11+), eliminating the VBScript dependency and the VBScriptDeprecationAlert warnings.

## [1.5.1] - 2026-09-10

### Fixed

- **Documentation now matches behavior** (addresses a ClawHub SkillSpector finding,
  "Underdeclared Capability"). Since 1.2.0 the enhancement polls the app shell with a
  same-origin `fetch('./', { cache: 'no-store' })` to notice server-side updates, but
  `SKILL.md`, `README.md` and `璇存槑.md` still claimed "no network access". The disclosure now
  states the same-origin poll explicitly (and lists it in the Disclosure table): same-origin
  only, no external host, no telemetry, no data leaves the machine.

### Verified

- Privacy scan clean (repo + publish core); `node --check` clean; install/uninstall
  round-trip re-verified; injected tag `pcl-model-picker.v8.js?h=84d1ba15` unchanged
  (docs only 鈥?the browser script is byte-identical to v1.5.0).

## [1.5.0] - 2026-09-10

### Added

- **Resizable picker (both axes) with remembered size.** The menu now carries a small grip
  in its bottom-right corner; drag it to grow or shrink the picker horizontally **and**
  vertically (min 360脳220, clamped to the viewport). The size is written to
  `localStorage['pcl-model-picker-size']` when the drag ends and restored the next time the
  picker opens, so a layout you like sticks. **Double-click the grip** to reset to the
  default size.
- **Long model names are readable.** Every model option now carries a `title` tooltip with
  its full name, and the name container is allowed to shrink so truncation never distorts
  the row 鈥?widen the picker (above) to read the whole id at a glance.
- Diagnostics: `pclModelPickerDiag()` now also reports `storedSize` and, per instance,
  `sized` and `grip`.

### Changed

- Enhancement file is now `pcl-model-picker.v8.js`. Sizing is driven by CSS custom
  properties (`--pcl-w` / `--pcl-h`) with the v7 defaults as fallback, so if the app resets
  inline styles the 1 s heartbeat restores the remembered size.

### Verified

- Local deployment: injected tag `pcl-model-picker.v8.js?h=84d1ba15`; the served asset
  returns HTTP 200 and reports `VERSION = 8`; `node --check` clean.

## [1.4.0] - 2026-09-10

### Fixed

- **The enhancement could silently revert to the stock flat list while the page stayed
  open, until a manual reload.** Root cause: the pass resolved its target with
  `document.querySelector(...)`, so it always enhanced the **first** matching instance in
  document order. The Control UI can mount more than one composer instance (main chat,
  side/session views, cached views), and the official code explicitly handles several
  coexisting pickers. As soon as a hidden instance appeared earlier in the DOM, the
  enhancement was applied to the hidden one and the visible picker fell back to the
  official layout. A reload remounted the app and restored the order, which is why
  "refresh fixes it".
- **The injected stylesheet was a single point of failure.** It was appended once at
  script load; if the document later lost it, nothing re-injected it, so the layout stayed
  stock until a reload.

### Added

- **Per-instance enhancement.** The script now walks every model-menu instance and
  enhances only the ones actually rendered; hidden/closed instances are left untouched, so
  a hidden sibling can no longer steal the enhancement.
- **Stylesheet self-healing + 1 s heartbeat.** `ensureStyle()` re-injects the stylesheet
  whenever it is missing, and a state-gated 1-second heartbeat re-runs the whole pass, so
  any silent loss (stylesheet removed, instance swapped, state cleared) recovers within a
  second without user action.
- **Diagnostics.** `window.pclModelPickerDiag()` now reports every instance (state,
  filtering, rendered, rail, chips) plus stylesheet presence, heartbeat count and the last
  self-heal event; `window.pclModelPickerLog()` returns the event ring buffer
  (`style-injected`, `rail-created`, `chip-cleared-search`, `fallback-narrow`).

### Changed

- **The official search filter no longer reverts the layout to native.** Typing in the
  model search keeps the two-column layout and the provider rail; groups with no visible
  match are hidden instead. Clicking a rail chip while filtering clears the search first
  and then applies the provider filter. The old `fallback-filter` state, which could get
  stuck, is gone.
- `scripts/pcl-patch.ps1` auto-selects the newest packaged `pcl-model-picker.v*.js`, so
  future script bumps no longer require editing the installer.

### Verified

- Real Chromium DOM harness (managed browser, script loaded from the published repo):
  baseline two-column; official search keeps two-column and recovers on clear;
  stylesheet removed -> re-injected and `display: grid` restored within the heartbeat;
  rail removed -> re-created; **hidden instance first + visible instance -> visible one
  stays two-column** (the regression that motivated 1.4.0); visible instance rebuilt after
  a hidden one exists -> still two-column; rebuild while open -> two-column.
- Local deployment: `pcl-model-picker.v7.js?h=b58534b1`, watchdog `-Check` exit 0.

## [1.3.0] - 2026-09-09

### Added

- **Auto-repair watchdog (GitHub package only, `platform/pcl-watchdog.ps1`).**
  `npm i -g openclaw@<version>` replaces the whole `dist/control-ui/` directory, deleting
  both the injected tag and the enhancement asset 鈥?the picker silently reverts to the
  stock list. The watchdog compares the injected tag against the packaged script (filename
  **and** content fingerprint) and re-runs the installer only when something is missing or
  stale. Registered as the scheduled task `BigLobster-PclModelPickerRepair` (default every
  15 minutes) it heals an upgrade within minutes; the enhancement's own self-update watchdog
  then reloads the open tab, so no manual step is needed.
  - `-Check` (exit `0` healthy / `10` needs repair), `-Repair`, `-Install`, `-Uninstall`,
    `-Status`; log at `%USERPROFILE%\.openclaw\logs\pcl-model-picker-watchdog.log`.
  - Read-only when healthy: it writes nothing unless the injection is actually missing.
  - Not part of the ClawHub artifact; the repository README documents the boundary.

### Verified

- Watchdog exercised end-to-end: healthy `-Check` (exit 0) 鈫?simulated upgrade wipe
  (tag and asset removed) 鈫?`-Check` exit 10 鈫?`-Repair` restored the injection 鈫?`-Check`
  exit 0 鈫?`-Install` registered the task (next run confirmed by `schtasks`).
- Compatibility re-checked against OpenClaw **2026.9.3**, which now renders the picker as a
  controlled `<details>` (`?open=` driven by component state; the trigger carries
  `--disabled`/`aria-disabled` until the session is ready). The enhancement does not depend
  on click events: with the menu open the probe reports `state: "two-col"`, `railFound: true`
  and 10 provider chips.

## [1.2.0] - 2026-09-09

### Added

- **Self-update watchdog.** An already-open Control UI tab keeps running the script it
  loaded, so a freshly patched server looked "unpatched" until the user reloaded by hand
  (symptom: click the picker 鈫?still the old layout; refresh 鈫?new layout). The enhancement
  now fetches the app shell (`./`, a network-first path the Service Worker never caches)
  30s after load and then every 5 minutes, parses the injected tag's version and content
  fingerprint, and reloads the page automatically when the server is newer.
  - Never downgrades: an older served build is ignored.
  - Loop-safe: the attempted build is recorded in `sessionStorage`.
  - Non-disruptive: waits while an input/textarea is focused (retries in 60s); background
    tabs reload immediately.
  - Manual check: `await window.pclModelPickerCheckUpdate()`.

### Changed

- Enhancement file is now `pcl-model-picker.v6.js`; `window.pclModelPickerDiag()` also
  reports `selfFp` (the content fingerprint the running script was loaded with).

### Verified

- End-to-end in a real authenticated Control UI: with the page open on v6, deploying v7
  server-side caused an automatic reload within ~25s and the picker came up as v7 with the
  two-column layout intact; reverting the server to v6 did **not** downgrade the page.

## [1.1.1] - 2026-09-09

### Changed

- Updated the attribution signature to `Pondsi (+MiMo-v2.5 +deepseek-v4.1-flash-expires-on-0910 +GLM5.3-flash) 鈥?automatically committed by OpenClaw` across `README.md`, `SKILL.md`, `璇存槑.md`, `SPONSORS.md` and this changelog.

## [1.1.0] - 2026-09-09

### Changed

- **Renamed the project to ModelSelectorOpenClaw** (previously published as *PCL Model
  Picker*). Skill slug: `modelselector-openclaw`. The enhancement file is now
  `pcl-model-picker.v5.js`; the installer is unchanged in name (`pcl-patch.ps1`).
- Documentation rewritten around the core selling point: a **provider navigation column**
  that makes picking a model two clicks even with many providers, each with many models.

### Fixed

- **Silent disappearance of the enhancement on narrower viewports.** The old guard used a
  hard `MIN_WIDTH = 520`; high-DPI scaling, a narrow window or a split view drops
  `window.innerWidth` below 520 CSS px, at which point the script silently reverted to the
  native flat list (`clearFilterState()`) 鈥?the user saw "the enhancement is gone" with no
  hint. The threshold is now **340px**, and the provider column width is responsive
  (`grid-template-columns: clamp(84px, 26%, 132px) minmax(0, 1fr)`), so narrow layouts keep
  the two-column behaviour instead of collapsing.
- **Same-filename content changes were pinned by the browser cache.** Control UI's Service
  Worker is cache-first for `/assets/` and the asset response is `immutable`. The injected
  URL now carries a content fingerprint (`./assets/pcl-model-picker.v5.js?h=<sha256-8>`),
  so any content change is a new cache key; `pcl-patch.ps1` recomputes it on every run.

### Added

- **Observability**: `<html data-pcl-model-picker="v5">`, menu attribute
  `data-pcl-state` (`two-col` / `fallback-narrow` / `fallback-filter`) and a one-line
  browser-console diagnostic `window.pclModelPickerDiag()`.
- **Menu lookup fallback**: if a future Control UI renders the menu in a top-layer portal
  instead of inside the `<details>` element, the enhancement still resolves it document-wide
  instead of failing silently.
- `.github/` issue templates and security policy (GitHub repository only).

### Verified

- End-to-end in a **real, authenticated Control UI** (fresh browser profile, headless Edge
  over CDP): at 1440px, 480px and 360px viewport widths the picker reports
  `state: "two-col"`, `railFound: true`, 10 provider chips, two-column grid, and the
  per-chat account row hidden. Previously 480px fell back to the native list.
- The fingerprint URL and the injected tag were confirmed on the live gateway
  (`/assets/pcl-model-picker.v5.js?h=鈥 returns HTTP 200).

## [1.0.0] - 2026-09-09

### Added

- Two-column master-detail model picker for the OpenClaw Control UI chat input:
  provider navigation chips (left) + the selected provider's models only (right),
  each column an independent scroll container (structural CSS Grid 鈥?no scroll coupling).
- Hides the official per-chat account control (`.chat-model-account`, e.g. `deepseek:default`)
  inside the model menu 鈥?unrelated to provider/model picking.
- Official design tokens throughout (`--bg-hover`, `--accent` mix, `--border`,
  `--scrollbar-*`); dark/light/custom `data-theme` follows automatically.
- State-gated DOM writes (zero no-op writes) 鈥?no MutationObserver self-excitation.
- Idempotent installer `scripts/pcl-patch.ps1`: auto-detects the OpenClaw Control UI
  directory (npm root, common prefixes, CLI on PATH, `-Dist` override), backs up
  `index.html` on first run, replaces the injected tag in place across versions,
  and keeps the two newest `pcl-model-picker.v*.js` assets to avoid stale-HTML 404s.
- `-Remove` switch for a clean uninstall.

### Engineering notes

- Control UI's Service Worker is cache-first for `/assets/`: content changes must change the
  URL (versioned filename, and since 1.1.0 also a content fingerprint) or browsers keep
  serving the stale script.
- Verified with a local harness (mirror of the official DOM) via headless Edge:
  24 assertions green, including layout, independent scrolling, theme probes,
  search fallback and the hidden account control.

---

Pondsi (+MiMo-v2.5 +deepseek-v4.1-flash-expires-on-0910 +GLM5.3-flash) 鈥?automatically committed by OpenClaw

