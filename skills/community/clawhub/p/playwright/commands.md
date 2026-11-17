# Commands — The Working Toolkit

Commands that shorten a debugging loop, not the ones in the README.

## Run Less, Faster

```bash
npx playwright test path/to/file.spec.ts:42     # one test, by line number
npx playwright test -g "checkout"               # by title substring
npx playwright test --project=chromium          # one project instead of all
npx playwright test --last-failed               # rerun only what failed last time (playwright >=1.44)
npx playwright test --repeat-each=20 -g "flaky" # measure a flake rate (flake.md)
npx playwright test --workers=1                 # serialize to test for cross-test leakage
npx playwright test --max-failures=1            # stop at the first red in a long suite
```

`--headed` shows the browser; `--debug` opens the Inspector **and disables timeouts** (same as `PWDEBUG=1`), so a paused test never dies under you.

## See What Happened

```bash
npx playwright test --trace on                  # force a trace for this run
npx playwright show-trace test-results/**/trace.zip
npx playwright show-report                      # open the last HTML report
npx playwright test --ui                        # watch mode: time-travel, pick tests, live locators
```

Trace viewer reading order: timeline → the failing action → **DOM snapshot before/after** → Network → Console. The before/after snapshots answer "was it there and covered?" faster than any rerun.

## Discover Locators And Flows

```bash
npx playwright codegen https://example.com          # record clicks into a spec
npx playwright codegen --device="iPhone 15" <url>   # record under emulation
npx playwright codegen --save-storage=auth.json <url>   # record a login, keep the session
npx playwright codegen --load-storage=auth.json <url>   # start recorded flows already signed in
npx playwright open <url>                           # a Playwright-controlled browser, no recording
```

Codegen output is a draft: it emits whatever locator it found, including brittle CSS. Keep the flow, rewrite the locators (`selectors.md`).

## Browsers And Environment

```bash
npx playwright install --with-deps chromium     # browsers + Linux system libs (needs root)
npx playwright install-deps                     # system libs only
npx playwright --version                        # must match the CI image tag exactly
```

- Binaries live in `~/.cache/ms-playwright` (Linux), `~/Library/Caches/ms-playwright` (macOS), `%USERPROFILE%\AppData\Local\ms-playwright` (Windows).
- `PLAYWRIGHT_BROWSERS_PATH=0` installs into `node_modules` instead — the fix when a shared cache is unwritable in a container.
- `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` at install time when the base image already ships them.

## Snapshots And Reports

```bash
npx playwright test --update-snapshots          # rewrite baselines — review the diff, never blind-accept
npx playwright merge-reports --reporter=html ./blob-reports   # one report from sharded runs
```

## Quick Captures Without Writing Code

```bash
npx playwright screenshot --full-page --viewport-size=1280,720 <url> out.png
npx playwright pdf <url> out.pdf                # Chromium headless only
```

## Environment Flags Worth Knowing

| Variable | Effect |
|---|---|
| `PWDEBUG=1` | Inspector + all timeouts disabled |
| `DEBUG=pw:api` | Log every Playwright call — the last line before a hang names the culprit |
| `DEBUG=pw:browser` | Browser process stdout/stderr; where crash reasons appear |
| `PLAYWRIGHT_HTML_REPORT` | Output dir for the HTML report |
| `CI=1` | Enables `forbidOnly` and the CI branches of a typical config |
