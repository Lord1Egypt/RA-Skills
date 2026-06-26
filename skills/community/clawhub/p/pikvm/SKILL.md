---
name: pikvm-control
description: Control and inspect PiKVM devices over the PiKVM HTTP API. Use when asked to operate a PiKVM, query power or HID status, type text or shortcuts remotely, take snapshots or OCR the host screen, manage virtual media, or control PiKVM switch ports. Supports per-request auth using X-KVMD headers or basic auth, plus session login if needed.
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - PIKVM_URL
        - PIKVM_USER
        - PIKVM_PASS
        - PIKVM_VERIFY_SSL
        - PIKVM_USE_BASIC_AUTH
      bins:
        - python3
    primaryEnv: PIKVM_PASS
    homepage: https://docs.pikvm.org/api/
---

# PiKVM Control

Use this skill when the user wants to interact with a PiKVM-managed machine or PiKVM hardware.

## What this skill covers

- Authentication against PiKVM HTTP API
- Device info and health checks
- ATX power state and button actions
- HID typing, key presses, shortcuts, and mouse actions
- Streamer status, screenshots, and OCR
- Mass Storage Device (virtual media) status and image handling
- PiKVM Switch active-port and port-level ATX control

Read [references/api-reference.md](references/api-reference.md) for endpoint details and parameter notes.

## Safety rules

Treat these actions as high impact and get explicit user approval before performing them unless the user already clearly requested the exact action in the current conversation:

- Power off, hard power off, or reset
- Clicking ATX power/reset buttons
- Connecting or disconnecting virtual media
- Uploading, removing, or replacing MSD images
- Switching active KVM ports in environments that may affect another machine
- Sending destructive keyboard shortcuts or arbitrary typed commands

For read-only requests, proceed without extra confirmation.

## Environment and auth

Prefer these environment variables when running the script:

- `PIKVM_URL` — base URL like `https://pikvm.local` or `https://10.0.0.7`
- `PIKVM_USER`
- `PIKVM_PASS`
- `PIKVM_VERIFY_SSL` — `true` or `false`
- `PIKVM_USE_BASIC_AUTH` — `true` to use HTTP Basic Auth instead of `X-KVMD-User` / `X-KVMD-Passwd`

Notes:

- PiKVM requires authentication for all API calls.
- For single-request auth, PiKVM supports either `X-KVMD-User` and `X-KVMD-Passwd` headers, or HTTP Basic Auth.
- If 2FA is enabled, append the current TOTP code directly to the password with no spaces.

## Default workflow

1. Validate that `PIKVM_URL`, `PIKVM_USER`, and `PIKVM_PASS` are available.
2. Start with a read-only request such as `info`, `atx-state`, `streamer-state`, `msd-state`, or `switch-state`.
3. Summarize the current state before taking action.
4. For write operations, restate the exact action being taken.
5. After any state-changing action, re-read the relevant state endpoint and report the result.

## Script

Use `scripts/pikvm_api.py`.

Common examples:

```bash
python scripts/pikvm_api.py info
python scripts/pikvm_api.py atx-state
python scripts/pikvm_api.py atx-power --action on
python scripts/pikvm_api.py atx-click --button reset
python scripts/pikvm_api.py hid-print --text "reboot\n" --slow
python scripts/pikvm_api.py hid-shortcut --keys ControlLeft,AltLeft,Delete
python scripts/pikvm_api.py snapshot --save-path /tmp/pikvm.jpg
python scripts/pikvm_api.py ocr --langs eng
python scripts/pikvm_api.py msd-state
python scripts/pikvm_api.py msd-set --image debian.iso --cdrom true --rw false
python scripts/pikvm_api.py msd-connect --connected true
python scripts/pikvm_api.py switch-active --port 2
python scripts/pikvm_api.py switch-atx-power --port 2 --action reset_hard
```

## When to use which operation

### Read-only inspection

- `info` → general PiKVM/device metadata
- `atx-state` → current power LED/busy state
- `streamer-state` → stream and capture health
- `msd-state` → mounted image and storage availability
- `switch-state` → PiKVM Switch overview

### Input control

- `hid-print` for plain text entry
- `hid-shortcut` for combinations like Ctrl+Alt+Delete
- `hid-key` for a single key press
- `mouse-button` / `mouse-move` for pointer actions

### Screen capture

- `snapshot` to save a JPEG locally
- `ocr` to extract visible text from the host screen
- Use OCR bounding box flags when only part of the screen matters

### Power and media

- `atx-power` for requested state changes (`on`, `off`, `off_hard`, `reset_hard`)
- `atx-click` to emulate case buttons
- `msd-set` to choose image and drive flags
- `msd-connect` to attach or detach the virtual drive from the host

### Switch environments

- `switch-active` to select a target port
- `switch-atx-power` for port-specific power control

## Reporting style

When using this skill in an agent workflow:

- State the PiKVM host being targeted.
- State whether SSL verification is enabled.
- For each action, show the endpoint-level intent in plain English.
- After changes, include the returned PiKVM state that matters most.
- Do not expose passwords, TOTP values, or session cookies.
