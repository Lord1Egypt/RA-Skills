---
name: nextjs-to-electron
description: Use when converting a Next.js static export into a Windows Electron desktop app, especially for offline machines without WebView2. Next.js 转 Windows Electron / 将 Next.js 静态导出打包成 exe. Confirm the project supports static export and Windows Electron is the intended target.

metadata:
  version: "1.1.17"
  openclaw:
    homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/nextjs-to-electron
    emoji: "⚛️"
    requires:
      bins: ["node"]
    files:
      - electron-files.md
---

# Next.js → Electron Desktop App

## Overview

Wrap a **static-exportable** Next.js (App Router) app in a thin Electron shell. Electron bundles its own Chromium, so unlike Tauri it needs **no system WebView2** — the reason to pick it for locked-down/intranet machines. Keep the web behavior intact and put shell-specific behavior in `electron/`. Make the source or configuration changes required for a working export.

**Core principle:** Serve the export over a custom `app://` protocol, NOT `file://`. Almost all migration pain is path/origin resolution, not React — and `file://` silently breaks both. (See [electron-files.md](electron-files.md) for all copy-paste code.)

## When to use

- The app is (or can be) a **static export** (`output: "export"`) — diff/format/calculator/viewer tools, no SSR or API-at-runtime.
- **Export prerequisites**: `output: "export"` in `next.config.*`. The default `next/image` optimizer needs a server; use `images.unoptimized: true` for the offline template, or retain an export-compatible custom loader after verifying its network requirements.
- You want a Windows desktop build that runs **fully offline**, especially where WebView2 is absent (LTSC/Server images, air-gapped intranet) so Tauri won't launch.

**Check platform and toolchain compatibility.** Confirm the target Windows version and architecture against the selected Electron release. Use a supported stable Electron line and compatible builder/updater versions from the project's package source; old release asset inventories do not establish current support.

For CI, select a supported Node version that satisfies the build tools' engines. An explicit Active LTS major is a reproducible default; retain a deliberate project pin policy. `engines.node` expresses compatibility, not simply the CI version. See [Electron releases](https://releases.electronjs.org/releases.json) and the [Node schedule](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json).

Runtime API routes, SSR and server actions need a separately assessed server/sidecar design. Consider `nextjs-to-tauri` when a system WebView is acceptable; measure package sizes from actual artifacts. Maintenance of an existing Electron app uses `desktop-app-standard` rather than repeating this migration.

Build-time Server Components and statically generated GET handlers can remain; do not convert them all to `"use client"`. Verify that their data is emitted into the export and does not need a runtime Next.js server. See [static-export support](https://nextjs.org/docs/app/guides/static-exports#supported-features).

This playbook targets **Windows** (`--win dir`/`portable`, SmartScreen, WebView2-less boxes). macOS/Linux packaging (`.dmg`/`.AppImage`, notarization, codesigning) is out of scope.

Local migration covers the necessary source/configuration changes. Remote tags, public releases and signing-service setup follow the user's authorized scope; a read-only assessment reports blockers and proposed checks without installing or building.

## Procedure

Adapt the following steps to the repository. Full code is in [electron-files.md](electron-files.md). Preserve existing web behavior and make only necessary export or desktop integration changes. Commands use **yarn**; in an npm or pnpm repo substitute the equivalent (`npm ci` for `yarn install --frozen-lockfile`) and match `setup-node`'s `cache:` to the lockfile you actually have — `cache: yarn` fails the job outright when there is no `yarn.lock`.

1. **Confirm the export is client-side and check its shape.** `yarn build`, then `ls out/` — you'll see flat files (`index.html`, `en.html`, `zh.html`) and `_next/`. `trailingSlash: false` (flat files) is fine; the resolver handles both layouts (gotcha #2). If the build stops on the default image loader, that is the `images.unoptimized` prerequisite above — set it and rebuild.

2. **Add the toolchain** (after the version check above): `yarn add -D electron electron-builder`. In `package.json` add `"main": "electron/main.js"` and scripts: `electron:dev` (`node scripts/electron-dev.cjs`, which sets `ELECTRON_DEV=1` and spawns electron), `electron:build` (`next build && electron-builder --win dir`), `test:electron` (list the test files explicitly — `node --test electron/resolvePath.test.js electron/store.test.js …`; choose a glob only when the project Node/shell supports it, gotcha #5). Add `electron/package.json` with `{"type":"commonjs"}` so the shell and its tests also run when the Next.js project's root declares `"type": "module"`.

3. **Create the `electron/` layer** (copy from electron-files.md). Split into **pure modules that must NOT `require("electron")`** (so `node --test` runs them) and Electron-bound ones:
   - `constants.js` — `SCHEME="app"`, `LOCALES[]`. `resolvePath.js` — `resolveAssetPath(outDir, pathname, exists)` with `.html`→`/index.html`→`404.html` fallback. `store.js` — dependency-free JSON store in `userData`. `locale.js` — `startUrl`/`parseLocale`/`trackLocale`. `window-state.js` — `createWindowStateKeeper`. (All pure → unit-tested.)
   - `protocol.js`, `tray.js`, `main.js` — the only files that import electron.

4. **Register and handle `app://`** using [the protocol template](electron-files.md). Register privileges before ready, install the handler after ready, and load the saved locale. Preserve the path resolver and failure handling; retain context isolation, sandboxing and disabled Node integration for renderer content.

5. **Wire the sample desktop features in main.js** (passive navigation/window events, gotchas #3, #4): single-instance lock + second-instance focus; restore window bounds from the store; `trackLocale(win, store)` persists locale on `did-navigate`; tray with close-to-tray via an `app.isQuitting` flag.

6. **Package** (gotcha #6). `electron-builder.yml`: `extraResources` maps `out → out` and `build/icon.png → icon.png`; `main.js` reads them at `process.resourcesPath/out` and `/icon.png` when packaged. Choose target: `dir` (unpacked folder — runs `<AppName>.exe` directly, fast) vs `portable` (self-extractor, re-unzips to %TEMP% every launch, slower) — gotcha #11.

7. **CI**: adapt the [bundled workflow](electron-files.md) to the actual lockfile and commands. It builds Windows artifacts; tag runs inject the version before build, create/reuse an unpublished draft, verify the ZIP, SHA256 and source commit, then publish automatically. Manual runs only upload workflow artifacts. Check the template's Action pins and Node version against the selected toolchain before adoption. For side branches or multiple apps, use its full-SHA source-map/coordinator guidance; do not overwrite an existing Tauri workflow or bypass the asset verifier with an ad hoc upload.

8. **Verify and deliver** using the checks below; distinguish pure-module tests from native Windows execution.

## Gotchas (diagnostic index)

The [copy-paste templates](electron-files.md) own the implementation; keep these numbers when following their inline references.

| # | Symptom | Check |
| --- | --- | --- |
| 1 | White screen or unstyled page | `file://` resolves `/_next/...` at the filesystem root. Use the procedure's standard, secure `app://` origin; it also gives storage a stable origin. |
| 2 | Flat export route 404 | Preserve the resolver's `.html`, directory-index and 404 fallbacks, with exact locale segments so `zh-hant` is not parsed as `zh`. |
| 3 | Locale resets | Static export has no middleware; enter the saved locale and persist explicit navigation in the main-process store. |
| 4 | Desktop integration breaks web | Prefer passive main-process events. Add narrow, guarded preload/IPC only for features that require it. |
| 5 | Tests import Electron or discover zero cases | Keep pure modules independent and verify discovery on the actual Node/shell; the example lists files explicitly. |
| 6 | Development works, packaged app fails | Match `extraResources` with `process.resourcesPath` and preserve the full unpacked folder. Packaging and ignore-rule examples are in the template. |
| 7 | Fonts hang offline | Self-host runtime fonts. `next/font/google` downloads at build time, so the build environment still needs access. |
| 8 | Tray disappears or app cannot quit | Retain the Tray reference and verify quit-flag and failed-tray fallbacks in `main.js`. |
| 9 | Second launch duplicates windows | Verify the single-instance lock and restore/show/focus path. |
| 10 | Manual workflow button is absent | Keep the workflow on the default branch for the button, and in each release-tag commit for tag-triggered builds. |
| 11 | Portable startup is slow or unsigned builds warn | `portable` re-extracts each launch; the unpacked-folder target avoids that cost. Disclose signing state; a certificate alone does not guarantee a particular SmartScreen result. |
| 12 | Release is empty or versions mismatch | Build the tag or its committed full source SHA, derive version/asset names from that tag, and verify current files before upload. See the template's multi-app source-map variant and publication policy. |

## Delivery

Run the pure-module tests and build the package, then launch the unpacked Windows app. Exercise rendering, locale persistence, window state, single-instance behavior, tray close/reopen and actual quit. Test a WebView2-less environment when required, and verify offline assets without assuming CI network access proves offline operation.

Deliver the runnable package, tests and UI checks actually performed, measured asset sizes and remaining environment limits. A build or process launch alone does not prove those behaviors.
