---
name: nextjs-to-tauri
version: 1.1.1
description: Use when converting or migrating a Next.js 16 (App Router) web app into a Tauri 2 desktop app — packaging a static-export site as a desktop/portable .exe, adding auto-update, language persistence, window-state, single-instance, or system tray, or setting up GitHub Actions Tauri builds. Covers next-intl i18n static-export gotchas (the trailingSlash white-screen), updater signing keys, and cross-platform CI.
tags: [tauri, nextjs, desktop, app-router, static-export, auto-update, next-intl, github-actions]
homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/nextjs-to-tauri

metadata:
  clawdbot:
    emoji: "🦀"
    files:
      - tauri-files.md
      - frontend-integration.md
      - desktop-build.yml
---

# Next.js 16 → Tauri 2 Desktop App

## Overview

Wrap a **client-side** Next.js 16 (App Router) app in a thin Tauri 2 native shell. The React code is untouched; Tauri serves the static export from its embedded asset server. Build in GitHub Actions so no local Rust is needed.

**Core principle:** Tauri loads the static export over its own asset protocol — which behaves differently from a real HTTP server. Most migration pain is path/routing resolution, not React.

## When to use

- The app is (or can be) a **static export** (`output: "export"`) — diffing/formatting/calculator/viewer tools, no SSR-at-runtime needed.
- You want a desktop/portable `.exe`, `.dmg`, `.AppImage`, optionally with auto-update.

**Do NOT use when** the app needs a live Node server at runtime (real API routes, SSR, server actions). Tauri can bundle a sidecar server, but that's a different, heavier playbook.

## Procedure

Do these in order. Copy-paste templates live in the supporting files.

1. **Verify latest versions first** (they drift — never trust the numbers in templates):
   - npm: `npm view @tauri-apps/cli version` (+ `plugin-opener`, `plugin-updater`)
   - crates: `curl -sA x https://crates.io/api/v1/crates/tauri | python -c "import sys,json;print(json.load(sys.stdin)['crate']['max_stable_version'])"` (repeat for each `tauri-plugin-*`)
   - actions: `gh api repos/actions/checkout/releases/latest --jq .tag_name` (+ `actions/setup-node`, `Swatinem/rust-cache`, `actions/upload-artifact`; `tauri-apps/tauri-action@v0` is the moving major)

2. **Gate static export on Tauri** in `next.config.*`, driven by an EXPLICIT build flag — NOT Tauri's auto-injected `TAURI_ENV_PLATFORM`, which isn't reliably set for the frontend build and silently yields flat files (gotcha #1). Merge into your existing config, keeping the `next-intl` plugin wrapper:
   ```ts
   import createNextIntlPlugin from "next-intl/plugin";
   const withNextIntl = createNextIntlPlugin();

   const isDev = process.env.NODE_ENV === "development";
   const isTauri = process.env.TAURI_BUILD === "1"; // set by `yarn build:tauri`

   const nextConfig = {
     // ...your existing config...
     ...(isDev ? {} : { output: "export" }),       // export is build-only (gotcha #2)
     ...(isTauri ? { trailingSlash: true } : {}),   // Tauri-only (gotcha #1)
     images: { unoptimized: true },
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
   yarn add -D @tauri-apps/cli@latest
   yarn tauri init --ci --app-name "<app>" --window-title "<Title>" \
     --frontend-dist "../out" --dev-url "http://localhost:3000" \
     --before-dev-command "yarn dev" --before-build-command "yarn build:tauri"
   yarn tauri icon public/logo.png   # needs a ≥512×512 source; rm src-tauri/icons/{android,ios} if desktop-only
   ```
   Then **fix `.gitignore`** — see gotcha #3.

4. **Edit `src-tauri/` config & Rust.** Copy from `tauri-files.md`: `tauri.conf.json` (window `url`, updater, `webviewInstallMode`, portable `mainBinaryName`), `Cargo.toml` (plugin deps + release profile), `src/lib.rs` (plugin registration + tray + single-instance), `capabilities/default.json` (permissions).

5. **Frontend integration** (only the features you need). Copy from `frontend-integration.md`: external-links util (opener-based), auto-update hook, and — for `next-intl` apps — the remember-language hook. Mount them in one `"use client"` component rendered inside your providers (e.g. antd `<App>`, inside `NextIntlClientProvider`). That component also installs the global external-link interceptor (gotcha #10). Switch locales with plain `router.push` (soft nav works in Tauri — never hard-nav a switch); if you remember the language, guard the launch redirect with a module-level flag (gotcha #11).

6. **Version single-source + CI.** Add `src-tauri/update-version.js` and an `update-version` script (copies `package.json` version into `tauri.conf.json`). Copy `desktop-build.yml` for cross-platform builds, signing, draft release with `latest.json`, and the portable-exe steps.
   - **Make the git tag the single source of truth (most robust — the template does this):** on tag push, inject the tag into `package.json` *before* `update-version` runs — `npm pkg set version="${GITHUB_REF_NAME#v}"`, guarded `if: github.event_name == 'push'`. `update-version` then propagates it into `tauri.conf.json`, so installer filenames, the embedded app version, and `tagName: v__VERSION__` all equal the tag automatically — you only ever set the version by tagging, never bump branches. **Do NOT instead point `tagName` at `github.ref_name`** (gotcha #13).
   - **If you skip injection, the pushed git tag MUST equal `package.json` version** (`v3.0.0` ↔ `"version": "3.0.0"`). `tauri-action` expands `__VERSION__` from the app version, and the portable-exe step uploads to `v${APP_VERSION}` — a mismatch silently breaks the portable upload.
   - **Windows is fully covered; macOS/Linux are not signed.** Unsigned `.dmg`/`.app` is blocked by macOS Gatekeeper, and unsigned `.AppImage` triggers warnings. If you ship beyond Windows, add Apple notarization / codesigning secrets — out of scope here.

7. **Auto-update signing keys** (only if shipping updates):
   ```bash
   yarn tauri signer generate --ci -p "" -w src-tauri/app.key -f   # private key — gitignore it, NEVER commit (gotcha #7)
   cat src-tauri/app.key.pub   # paste this base64 into tauri.conf.json plugins.updater.pubkey
   ```
   The CI signing step needs the private key as a repo secret — **without it every signed build fails**. The agent doing the migration usually can't set repo secrets, so it MUST **remind the user to run this (or set it in the GitHub UI)**:
   ```bash
   gh secret set TAURI_SIGNING_PRIVATE_KEY < src-tauri/app.key   # bash / Git Bash
   # only if you generated the key WITH a password (not `-p ""`):
   gh secret set TAURI_SIGNING_PRIVATE_KEY_PASSWORD
   ```
   **PowerShell** has no `<` redirection — pipe instead:
   ```powershell
   Get-Content src-tauri/app.key -Raw | gh secret set TAURI_SIGNING_PRIVATE_KEY
   ```
   Manual path: repo → Settings → Secrets and variables → Actions → New repository secret.

8. **Verify** (without Rust): `yarn build:tauri`, then confirm the export shape:
   ```bash
   ls out/en/index.html   # MUST exist (not out/en.html) — proves trailingSlash worked
   ```
   The Rust shell (tray/single-instance API) only compiles in CI — flag that you can't compile it locally and let the first Actions run validate it.

## Handoff — remind the user (manual, easy to forget, fail silently)

The code migration is done by the agent; these steps need the human and break things quietly if skipped. **After migrating, surface them explicitly:**

1. **Set the signing secret** before the first build — bash: `gh secret set TAURI_SIGNING_PRIVATE_KEY < src-tauri/app.key`; PowerShell: `Get-Content src-tauri/app.key -Raw | gh secret set TAURI_SIGNING_PRIVATE_KEY`; or the GitHub UI. Without it, CI signing fails (step 7).
2. **Publish (un-draft) the first release** — builds produce a *draft*; the updater resolves `releases/latest`, which ignores drafts, so updates never reach anyone until you un-draft it (gotcha #6).
3. **Tag from a `main`/default-branch commit that already has the corrected workflow** — a tag-triggered run uses the workflow from the *tagged commit*, not the branch tip, so a fix landed after the tag silently doesn't apply (gotcha #13). With the template's tag-injection step you no longer hand-sync versions; only if you removed it must you keep `package.json` == the pushed `v*` tag (step 6).

## Gotchas (the non-obvious, hard-won ones)

| # | Gotcha | Fix |
|---|--------|-----|
| 1 | **White screen / flat files.** Static export puts `/en` at `en.html` + an `en/` dir of RSC data; Tauri's asset server serves a directory's `index.html` but does **not** append `.html` to extensionless paths. | `trailingSlash: true` (Tauri builds only) → emits `en/index.html`, resolved by directory-index. **Gate it with an explicit `TAURI_BUILD` flag (`yarn build:tauri`), NOT the auto-injected `TAURI_ENV_PLATFORM`** — the latter isn't reliably set, so a stray `yarn build` emits flat files and locale routing breaks. Set window `url: "/en/"` as a safe entry; don't rely on the root `/`→`/en` redirect (emitted without a trailing slash, 404s in Tauri). |
| 2 | **`output: "export"` + middleware is forbidden in Next 16 — even in dev.** `next-intl` ships middleware (`proxy.ts`/`middleware.ts`). Setting `output` in dev silently kills locale redirects. | Make `output` build-only (`isDev ? {} : {...}`). |
| 3 | **`src-tauri/` vanishes from `git status`.** Some repo `.gitignore`s have a bare `src-tauri` line. | Replace with `src-tauri/target` + `src-tauri/gen/schemas`. Verify: `git check-ignore src-tauri/tauri.conf.json` returns nothing. |
| 4 | **`isTauri()` false positives** if you detect by dynamic-importing `@tauri-apps/api`. It imports fine in a plain browser; `invoke` only throws at call time. | Detect via runtime globals: `window.__TAURI_INTERNALS__` / `__TAURI__` / UA contains `Tauri`. Same bundle ships to web + desktop. |
| 5 | **Single-instance plugin must be registered FIRST**, before all other plugins, or second-launch refocus won't route. Desktop-only (target-gate it off mobile). | See `lib.rs` ordering in `tauri-files.md`. |
| 6 | **Auto-update never reaches clients** though CI "succeeds." The updater endpoint resolves `releases/latest`, which **ignores draft and prerelease** releases. | Builds publish a draft; you must manually un-draft to roll out. Document this in the workflow. |
| 7 | **Committing the private signing key** lets anyone sign malicious auto-updates your clients auto-trust. The `.pub` is public/safe; the bare key is not. | `.gitignore` the private key; store it only as a GitHub secret. If one ever lands in git history, rotate it. |
| 8 | **Portable "green" exe + auto-update are incompatible.** `update.install()` expects an installed-app layout; on a standalone exe it fails/no-ops. The portable exe also needs the **WebView2** runtime (preinstalled Win 11 / current Win 10; absent on old LTSC/Server). | It's the raw `target/release/<mainBinaryName>.exe` (web assets compiled in). Ship it for convenience, but document "no self-update" and the WebView2 dependency. The failed `install()` is already caught by the hook, so it degrades gracefully. You can't cleanly detect "am I portable?" at runtime — it's the *same* compiled binary as the one inside the installers — so to truly hide the update prompt you'd produce a separate build with the updater plugin disabled. |
| 9 | **System-language autodetect is unreliable on macOS/Linux.** `navigator.language` in WKWebView/WebKitGTK can be `en-US` regardless of OS. Also `lang.split("-")[0]` can yield an unsupported locale. | Treat saved preference as source of truth; validate the detected locale against your locale list (`validLocales.includes(...)`) before using/saving it. |
| 10 | **External links open inside the app webview**, hijacking the tool; or `openUrl` does nothing at all. | One capture-phase `document` click delegate routes external http(s)/`mailto`/`tel` through `@tauri-apps/plugin-opener`'s `openUrl` (not shell); same-origin links fall through to the router. **Capability must be `opener:default`** — bare `opener:allow-open-url` has no URL scope, so the call is denied at runtime and nothing opens. `opener:default` bundles `allow-open-url` + `allow-default-urls` (http/https/mailto/tel). |
| 11 | **Language switching looks broken / bounces back to one locale.** Two self-inflicted causes: (a) hard-navigating a switch, and (b) a startup "remember-language" redirect guarded by a `useRef`. A locale switch **remounts the `[locale]` layout subtree**, so a hard reload re-resolves paths AND a `useRef` guard resets → the redirect re-fires and bounces every switch. | **Switch with plain `router.push` (soft nav) — it works in Tauri; never hard-nav a switch.** If you redirect to a remembered locale at launch, guard it with a **MODULE-LEVEL flag (not `useRef`)** so it fires once per session, use a **soft** `router.replace`, and save the preference **in the switcher**, not a navigation effect. |
| 12 | **App aborts or shows a blank window on some Linux desktops** (Xfce, VMs, hybrid/NVIDIA, and *especially* rolling distros — Manjaro/Arch/CachyOS) with `Could not create surfaceless EGL display: EGL_BAD_ALLOC. Aborting...`. (Surrounding `xapp-gtk3-module` / `atk-bridge` lines are harmless GTK/at-spi noise.) NOT a routing/white-screen (gotcha #1): EGL errors are present, it's platform-specific, Windows renders fine. **Two *different* layers fail with near-identical output — the decisive tell is whether the EGL line DISAPPEARS once `WEBKIT_DISABLE_DMABUF_RENDERER=1` is actually in effect.** **Layer A — WebKit render layer:** disabling DMABUF makes the line vanish and the app works. **Layer B — EGL-init layer, *below* WebKit:** the EGL line **persists unchanged no matter what `WEBKIT_*` vars you set** (the process aborts before WebKit ever reads its env vars), because the AppImage ships its own `libwayland-*.so` that clashes with the host's newer Mesa/libEGL — libwayland's protocol/ABI must match the loaded libEGL/Mesa, and on a rolling distro the bundled (older, Ubuntu-build-host) copy doesn't. **A persisting EGL line after the env var is confirmed-baked-in ⇒ layer B; stop adding `WEBKIT_*` vars.** | **Layer A:** set `WEBKIT_DISABLE_DMABUF_RENDERER=1` at the **very top of `run()`, before `Builder::default()`** (must precede GTK/WebView init), `#[cfg(target_os = "linux")]` + only-if-unset (`var_os(...).is_none()`). GPU-buffer **sharing** only — still accelerated, near-zero cost. *(`WEBKIT_DISABLE_COMPOSITING_MODE=1` forces **software** rendering and only helps a genuine GL-compositing failure; do **NOT** bake it in to chase a *persisting* EGL line — that's layer B and this won't fix it. We first misdiagnosed Manjaro Xfce as needing it — it didn't.)* **Layer B:** `WEBKIT_*` cannot help — fix the library clash. **Confirm** by having the reporter strip the bundled libs: `./App.AppImage --appimage-extract && find squashfs-root -name 'libwayland-*.so*' -delete && ./squashfs-root/AppRun` — if it paints, it's layer B. **Permanent fix:** at the very top of `run()` (before the WEBKIT block), when inside an AppImage (`APPIMAGE` env set), find the host `libwayland-client.so.0` (try `/usr/lib/x86_64-linux-gnu/`, `/usr/lib64/`, `/usr/lib/`), prepend it to `LD_PRELOAD`, and `exec()` re-run self **once** (sentinel env var to avoid a loop) so the loader overrides the stale bundled lib. Self-contained, ecosystem norm (yaak, tolaria). **Confirmed** fixing Manjaro Xfce where every layer-A/`WEBKIT_*` attempt had failed (subtitle-translator v3.0.0). Alternative: strip those 4 libs (`libwayland-client`/`cursor`/`egl`/`server`) from the AppImage in CI. See `tauri-files.md` `lib.rs`. Refs: [tauri #9394](https://github.com/tauri-apps/tauri/issues/9394), [espressif/idf-im-ui #755 (Arch/CachyOS)](https://github.com/espressif/idf-im-ui/issues/755), [tolaria fix](https://github.com/refactoringhq/tolaria/commit/8c286a4856637d662f05428f679faa4aee607c66). |
| 13 | **A CI fix on `main` doesn't apply to the release; or the release comes out empty / with mismatched installers.** Tag-triggered runs execute the workflow definition **from the tagged commit**, not the branch tip — tag a commit whose history predates your fix and the *old* workflow runs (or a newly-added `push: tags` trigger never fires at all). Separately, pointing `tagName` at `github.ref_name` ships a release *named* `v3.0.1` containing `..._3.0.0_...` installers, because installer names + embedded version come from `tauri.conf.json`, not `tagName` (and on `workflow_dispatch`, `github.ref_name` is a branch name). | Cut the `v*` tag from a commit that already contains the corrected workflow. To rescue a broken/empty release, re-tag after fixing: `gh release delete vX --yes; git push origin :refs/tags/vX; git tag vX <fixed-commit>; git push origin vX`. For version coherence, inject the tag into `package.json` at build time (step 6), don't fiddle with `tagName`. **Multi-app "release hub"** (one tag on `main` fans out to Tauri + Electron, each workflow pinning `checkout … ref: <feature-branch>` to build that app's code): keep the workflows **only on `main`** and trigger from there — duplicate copies on feature branches drift out of sync and mislead, since the feature-branch copy is never what a tag runs. |

## What to expect

A typical multi-locale next-intl tool migrates in a single branch: React untouched, a ~3–10 MB exe (vs ~120 MB for Electron), fully offline, CI-only builds across Windows/macOS/Linux plus a portable exe. The frontend build verifies locally; Rust compiles in CI.
