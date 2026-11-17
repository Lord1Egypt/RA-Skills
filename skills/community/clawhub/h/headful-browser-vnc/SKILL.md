---
name: headful-browser-vnc
description: Run a persistent Linux Chrome session with VNC/noVNC human takeover and capture an existing tab through CDP. Use for remote browser workflows that need manual login, MFA, or operator inspection followed by automation.
metadata:
  version: "2.0.0"
  author: waylonsong
---

# Headful Browser (VNC)

Run commands from this skill's directory, or use absolute script paths.
Runtime requires Linux, Python 3.10+, Node 22+, Xvfb, xauth, x11vnc,
xdpyinfo, Chrome/Chromium and the locked npm dependencies.
Read [README.md](README.md) for installation, configuration, migration and limits.

## Session workflow

1. Run `./scripts/setup.sh --check-only`. Install missing dependencies using the documented host instructions.
2. Configure an owned binary rfbauth passfile, mode 0600/0400, through `VNC_PASSFILE`.
3. Start: `./scripts/browser.sh start <session>`. Output is JSON containing actual VNC/CDP ports and the session directory. Explicit startup options are documented in README.
4. List tabs: `./scripts/browser.sh pages <session>`. Retain the exact `targetId` of the intended tab; do not guess it.
5. Capture without navigation: `./scripts/browser.sh capture <session> --target <targetId>`.
6. Stop owned processes: `./scripts/browser.sh stop <session>`. Profiles and artifacts are retained.

Use `navigate-and-capture <session> --target <targetId> --url <http(s)-url>` only when navigation is intended. Never replace a current-page capture with a fresh request, a new tab, or wget.

## Human takeover

Run `pause <session>`, suspend the calling automation loop, then give the operator the VNC SSH tunnel or optional noVNC URL from `status`. Wait for the operator to finish. Run `resume <session>` and refresh `pages` before continuing; page state may have changed.

Pause is cooperative: this CLI blocks its own navigation while paused. It cannot stop an independent CDP client from clicking or navigating. External controllers must honor the state and release control themselves.

## Artifacts and failures

Capture writes HTML, PNG and a manifest to a unique private directory, without cookies.
Use `cookies <session> --url <http(s)-url>` only when cookie export is requested.
Use `storage-state <session> --target <targetId>` for cookies scoped to that page URL and localStorage for its current origin. It does not export IndexedDB, sessionStorage, passkeys or a complete browser profile.

Read JSON `success` and the exit status. Partial capture returns nonzero and records individual artifact failures. Do not report success merely because an output directory exists.
HTML is a DOM snapshot, not an offline archive or a complete record of live form properties.

VNC, CDP and optional noVNC bind to loopback. Use SSH forwarding for remote access.
Chrome runs as non-root with sandbox enabled. Do not introduce global process kills or silently disable the sandbox to make startup pass.
