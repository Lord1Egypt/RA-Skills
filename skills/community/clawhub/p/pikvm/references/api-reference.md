# PiKVM API reference notes

These notes summarize the PiKVM HTTP API routes most useful for an OpenClaw skill.

## Authentication

PiKVM protects all API routes. Supported auth patterns:

- Per-request `X-KVMD-User` and `X-KVMD-Passwd` headers
- HTTP Basic Auth
- Session cookie via `POST /api/auth/login`

If PiKVM 2FA is enabled, append the current one-time code directly to the password string.

Useful auth routes:

- `POST /api/auth/login`
- `GET /api/auth/check`
- `POST /api/auth/logout`

## General info

- `GET /api/info` — general PiKVM information
- `GET /api/auth/check` — auth validation
- `GET /api/export/prometheus/metrics` — metrics export

## HID

- `POST /api/hid/set_connected`
- `POST /api/hid/reset`
- `GET /api/hid/keymaps`
- `POST /api/hid/print`
- `POST /api/hid/events/send_shortcut`
- `POST /api/hid/events/send_key`
- `POST /api/hid/events/send_mouse_button`
- `POST /api/hid/events/send_mouse_move`

## ATX

- `GET /api/atx`
- `POST /api/atx/power?action=on|off|off_hard|reset_hard`
- `POST /api/atx/click?button=power|power_long|reset`

## Streamer, snapshots, OCR

- `GET /api/streamer`
- `GET /api/streamer/snapshot`
- `DELETE /api/streamer/snapshot`
- `GET /api/streamer/ocr`

Snapshot supports:

- `save`
- `load`
- `allow_offline`
- `ocr`
- `ocr_langs`
- `ocr_left`, `ocr_top`, `ocr_right`, `ocr_bottom`
- `preview`
- `preview_max_width`, `preview_max_height`, `preview_quality`

## Mass Storage Device

- `GET /api/msd`
- `POST /api/msd/write?image=...`
- `POST /api/msd/write_remote?url=...&image=...`
- `POST /api/msd/set_params`
- `POST /api/msd/set_connected?connected=0|1`
- `POST /api/msd/remove?image=...`
- `POST /api/msd/reset`

## Switch

- `GET /api/switch`
- `POST /api/switch/set_active_prev`
- `POST /api/switch/set_active_next`
- `POST /api/switch/set_active?port=...`
- `POST /api/switch/set_beacon`
- `POST /api/switch/set_port_params`
- `POST /api/switch/atx/power?port=...&action=...`

## WebSocket

PiKVM also exposes `wss://<host>/api/ws?stream=0` for event/state updates and interactive input.

Typical useful events include:

- `atx_state`
- `hid_state`
- `msd_state`
- `streamer_state`
- `gpio_state`
- `loop` to mark completion of the initial state bundle
- `ping` / `pong`

Use WebSocket only when real-time event flow is needed. For most agent actions, HTTP routes are simpler and easier to audit.
