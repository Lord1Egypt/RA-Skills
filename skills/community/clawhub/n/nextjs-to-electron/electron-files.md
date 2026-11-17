# Electron files (copy-paste templates)

All paths relative to the Next.js project root. Preserve web behavior; adjust source or Next config when static export or a requested desktop feature requires it. The template's comments are written in English; rename or translate them if you prefer — they are yours to change. Adapt names (`TextDiff`, `app://local`, the `LOCALES` list, `appId`) to your app.

## Layout

```
electron/
  package.json       CommonJS scope for the shell and tests
  constants.js        SCHEME + LOCALES         (pure — no require("electron"))
  resolvePath.js      static-asset resolver    (pure)  + resolvePath.test.js
  store.js            JSON store in userData   (pure)  + store.test.js
  locale.js           startUrl/parseLocale/trackLocale (pure)  + locale.test.js
  window-state.js     window bounds keeper     (pure)  + window-state.test.js
  protocol.js         app:// scheme            (electron)
  tray.js             tray + close-to-tray     (electron)
  main.js             entry — wires everything (electron)
scripts/electron-dev.cjs
electron-builder.yml
build/icon.png        (≥256×256 square; reuse public/logo.png)
.github/workflows/electron.yml
```

## package.json additions

```jsonc
{
  "main": "electron/main.js",
  "scripts": {
    "electron": "electron .",
    "electron:dev": "node scripts/electron-dev.cjs",
    "electron:build": "next build && electron-builder --win dir",
    "test:electron": "node --test electron/resolvePath.test.js electron/store.test.js electron/locale.test.js electron/window-state.test.js"
  }
  // devDependencies: electron, electron-builder  (yarn add -D electron electron-builder)
}
```
**Runtime installation:** Electron versions without a postinstall download fetch the binary on first use. For offline CI or predictable build stages, invoke the installed package's installer explicitly after dependency installation; follow the selected version's package layout.

The sample test script lists files explicitly for shell portability. A project may use another discovery command if its Node version and CI shell support it; confirm that tests actually run.

### electron/package.json

```json
{
  "type": "commonjs"
}
```

This package scope makes the shell's `.js` files and tests use CommonJS even when the root package declares `"type": "module"`. Include it in the packaged `electron/**` files. The development launcher uses `.cjs` because it lives outside this scope.

## Pure modules (no `require("electron")` → unit-testable with `node --test`)

### electron/constants.js
```js
const SCHEME = "app";
// One entry per messages/<locale>.json. Exact-match (includes), so order is irrelevant.
const LOCALES = ["ar", "bn", "de", "en", "es", "fr", "hi", "id", "it", "ja", "ko", "pt", "ru", "th", "tr", "vi", "zh-hant", "zh"];
module.exports = { SCHEME, LOCALES };
```

### electron/resolvePath.js
```js
const path = require("path");

// Pure: map a request pathname to a file path inside outDir.
// `exists` is injected so this is testable without touching the real FS.
function resolveAssetPath(outDir, pathname, exists) {
  // decodeURIComponent throws on a malformed escape ("/%", "/a%zz"), and Chromium leaves a
  // lone % in a standard-scheme path uncanonicalised, so this IS reachable. The throw is
  // synchronous, so protocol.js's .catch on net.fetch never sees it — it would surface as
  // an unhandled protocol error and a blank window. Treat undecodable as not-found.
  let rel;
  try {
    rel = decodeURIComponent(pathname).replace(/^\/+/, "");
  } catch {
    return path.join(outDir, "404.html");
  }
  if (rel === "") rel = "index.html";

  // Normalize, then enforce containment: bail to 404 if the path escapes outDir.
  // Catches both "../../x" and a bare ".." (which a leading-"../"-strip alone misses),
  // on Windows and POSIX. Only the CHECK uses path.resolve; `candidate` stays
  // path.join-based so the rest of the resolver (and its tests) behave identically.
  const safe = path.normalize(rel).replace(/^(\.\.[\\/])+/, "");
  const root = path.resolve(outDir);
  const resolved = path.resolve(root, safe);
  if (resolved !== root && !resolved.startsWith(root + path.sep)) {
    return path.join(outDir, "404.html");
  }
  let candidate = path.join(outDir, safe);

  const hasExt = path.extname(safe) !== "";
  if (!hasExt) {
    const asHtml = path.join(outDir, safe + ".html");        // /zh   -> zh.html
    const asIndex = path.join(outDir, safe, "index.html");   // /zh   -> zh/index.html (trailingSlash mode)
    if (exists(asHtml)) candidate = asHtml;
    else if (exists(asIndex)) candidate = asIndex;
    else candidate = path.join(outDir, "404.html");
  } else if (!exists(candidate)) {
    candidate = path.join(outDir, "404.html");
  }
  return candidate;
}

module.exports = { resolveAssetPath };
```

### electron/resolvePath.test.js
```js
const { test } = require("node:test");
const assert = require("node:assert");
const path = require("path");
const { resolveAssetPath } = require("./resolvePath");

const OUT = path.join("C:", "out");
const j = (...p) => path.join(OUT, ...p);

test("root maps to index.html", () => {
  assert.strictEqual(resolveAssetPath(OUT, "/", () => true), j("index.html"));
});
test("clean locale path falls back to <path>.html", () => {
  assert.strictEqual(resolveAssetPath(OUT, "/zh", (p) => p === j("zh.html")), j("zh.html"));
});
test("zh-hant is not matched as zh", () => {
  assert.strictEqual(resolveAssetPath(OUT, "/zh-hant", (p) => p === j("zh-hant.html")), j("zh-hant.html"));
});
test("asset with extension served directly", () => {
  const exists = (p) => p === j("_next", "static", "x.js");
  assert.strictEqual(resolveAssetPath(OUT, "/_next/static/x.js", exists), j("_next", "static", "x.js"));
});
test("dir index fallback", () => {
  assert.strictEqual(resolveAssetPath(OUT, "/foo", (p) => p === j("foo", "index.html")), j("foo", "index.html"));
});
test("missing falls back to 404.html", () => {
  assert.strictEqual(resolveAssetPath(OUT, "/nope", () => false), j("404.html"));
});
test("blocks path traversal", () => {
  assert.ok(resolveAssetPath(OUT, "/../../secret", () => false).startsWith(OUT));
});
test("blocks bare /.. escape", () => {
  assert.strictEqual(resolveAssetPath(OUT, "/..", () => false), j("404.html"));
});
```

### electron/store.js
```js
const fs = require("fs");
const path = require("path");

// Minimal JSON store. No third-party deps (minimal-dependency for offline/intranet).
function createStore(dir, filename = "app-state.json") {
  const file = path.join(dir, filename);
  let data = {};
  try {
    data = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    data = {}; // missing or corrupt -> empty
  }
  return {
    get(key, fallback) {
      return data[key] !== undefined ? data[key] : fallback;
    },
    set(key, value) {
      // Compare by value, not reference: windowState is a fresh object literal on every
      // save, so `===` never matches it. Value comparison also avoids writing unchanged
      // bounds when the close handler flushes a completed resize.
      // Wrapped because JSON.stringify throws on a circular value: skipping a redundant
      // write must never be the thing that takes down the main process.
      try {
        if (JSON.stringify(data[key]) === JSON.stringify(value)) return;
      } catch {
        // not comparable — fall through and write
      }
      data[key] = value;
      try {
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(file, JSON.stringify(data, null, 2));
      } catch {
        // read-only env: write failure is non-fatal
      }
    },
  };
}

module.exports = { createStore };
```

### electron/store.test.js
```js
const { test } = require("node:test");
const assert = require("node:assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { createStore } = require("./store");
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), "store-"));

test("returns fallback when unset", () => {
  assert.strictEqual(createStore(tmp()).get("locale", "en"), "en");
});
test("persists across instances", () => {
  const dir = tmp();
  createStore(dir).set("locale", "zh");
  assert.strictEqual(createStore(dir).get("locale", "en"), "zh");
});
test("corrupt JSON does not throw", () => {
  const dir = tmp();
  fs.writeFileSync(path.join(dir, "app-state.json"), "{ not json");
  assert.strictEqual(createStore(dir).get("locale", "en"), "en");
});
test("round-trips object values", () => {
  const dir = tmp();
  createStore(dir).set("windowState", { width: 800, height: 600 });
  assert.deepStrictEqual(createStore(dir).get("windowState", {}), { width: 800, height: 600 });
});
```

### electron/locale.js
```js
const { SCHEME, LOCALES } = require("./constants");

// No require("electron"): win is passed in, so startUrl/parseLocale are unit-testable.
function startUrl(store) {
  const locale = store.get("locale", "");
  return `${SCHEME}://local/${locale}`; // "app://local/" first run, "app://local/zh" thereafter
}

function parseLocale(urlString) {
  try {
    const { pathname } = new URL(urlString);
    const seg = pathname.replace(/^\/+/, "").split("/")[0].replace(/\.html$/, "");
    return LOCALES.includes(seg) ? seg : null;
  } catch {
    return null;
  }
}

function trackLocale(win, store) {
  const save = (_e, navUrl) => {
    const loc = parseLocale(navUrl);
    if (loc) store.set("locale", loc); // null guard: never overwrite a good locale with blank
  };
  win.webContents.on("did-navigate", save); // full document loads
  win.webContents.on("did-navigate-in-page", save); // App Router client-side (pushState) locale switches
}

module.exports = { startUrl, parseLocale, trackLocale };
```

### electron/locale.test.js
```js
const { test } = require("node:test");
const assert = require("node:assert");
const { startUrl, parseLocale } = require("./locale");
const fakeStore = (val) => ({ get: (_k, fb) => (val !== undefined ? val : fb), set() {} });

test("startUrl is root when unset", () => assert.strictEqual(startUrl(fakeStore(undefined)), "app://local/"));
test("startUrl carries locale when set", () => assert.strictEqual(startUrl(fakeStore("zh")), "app://local/zh"));
test("parseLocale reads .html pages", () => assert.strictEqual(parseLocale("app://local/zh.html"), "zh"));
test("parseLocale reads clean paths", () => assert.strictEqual(parseLocale("app://local/ja"), "ja"));
test("parseLocale distinguishes zh-hant from zh", () => assert.strictEqual(parseLocale("app://local/zh-hant"), "zh-hant"));
test("parseLocale returns null for non-locale/root", () => {
  assert.strictEqual(parseLocale("app://local/_next/static/x.js"), null);
  assert.strictEqual(parseLocale("app://local/"), null);
});
```

### electron/window-state.js
```js
// No require("electron"): win is passed to track().
function createWindowStateKeeper(store) {
  const saved = store.get("windowState", { width: 1200, height: 800 });

  function track(win) {
    let pending = saved;
    let timer;
    const capture = () => {
      if (win.isMaximized()) {
        pending = { ...pending, maximized: true };
      } else if (!win.isMinimized()) {
        pending = { ...win.getBounds(), maximized: false };
      }
    };
    const flush = () => store.set("windowState", pending);
    const schedule = () => {
      capture(); // Keep the last normal bounds even if maximized before the timer fires.
      clearTimeout(timer);
      timer = setTimeout(flush, 150);
    };
    win.on("resize", schedule);
    win.on("move", schedule);
    win.on("close", () => {
      capture();
      clearTimeout(timer);
      flush();
    });
    if (saved.maximized) win.maximize();
  }

  return { saved, track };
}

module.exports = { createWindowStateKeeper };
```

### electron/window-state.test.js
```js
const { test } = require("node:test");
const assert = require("node:assert");
const { createWindowStateKeeper } = require("./window-state");

// In-memory store + a controllable fake window — no Electron needed.
function memStore(init = {}) {
  const data = { ...init };
  return { get: (k, fb) => (data[k] !== undefined ? data[k] : fb), set: (k, v) => { data[k] = v; }, raw: () => data };
}
function fakeWin({ maximized = false, minimized = false, bounds = { x: 10, y: 20, width: 900, height: 700 } } = {}) {
  const h = {};
  return {
    maximizeCalled: false,
    isMaximized: () => maximized,
    isMinimized: () => minimized,
    getBounds: () => bounds,
    on: (ev, fn) => { (h[ev] = h[ev] || []).push(fn); },
    maximize() { this.maximizeCalled = true; },
    _fire: (ev) => (h[ev] || []).forEach((f) => f()),
    _setMaximized: (v) => { maximized = v; },
  };
}

test("saved defaults to 1200x800 when store empty", () => {
  assert.deepStrictEqual(createWindowStateKeeper(memStore()).saved, { width: 1200, height: 800 });
});
test("normal resize persists bounds with maximized:false", () => {
  const store = memStore();
  const win = fakeWin({ bounds: { x: 10, y: 20, width: 900, height: 700 } });
  createWindowStateKeeper(store).track(win);
  win._fire("close");
  assert.deepStrictEqual(store.raw().windowState, { x: 10, y: 20, width: 900, height: 700, maximized: false });
});
test("first-run maximize (before any move) still persists a size", () => {
  const store = memStore(); // empty
  const win = fakeWin({ maximized: true });
  createWindowStateKeeper(store).track(win);
  win._fire("close");
  const s = store.raw().windowState;
  assert.strictEqual(s.maximized, true);
  assert.strictEqual(s.width, 1200);  // NOT undefined — the bug the `saved` fallback prevents
  assert.strictEqual(s.height, 800);
});
test("un-maximize clears the maximized flag", () => {
  const store = memStore({ windowState: { x: 5, y: 6, width: 800, height: 600, maximized: false } });
  const win = fakeWin({ maximized: true, bounds: { x: 5, y: 6, width: 800, height: 600 } });
  createWindowStateKeeper(store).track(win);
  win._fire("close");                       // maximized save
  assert.strictEqual(store.raw().windowState.maximized, true);
  win._setMaximized(false);
  win._fire("close");                       // restore
  assert.strictEqual(store.raw().windowState.maximized, false);
});
test("saved.maximized triggers win.maximize() on track", () => {
  const win = fakeWin();
  createWindowStateKeeper(memStore({ windowState: { width: 800, height: 600, maximized: true } })).track(win);
  assert.strictEqual(win.maximizeCalled, true);
});
```

## Electron-bound modules

### electron/protocol.js
```js
const { protocol, net } = require("electron");
const fs = require("fs");
const url = require("url");
const { SCHEME } = require("./constants");
const { resolveAssetPath } = require("./resolvePath");

// Must be called BEFORE app 'ready'.
function registerScheme() {
  protocol.registerSchemesAsPrivileged([
    { scheme: SCHEME, privileges: { standard: true, secure: true, supportFetchAPI: true } },
  ]);
}

// Must be called AFTER app 'ready'.
function handleProtocol(outDir) {
  protocol.handle(SCHEME, (request) => {
    const { pathname } = new URL(request.url);
    const filePath = resolveAssetPath(outDir, pathname, fs.existsSync);
    // net.fetch reads the file:// URL and infers Content-Type.
    // .catch so a rejected fetch becomes a 404, not an unhandled protocol error / blank page.
    return net.fetch(url.pathToFileURL(filePath).toString()).catch(
      () => new Response("Not found", { status: 404 })
    );
  });
}

module.exports = { registerScheme, handleProtocol };
```

### electron/tray.js
```js
const { Tray, Menu, nativeImage } = require("electron");

// Tray icon + Quit item. The window's close→hide-to-tray handler lives in main.js
// (createWindow) so it's wired even if tray creation throws. getWin returns the
// current BrowserWindow (or null). Quit sets app.isQuitting (initialized in main.js).
function setupTray(app, getWin, iconPath) {
  const tray = new Tray(nativeImage.createFromPath(iconPath));
  tray.setToolTip("TextDiff");

  const show = () => {
    const w = getWin();
    if (w) { w.show(); w.focus(); }
  };

  tray.setContextMenu(
    Menu.buildFromTemplate([
      { label: "Show window", click: show },
      { type: "separator" },
      { label: "Quit", click: () => { app.isQuitting = true; app.quit(); } },
    ])
  );
  tray.on("click", show);
  return tray; // caller must retain this (assign to a var) or the icon is GC'd
}

module.exports = { setupTray };
```

### electron/main.js
```js
const { app, BrowserWindow } = require("electron");
const path = require("path");
const { registerScheme, handleProtocol } = require("./protocol");
const { createStore } = require("./store");
const { startUrl, trackLocale } = require("./locale");
const { createWindowStateKeeper } = require("./window-state");
const { setupTray } = require("./tray");

const isDev = process.env.ELECTRON_DEV === "1";
// Packaged paths must match electron-builder extraResources `to:` targets.
const OUT_DIR = app.isPackaged
  ? path.join(process.resourcesPath, "out")
  : path.join(__dirname, "..", "out");
const ICON_PATH = app.isPackaged
  ? path.join(process.resourcesPath, "icon.png")
  : path.join(__dirname, "..", "build", "icon.png");

registerScheme(); // before ready

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
  let win = null;
  let tray = null;
  app.isQuitting = false; // flipped true only by the tray "Quit" item
  const store = createStore(app.getPath("userData"));
  const windowState = createWindowStateKeeper(store);

  app.on("second-instance", () => {
    if (win) {
      if (win.isMinimized()) win.restore();
      if (!win.isVisible()) win.show();
      win.focus();
    }
  });

  function createWindow() {
    const s = windowState.saved;
    win = new BrowserWindow({
      width: s.width, height: s.height, x: s.x, y: s.y,
      show: false,
      icon: ICON_PATH,
      webPreferences: { contextIsolation: true, nodeIntegration: false },
    });

    windowState.track(win);
    trackLocale(win, store);

    win.on("close", (e) => {
      // Close = hide to tray — UNLESS we're really quitting, the tray failed to init
      // (no tray ⇒ let it close so window-all-closed can quit; no unquittable zombie),
      // or we're in dev (X should terminate the dev process, not orphan it in the tray).
      if (!isDev && !app.isQuitting && tray) { e.preventDefault(); win.hide(); }
    });

    if (isDev) win.loadURL("http://localhost:3000");   // run `yarn dev` separately
    else win.loadURL(startUrl(store));                 // app://local/<saved locale>
    win.once("ready-to-show", () => win.show());
    return win;
  }

  app.whenReady().then(() => {
    if (!isDev) handleProtocol(OUT_DIR); // after ready
    createWindow();
    try {
      tray = setupTray(app, () => win, ICON_PATH); // leaves tray=null if it throws
    } catch (err) {
      console.error("Tray init failed; close will quit instead of hide-to-tray.", err);
    }
    app.on("activate", () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });

  // Stay resident in the tray on close (Windows). Tray "Quit" sets app.isQuitting then app.quit().
  // If the tray never initialized, quit normally so the app can't get stuck headless.
  app.on("window-all-closed", () => {
    if (isDev || !tray) app.quit();
  });
}
```

### scripts/electron-dev.cjs
```js
// Launch electron with ELECTRON_DEV=1, pointed at `next dev` (localhost:3000).
// A node launcher sets the env var without a cross-env dependency.
process.env.ELECTRON_DEV = "1";
const { spawn } = require("child_process");
const electron = require("electron"); // under plain node, require returns the electron binary path
spawn(electron, ["."], { stdio: "inherit" }).on("close", (code) => process.exit(code ?? 0));
```

## Packaging

### electron-builder.yml
```yaml
appId: top.example.textdiff
productName: TextDiff
directories:
  output: dist-electron
files:
  - electron/**
  - "!electron/*.test.js"   # don't ship tests into the asar
  - package.json
extraResources:             # static export + tray icon live in resources/, NOT the asar
  - from: out
    to: out                 # -> process.resourcesPath/out   (OUT_DIR)
  - from: build/icon.png
    to: icon.png            # -> process.resourcesPath/icon.png (ICON_PATH)
win:
  target: dir               # unpacked folder: runs TextDiff.exe directly, fast startup
  icon: build/icon.png
```
`target: dir` → `dist-electron/win-unpacked/` (distribute the folder; zip for transport). Swap to `target: portable` only if you must have a single file — it re-extracts to %TEMP% every launch (slower). If a stray `/build` rule (a CRA leftover) would ignore the committed icon, note that `!build/icon.png` **cannot** rescue it — git will not re-include a file whose parent directory is excluded. Exclude the directory's *contents* instead: `/build/*` followed by `!/build/icon.png`.

### .gitignore additions
```
dist-electron/
out/
```
Only add the `build/` pair below if some existing rule already ignores that directory —
and note the ordering, because `!build/icon.png` under a plain `/build` rule does nothing:
```
/build/*
!/build/icon.png
```

## CI

### .github/workflows/electron.yml (full — build the tagged commit; source-map variant below)
```yaml
name: Build Electron (Windows unpacked)
on:
  push:
    tags: ["v*"]
  workflow_dispatch:
concurrency:
  group: desktop-release-promotion
  cancel-in-progress: false
  queue: max
jobs:
  build:
    runs-on: windows-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v7
        with: { ref: '${{ github.sha }}' }
      # Pin the Node major; desktop-app-standard's audit checks nodejs/Release (verify Electron's floor with `npm view electron engines`).
      - uses: actions/setup-node@v7
        with:
          node-version: 26
          cache: yarn
      - name: Set the release version from the tag
        if: startsWith(github.ref, 'refs/tags/v')
        shell: bash
        run: |
          [[ "$GITHUB_REF_NAME" =~ ^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?$ ]] || exit 1
          npm pkg set version="${GITHUB_REF_NAME#v}"
      - run: yarn install --frozen-lockfile
      - run: yarn test:electron
      - run: yarn electron:build
      - name: Upload unpacked artifact
        uses: actions/upload-artifact@v7
        with:
          name: TextDiff-unpacked
          path: dist-electron/win-unpacked     # GitHub auto-zips a folder artifact
          if-no-files-found: error
      - name: Zip unpacked for release
        if: startsWith(github.ref, 'refs/tags/v')
        shell: pwsh
        run: Compress-Archive -Path dist-electron/win-unpacked/* -DestinationPath "dist-electron/TextDiff-$env:GITHUB_REF_NAME-win.zip"
      - name: Verify the draft assets and publish on tag
        if: startsWith(github.ref, 'refs/tags/v')
        shell: bash
        env:
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
        run: |
          node <<'NODE'
          const fs = require('node:fs');
          const crypto = require('node:crypto');
          const { execFileSync } = require('node:child_process');
          const { REPO, GITHUB_REF_NAME: tag } = process.env;
          const commit = execFileSync('git', ['rev-parse', 'HEAD'], {encoding: 'utf8'}).trim();
          const gh = args => execFileSync('gh', args, {encoding: 'utf8'}).trim();
          const api = endpoint => JSON.parse(gh(['api', endpoint]));
          const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
          if (tag !== 'v' + pkg.version) throw new Error('version mismatch');
          const releases = JSON.parse(gh(['api', '--paginate', '--slurp', `repos/${REPO}/releases?per_page=100`])).flat();
          const matches = releases.filter(release => release.tag_name === tag);
          if (matches.length > 1 || matches.some(release => !release.draft)) throw new Error('Release must be a unique draft');
          if (!matches.length) gh(['release', 'create', tag, '-R', REPO, '--draft', '--verify-tag', '--generate-notes']);
          const drafts = JSON.parse(gh(['api', '--paginate', '--slurp', `repos/${REPO}/releases?per_page=100`])).flat().filter(release => release.tag_name === tag);
          if (drafts.length !== 1 || !drafts[0].draft) throw new Error('Release must remain a unique draft');
          const draft = drafts[0];
          const name = `TextDiff-${tag}-win.zip`;
          const digest = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
          const zip = 'dist-electron/' + name;
          const sums = 'dist-electron/SHA256SUMS';
          fs.writeFileSync(sums, `${digest(zip)}  ${name}\n`);
          gh(['release', 'upload', tag, '-R', REPO, zip, sums, '--clobber']);
          const assets = JSON.parse(gh(['api', '--paginate', '--slurp', `repos/${REPO}/releases/${draft.id}/assets?per_page=100`])).flat();
          const expected = new Map([[name, digest(zip)], ['SHA256SUMS', digest(sums)]]);
          if (assets.length !== expected.size || assets.some(asset => asset.digest !== 'sha256:' + expected.get(asset.name))) {
            throw new Error('Draft asset set or digest differs from this build');
          }
          if (api(`repos/${REPO}/commits/${tag}`).sha !== commit) throw new Error('Tag moved after checkout');
          const newer = releases.some(release => !release.draft && !release.prerelease && /^v\d+\.\d+\.\d+$/.test(release.tag_name) && release.tag_name.localeCompare(tag, 'en', {numeric: true}) > 0);
          gh(['api', '-X', 'PATCH', `repos/${REPO}/releases/${draft.id}`, '-F', 'draft=false', '-F', `prerelease=${tag.includes('-')}`, '-f', `make_latest=${!tag.includes('-') && !newer}`]);
          if (!tag.includes('-') && !newer && api(`repos/${REPO}/releases/latest`).tag_name !== tag) throw new Error('Latest release mismatch');
          NODE
```

The single-app template publishes automatically after draft verification. Interrupted uploads
can retry while the release is a draft. A published version is repaired with a new tag.

### Building code maintained on a side branch

Tag the exact commit containing the Electron code and workflow. Keep the workflow in that
commit, and let checkout use the triggering tag for releases. For a manual run, select that
same tag in GitHub's workflow UI. Record the resolved commit SHA in the run summary.

### Variant: two desktop apps in one repo, released by one tag

Keep the workflows on the release branch. Commit a source map, such as
`.github/desktop-sources.json`, in the commit receiving the release tag. Record each
desktop branch's full commit SHA in the `electron` and `tauri` fields before tagging.
This supports separate source branches and makes a rerun select the same source.

For each workflow, checkout the tagged release commit to read the map, then checkout
the recorded source commit. The Electron workflow uses the following steps. The Tauri
workflow uses the `tauri` field.

```yaml
      - uses: actions/checkout@v7
      - name: Read the Electron source commit from the tagged source map
        id: source
        shell: bash
        run: |
          node <<'NODE'
          const fs = require("node:fs");
          const { electron } = JSON.parse(fs.readFileSync(".github/desktop-sources.json", "utf8"));
          if (!/^[0-9a-f]{40}$/i.test(electron)) throw new Error("electron must be a full commit SHA");
          fs.appendFileSync(process.env.GITHUB_OUTPUT, `commit=${electron}\n`);
          NODE
      - uses: actions/checkout@v7
        with:
          ref: ${{ steps.source.outputs.commit }}
      - name: Set the release version from the tag
        if: startsWith(github.ref, 'refs/tags/v')
        shell: bash
        run: npm pkg set version="${GITHUB_REF_NAME#v}"
```

Continue with dependency installation, tests and packaging after these steps. In the
Tauri workflow, propagate the injected version into `tauri.conf.json` before building.

Use one coordinator workflow to create the draft, collect both build jobs' file lists
and digests, verify their combined asset set, and publish once. Remove the standalone
publication steps and apply the repository promotion concurrency group to the coordinator's
publish job; build jobs must not hold that group while waiting for each other. The
single-app verifier intentionally rejects another application's unrecorded assets.
The coordinator must compare the tag's current SHA to the tagged source-map commit,
and each build's SHA to its own entry in that map, rather than comparing both to one SHA.
For manual rebuilds, select the release tag so the source map also comes from that tag.
Keep a workflow copy in every commit that may itself receive a triggering tag.
