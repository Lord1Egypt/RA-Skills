# Electron files (copy-paste templates)

All paths relative to the Next.js project root. The web source (`src/`, `messages/`, `next.config.*`) is **not** edited. Comments are English here; adapt names (`TextDiff`, `app://local`, the `LOCALES` list, `appId`) to your app.

## Layout

```
electron/
  constants.js        SCHEME + LOCALES         (pure — no require("electron"))
  resolvePath.js      static-asset resolver    (pure)  + resolvePath.test.js
  store.js            JSON store in userData   (pure)  + store.test.js
  locale.js           startUrl/parseLocale/trackLocale (pure)  + locale.test.js
  window-state.js     window bounds keeper     (pure)
  protocol.js         app:// scheme            (electron)
  tray.js             tray + close-to-tray     (electron)
  main.js             entry — wires everything (electron)
scripts/electron-dev.js
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
    "electron:dev": "node scripts/electron-dev.js",
    "electron:build": "next build && electron-builder --win dir",
    "test:electron": "node --test electron/resolvePath.test.js electron/store.test.js electron/locale.test.js electron/window-state.test.js"
  }
  // devDependencies: electron, electron-builder  (yarn add -D electron electron-builder)
}
```
**List the test files explicitly** — the tempting `node --test electron/*.test.js` is a trap that fails in CI: PowerShell (GitHub's default Windows shell) does **not** expand the `*` glob, and `node --test`'s own glob support only exists on Node ≥ 21, so the literal `electron/*.test.js` is passed through and matches nothing. (CI now uses `node-version: lts/*`, currently ≥ 21, so Node itself could expand it — but an explicit list stays correct on every shell and Node version, so prefer it.) `node --test electron` / `node --test electron/` are also wrong — Node tries to load `electron` as a module/entry, not search the dir. An explicit list works on every Node version and shell; add new test files to it as you create them.

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
  let rel = decodeURIComponent(pathname).replace(/^\/+/, "");
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
      if (data[key] === value) return; // skip redundant writes (same locale re-set on every in-page nav)
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
    const save = () => {
      if (win.isMaximized()) {
        // Keep last NORMAL bounds. Fall back to `saved` (always has width/height),
        // not {} — else maximizing before any move/resize persists no size and the
        // next launch restores to a default-sized, unplaced window.
        const prev = store.get("windowState", saved);
        store.set("windowState", { ...saved, ...prev, maximized: true });
      } else if (!win.isMinimized()) {
        const b = win.getBounds();
        store.set("windowState", { ...b, maximized: false });
      }
    };
    win.on("resize", save);
    win.on("move", save);
    win.on("close", save);
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
  win._fire("resize");
  assert.deepStrictEqual(store.raw().windowState, { x: 10, y: 20, width: 900, height: 700, maximized: false });
});
test("first-run maximize (before any move) still persists a size", () => {
  const store = memStore(); // empty
  const win = fakeWin({ maximized: true });
  createWindowStateKeeper(store).track(win);
  win._fire("resize");
  const s = store.raw().windowState;
  assert.strictEqual(s.maximized, true);
  assert.strictEqual(s.width, 1200);  // NOT undefined — the bug the `saved` fallback prevents
  assert.strictEqual(s.height, 800);
});
test("un-maximize clears the maximized flag", () => {
  const store = memStore({ windowState: { x: 5, y: 6, width: 800, height: 600, maximized: false } });
  const win = fakeWin({ maximized: true, bounds: { x: 5, y: 6, width: 800, height: 600 } });
  createWindowStateKeeper(store).track(win);
  win._fire("resize");                       // maximized save
  assert.strictEqual(store.raw().windowState.maximized, true);
  win._setMaximized(false);
  win._fire("resize");                       // restore
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

### scripts/electron-dev.js
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
`target: dir` → `dist-electron/win-unpacked/` (distribute the folder; zip for transport). Swap to `target: portable` only if you must have a single file — it re-extracts to %TEMP% every launch (slower). Add `!build/icon.png` to `.gitignore` if a stray `/build` rule (CRA leftover) would ignore the committed icon.

### .gitignore additions
```
dist-electron/
out/
!build/icon.png
```

## CI

### .github/workflows/electron.yml (full — host on `main`; add `ref:` to checkout if the code is on a side branch, see below)
```yaml
name: Build Electron (Windows unpacked)
on:
  push:
    tags: ["v*"]
  workflow_dispatch:
jobs:
  build:
    runs-on: windows-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: lts/* # track current LTS; electron@42+ needs node >= 22.12
          cache: yarn
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
        run: Compress-Archive -Path dist-electron/win-unpacked/* -DestinationPath dist-electron/TextDiff-${{ github.ref_name }}-win.zip
      - name: Publish release on tag
        if: startsWith(github.ref, 'refs/tags/v')
        uses: softprops/action-gh-release@v2
        with:
          files: dist-electron/*.zip
```

### Hosting the workflow when the code lives on a side branch
The "Run workflow" button only renders for workflows on the **default branch**, and a tag push only runs workflows present in the *tagged commit's tree*. So when the app code lives on a side branch, host the workflow **on `main`** and pin its checkout to that branch with `ref:` — one file then serves both the manual button and tag releases, and you keep **no** copy on the side branch (it would never run for a tag and would only drift). Keep it as a SEPARATE file alongside any existing desktop/Tauri workflow — don't overwrite that.
```yaml
name: Build Electron (Windows unpacked)
on:
  workflow_dispatch:        # manual "Run workflow" button (renders on the default branch)
  push:
    tags: ["v*"]            # also build on tag (add the release steps from the full template above); pinned ref below builds the side branch
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v6
        with:
          ref: feat/electron-desktop   # <-- pin to the branch that has electron/. Update if it merges/renames.
      - uses: actions/setup-node@v6
        with: { node-version: lts/*, cache: yarn } # electron@42+ needs node >= 22.12
      - run: yarn install --frozen-lockfile
      - run: yarn test:electron
      - run: yarn electron:build
      - uses: actions/upload-artifact@v7
        with:
          name: TextDiff-unpacked
          path: dist-electron/win-unpacked
          if-no-files-found: error
```

### Variant: two desktop apps in one repo, released by one tag
Only needed when the **same repo also ships another desktop app** (e.g. Tauri on its own branch) and you want **one tag to release both**. Don't reach for this for a single app — the single-branch model above is simpler.

Key constraint: on a tag push, GitHub runs only the workflows present in the *tagged commit's tree*. A workflow living on a side branch will **not** run for a tag on `main`. So make `main` the release hub:

- Keep both workflows **only on `main`**, each pinning checkout to its own feature branch (`ref: feat/electron-desktop`, `ref: feat/tauri-desktop`). Do **not** leave workflow copies on the feature branches — they never run for a tag (only the tagged `main` commit's tree does), they silently drift, and they mislead. Both the tag trigger *and* the manual "Run workflow" button work from `main`, and the pinned `ref` builds the branch code either way, so the side-branch copy buys nothing.
- Let the Tauri workflow be the one that **creates the (draft) Release**; the Electron one triggers on `workflow_dispatch + push: tags`, builds, then **polls until that Release exists** (`gh release view "$TAG"` in a retry loop — Tauri compiles Rust and is much slower) and uploads the `win-unpacked` zip with `gh release upload "$TAG" … --clobber`.
- **Make the git tag the single source of truth for the version** — on tag push, inject it before build in *both* workflows (`npm pkg set version="${GITHUB_REF_NAME#v}"`, guarded `if: github.event_name == 'push'`; the Tauri side then runs `update-version` to propagate it into `tauri.conf.json`). This makes the Tauri Release name (derived from the app version), the installer/zip names, and the tag all agree automatically. Without it, Electron uploads to `github.ref_name` while Tauri may name the Release from a stale `package.json` — so Electron polls a Release that never appears and times out, leaving an empty release.
- Tag **only on `main`, on a commit whose tree already contains the corrected workflows** — a tag-triggered run uses the workflow from the *tagged commit*, not `main`'s tip, so fix-then-tag or the old definition runs (a stale tag can even skip the Electron build entirely if its `electron.yml` predates the `push: tags` trigger). The build uses each feature branch's current HEAD, so push the feature branches first. To rescue a broken/empty release, re-tag: `gh release delete vX --yes; git push origin :refs/tags/vX; git tag vX <fixed-commit>; git push origin vX`.
