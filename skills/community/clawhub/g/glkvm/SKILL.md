---
name: glkvm
description: Remotely control a target host via GLKVM HTTP API, supporting keyboard/mouse input, screenshot capture, OCR recognition, Fingerbot physical button control, and ATX power management. Access via HTTPS with certificate errors ignored.
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

### 2a. Send Single Key

```bash
# Full click (press + release)
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_key?key=KEY_A"

# Press only
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_key?key=KEY_A&state=true"

# Release only
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_key?key=KEY_A&state=false"
```

Common key names (USB HID keycodes):
- Letters: `KEY_A` ~ `KEY_Z`
- Numbers: `KEY_1` ~ `KEY_0`
- Function keys: `KEY_F1` ~ `KEY_F12`
- Special keys: `KEY_ENTER`, `KEY_BACKSPACE`, `KEY_TAB`, `KEY_ESC`, `KEY_SPACE`
- Arrow keys: `KEY_UP`, `KEY_DOWN`, `KEY_LEFT`, `KEY_RIGHT`
- Modifier keys: `KEY_LEFTCTRL`, `KEY_LEFTSHIFT`, `KEY_LEFTALT`, `KEY_LEFTMETA`
- Others: `KEY_DELETE`, `KEY_HOME`, `KEY_END`, `KEY_PAGEUP`, `KEY_PAGEDOWN`, `KEY_INSERT`

### 2b. Send Keyboard Shortcuts

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

The `keys` parameter is comma-separated, following the Web KeyboardEvent.code specification:
`ControlLeft`, `ShiftLeft`, `AltLeft`, `MetaLeft`, `KeyA`~`KeyZ`, `Digit0`~`Digit9`, `F1`~`F12`, `Enter`, `Escape`, `Backspace`, `Tab`, `Space`, `Delete`, etc.

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
- `limit` (int, default 1024): Maximum characters to send, 0 = unlimited
- `keymap`: Key mapping name
- `slow` (bool): Slow mode, adds delay per key

**Note:** Only characters present in the keymap are supported; special characters such as Chinese cannot be typed directly.

### 2d. Reset HID (Release All Keys)

```bash
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/reset"
```

Call this when keys are stuck or the state is abnormal.

### 2e. Check HID Status

```bash
curl -sk -b /tmp/glkvm_cookies.txt \
  "https://<IP>/api/hid"
```

Returns keyboard/mouse online status, LED indicators (CapsLock/NumLock/ScrollLock), and mouse positioning mode (absolute/relative).

---

## Feature 3: Mouse Control

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

### 3b. Absolute Mouse Move (for absolute positioning mode)

Coordinate system: (0,0) = screen center; (-32768,-32768) = top-left; (32767,32767) = bottom-right

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

### 3c. Relative Mouse Move

```bash
# Move right 50, down 30
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_relative?delta_x=50&delta_y=30"
```

Range -127 ~ 127; call multiple times for larger movements.

### 3d. Mouse Scroll Wheel

```bash
# Scroll up
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_wheel?delta_x=0&delta_y=3"

# Scroll down
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/hid/events/send_mouse_wheel?delta_x=0&delta_y=-3"
```

delta_y positive = scroll up, negative = scroll down; range -127 ~ 127.

---

## Feature 4: Fingerbot Physical Button Robot

Fingerbot controls a physical press robot via Bluetooth to simulate pressing physical buttons (power button, reset button, etc.).

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

---

## Feature 6: System Control

### Reboot GLKVM Device Itself

```bash
curl -sk -b /tmp/glkvm_cookies.txt -X POST \
  "https://<IP>/api/upgrade/reboot"
```

**Note: This reboots the GLKVM device, not the controlled host.**

---

## Feature 7: Firmware Upgrade

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
1. Take screenshot -> View with Read tool -> Analyze target element pixel coordinates (px, py)
2. Confirm screen resolution W x H (inferred from screenshot image size)
3. Convert to HID coordinates:
   to_x = round(px / W * 65535 - 32768)
   to_y = round(py / H * 65535 - 32768)
4. send_mouse_move to move
5. send_mouse_button?button=left to click
6. Take screenshot to verify
```

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
| Screenshot returns 503 | Video stream unavailable, check HDMI connection and retry |
| HID key stuck | Call `/api/hid/reset` to release all keys |
| Fingerbot exist returns false | Bluetooth adapter not connected, cannot use Fingerbot/ATX |
| Cookie expired (401) | Re-execute login process |
| No response to operation | Take screenshot to confirm current state, then decide next step |
