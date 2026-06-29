---
name: nextjs-to-electron
version: 1.1.0
description: Use when converting or migrating a Next.js (App Router) web app into an Electron desktop app — packaging a static-export site as a Windows desktop/portable/unpacked build, especially for fully-offline or intranet machines that lack the WebView2 runtime (where Tauri fails), or adding language persistence, window-state, single-instance, system tray, or GitHub Actions Electron builds. Covers the file:// white-screen trap, next-intl static-export i18n, custom app:// protocol, and electron-builder packaging. Also matches "nextjs2electron".
tags: [electron, nextjs, desktop, app-router, static-export, offline, next-intl, electron-builder, github-actions, webview2]
homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/nextjs-to-electron

metadata:
  clawdbot:
    emoji: "⚛️"
    requires:
      bins: ["node"]
    files:
      - electron-files.md
---

# Next.js → Electron Desktop App

## Overview

Wrap a **client-side** Next.js (App Router) static export in a thin Electron shell. Electron bundles its own Chromium, so unlike Tauri it needs **no system WebView2** — the reason to pick it for locked-down/intranet machines. The React code stays **untouched**; all desktop behavior lives in a `electron/` main-process layer that serves the static export.

**Core principle:** Serve the export over a custom `app://` protocol, NOT `file://`. Almost all migration pain is path/origin resolution, not React — and `file://` silently breaks both. (See [electron-files.md](electron-files.md) for all copy-paste code.)

## When to use

- The app is (or can be) a **static export** (`output: "export"`) — diff/format/calculator/viewer tools, no SSR or API-at-runtime.
- You want a Windows desktop build that runs **fully offline**, especially where WebView2 is absent (old LTSC/Server, air-gapped intranet) so Tauri won't launch.

**Do NOT use when** the app needs a live Node server at runtime (real API routes, SSR, server actions). **Prefer `nextjs-to-tauri`** when the targets have WebView2 and you want a ~3–10 MB exe with auto-update — Electron is ~150 MB because it ships Chromium.

This playbook targets **Windows** (`--win dir`/`portable`, SmartScreen, WebView2-less boxes). macOS/Linux packaging (`.dmg`/`.AppImage`, notarization, codesigning) is out of scope.

## Procedure

Do these in order. Full code is in [electron-files.md](electron-files.md). The web source under `src/`, `messages/`, `next.config.*` stays untouched.

1. **Confirm the export is client-side and check its shape.** `yarn build`, then `ls out/` — you'll see flat files (`index.html`, `en.html`, `zh.html`) and `_next/`. `trailingSlash: false` (flat files) is fine; the resolver handles both layouts (gotcha #2).

2. **Add the toolchain:** `yarn add -D electron electron-builder`. In `package.json` add `"main": "electron/main.js"` and scripts: `electron:dev` (a node launcher that sets `ELECTRON_DEV=1` and spawns electron — avoids a `cross-env` dep), `electron:build` (`next build && electron-builder --win dir`), `test:electron` (list the test files explicitly — `node --test electron/resolvePath.test.js electron/store.test.js …`; prefer this to the glob `electron/*.test.js`, which PowerShell won't expand in CI, so it leans entirely on `node --test`'s own glob (Node ≥ 21) — an explicit list is portable across every shell and Node version).

3. **Create the `electron/` layer** (copy from electron-files.md). Split into **pure modules that must NOT `require("electron")`** (so `node --test` runs them) and Electron-bound ones:
   - `constants.js` — `SCHEME="app"`, `LOCALES[]`. `resolvePath.js` — `resolveAssetPath(outDir, pathname, exists)` with `.html`→`/index.html`→`404.html` fallback. `store.js` — dependency-free JSON store in `userData`. `locale.js` — `startUrl`/`parseLocale`/`trackLocale`. `window-state.js` — `createWindowStateKeeper`. (All pure → unit-tested.)
   - `protocol.js`, `tray.js`, `main.js` — the only files that import electron.

4. **Load via the `app://` protocol, never `file://`** (gotcha #1). Before `app.ready`: `protocol.registerSchemesAsPrivileged([{scheme:"app", privileges:{standard:true, secure:true, supportFetchAPI:true}}])`. After ready: `protocol.handle("app", …)` mapping `app://local/<path>` → `resolveAssetPath` → `net.fetch(pathToFileURL(file))` (with a `.catch` returning a 404 Response). Load `app://local/` + the saved locale.

5. **Wire the desktop features in main.js** (all passive — zero renderer changes, gotchas #3, #4): single-instance lock + second-instance focus; restore window bounds from the store; `trackLocale(win, store)` persists locale on `did-navigate`; tray with close-to-tray via an `app.isQuitting` flag.

6. **Package** (gotcha #6). `electron-builder.yml`: `extraResources` maps `out → out` and `build/icon.png → icon.png`; `main.js` reads them at `process.resourcesPath/out` and `/icon.png` when packaged. Choose target: `dir` (unpacked folder — runs `TextDiff.exe` directly, fast) vs `portable` (self-extractor, re-unzips to %TEMP% every launch, slower) — gotcha #11.

7. **CI** (`.github/workflows/electron.yml`): `windows-latest` → setup-node → `yarn install --frozen-lockfile` → `yarn test:electron` → `yarn electron:build` → upload the build as an artifact. If the desktop work lives on a side branch, host this workflow **on the default branch** and pin its checkout to that branch (`ref:`) — one file serves both the manual button and tag builds, with no drifting copy on the side branch (gotcha #10). To **also attach the build to a GitHub Release** (e.g. ship it alongside a Tauri release in the same tag), add a `push: tags` trigger, derive the version from the tag (`npm pkg set version="${GITHUB_REF_NAME#v}"`, guarded `if: github.event_name == 'push'`), name the zip from the tag, and `gh release upload "$GITHUB_REF_NAME" <zip> --clobber` — see gotcha #12 for the tag/version traps that silently produce an empty release.

8. **Verify:** `yarn test:electron` (pure modules), then `yarn electron:build` and run the unpacked `TextDiff.exe`. GUI/visual QA (no white screen, i18n, persistence, tray) must be done by a human on a real (ideally WebView2-less) Windows box — a headless agent can only confirm the process launches without crashing.

## Gotchas (the non-obvious, hard-won ones)

| # | Gotcha | Fix |
|---|--------|-----|
| 1 | **White screen / unstyled — the `file://` trap.** `win.loadFile("out/index.html")` makes absolute asset paths `/_next/...` resolve to the **filesystem root**, not the app dir → every asset 404s. `loadFile` does NOT rebase absolute paths. (Agents confidently claim it "resolves relative to the file" — it does not.) | Register a custom **`app://` standard+secure** scheme and serve `out/` via `protocol.handle`; `loadURL("app://local/")`. Absolute `/_next/...` then resolve against the protocol origin. Bonus: a stable origin makes `localStorage` (theme/locale via next-themes) persist reliably — `file://`'s opaque origin silently breaks it. |
| 2 | **`trailingSlash:false` → flat files, no directory index.** Pages are `en.html`/`zh.html`, not `en/index.html`; a file/protocol server won't append `.html`. | Resolver fallback: try `path` → `path + ".html"` → `path + "/index.html"` → `404.html`. Handles both trailingSlash modes. Use exact-segment matching so `zh-hant` isn't swallowed by `zh`. |
| 3 | **Language not remembered across launches.** Static export has **no middleware**, so root `index.html` redirects to the *default* locale every launch — the web app cannot remember. | Persist locale in a **main-process** JSON store; launch with `loadURL("app://local/" + savedLocale)`; capture changes via `webContents.on("did-navigate", …)` parsing the locale segment from the URL. |
| 4 | **Don't couple the web app to Electron.** The naive instinct is a `preload.js` + `ipcMain.handle("set-locale")` that the React switcher must call — this edits `src/` and breaks the plain web build. | Everything (locale, window-state) is doable **passively** in the main process (`did-navigate`, window events). No preload, no IPC, no renderer edits. Keep `src/` byte-identical. |
| 5 | **`node --test` can't run if pure logic imports electron.** `require("electron")` outside an Electron runtime throws. | Keep path-resolution, locale-parsing, and the store in modules that import only Node built-ins + `./constants`. Pass `win`/`app` in as parameters. Import electron ONLY in protocol.js/tray.js/main.js. Also: `test:electron` should **list the test files explicitly** (`node --test electron/resolvePath.test.js …`) — the `electron/*.test.js` glob is fragile (PowerShell won't expand it, so it leans on `node --test`'s own glob, which needs Node ≥ 21), and `node --test electron` tries to load `electron` as a module. |
| 6 | **Packaged resource paths must match electron-builder; works in dev, white-screens packaged.** `main.js` uses `process.resourcesPath/out` and `/icon.png` when `app.isPackaged`. | `extraResources` must map `from: out → to: out` and `from: build/icon.png → to: icon.png` so the runtime paths line up. The static export is NOT in the asar — it's real files under `resources/`. |
| 7 | **Web fonts hang offline.** A raw `<link href="fonts.googleapis.com">` fetches at runtime → FOUT/hang on an air-gapped box. | `next/font/google` self-hosts fonts into `_next/static/media` at **build** time (fine offline, as long as the CI build machine has internet). Self-host any other web fonts; never CDN-link them. |
| 8 | **App can never quit / tray icon vanishes.** Close-to-tray that always `preventDefault`s traps the user; a `Tray` with no retained reference is garbage-collected and disappears. | Intercept window `close` → `preventDefault()`+`hide()` **UNLESS `app.isQuitting`**; only the tray "Quit" item sets `app.isQuitting=true` then `app.quit()`. Assign the `Tray` to a variable that outlives setup. |
| 9 | **Relaunch spawns duplicate windows.** | `app.requestSingleInstanceLock()`; `app.quit()` if not primary; on `second-instance` restore/show/focus the existing window. |
| 10 | **`workflow_dispatch` button missing.** GitHub only shows "Run workflow" if the workflow file is on the **default branch**. Keeping the desktop build on a side branch hides the button. | Keep the workflow **only on `main`** with `checkout: { with: { ref: <desktop-branch> } }` — the pinned `ref` makes both the manual button *and* tag pushes build the branch's code, so you don't need (or want) a copy on the desktop branch, which would only drift. Keep it separate from any existing Tauri/desktop workflow rather than overwriting it. |
| 11 | **`portable` exe is slow to start; unsigned exe warns.** electron-builder `portable` = a self-extractor that re-unzips to %TEMP% on **every** launch. And any unsigned build trips Windows SmartScreen "unknown publisher". | For intranet, `target: dir` → `win-unpacked/` runs `TextDiff.exe` directly (no per-launch extraction). Distribute the folder (zip for transport; GitHub auto-zips an uploaded folder artifact). SmartScreen needs a code-signing cert to silence — usually acceptable internally. |
| 12 | **Release ends up empty / Electron build never ran when shipping in the same tag as Tauri.** Three traps: (a) tag-triggered runs execute the workflow **from the tagged commit**, so a fix merged to `main` *after* you tag doesn't apply — and if the tagged commit's `electron.yml` lacks a `push: tags` trigger, the Electron build never fires (only Tauri does); (b) if Electron polls for the Tauri-created **draft** Release by git-tag name but Tauri names the release from its **app version**, a version mismatch makes Electron wait then time out, attaching nothing; (c) naming the zip from the (possibly stale) feature-branch `package.json` mislabels the asset. | Cut the tag from a commit whose `main` already has the corrected workflow; rescue a bad one by re-tagging (`gh release delete vX --yes; git push origin :refs/tags/vX; git tag vX <fixed-commit>; git push origin vX`). Make the **git tag the single source of truth** on *both* workflows: inject it before build (`npm pkg set version="${GITHUB_REF_NAME#v}"`, guarded to `push`), and have the zip name + the `gh release upload` target both derive from the tag (`${GITHUB_REF_NAME#v}` / `$GITHUB_REF_NAME`), never the branch `package.json`. Keep workflows on `main` only (gotcha #10). The Release is a **draft** until you publish it. |

## Real-world result

An 18-locale next-intl static-export tool wrapped in one branch: `src/` untouched, the hard logic (path resolution, locale parsing, store) unit-tested as pure Node modules (`node --test`), ~150 MB self-contained Windows build that runs with **no WebView2 / no network**, remembers language + window state, single-instance, close-to-tray. Pure modules verify locally; GUI QA is human-on-Windows.
