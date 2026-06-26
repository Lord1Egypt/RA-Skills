---
name: headful-browser-vnc
description: "Headful Chromium with VNC/noVNC operator UI and Chrome CDP exports (cookies, screenshots, outerHTML)."
required_env:
  - VNC_PASSFILE
  - REMOTE_DEBUG_PORT
  - PROXY_URL
  - OUT_DIR
  - ALLOW_CHROME_FORCE_RESTART
  - CHROME_USER_DATA_DIR
  - VNC_IMPLEMENTATION
---

# headful-browser-vnc

## Overview

`headful-browser-vnc` provides a controlled, auditable, headful Chromium browsing environment on a server for cases where full browser rendering and occasional human interaction are required. It combines `Xvfb`, a window manager, and `x11vnc` (optional noVNC) to present the server-side browser UI to an operator, while offering programmatic integration points (Chrome Remote Debugging / CDP) for automated capture of cookies, rendered HTML, and screenshots.

## Primary objective

- Enable reliable, repeatable automation workflows that require the ability to escalate to a human operator for tasks that cannot be solved purely by automation (CAPTCHA solving, challenge pages, multi-factor authentication, manual login flows). The skill's intent is to: (1) run a headful Chrome instance in an isolated profile; (2) expose a secure operator-visible UI to the server browser (VNC/noVNC) so a human can intervene; (3) preserve and export the resulting browser session artifacts (cookies, outerHTML, screenshots) back into automated pipelines for continued processing.

## Key capabilities

- **Headful browser execution**: launch Google Chrome / Chromium with an isolated user data directory and configurable flags (proxy, remote-debugging-port, extra args) on a server X display provided by `Xvfb`.
- **Operator UI**: present the running browser to an operator via `x11vnc` (or optional noVNC web proxy). Operators can connect over SSH-forwarded ports or noVNC with token gating to perform manual actions (solve CAPTCHAs, authenticate), then signal the system to capture artifacts.
- **Programmatic capture**: export rendered `outerHTML`, full-page screenshots, and cookies using Chrome CDP (Playwright/Puppeteer compatible). Exports are intended for downstream automated analysis or storage.
- **Safe restart and recovery**: helpers to restart Chrome when flags change, with explicit user confirmation required for any action that may terminate existing browser instances.
- **Artifact hygiene**: captured artifacts are written to an artifacts directory with restrictive file permissions. The skill logs actions and writes diagnostic artifacts to facilitate debugging and comparison-based analysis.

## Security, privacy, and operational notes

- **VNC security**: the skill creates per-session passfiles (`rfbauth`) when possible; noVNC should be bound to loopback or token-gated. Do not expose VNC/noVNC endpoints to the public internet without additional access controls. Store passfiles with mode `600`.
- **Sensitive artifacts**: cookies and rendered page artifacts are sensitive. They are stored under the skill's `out/` directory with restrictive permissions; users are responsible for secure storage and timely cleanup.
- **Privileged operations**: installing system packages and enabling systemd units require `sudo` and explicit user consent. The scripts will not perform privileged actions automatically unless the operator explicitly enables the auto-install path (see below).

## Supported VNC implementations

The skill supports multiple VNC backends; behavior is controlled via the skill-local `.env` file (`VNC_IMPLEMENTATION`): `auto` (default), `tigervnc`, `tightvnc`, `realvnc`. When possible the skill prefers non-interactive `rfbauth` generation via `vncpasswd`; when unavailable it prompts the operator and documents fallback behavior.

## Runtime files & usage

This section documents each file included in the skill release branch, its purpose, usage examples, preconditions, and relations to other files. All script examples assume you run them from the workspace root unless noted.

### `skills/headful-browser-vnc/scripts/setup.sh`
- **Purpose**: interactive, documented installer and validator for the skill's runtime dependencies (`Xvfb`, `x11vnc`, Chrome/Chromium, node, tooling). Primarily guidance-only: prints distro-aware commands; only runs package-manager operations when explicitly allowed.
- **Usage**:
  ```bash
  ./skills/headful-browser-vnc/scripts/setup.sh [--check-only] [--auto-install] [--yes] [--set-password]
  ```
- **Preconditions**: network access to package repositories; `sudo` available for host installs (not required inside containers when running as root). When running inside a container, auto-installs require either root or `CONTAINER_AUTO_OK=true`.
- **Relations**: updates/creates `skills/headful-browser-vnc/.env`; generates VNC passfiles via `vncpasswd` when available; consults `templates/` for service unit guidance.

### `skills/headful-browser-vnc/scripts/start_vnc.sh`
- **Purpose**: start an `Xvfb` display, optional window manager, and `x11vnc` to expose the display. Emits a one-line summary with the VNC port and display id.
- **Usage**:
  ```bash
  skills/headful-browser-vnc/scripts/start_vnc.sh <session_id> [--display=:99] [--resolution=1366x768] [--port=5901]
  ```
- **Preconditions**: `Xvfb` and `x11vnc` installed (or available in Docker image), `VNC_PASSFILE` permission `600` if provided.
- **Relations**: `start_vnc.sh` creates the `DISPLAY` and user-data directory used by `start_chrome_debug.sh`; `stop_vnc.sh` undoes the session.

### `skills/headful-browser-vnc/scripts/stop_vnc.sh`
- **Purpose**: stop and clean up a running VNC/Xvfb session previously started by `start_vnc.sh`.
- **Usage**:
  ```bash
  skills/headful-browser-vnc/scripts/stop_vnc.sh <session_id> [--display=:99]
  ```
- **Preconditions**: session id matches an active session created by `start_vnc.sh`.

### `skills/headful-browser-vnc/scripts/start_chrome_debug.sh`
- **Purpose**: launch a headful Chrome/Chromium instance attached to a session `DISPLAY` with a dedicated user-data dir and remote-debugging port for CDP access.
- **Usage**:
  ```bash
  skills/headful-browser-vnc/scripts/start_chrome_debug.sh <session_id> [--proxy=http://...] [--remote-debug-port=9222]
  ```
- **Preconditions**: Chrome/Chromium binary available and readable; `DISPLAY` is set (`start_vnc.sh` must have run); user-data directory writable by the process owner.
- **Relations**: other scripts (`export_page.sh`, `export_cookies.sh`) connect to the remote-debugging port started by this script.

### `skills/headful-browser-vnc/scripts/export_page.sh`
- **Purpose**: instruct Chrome to load a URL and export rendered `outerHTML` and a full-page screenshot for later analysis.
- **Usage**:
  ```bash
  skills/headful-browser-vnc/scripts/export_page.sh <session_id> <url> [--devtools-port=9222]
  ```
- **Preconditions**: headful Chrome with remote-debugging port active and reachable (`start_chrome_debug.sh`).

### `skills/headful-browser-vnc/scripts/export_cookies.sh`
- **Purpose**: export cookies from a running Chrome instance via the Chrome DevTools Protocol.
- **Usage**:
  ```bash
  skills/headful-browser-vnc/scripts/export_cookies.sh <session_id> [--devtools-port=9222]
  ```

### General Notes on Export Helpers
- **Note**: these export helpers (`export_page.sh`, `export_cookies.sh`) are designed to be idempotent and safe to run after manual operator interventions. They place artifacts into `out/<session_id>/` with restrictive permissions.

### Combined Script Usage Flow
- **Flow**: `start_vnc.sh <id>` → `start_chrome_debug.sh <id>` → operator attaches via VNC → operator interacts → `export_page.sh` / `export_cookies.sh` → `stop_vnc.sh <id>`

### `skills/headful-browser-vnc/docker/`
- **Purpose**: reference `docker/` directory containing entrypoint and `docker-compose.yml` plus an embedded `Dockerfile` in `README.docker.md` for reproducible builds. ClawHub does not accept Dockerfile uploads, so the Dockerfile content has been included in `skills/headful-browser-vnc/README.docker.md` as a code block.
- **Recommendation**: For reproducibility and security, build dependencies into the image (`Dockerfile`) rather than relying on runtime package installs inside a running container. If you must allow in-container auto-installs, see `setup.sh` gating (`CONTAINER_AUTO_OK` and `container_auto_allowed()`).

### `skills/headful-browser-vnc/templates/`
- **Purpose**: Jinja2-style templates for systemd unit files (`x11vnc`/`noVNC`). Use them as references; deploying them on a host requires `sudo` and careful service permissions.

### `skills/headful-browser-vnc/tests/smoke_test.sh`
- **Purpose**: non-privileged smoke test exercising start → launch → export → cleanup sequence to validate runtime behavior in CI-friendly environments.
- **Usage**:
  ```bash
  ./skills/headful-browser-vnc/tests/smoke_test.sh
  ```

## Configuration (`.env`)

Place a skill-local `skills/headful-browser-vnc/.env` (`chmod 600`) to persist runtime defaults. Key fields:

- `VNC_PASSFILE`: path to passfile (e.g. `/home/user/.vnc/passwd` or `./vnc_passwd`)
- `VNC_PORT`: optional explicit TCP port to bind `x11vnc` (if omitted the script will report the actual port in use)
- `VNC_IMPLEMENTATION`: `auto`|`tigervnc`|`tightvnc`|`realvnc`
- `VNC_DISPLAY`: X display (default `:99`)
- `VNC_RESOLUTION`: screen resolution (default `1366x768`)
- `REMOTE_DEBUG_PORT`: Chrome remote debugging port (default `9222`)
- `PROXY_URL` / `HTTP_PROXY` / `HTTPS_PROXY`: optional proxy settings

## Install and dependencies

- `setup.sh` contains interactive guidance and optional prompts for installing Chrome, node, Playwright, and VNC helper tools. The installer will not run `sudo` operations without explicit consent.
- Programmatic export paths prefer Node + Playwright; a Python fallback is available but optional.

## Auto-install behaviour and safety (enforced)

The installer supports an optional auto-install path but it is gated behind explicit confirmations and container-aware checks:
- CLI flag: `--auto-install` (sets `AUTO_INSTALL=true` for the run).
- Runtime confirmation: when the installer proposes a distro-specific command it will first ask for a `y/N` confirmation, then print the exact command and require the operator to type the full word `yes` (not `y`). Only if both confirmations are provided will the installer execute the command.
- Container extra gate: inside a detected container (`/.dockerenv` or `/proc/1/cgroup` contains `docker/containerd/kubepods`), automatic package-manager operations will only run if the process is root (`id -u == 0`) or if `CONTAINER_AUTO_OK=true`.

Default behaviour remains conservative: without `--auto-install` the installer only prints distro-appropriate commands and will not run package-manager commands automatically.

## Templates and integration

- `templates/x11vnc.service.j2` — systemd unit template for persistent sessions (requires `sudo` to install)
- `templates/novnc.service.j2` — noVNC service template

## Integration guidance for maintainers

- Use Chrome CDP (devtools) for deterministic exports. Prefer attaching to an already-running headful Chrome instance rather than launching short-lived headless instances when reproducing a previously observed UI state.
- Persist session artifacts and index them (timestamp, URL, session id, VNC port, devtools port) so comparison automation can operate on operator-validated examples.
- When embedding into automated pipelines, clearly separate automated actions from operator interventions; require explicit human confirmation for destructive actions (Chrome restarts, service reconfiguration).

## Testing

A non-privileged smoke test is provided at `skills/headful-browser-vnc/tests/smoke_test.sh`. It performs a basic start → launch → export → cleanup sequence and is useful for CI verification.

## Support and contribution

The skill is maintained in this workspace. When contributing changes, follow the repository conventions: create backups before modifying scripts, run `bash -n` for syntax validation, and preserve audit logs and artifacts.

## License

Include an appropriate `LICENSE` file when publishing (e.g., MIT). Update author/maintainer fields in `SKILL.md` prior to external publication.

## Example: safe auto-install run

To allow the installer to perform distro package manager actions automatically, run with explicit `--auto-install` and be prepared to type the full confirmation word. Example:

```bash
AUTO_INSTALL=true ./skills/headful-browser-vnc/scripts/setup.sh --auto-install
```

The script will: (1) detect your distro and print the exact command it plans to run; (2) ask for a normal `y/N` confirmation; (3) print the command and require you to type the exact word `yes` to proceed; (4) only then execute the command.

If you prefer to always review and run commands manually, omit `--auto-install` and the script will only print distro-appropriate commands for you to run yourself.

---

## Short example run transcript (what prompts look like)

Below is a short, representative transcript demonstrating the installer flow when a few components are missing and the operator chooses the manual path (no auto-install). Prompts shown are exact prompts produced by the current `setup.sh`.

```
$ ./skills/headful-browser-vnc/scripts/setup.sh
Platform install hints (guidance-only — these commands will NOT be run automatically):

Debian / Ubuntu (apt):
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends \
    xvfb x11vnc fluxbox x11-utils tigervnc-standalone-server tightvnc-tools \
    fonts-noto-cjk fontconfig chromium-browser google-chrome-stable \
    nodejs npm python3-pip

---
Missing requirements: Xvfb x11vnc chrome node VNC_PASSFILE .env
--- Handling missing: Xvfb ---
Install Xvfb? (y/N) n
Skip. Manual: sudo apt-get install xvfb
Press Enter when done...
--- Handling missing: x11vnc ---
Install x11vnc? (y/N) y
VNC Port [5901]: 5901
Enter VNC passfile path [/home/user/vnc_passwd]: /home/user/.vnc/passwd
Tool 'vncpasswd' found. Preparing automated generation...
Enter VNC password (hidden): ********
Confirm password: ********
SUCCESS: rfbauth generated at /home/user/.vnc/passwd
--- Handling missing: chrome ---
Select Chrome version:
1) Google Chrome (Recommended)
2) Chromium (Snap)
3) Skip
Choice [1-3] (default 1): 3
Skipped.
--- Handling missing: node ---
Install Node.js v22+ using suggested command? (y/N) n
Skipped automatic install. Please run the printed command manually.
--- Handling missing: .env ---
Create template .env? (y/N) y
Created skills/headful-browser-vnc/.env
```
