---
name: nextjs-to-tauri
description: Use when converting a Next.js 16 App Router static export into a Tauri 2 desktop app. Next.js 静态导出转 Tauri 2 / 打包 Next.js 为 Tauri 桌面应用. Covers native shell, tray, optional updater and GitHub Actions. Existing Tauri maintenance uses desktop-app-standard.

metadata:
  version: "1.1.22"
  openclaw:
    homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/nextjs-to-tauri
    emoji: "🦀"
    requires:
      bins: ["node"]
    files:
      - tauri-files.md
      - frontend-integration.md
      - desktop-build.yml
      - tauri-build.yml
      - release-workflow.md
      - release-assets.js
      - release-assets/**
      - ci/**
---

# Next.js 16 → Tauri 2 Desktop App

## Overview

Wrap a **static-exportable** Next.js 16 (App Router) app in a thin Tauri 2 native shell. Preserve web behavior while adding the export configuration and desktop integrations needed. Tauri serves the export from its embedded asset server. GitHub Actions can build the native shell when a local Rust toolchain is unavailable.

**Core principle:** Tauri loads the static export over its own asset protocol — which behaves differently from a real HTTP server. Most migration pain is path/routing resolution, not React.

## When to use

- The app is (or can be) a **static export** (`output: "export"`) — diffing/formatting/calculator/viewer tools, no SSR-at-runtime needed.
- You want a desktop/portable `.exe`, `.dmg`, `.AppImage`, optionally with auto-update.

A live Node server, runtime API routes, SSR or server actions require a different packaging design, such as a separately assessed sidecar. This playbook covers Next.js static exports.

Keep Server Components and GET handlers that resolve fully at build time; verify their exported files rather than converting the whole app to `"use client"`. Desktop hooks alone need the client boundary shown in the integration template. See [static-export support](https://nextjs.org/docs/app/guides/static-exports#supported-features).

## Project changes

Adapt templates into the target project: Next config and package scripts, `src-tauri/`, selected desktop frontend code, icons, ignore rules and the build workflow. Preserve unrelated web behavior. Migration authorization covers these necessary local changes; do not add a separate approval before every file write. Signing-service configuration and publication follow the user's authorized scope.

## Procedure

Adapt these steps to the repository. Supporting files contain the configuration and code templates.

Read-only assessment stops at findings and proposed checks. The bundled workflow verifies a draft before manual publication; `desktop-app-standard` has a separate direct-publication default. Preserve the requested release policy rather than mixing those workflows.

**Package manager:** the commands and `desktop-build.yml` assume Yarn Classic. In an npm or pnpm repo substitute the equivalent (`npm ci` / `pnpm install --frozen-lockfile`, `npm exec --no -- tauri` / `pnpm tauri`) and change the workflow's `cache:` and install line — `cache: yarn` fails outright when there is no `yarn.lock`.

1. **Verify target-compatible stable versions** (this playbook targets Tauri 2):
   - npm: query the published 2.x versions of `@tauri-apps/cli` and the plugins used, then confirm JS/Rust compatibility. An upstream `latest` in a higher major does not change this playbook's target.
   - crates: read and parse the package metadata as JSON, for example:
     ```bash
     # Save metadata, then parse it as data.
     curl -sA x -o crates-tauri.json https://crates.io/api/v1/crates/tauri
     node -p "JSON.parse(require('fs').readFileSync('crates-tauri.json','utf8')).crate.max_stable_version"
     ```
     `max_stable_version` is an upstream reference, not the install target when it is outside 2.x. Select published, non-yanked stable 2.x releases for core and each required plugin (`tauri-plugin-opener`, `tauri-plugin-updater`, …), and verify their compatibility.
   - actions: `gh api repos/actions/checkout/releases/latest --jq .tag_name` (+ `actions/setup-node`, `Swatinem/rust-cache`, `actions/upload-artifact`; `tauri-apps/tauri-action@v1` is the moving major tag — check its README, not the release list)
   - node: current Active LTS from the [official schedule](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json). Pin that major in `desktop-build.yml`; **do not use `lts/*` or `latest`** — CI would jump to a new line without a reviewed upgrade.
   - `engines.node` is the code's real floor (take it from Next.js/Tauri CLI constraints), not a copy of the CI major; `.nvmrc` is optional.
   - optional: when `desktop-app-standard` is available, its audit can supplement version and CI checks. The migration does not depend on installing another skill.

2. **Gate static export on Tauri** in `next.config.*`, using the explicit `TAURI_BUILD` flag shown below (gotcha #1). Existing reliable build gating can be retained. Merge into your existing config, keeping the `next-intl` plugin wrapper:
   ```ts
   // The NextConfig annotation is load-bearing: spreading `{ output: "export" }` into an
   // un-annotated object literal widens output to `string`, and withNextIntl() then
   // rejects it — `yarn build:tauri` fails type-checking before it ever builds.
   import type { NextConfig } from "next";
   import createNextIntlPlugin from "next-intl/plugin";
   const withNextIntl = createNextIntlPlugin();

   const isTauri = process.env.TAURI_BUILD === "1"; // set by `yarn build:tauri`

   const nextConfig: NextConfig = {
     // ...your existing config...
     ...(isTauri ? { output: "export", trailingSlash: true } : {}),
     images: {
       // ...preserve existing image settings...
       ...(isTauri ? { unoptimized: true } : {}),
     },
   };

   export default withNextIntl(nextConfig);  // keep your existing wrapper(s)
   ```
   Add the flag-setting script (`yarn add -D cross-env`) — tauri.conf's `beforeBuildCommand` runs it, NOT plain `yarn build`:
   ```jsonc
   // package.json → "scripts"
   "build:tauri": "cross-env TAURI_BUILD=1 next build"
   ```

3. **Scaffold** (CLI steps are JS — no Rust needed):
   ```bash
   yarn add -D @tauri-apps/cli@^2
   yarn tauri init --ci --app-name "<app>" --window-title "<Title>" \
     --frontend-dist "../out" --dev-url "http://localhost:3000" \
     --before-dev-command "yarn dev" --before-build-command "yarn build:tauri"
   # The source must be SQUARE (the CLI says "squared PNG or SVG") and 1024x1024 — that
   # is the master Tauri's icon generator works from, so a smaller source gets scaled up.
   yarn tauri icon public/logo.png
   ```
   Mobile icon directories need no cleanup for this migration. Retain them if the project has mobile targets.

   Then **fix `.gitignore`** — see gotcha #3.

4. **Edit `src-tauri/` config & Rust.** Adapt `tauri-files.md`, including its CSP and optional-updater checklist: `tauri.conf.json` (window `url`, updater, `webviewInstallMode`, portable `mainBinaryName`), `Cargo.toml` (plugin deps + release profile), `src/lib.rs` (plugin registration + tray + single-instance), `capabilities/default.json` (permissions).

5. **Frontend integration** (only the features you need). Adapt [frontend-integration.md](frontend-integration.md) to the project's existing desktop boundary (the examples use `src/app/desktop/`): external-links util (opener-based), auto-update hook, and — for `next-intl` apps — the language-choice hook (it remembers the locale the **user** picked in the switcher). Mount them in one `"use client"` component rendered inside your providers (e.g. antd `<App>`, inside `NextIntlClientProvider`). That component also installs the global external-link interceptor (gotcha #10). Switch locales with plain `router.push` (soft nav works in Tauri — never hard-nav a switch); if you remember the language, guard the launch redirect with a module-level flag (gotcha #11).
   The supplied updater downloads in the background before asking to install; include it only when that matches the product's update policy. Timing and network behavior are documented in `frontend-integration.md`.

6. **Version single-source + CI.** Add `src-tauri/update-version.cjs` and an `update-version` script (copies `package.json` version into `tauri.conf.json`). Install both workflow templates and all release scripts using the copy map in [release-workflow.md](release-workflow.md). The caller handles the serial build matrix and draft gate; the reusable build workflow handles each target. The modular verifier compares exact draft files and digests against this run’s per-target evidence before checksums and attestation.
   The helper copies the project package version into Tauri config; review the resulting project diff with the migration changes.

   - **Make the git tag the single source of truth (the template does this):** on tag push, `npm pkg set version="${GITHUB_REF_NAME#v}"` (guarded `if: github.event_name == 'push'`) runs *before* `update-version`, so installer filenames, the embedded app version and `tagName: v__VERSION__` all equal the tag — you set the version by tagging, never by bumping branches. Do NOT point `tagName` at `github.ref_name` (gotcha #13).
   - **If you skip injection, the pushed git tag MUST equal `package.json` version** (`v3.0.0` ↔ `"version": "3.0.0"`). `tauri-action` expands `__VERSION__` from the app version, and the portable-exe step uploads to `v${APP_VERSION}` — a mismatch silently breaks the portable upload.
   - **Verify signing by platform.** Updater signatures and OS code signing are separate. Configure the required Windows/macOS signing and notarization for the actual distribution, and report unsigned or unverified paths rather than assuming the template covers them.

7. **Configure update signing only when needed.** Follow [Updater signing keys](tauri-files.md#updater-signing-keys) for generation, public/private key handling, existing-key preservation and repository secrets. Never commit or silently replace a private key.

8. **Verify the frontend export:** `yarn build:tauri`, then confirm the export shape:
   ```bash
   ls "out/<default-locale>/index.html"   # use the configured locale; single-locale apps use out/index.html
   ```
   If Rust and platform dependencies are available, build and exercise the shell locally. Otherwise use CI and report which native checks remain unverified.

## Delivery and remaining setup

Report the generated package and checks actually performed. Hand off only unfinished actions, such as missing signing credentials, target-device checks or publication outside the authorized scope. The supplied workflow creates a verified draft; `releases/latest` ignores drafts, so the release must be published before clients can discover it. A tag must include the applicable workflow and select the intended source commit.

## Gotchas (the non-obvious, hard-won ones)

| # | Gotcha | Fix |
|---|--------|-----|
| 1 | **White screen / flat files.** The asset server may not resolve an extensionless path to `en.html`. | For this directory-index template, use `trailingSlash: true` in the desktop export and enter the configured locale directory, e.g. `/en/`. Keep the window URL and frontend default locale consistent. `TAURI_BUILD` makes the build choice explicit; retain another verified configuration when appropriate. |
| 2 | **Runtime locale middleware is unavailable in static export.** | Gate desktop export with `TAURI_BUILD` so ordinary web builds keep their configuration. Validate exported locale entry files instead of relying on Proxy redirects; see [Next.js static-export limits](https://nextjs.org/docs/app/guides/static-exports#unsupported-features). |
| 3 | **`src-tauri/` vanishes from `git status`.** Some repo `.gitignore`s have a bare `src-tauri` line. | Replace with `src-tauri/target` + `src-tauri/gen/schemas`. Verify: `git check-ignore src-tauri/tauri.conf.json` returns nothing. |
| 4 | **`isTauri()` false positives** if you detect by dynamic-importing `@tauri-apps/api`. It imports fine in a plain browser; `invoke` only throws at call time. | Detect via runtime globals: `window.__TAURI_INTERNALS__` / `__TAURI__` / UA contains `Tauri`. Same bundle ships to web + desktop. |
| 5 | **Single-instance plugin must be registered FIRST**, before all other plugins, or second-launch refocus won't route. Desktop-only (target-gate it off mobile). | See `lib.rs` ordering in `tauri-files.md`. |
| 6 | **CI succeeds but clients see no update.** Stable `releases/latest` ignores draft and prerelease releases. | Check the actual endpoint and publication state. The supplied workflow verifies a draft before publication; do not delete a published release to make a draft-only rerun work. Use a new version for published corrections, or adapt to the repository's existing publication policy. |
| 7 | **Committing the private signing key** lets anyone sign malicious auto-updates your clients auto-trust. The `.pub` is public/safe; the bare key is not. | `.gitignore` the private key; store it only as a GitHub secret. If one ever lands in git history, rotate it. |
| 8 | **Portable exe is mistaken for an installed, self-updating app.** | The raw binary still needs WebView2 and is distributed without a self-update guarantee. Catch and surface install failures; test any proposed portable update path separately. If portable builds must make no updater requests, use the [no-updater checklist](tauri-files.md#optional-updater-keep-the-layers-consistent) or another verified package-specific switch. |
| 9 | **System-language detection returns the wrong or unsupported locale.** | Preserve the product's language policy. The example starts at the configured default and remembers an explicit choice. If auto-detection is wanted, validate against supported locales with a fallback and never overwrite an existing user preference. |
| 10 | **External links replace the app page or opener calls are denied.** | Route intended external URLs through plugin-opener and keep internal links with the router. Grant the needed URL scopes: `opener:default` covers common schemes, or use explicit scoped permissions. A bare command permission without matching scope is insufficient. |
| 11 | **Locale switching bounces back.** Startup redirects or hard reloads run again after the locale layout remounts. | Prefer soft router navigation. Keep the startup guard stable across remounts (the example uses a module variable), and persist explicit choices after startup restoration so the entry locale cannot overwrite a saved preference. |
| 12 | **Linux aborts with EGL errors or an AppImage opens blank.** | Distinguish WebKit DMABUF failure from bundled Wayland/host library incompatibility before applying workarounds; see [Linux diagnosis](tauri-files.md#linux-egl-与-appimage-兼容性). |
| 13 | **Tag workflow misses a CI fix, builds mismatched versions or uploads no assets.** | The tag commit must contain the applicable workflow. Follow step 6 for version injection and the workflow verifier. For a multi-app release hub, keep its full-SHA source map in that release commit and preserve it on reruns. Repair a published version with a new tag; review stale assets before rerunning an unpublished draft. |

## Validation boundary

Confirm the export and native startup, tray, locale persistence and any updater behavior on supported platforms. Include offline/portable constraints and measured package sizes in the delivery record above. A frontend build or CI compile alone does not prove desktop behavior.
