---
name: html2app
description: Package an existing local HTML/CSS/JavaScript site or built frontend into a self-contained, offline-first Electron desktop application. Use when Codex needs to turn a local web page or web project into a macOS .app/.dmg or Windows .exe installer without deploying it to a server.
---

# Package Local Web as Electron

Package existing web content; do not rewrite its visual product unless packaging exposes a concrete compatibility issue.

## Inspect and choose the input

Run `scripts/inspect_web_app.sh <project-dir>` first. Treat a standalone `.html` file as a static input. For a framework project, use its existing production build command and package the build output, never its development server.

Read `references/packaging-matrix.md` before selecting targets or release settings.

Stop and explain the limitation if the site requires a server-side API, database, OAuth callback, CDN-only assets, or secret. Local Electron packaging cannot make those dependencies offline by itself.

## Create the Electron shell

1. Add Electron and `electron-builder` to the project, preserving existing package tooling.
2. Create a minimal main process which creates one `BrowserWindow` and loads the selected local HTML with `loadFile`.
3. Set `contextIsolation: true`, `sandbox: true`, and `nodeIntegration: false`. Add a preload bridge only for explicitly required local capabilities; validate every input exposed through it.
4. Add `start`, `dist`, and platform-specific package scripts. Configure `electron-builder` with app name, identifier, output directory, files allowlist, and an icon.
5. Keep all first-party static assets within the packaged files. Surface any remaining network requests to the user.

## Give every app an icon

Use a user-provided icon when available. Otherwise, generate a simple, high-contrast default icon that reflects the app's purpose; never leave the Electron default icon in a deliverable.

1. On macOS, run `scripts/generate_default_icon_macos.sh <output-dir>` to create `icon.svg` and `icon.icns`.
2. Set `build.mac.icon` to the generated `.icns`. On Windows, provide a matching `.ico`; use a PNG/SVG only where the target accepts it.
3. Verify the built application's `Contents/Resources` contains the intended icon. Record whether it is a generated fallback or a user-supplied brand asset.

## Preflight the toolchain

1. Run `npm install` and confirm that Electron's platform binary actually downloaded; a successful dependency-resolution phase alone is insufficient.
2. Select the artifact architecture explicitly (`arm64`, `x64`, or `universal` on macOS). Match it to the user's intended devices.
3. If Electron's binary download is unavailable, look for the exact Electron version and architecture in `~/Library/Caches/electron/`. Use the cached-runtime fallback only when they match; do not relabel a different architecture or version as the requested release.
4. If `electron-builder` fails before producing artifacts, retain its complete log and report the blocker. On macOS, use `scripts/package_cached_electron_macos.sh` only for an available matching cached Electron runtime.

## Add local SQLite storage

Keep SQLite in the Electron main process. Place the database at `path.join(app.getPath('userData'), '<app>.sqlite')`; never write it beside renderer files or under `Contents/Resources`.

1. Prefer a compatible SQLite runtime for the selected Electron version. For `node:sqlite`, verify the bundled Electron Node version supports it; otherwise choose and package a compatible dependency.
2. Create schema migrations with `CREATE TABLE IF NOT EXISTS` or a versioned migration table.
3. Expose narrow, validated IPC handlers (`task:add`, `task:list`), then expose only those methods through preload. Do not expose generic SQL execution to the renderer.
4. Package every renderer page and its relative assets; `loadFile` and normal relative links work for static multi-page navigation.

## Build and verify

- Run the existing web build, when applicable, then run Electron locally before packaging.
- Build native artifacts on their native host whenever possible. On macOS, produce `.dmg` and `.zip`; on Windows, produce NSIS `.exe` and optionally portable `.exe`.
- Verify an `.app` with `codesign --verify --deep --strict`. Treat this as an integrity check, not Gatekeeper approval. Run `spctl --assess --type execute` and report its result.
- For SQLite projects, create a record, close the app, reopen it, and verify the record survives. Confirm the database resides in `userData` and not inside the app bundle.
- Use unsigned or ad-hoc output only for local testing unless the user supplies signing credentials. Do not claim a distributable signed build without Apple notarization or Windows code signing.
- Report exact artifact paths, target architecture, signing and notarization status, test result, and all online dependencies found.

## Regression cases

Run `scripts/run_fixture_checks.sh` whenever changing the inspection or packaging workflow. Read `references/test-cases.md` before packaging a multi-page or data-persisting project. Treat its acceptance criteria as release gates, not suggestions.

For local storage, keep mutable data in `app.getPath('userData')`, never inside the packaged app. Expose storage through a narrow preload API; do not enable renderer Node access. For a remote backend, stop and identify the service, credentials, connectivity, and offline behavior that must be decided before packaging.

## Resources

- `scripts/inspect_web_app.sh`: enumerate likely entry points, package scripts, and remote asset/API references.
- `scripts/package_cached_electron_macos.sh`: assemble a locally testable `.app` from an exact cached Electron archive when normal binary acquisition is unavailable.
- `scripts/generate_default_icon_macos.sh`: create a high-contrast fallback SVG and macOS `.icns` icon.
- `scripts/run_fixture_checks.sh`: generate and inspect static, local-storage, and remote-backend fixtures.
- `references/packaging-matrix.md`: target selection and signing constraints.
- `references/test-cases.md`: packaging test cases and acceptance criteria.
