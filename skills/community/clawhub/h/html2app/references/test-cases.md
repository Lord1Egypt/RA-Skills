# Packaging test cases

## Case 1: Multi-page static site

**Fixture:** `index.html` links to `about.html`; both use local CSS, JavaScript, and image assets.

**Expected:** classify as static; package both pages and assets; navigation works under `file://`; inspection finds no remote URL.

**Release gate:** open the packaged app, follow every in-app link, refresh each page, and confirm no missing-resource errors in DevTools.

## Case 2: Built multi-page frontend

**Fixture:** a framework output directory containing a root page, nested route page, hashed assets, and no development server requirement.

**Expected:** package only production output; resolve all asset paths under `file://`; avoid loading `localhost` or a dev-server URL.

**Release gate:** run the production build first, package the declared output directory, and smoke-test direct navigation to a nested page.

## Case 3: Local persistent data

**Fixture:** a notes app with a renderer, preload bridge, and main-process storage module. The main process writes data to `app.getPath('userData')` (SQLite, JSON, or IndexedDB as appropriate).

**Expected:** classify as local persistence, not a server dependency; retain `contextIsolation: true`, `sandbox: true`, and `nodeIntegration: false`; restrict preload methods to named operations such as `notes:list` and `notes:save`.

**Release gate:** create a record, quit fully, reopen, verify the record exists, and verify no mutable file was written below `Contents/Resources`.

### SQLite-specific checks

- Verify the Electron runtime supports the chosen SQLite API before packaging; `node:sqlite` availability follows Electron's bundled Node version, not the host Node version.
- Assert schema creation/migration occurs before the first IPC handler is accepted.
- Reject malformed IPC input and do not expose an arbitrary `query(sql)` renderer API.
- Check that `workbench.sqlite` or equivalent is created below `app.getPath('userData')` and survives a full app restart.

## Case 4: Remote backend dependency

**Fixture:** a dashboard that fetches `https://api.example.test`, authenticates a user, and displays remote data.

**Expected:** flag as online-dependent; do not describe it as offline or self-contained.

**Release gate:** obtain a user decision on backend reachability, credential storage, OAuth callback handling, offline UX, and API allowlisting before packaging. Test disconnected startup and expired credentials.

## Case 5: Local companion service

**Fixture:** a renderer uses `http://127.0.0.1:<port>` to reach a bundled local process.

**Expected:** flag the loopback endpoint; package, launch, health-check, and terminate the companion from the main process. Never assume localhost is already running.

**Release gate:** verify clean first launch, port collision handling, restart behavior, and complete process shutdown.
