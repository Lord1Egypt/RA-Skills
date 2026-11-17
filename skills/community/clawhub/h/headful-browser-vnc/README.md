# Headful Browser (VNC)

A persistent Linux Chrome session that an operator can view and control over VNC,
with CDP capture of the **same existing tab**. Version 2.0.0 introduces an
intentionally revised CLI; see migration and VALIDATION.md for testing limits.

The runtime keeps Xvfb, optional fluxbox, x11vnc, optional noVNC/websockify and
Chrome in one owned session. A Python standard-library manager tracks process
identity and ports. Playwright attaches only for captures; it does not launch
replacement browser contexts or navigate during a normal capture.

## Install

Supported runtime: Linux with /proc, Python >=3.10, Node >=22, Xvfb, xauth,
xdpyinfo, x11vnc and Chrome/Chromium. Use a dedicated non-root OS user.
Debian 12/13 host example (review package names for your distribution):

```bash
sudo apt-get update
sudo apt-get install -y xvfb xauth x11vnc x11-utils fluxbox chromium fonts-noto-cjk
# Optional noVNC operator UI:
sudo apt-get install -y novnc websockify
npm ci --omit=dev
```

Install Node >=22 using reviewed distribution/vendor packages. Ubuntu's
chromium-browser package may use Snap; an installed Google Chrome vendor package
is another option. The runtime discovers google-chrome, google-chrome-stable,
chromium, or chromium-browser; CHROME_BIN can select an executable explicitly.

Generate a new binary VNC password file interactively. The parent directory must
already exist and should be private. The helper refuses to overwrite an existing file:

```bash
mkdir -p ~/.vnc
chmod 700 ~/.vnc
./scripts/setup.sh --set-password "$HOME/.vnc/headful.passwd"
export VNC_PASSFILE="$HOME/.vnc/headful.passwd"
./scripts/setup.sh --check-only
```

Traditional VNC passwords use only the first eight characters. The VNC password
is not transport encryption. Use SSH tunnels.

## Quick start

```bash
./scripts/browser.sh start demo
./scripts/browser.sh pages demo
# Substitute the exact targetId returned by pages:
./scripts/browser.sh capture demo --target TARGET_ID
./scripts/browser.sh stop demo
```

Commands print one JSON object to stdout. Successful operations exit 0.
Failures exit nonzero; parse success and, for captures, individual artifact results.
Lifecycle logs are private files in the session directory.

The start output contains vncAddress and cdpEndpoint. With the returned VNC port:

```bash
ssh -N -L 5901:127.0.0.1:5901 user@server
# Connect your local VNC viewer to 127.0.0.1:5901.
```

Ports default to the first available port in the ranges starting at 5901 (VNC)
and 9222 (CDP); displays start at :99. Allocation is serialized across sessions
in the same state root. Explicit occupied ports/displays fail; existing processes
are never adopted. External allocation races fail readiness rather than attaching
to another session. Use actual returned ports, not a display-to-port formula.

## CLI

```text
browser.sh start SESSION [--display=:99] [--resolution=1366x768]
  [--port=5901] [--passfile=/absolute/path] [--remote-debug-port=9222]
  [--proxy=http://127.0.0.1:3128] [--novnc-port=6080]
  [--novnc-web=/usr/share/novnc]

browser.sh start-vnc SESSION [VNC options above]
browser.sh start-chrome SESSION [--remote-debug-port=9222] [--proxy=URL]
browser.sh status SESSION
browser.sh pages SESSION
browser.sh pause SESSION
browser.sh resume SESSION
browser.sh capture SESSION --target TARGET_ID
browser.sh navigate-and-capture SESSION --target TARGET_ID --url https://example.com/
browser.sh cookies SESSION --url https://example.com/account
browser.sh storage-state SESSION --target TARGET_ID
browser.sh stop SESSION
browser.sh doctor
```

start creates VNC and Chrome together and rolls back owned processes if startup
fails. start-vnc and start-chrome also support a split workflow; if Chrome fails
in that workflow, the already running VNC session remains for diagnosis/retry.
A second start reports an existing session rather than ignoring changed flags.
Use status to inspect it, or stop before changing startup options.
stop is idempotent, including for an unknown session, and retains profiles,
logs, Xauthority and exports. No global pkill fallback exists.

The compatibility script names remain available with the new named arguments:
start_vnc.sh → start-vnc; start_chrome_debug.sh → start-chrome;
stop_vnc.sh → stop; export_page.sh → capture; export_cookies.sh → cookies.

## Operator handoff

```text
vnc-ready → running → paused → running → stopped
startup failure → failed
missing owned process → degraded (status)
```

Run pause before inviting the operator to take control. Pause blocks this CLI's
navigate-and-capture; capture remains available for inspection. Stop remains
available. The automation controller must suspend its own action loop, await the
operator's completion signal, resume, list pages again and reread page state.
The CLI does not physically block other CDP clients or VNC input.

For optional noVNC, install both novnc and websockify and supply --novnc-port.
The manager serves the installed noVNC assets and proxies to its own VNC port:

```bash
./scripts/browser.sh start demo --novnc-port=6080
ssh -N -L 6080:127.0.0.1:6080 user@server
# Open http://127.0.0.1:6080/vnc.html
```

There is no public HTTP gateway, token service or TLS termination in this release.

## Capture and authentication state

capture selects the exact CDP targetId from pages. It never creates a new tab or
reloads the selected one. navigate-and-capture explicitly navigates that existing
tab, waits for DOMContentLoaded, then captures. HTTP >=400 and navigation failures
return nonzero. Neither command promises an application-specific readiness
condition: wait for the expected application state in your controller first.

Each export goes under OUT_DIR/SESSION/UTC-TIMESTAMP-RANDOM/ with directory mode
0700 and file mode 0600. capture creates page.html, page.png and manifest.json.
If one capture fails, the other artifact is retained and the manifest reports
partial failure. Prior exports are never overwritten.

page.html is a rendered DOM snapshot. It does not serialize every live form
property, canvas contents, cross-origin iframe document, or offline resource.
Screenshots and page HTML are sequential, not an atomic snapshot. A detected URL
change during capture is reported as failure.

cookies requires an explicit URL and exports matching cookies from the session's
default browser context. It is never implicitly included in a page capture.
storage-state exports matching cookies plus localStorage for the selected page's
current origin in Playwright's cookies/origins format. The implementation reads
the page directly because CDP attachment may not register previously visited
origins for context.storageState(). IndexedDB, sessionStorage, service workers,
passkeys and device-bound credentials are omitted. Reuse of exported state does
not guarantee login restoration; keep using the original session when possible.

## Configuration

Copy config.example.env to .env, then chmod 600 .env. Only the skill-root .env is read.
Environment variables override file values; command-line options override both.
Values are literal KEY=value, optionally wrapped in matching quotes; no variable
expansion, command substitution, export statements, or executable shell syntax.
Unknown keys and insecure/symlink config files are rejected.

| Key | Default / meaning |
| --- | --- |
| VNC_PASSFILE | Required on start; owned 8-byte rfbauth file, mode 0600 or 0400 |
| VNC_DISPLAY | Auto-allocate from :99 |
| VNC_RESOLUTION | 1366x768 |
| VNC_PORT | Auto-allocate from 5901 |
| REMOTE_DEBUG_PORT | Auto-allocate from 9222 |
| PROXY_URL | Optional Chrome HTTP(S)/SOCKS5 proxy |
| CHROME_BIN | Optional Chrome executable name or absolute path |
| NOVNC_PORT | Disabled unless set |
| NOVNC_WEB | /usr/share/novnc |
| OUT_DIR | Skill directory/out |
| BROWSER_STATE_DIR | XDG_STATE_HOME/headful-browser-vnc or ~/.local/state/headful-browser-vnc |

Profiles always belong to a session under its private state directory.
Per-process PID/start-time/group identity and a session token prevent broad
process matching and PID-file reuse from terminating unrelated sessions.
Xauthority protects each display; Xvfb TCP access is disabled.
VNC, noVNC and CDP readiness checks verify loopback-only listeners owned by
the launched process group. Chrome sandbox is kept enabled; root startup fails.

Loopback services are accessible to other processes with access to the same
host/network namespace, and CDP has no application authentication. Use a
dedicated host/user or suitable isolation for untrusted local tenants.
Sensitive outputs and profiles are retained until you deliberately delete them.

## Tests

```bash
npm ci
npm test
python3 -m unittest discover -s tests -p 'test_*.py'
# Real browser; requires installed Chrome/Chromium (sandbox enabled):
TEST_CHROME_BIN=/usr/bin/google-chrome npm run test:browser
# Full Linux start → capture → handoff → stop, including two-session isolation:
./tests/smoke_test.sh
```

On macOS, the real CDP exporter test can use installed Google Chrome; the session
manager still requires Linux. The full Linux test must run as non-root with all
runtime dependencies. It fails on missing dependencies instead of suppressing
errors. The source archive includes a GitHub Actions workflow; the complete Linux
smoke test passed in CI. See VALIDATION.md for the run and remaining limits.

## Migration from 1.0.2

This is a major CLI revision. Old positional display/resolution/port arguments
are replaced by named arguments. export_page.sh no longer accepts a URL:
use --target for same-tab capture, or navigate-and-capture when navigation is intended.

Recreate .env from the example. Remove VNC_IMPLEMENTATION (runtime is x11vnc),
ALLOW_CHROME_FORCE_RESTART, CHROME_EXTRA_FLAGS, CHROME_USER_DATA_DIR and legacy
TMP_* settings. setup.sh no longer supports --auto-install or --yes; dependency
installation is a reviewed host step. The sourced shell .env loader is removed.
State and output paths are now per session, and cookies require explicit export.

The imported source version and file inventory are recorded in SOURCE.json.
License: MIT-0, consistent with the published skill card.
