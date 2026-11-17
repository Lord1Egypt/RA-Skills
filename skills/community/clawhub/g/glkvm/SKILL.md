---
name: glkvm
description: Remotely control a target host through the GLKVM IP-KVM HTTP API - keyboard/mouse input, screenshots and OCR, Fingerbot physical button control, and ATX power management. Also manages the GLKVM device itself (reboot, firmware upgrade) and its virtual MSD storage (remote ISO download and mounting). Network access uses HTTPS with certificate verification disabled.
---

# GLKVM Control Skill

## Initialization

**The following steps must be performed at the start of each session:**

### Step 1: Get Connection Information

Ask the user for the following information (if not already provided):

1. **GLKVM IP address** (e.g., `192.168.1.100`)
2. **Login password** (username is fixed as `admin`)

### Step 2: Login to Obtain Token

```bash
curl -sk -c /tmp/glkvm_cookies.txt \
  -F "user=admin" \
  -F "passwd=<PASSWORD>" \
  "https://<IP>/api/auth/login"
```

- Response `ok: true` with a `token` indicates successful login; the auth_token is also saved in the cookie.
- Response with `two_step_required: true` means waiting for two-step approval.
- All subsequent requests must include `-b /tmp/glkvm_cookies.txt`.

**All requests use HTTPS with `-k` (ignore certificate errors).**

> ⚠️ **Security and privacy notes.**
> - The login token grants full administrative control over the GLKVM device and the attached host.
>   The cookie file `/tmp/glkvm_cookies.txt` contains this token - delete it at the end of the
>   session and treat it as a credential.
> - Screenshots and OCR output can expose whatever is on the target host's screen; handle them as
>   sensitive data and do not retain them beyond the task.
> - Use this skill only on a trusted network and against devices you are authorized to administer.
> - Several operations in this document are **disruptive** (force power off, reset, reboot,
>   firmware upgrade, MSD writes). Before each one, tell the user what you are about to do and get
>   their explicit confirmation - never perform them silently.

---

## Feature 1: Screenshot / View Current Screen

**Capture and save a screenshot:**
```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/streamer/snapshot" \
  --output /tmp/glkvm_snapshot.jpg
```
Then use the Read tool to read `/tmp/glkvm_snapshot.jpg` to view the image content.

**Get thumbnail (recommended for quick preview):**
```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/streamer/snapshot?preview=true&preview_max_width=1280&preview_max_height=720&preview_quality=80" \
  --output /tmp/glkvm_snapshot.jpg
```

**Screenshot with OCR recognition (returns text):**
```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/streamer/snapshot?ocr=true&ocr_langs=chi_sim,eng"
```

**Parameter description:**
- `save=true`: Save screenshot to device disk
- `load=true`: Load previously saved screenshot without re-capturing
- `allow_offline=true`: Allow response even when video stream is offline
- `ocr_left/ocr_top/ocr_right/ocr_bottom`: OCR region coordinates (-1 = no crop)

**Working principle: After taking a screenshot, you must use the Read tool to view the image, understand the current screen state, then decide the next action.**

---

## Feature 2: Keyboard Control

> **Key names use the Web `KeyboardEvent.code` vocabulary** — `KeyA`, `Digit1`, `ControlLeft`,
> `ArrowUp`, `Escape` — **not** the evdev/Linux macro names (`KEY_A`, `KEY_1`, `KEY_LEFTCTRL`).
> An evdev-style name is rejected with HTTP 400:
> `{"ok":false,"result":{"error":"ValidatorError","error_msg":"The argument 'KEY_A' is not a valid Keyboard key"}}`
> Names are **case-sensitive** and there are exactly 115 of them; the full list is in 2f.
> Anything outside that list is a 400, including plausible-looking guesses such as `Up`, `Ctrl`,
> `Control`, `Meta`, `Win`, `Esc` or `Del`.

### 2a. Send Single Key

```bash
# Press + release (non-modifier keys only — see the warning below)
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_key?key=KeyA"

# Press only
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_key?key=KeyA&state=true"

# Release only
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_key?key=KeyA&state=false"
```

Query parameters:
- `key` (required): a Web `KeyboardEvent.code` name from the list in 2f.
- `state` (bool, optional): `true` = press, `false` = release. **When omitted**, the key is pressed
  and auto-released — except for the keys listed in the warning below.
- `finish` (bool, default `false`): only meaningful with `state=true`; requests the same
  auto-release, with the same modifier exception.

> ⚠️ **Modifier keys are never auto-released.**
> The auto-release is deliberately skipped for `ControlLeft`, `ControlRight`, `ShiftLeft`,
> `ShiftRight`, `AltLeft`, `AltRight`, `MetaLeft`, `MetaRight` and `PrintScreen`.
> So `send_key?key=ControlLeft` **holds Ctrl down indefinitely** — every later keystroke becomes a
> Ctrl+… combination until it is released, and the API returns `{"ok":true}` the whole time.
>
> **Never send a modifier through the bare `send_key` form.** Either use `send_shortcut` (2b), which
> handles press/release for you, or pair the calls explicitly:
> ```bash
> curl ... "send_key?key=ShiftLeft&state=true"
> curl ... "send_key?key=Digit1&state=true"
> curl ... "send_key?key=Digit1&state=false"
> curl ... "send_key?key=ShiftLeft&state=false"   # must not be forgotten
> ```
> If keys are already stuck, call `/api/hid/reset` (2d).

### 2b. Send Keyboard Shortcuts

**This is the recommended way to send anything involving a modifier.** The endpoint presses the keys
in the given order, then releases them in reverse order, so no key is left held.

```bash
# Ctrl+C
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_shortcut?keys=ControlLeft,KeyC"

# Ctrl+Alt+Delete
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_shortcut?keys=ControlLeft,AltLeft,Delete"

# Win+L (lock screen)
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_shortcut?keys=MetaLeft,KeyL"

# Alt+F4
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_shortcut?keys=AltLeft,F4"
```

The `keys` parameter is a comma-separated list of the **same** `KeyboardEvent.code` names used by
`send_key` (2f). A single bad name rejects the whole request with HTTP 400
(`Failed sub-validator on one of the item of [...]`). The request blocks until the whole sequence has
been sent (a fixed 30 ms per key event), so a long combination takes a few hundred milliseconds.

### 2c. Type Text String

```bash
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  -H "Content-Type: text/plain" \
  --data-raw "Hello, World!" \
  "https://<IP>/api/hid/print"

# Slow mode (better compatibility)
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  -H "Content-Type: text/plain" \
  --data-raw "Hello" \
  "https://<IP>/api/hid/print?slow=true"
```

Query parameters:
- `limit` (int, default 1024): maximum characters to send, 0 = unlimited. Text beyond the limit is
  **truncated silently**.
- `keymap` (default `en-us`): key mapping name. An unknown name returns HTTP 400
  (`The argument 'nosuch' is not a valid keymap`). Query the available ones with
  `GET /api/hid/keymaps` — 35 layouts are shipped (`de`, `fr`, `ja`, `ru`, `pt-br`, …).
- `slow` (bool): 30 ms per key event instead of 5 ms.

> ⚠️ **Unmappable characters are dropped silently.** Only characters present in the selected keymap
> can be typed; anything else (CJK, emoji, …) is skipped and the API still returns `{"ok":true}`.
> `--data-raw "你好abc"` types `abc` and reports success. Always verify with a screenshot instead of
> trusting the response.

### 2d. Reset HID (Release All Keys)

```bash
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/reset"
```

Call this when keys are stuck (see the modifier warning in 2a) or the state is abnormal.

### 2e. Check HID Status

```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/hid"
```

Returns keyboard/mouse online status, LED indicators (CapsLock/NumLock/ScrollLock), and the mouse
positioning mode. The two fields worth checking before any input:

- `result.keyboard.online` / `result.mouse.online` — `false` means the USB gadget is not attached to
  a target host. Requests still return `{"ok":true}` but **nothing reaches any machine**.
- `result.mouse.absolute` and `result.mouse.outputs.active` — decide which move endpoint works, see 3e.

### 2f. Complete List of Accepted Key Names

These 115 names are the entire accepted vocabulary for both `send_key` and `send_shortcut`.

| Group | Names |
|---|---|
| Letters (26) | `KeyA` `KeyB` `KeyC` `KeyD` `KeyE` `KeyF` `KeyG` `KeyH` `KeyI` `KeyJ` `KeyK` `KeyL` `KeyM` `KeyN` `KeyO` `KeyP` `KeyQ` `KeyR` `KeyS` `KeyT` `KeyU` `KeyV` `KeyW` `KeyX` `KeyY` `KeyZ` |
| Digits (10) | `Digit1` `Digit2` `Digit3` `Digit4` `Digit5` `Digit6` `Digit7` `Digit8` `Digit9` `Digit0` |
| Function (13) | `F1` `F2` `F3` `F4` `F5` `F6` `F7` `F8` `F9` `F10` `F11` `F12` `F20` |
| Modifiers (8) | `ControlLeft` `ControlRight` `ShiftLeft` `ShiftRight` `AltLeft` `AltRight` `MetaLeft` `MetaRight` — **never auto-released, see 2a** |
| Arrows (4) | `ArrowUp` `ArrowDown` `ArrowLeft` `ArrowRight` |
| Editing / navigation (11) | `Enter` `Escape` `Backspace` `Tab` `Space` `Insert` `Delete` `Home` `End` `PageUp` `PageDown` |
| Punctuation (12) | `Minus` `Equal` `BracketLeft` `BracketRight` `Backslash` `Semicolon` `Quote` `Backquote` `Comma` `Period` `Slash` `IntlBackslash` |
| Locks / system (7) | `CapsLock` `NumLock` `ScrollLock` `Pause` `PrintScreen` `ContextMenu` `Power` |
| Numpad (16) | `Numpad0` `Numpad1` `Numpad2` `Numpad3` `Numpad4` `Numpad5` `Numpad6` `Numpad7` `Numpad8` `Numpad9` `NumpadAdd` `NumpadSubtract` `NumpadMultiply` `NumpadDivide` `NumpadDecimal` `NumpadEnter` |
| Media (3) | `AudioVolumeMute` `AudioVolumeUp` `AudioVolumeDown` |
| IME / intl (5) | `IntlYen` `IntlRo` `KanaMode` `Convert` `NonConvert` |

If a name is not in this table the request fails with HTTP 400 — there are no aliases and no
evdev-style fallbacks.

---

## Feature 3: Mouse Control

> ⚠️ **Check the mouse mode before moving the pointer.** The mouse gadget runs either in *absolute*
> mode or in *relative* mode, and an event sent for the wrong mode is **silently discarded while the
> API still answers `{"ok":true}`**:
> - in relative mode (`usb_rel`, often the default) `send_mouse_move` does nothing;
> - in absolute mode (`usb`) `send_mouse_relative` does nothing.
>
> There is no error to detect this by — always read the current mode first (3e) and switch if needed.
> Buttons and the wheel work in both modes.

### 3a. Mouse Button Click

```bash
# Left click
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_button?button=left"

# Right click
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_button?button=right"

# Middle click
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_button?button=middle"

# Left button press (hold, for dragging)
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_button?button=left&state=true"

# Left button release
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_button?button=left&state=false"
```

Accepted `button` values — anything else is HTTP 400 (`back` and `forward` are **not** accepted):

| Value | Actual button |
|---|---|
| `left` | left |
| `right` | right |
| `middle` | middle |
| `up` | side button **Back** |
| `down` | side button **Forward** |

Note the counter-intuitive naming of the two side buttons. Unlike key names, `button` values are
**case-insensitive** (`Left` and `LEFT` also work). Omitting `state` performs a full press+release;
unlike keyboard modifiers, mouse buttons have no auto-release exception.

### 3b. Absolute Mouse Move (requires absolute mode — see 3e)

Coordinate system: (0,0) = screen center; (-32768,-32768) = top-left; (32767,32767) = bottom-right.
Out-of-range values are **clamped, not rejected** — `to_x=99999` returns `{"ok":true}` and lands at
32767.

```bash
# Move to screen center
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_move?to_x=0&to_y=0"

# Move to top-left corner
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_move?to_x=-32768&to_y=-32768"
```

**Pixel coordinate conversion (screen resolution W x H, target pixel px, py):**
```
to_x = round(px / W * 65535 - 32768)
to_y = round(py / H * 65535 - 32768)
```
Use the pixel size of the screenshot you actually received; a scaled-down preview works fine because
the conversion is a ratio.

### 3c. Relative Mouse Move (requires relative mode — see 3e)

```bash
# Move right 50, down 30
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_relative?delta_x=50&delta_y=30"
```

Both `delta_x` and `delta_y` are **required** — omitting one returns HTTP 400
(`None argument is not a valid Mouse delta`). Range -127 ~ 127; larger values are clamped, not
rejected, so a bigger movement needs several calls.

### 3d. Mouse Scroll Wheel

```bash
# Scroll up
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_wheel?delta_x=0&delta_y=3"

# Scroll down
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_wheel?delta_x=0&delta_y=-3"
```

`delta_y` positive = scroll up, negative = scroll down; range -127 ~ 127 (clamped). Both `delta_x`
and `delta_y` are required here too. The wheel works in both mouse modes.

### 3e. Check and Switch the Mouse Mode

```bash
# Current mode
curl -sk -b /tmp/glkvm_cookies.txt "https://<IP>/api/hid"
#   -> result.mouse.absolute        : true = absolute, false = relative
#   -> result.mouse.outputs.active  : "usb" | "usb_rel" | "usb_hybrid" | "usb_touch"
#   -> result.mouse.outputs.available : modes this device actually supports

# Switch to absolute positioning (needed for send_mouse_move)
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/set_params?mouse_output=usb"

# Switch back to relative
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/set_params?mouse_output=usb_rel"
```

`mouse_output` accepts `usb` (absolute), `usb_rel` (relative), `usb_hybrid`, `usb_touch`, `ps2`,
`disabled` — but only the values listed in `outputs.available` will actually take effect. The switch
applies at runtime only and is **not** persisted, so the device returns to its configured default
after a reboot. Confirm the switch by re-reading `/api/hid` before relying on it, and restore the
original mode when you are done if the user was using the device interactively.

---

## Feature 4: Fingerbot Physical Button Robot

Fingerbot controls a physical press robot via Bluetooth to simulate pressing physical buttons (power button, reset button, etc.).

> ⚠️ **Presses act on real physical buttons of the target host.** In particular the *force shutdown*
> (long press, `press_time=5000`) and *reset* (`press_time=200`) examples below can interrupt work in
> progress or cause data loss. State what you are about to press and obtain the user's explicit
> confirmation before performing either of them.

### 4a. Check Connection

```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/fingerbot/exist"
```

Returns `result.exist: true` if the Bluetooth adapter is connected.

### 4b. Check Battery

```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/fingerbot/battery"
```

Returns `result.battery`: battery percentage from 0 to 100.

### 4c. Perform Press Click

```bash
# Short press (100ms, high angle, suitable for normal buttons)
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/fingerbot/click?press_time=100&angle_enum=2"

# Short press power button to power on (500ms)
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/fingerbot/click?press_time=500&angle_enum=2"

# Long press power button to force shutdown (5 seconds)
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/fingerbot/click?press_time=5000&angle_enum=2"

# Press reset button (200ms)
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/fingerbot/click?press_time=200&angle_enum=2"
```

**Parameter description:**
- `press_time`: Press duration (milliseconds), range 100~60000
- `angle_enum`: `1` = low angle (light press), `2` = high angle (deep press)

### 4d. Check Firmware Version

```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/fingerbot/local_version"
```

---

## Feature 5: ATX Power Management

ATX power control is achieved through **Fingerbot physical pressing** (no separate ATX interface in the API).

Before use, confirm that Fingerbot is connected and installed near the host's power/reset button:

```bash
curl -sk -b /tmp/glkvm_cookies.txt "https://<IP>/api/fingerbot/exist"
curl -sk -b /tmp/glkvm_cookies.txt "https://<IP>/api/fingerbot/battery"
```

| Operation | Command |
|-----------|---------|
| Power on | `click?press_time=500&angle_enum=2` |
| Normal shutdown (trigger ACPI) | `click?press_time=500&angle_enum=2` |
| Force power off | `click?press_time=5000&angle_enum=2` |
| Reset | `click?press_time=200&angle_enum=2` |

> ⚠️ **Force power off and Reset are disruptive:** they can interrupt work and cause data loss on the
> target host. Before executing either of them, tell the user and obtain their explicit confirmation.

---

## Feature 6: System Control

### Reboot GLKVM Device Itself

```bash
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/upgrade/reboot"
```

> ⚠️ **This reboots the GLKVM device itself, not the controlled host.** All active connections
> (web UI, streaming, input) are dropped and the device takes ~1 minute to come back. The controlled
> host keeps running. This is a disruptive action - tell the user and get their explicit
> confirmation first.

---

## Feature 7: Firmware Upgrade

> ⚠️ **Firmware operations change the GLKVM device itself.** Applying an upgrade (7e) reboots the
> device, can alter its behavior, and with `save_config=false` resets it to factory defaults. Only
> upgrade with firmware you trust (the device's own update server, or a file you verified yourself),
> and get the user's explicit confirmation before starting an upgrade.

### 7a. Get Local Firmware Version

```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/upgrade/version"
```

Response fields:
- `result.version`: Local firmware version string
- `result.model`: Device model (e.g., `RM1`)

### 7b. Compare with Server Version

```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/upgrade/compare"
```

Response fields:
- `result.local_version` / `result.local_model`: Current firmware version and model
- `result.server_version` / `result.server_model`: Latest version available on the update server
- `result.release_note`: English release notes
- `result.release_note_cn`: Chinese release notes

### 7c. Download Firmware from Cloud (OTA)

Trigger cloud download (returns immediately, downloads in background):
```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/upgrade/download"
```

Response: `result.size` = total firmware size in bytes.

Check download progress:
```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/upgrade/download_info"
```

Response: `result.size` = bytes downloaded so far, `result.total_size` = total size.

Cancel an in-progress download:
```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/upgrade/download_cancel"
```

### 7d. Upload Firmware File Manually

```bash
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  -F "file=@/path/to/update.img" \
  "https://<IP>/api/upgrade/upload"
```

- Request body: `multipart/form-data`, field name `file`
- Requires `Content-Length` header (curl sets it automatically)
- Firmware is saved to `/userdata/update.img` on the device
- Response: `result.filename` (original filename) and `result.size` (bytes)

### 7e. Start Firmware Upgrade

```bash
# Upgrade and preserve existing config (default)
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/upgrade/start?save_config=true"

# Upgrade and reset to factory defaults
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/upgrade/start?save_config=false"
```

- Must upload or download firmware first (step 7c or 7d)
- Device reboots automatically after upgrade completes
- Response: `result.status` (`"Upgrade started"` or `"Upgrade failed"`), `result.stdout`, `result.stderr`

**Typical OTA upgrade workflow:**
```
1. /api/upgrade/compare     → check if update available
2. /api/upgrade/download    → start background download
3. /api/upgrade/download_info (poll) → wait until size == total_size
4. /api/upgrade/start       → apply upgrade (device reboots)
```

---

## Feature 8: MSD Remote ISO Download

Download an ISO image from a remote URL directly to the MSD storage, without transferring through the client machine.

> ⚠️ **This writes to the device's virtual USB storage and changes what the target host can boot.**
> Existing MSD contents are overwritten, and connecting the partition (8a workflow step 4) presents
> the new image to the host as a bootable drive. Only download ISOs from sources you trust, and get
> the user's explicit confirmation before writing. The `insecure=1` option disables TLS
> verification and should only be used for URLs you have independently verified.

### 8a. Remote Download to MSD

```bash
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/msd/write_remote?url=http://example.com/ubuntu.iso"

# Specify target filename
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/msd/write_remote?url=http://example.com/ubuntu.iso&image=ubuntu.iso"

# Skip TLS verification for HTTPS URLs
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/msd/write_remote?url=https://example.com/ubuntu.iso&insecure=1"
```

Query parameters:
- `url` (required): Remote file download URL
- `image` (optional): Target image name on MSD storage; auto-inferred from URL if omitted
- `prefix` (optional): Subdirectory path prefix
- `insecure` (optional): Skip TLS certificate verification, default `false`
- `timeout` (optional): Connection timeout in seconds, default `10.0`
- `remove_incomplete` (optional): If `1`, deletes partial file on write failure

**Response: Streaming NDJSON** (`Content-Type: application/x-ndjson`)

Each line is a JSON object reporting progress; the last line is the final result:
```json
{"image": {"name": "ubuntu.iso", "size": 1234567890, "written": 102400000}}
```

Fields:
- `image.name`: Image filename
- `image.size`: Total file size in bytes (0 if server did not return `Content-Length`)
- `image.written`: Bytes written so far

Error responses:
- `400`: Remote URL unreachable or request failed
- `507`: Insufficient storage space on MSD partition

**Typical workflow for remote ISO installation:**
```
1. /api/msd/partition_disconnect          → ensure drive is disconnected
2. /api/msd/write_remote?url=<ISO_URL>    → download ISO directly from internet
3. (Poll NDJSON stream until size == written)
4. /api/msd/partition_connect             → present drive to target host
5. (On target host) boot from USB drive, complete installation
6. /api/msd/partition_disconnect          → disconnect when done
```

---

## Standard Operation Workflows

### Click a Specific Position on Screen

```
0. GET /api/hid -> check result.mouse.absolute
   - false: POST /api/hid/set_params?mouse_output=usb, then re-read /api/hid to confirm
   - (without this, send_mouse_move returns ok:true and does nothing)
1. Take screenshot -> View with Read tool -> Analyze target element pixel coordinates (px, py)
2. Confirm screen resolution W x H (inferred from screenshot image size)
3. Convert to HID coordinates:
   to_x = round(px / W * 65535 - 32768)
   to_y = round(py / H * 65535 - 32768)
4. send_mouse_move to move
5. send_mouse_button?button=left to click
6. Take screenshot to verify
```

If the device only supports relative mode, drive the pointer with repeated
`send_mouse_relative` calls (max ±127 per call) instead and verify by screenshot after each batch.

### Type Text

```
1. Take screenshot to confirm focus is in the correct input field
2. /api/hid/print to send text
3. Take screenshot to confirm input is correct
```

### General Automation Workflow

```
Initialize login -> Take screenshot to observe -> Perform action -> Take screenshot to verify -> Loop until complete
```

---

## Error Handling

| Situation | Solution |
|-----------|----------|
| Login returns 401/403 | Wrong password, ask the user again |
| Cookie expired (401) | Re-execute login process |
| Screenshot returns 503 | Video stream unavailable, check HDMI connection and retry |
| `... is not a valid Keyboard key` (400) | You used an evdev name such as `KEY_A`. Use the `KeyboardEvent.code` name from 2f (`KeyA`) |
| `Failed sub-validator on one of the item of [...]` (400) | One of the names in `send_shortcut?keys=` is invalid — check every item against 2f |
| `... is not a valid Mouse button` (400) | Only `left`, `right`, `middle`, `up`, `down` are accepted; `back`/`forward` are not |
| `None argument is not a valid Mouse delta` (400) | `send_mouse_relative` / `send_mouse_wheel` need **both** `delta_x` and `delta_y` |
| HID key stuck / everything becomes a Ctrl+ combination | A modifier was sent through the bare `send_key` form and never released. Call `/api/hid/reset`, then use `send_shortcut` instead (2a, 2b) |
| Mouse does not move but API returns `ok:true` | Wrong mouse mode — `send_mouse_move` needs absolute mode, `send_mouse_relative` needs relative mode. Check and switch via 3e |
| Typed text is missing characters, response was `ok:true` | Those characters are not in the keymap (CJK, emoji) and were dropped silently. Use a different input path, e.g. paste from the target host's own clipboard |
| Everything returns `ok:true` but nothing happens on the host | Check `result.keyboard.online` / `result.mouse.online` in `/api/hid` — `false` means the USB gadget is not attached to any host |
| Fingerbot exist returns false | Bluetooth adapter not connected, cannot use Fingerbot/ATX |
| No response to operation | Take screenshot to confirm current state, then decide next step |
