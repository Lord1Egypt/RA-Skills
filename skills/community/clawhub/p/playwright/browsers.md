# Browsers — Engines, Channels, and Installs

Playwright ships its own browser builds, pinned to the package version. Most "works on my machine" browser problems are a version or channel mismatch, not a bug.

## Engines

| Engine | What it really is | Test it when |
|---|---|---|
| `chromium` | Playwright's Chromium build | Default; matches Chrome and Edge behavior closely enough for almost everything |
| `firefox` | Playwright's Gecko build | You support Firefox; also catches spec-correct behavior Chromium tolerates |
| `webkit` | WebKit engine, **not Safari** | Closest available proxy for Safari and iOS; shares the engine, not the browser |
| `channel: 'chrome'` / `'msedge'` | Your installed branded browser | Widevine DRM, proprietary codecs, Chrome-specific APIs, or a bug reported only in real Chrome |

WebKit on Linux differs from Safari on macOS in fonts, codecs, and media support. A WebKit-only failure is worth investigating, but "passes in WebKit" is not proof it works in Safari — for release-critical Safari behavior, run a real device or a hosted Safari.

Engine differences that actually bite: date and number formatting via Intl, `input[type=date]` widgets, clipboard permissions (Chromium-only), `isMobile` (unsupported in Firefox), download handling, and font fallback affecting layout.

Exclude the affected case, not the engine: `test.skip(browserName === 'firefox', 'isMobile unsupported')` keeps the rest of the file running on Firefox and states why in the report (annotations: `testing.md`). Dropping the whole project to dodge one case is how cross-browser coverage quietly ends.

## Headless

Chromium has two headless implementations: the old separate headless shell (fast, small) and the browser's own headless mode, which behaves like headed and supports extensions. Playwright >=1.49 exposes the browser-native one as `channel: 'chromium'`. When a bug reproduces headed but not headless, switching to the browser-native mode is the first thing to try — before rewriting the test.

Headless differences to expect regardless: no window manager (so window-size APIs report the configured viewport), a different default UA in older builds, no GPU by default, and no extensions in the old shell.

## Install And Version Locking

```bash
npx playwright install                      # all configured browsers
npx playwright install chromium --with-deps # one browser plus Linux system libraries (needs root)
npx playwright install-deps                 # libraries only
npx playwright --version                    # the number the CI image tag must match
```

- Browser builds are tied to the package version: upgrading `@playwright/test` without re-running `install` gives `Executable doesn't exist at ...`.
- The Docker image tag must match exactly: `mcr.microsoft.com/playwright:v1.XX.Y-noble` with `@playwright/test@1.XX.Y`. A mismatched image either fails to find browsers or runs different builds than developers do.
- Cache location: `~/.cache/ms-playwright` (Linux), `~/Library/Caches/ms-playwright` (macOS), `%USERPROFILE%\AppData\Local\ms-playwright` (Windows). Override with `PLAYWRIGHT_BROWSERS_PATH`; `=0` installs inside `node_modules` (the fix for read-only or per-user cache problems in containers).
- `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` when the base image already contains them — otherwise every CI job re-downloads hundreds of megabytes.
- Old browser versions accumulate in the cache across upgrades; `npx playwright uninstall --all` reclaims the space when disk gets tight.

## Launch Options Worth Knowing

```typescript
use: {
  launchOptions: {
    args: ['--disable-dev-shm-usage'],     // Docker: /dev/shm defaults to 64 MB (ci-cd.md)
    slowMo: 250,                            // debugging only, never committed
  },
  contextOptions: { reducedMotion: 'reduce' },
}
```

- `--no-sandbox` is the reflex fix for container crashes and the wrong one: it disables Chromium's sandbox. Run as a non-root user in the image, or use the official image which is set up for it.
- `slowMo` and `headless: false` are investigation tools; a committed `slowMo` silently multiplies suite time.
- Custom `args` are Chromium-only; Firefox uses `firefoxUserPrefs`, WebKit accepts almost none.

## Choosing A Matrix

| Suite | Matrix |
|---|---|
| PR gate | Chromium only — the fastest signal, catches most regressions |
| Nightly | Chromium + Firefox + WebKit |
| Release | Add branded `chrome`/`msedge` channels and a mobile viewport project |
| Public-facing consumer app | Add real-device Safari verification outside Playwright |

Running three engines on every PR triples cost for a low yield: cross-engine failures are real but rare, and finding them a few hours later on a nightly run is usually acceptable. Decide from your own analytics, not from the browser list.

Which row is the default is the `cross_browser_cadence` preference (`pr` | `nightly` | `release`, default `nightly`); the jobs that implement each gate are in `ci-cd.md`.

## Electron And Android

Playwright can drive Electron apps (`_electron.launch({ args: ['.'] })`, then `electronApp.firstWindow()`) and Chrome on Android over adb. Both are supported but thinner than the web path: expect fewer conveniences, more version sensitivity, and less documentation. Verify the API shape against the installed version before building a suite on either.
