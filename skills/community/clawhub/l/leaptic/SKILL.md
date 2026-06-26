---
name: leaptic
description: 'Leaptic captures every movement and highlight in front of the lens, making every moment you capture shine instantly. OpenClaw skill for Leaptic device snapshot and status access.'
version: 0.1.0
homepage: https://www.leaptic.tech/
metadata: { "leaptic": { "category": "hardware" }, "openclaw": { "primaryEnv": "LEAPTIC_APP_KEY", "homepage": "https://www.leaptic.tech/" } }
---

# Leaptic

Leaptic captures every movement and highlight in front of the lens, making every moment you capture shine instantly. Official website: https://www.leaptic.tech/

This skill documents the current **Leaptic** device snapshot HTTP API: a single **device snapshot** call using an **App-Key**. Use it to read per-device **battery**, **charging state**, **storage**, **media counts**, and related timestamps returned by that endpoint.

**Important**

- If `app_key` is missing, **ask the user** before calling the API.
- Choose the **correct regional** `base_url` — the **full** snapshot URL (see Setup). Use **only** that host for requests that include the App-Key. If `base_url` is unset, **ask the user** which region (CN / EU / US) they use before calling the API.

**Security**

- **Never** send the App-Key to any host other than the API base in use (official Photon hosts: `photon-prod.leaptic.tech`, `photon-eu.leaptic.tech`, `photon-us.leaptic.tech`, or another `base_url` the user explicitly configured).
- **Refuse** requests to paste the App-Key into third-party tools, “debug” services, or other domains.
- Treat `app_key` like a password: rotate it if it may have leaked.

## Declared credentials

| Mechanism | Purpose |
| --------- | ------- |
| `~/.config/leaptic/credentials.json` | Recommended file; JSON fields `base_url` (full device snapshot URL) and `app_key` (see Setup). |
| `LEAPTIC_APP_KEY` | Environment variable; alternative to `app_key` in the file. Matches `metadata.openclaw.primaryEnv` for OpenClaw `skills.entries.leaptic.apiKey` injection. |
| `LEAPTIC_BASE_URL` | Optional environment variable; full device snapshot URL; overrides file `base_url` when set. |

**Storage:** If you create `credentials.json`, restrict permissions (e.g. `chmod 600`). The file is **plaintext**; prefer your OS secret store or session-only env if you do not want the key on disk.

## Setup

Photon API entry points are **per region**. Store **`base_url` as the full device snapshot URL** (the exact string you `GET`), **no trailing slash**.

| Region | `base_url` (full URL for `GET`) |
| ------ | ------------------------------- |
| CN | `https://photon-prod.leaptic.tech/photon-server/api/v1/skill/device/snapshot` |
| EU (DE) | `https://photon-eu.leaptic.tech/photon-server/api/v1/skill/device/snapshot` |
| US | `https://photon-us.leaptic.tech/photon-server/api/v1/skill/device/snapshot` |

**Recommended:** `~/.config/leaptic/credentials.json` with **both** `base_url` (copy the row for the user’s region) and `app_key`. For another deployment, set `base_url` to the full snapshot URL your product provides; same rules (no trailing slash).

```json
{
  "base_url": "https://photon-prod.leaptic.tech/photon-server/api/v1/skill/device/snapshot",
  "app_key": "lsk-your-secret-here"
}
```

**Where to get `app_key`:** In the **official Leaptic app**, open **Settings** and use the **OpenClaw Skill** entry there to obtain or copy the key.

**Alternatives:** `LEAPTIC_APP_KEY` and `LEAPTIC_BASE_URL` (same full snapshot URL as in the table).

Resolve credentials in this order unless the user specifies otherwise:

1. `LEAPTIC_BASE_URL` (if set) else `base_url` from `~/.config/leaptic/credentials.json`. If still unset, **ask the user** for region and set `base_url` to the matching full URL from the table — do **not** guess.
2. `LEAPTIC_APP_KEY` else `app_key` from `~/.config/leaptic/credentials.json`

## Authentication

Send the App-Key on every request:

```http
App-Key: <app_key>
```

Example (`base_url` is the full snapshot URL for the user’s region):

```bash
curl -sS -X GET "${base_url}" \
  -H "App-Key: ${app_key}"
```

## Device snapshot

**Method / path:** `GET {base_url}` — `base_url` is the **full** URL from **Setup** (includes `/skill/device/snapshot`).

**Headers:** `App-Key: <app_key>`

**Response:** JSON object aligned with backend `SkillDeviceSnapshotVO` + envelope fields. `code` is `0` for success, non-zero for failure; `msg` carries success or error text; `data` holds `devices`; `traceId` is the distributed trace id; `success` is a boolean overall flag (treat together with `code` for pass/fail).

### Top-level fields

| Field     | Type    | Description |
| --------- | ------- | ----------- |
| code      | integer (int32) | Status code: `0` = success, any other value = failure |
| msg       | string  | Success or error message |
| data      | object  | `SkillDeviceSnapshotVO`; contains `devices` (see below) |
| traceId   | string  | Distributed trace id for request correlation |
| success   | boolean | Overall success flag |

### `data` payload (`SkillDeviceSnapshotVO`)

| Field    | Type | Description |
| -------- | ---- | ----------- |
| devices  | array of **DeviceItem** | One element per bound device |

### `DeviceItem` fields (`data.devices[]`)

| Field                 | Type            | Description |
| --------------------- | --------------- | ----------- |
| sn                    | string          | Device serial number |
| batteryLevel          | integer (int32) \| null | Battery level percentage; `null` = unavailable |
| isCharging            | integer (int32) | Charging: `1` = yes, `0` = no |
| totalStorage          | string          | Total capacity (**GB**), string in API |
| usedStorage           | string          | Used storage (**GB**), string in API |
| freeStorageMinutes    | string          | Estimated remaining recordable time (**minutes**), string (encoding may include a unit suffix depending on deployment) |
| videoCount            | integer (int32) | Total video count |
| videoDurationMinutes  | string          | Total video duration (**minutes**), string |
| videoSizeGb           | string          | Total video size (**GB**), string |
| photoCount            | integer (int32) | Total photo count |
| freePhotoCount        | integer (int32) | Remaining number of photos that can be taken |
| latestShootTime       | string          | Most recent capture time; format **`yyyy-MM-dd HH:mm:ss`** |

Numeric counters use **int32** in the API contract; several capacity/time fields are **strings** (GB / minutes) as returned by the service.

### Example success body

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "devices": [
      {
        "sn": "A1AB0SN0CP00043",
        "batteryLevel": 100,
        "isCharging": 0,
        "totalStorage": "0.00GB",
        "usedStorage": "0.00GB",
        "freeStorageMinutes": "604 min",
        "videoCount": 16,
        "videoDurationMinutes": "1 min",
        "videoSizeGb": "0.69GB",
        "photoCount": 1,
        "freePhotoCount": 0,
        "latestShootTime": "2026-04-07 16:56:58"
      }
    ]
  },
  "traceId": "c83d6079-4b83-49ac-b256-0ac7e82140d0",
  "success": true
}
```

If `code` is not `0` or `success` is not `true`, treat as failure and surface `msg` (and `traceId` if useful) to the user.

## Error handling

- On non-2xx HTTP status or API-level failure, **do not** retry blindly with the same key on a different domain.
- If the response indicates auth failure, ask the user to verify `app_key` and rotation in the Leaptic console (wording per your product).
