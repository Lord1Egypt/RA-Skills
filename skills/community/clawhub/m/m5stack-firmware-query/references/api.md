# M5Burner Public Query API

This reference describes the read-only routes used by the bundled CLI. The production catalog is dynamic, so do not copy current counts, rankings, versions, or download totals into long-lived documentation.

## Base URL

The default base URL is:

```text
https://burner.m5stack.com
```

Set `M5BURNER_API_BASE_URL` or pass `--base-url` to use a compatible deployment. The CLI appends the route under `/api/v1`.

## Supported Routes

| CLI mode | Method and route | Main parameters |
| --- | --- | --- |
| `search` | `GET /api/v1/firmwares` | `keyword`, `categoryId`, `deviceId`, `sort`, `pageNum`, `pageSize` |
| `intent-search` | aggregate of `GET /api/v1/firmwares` and public detail routes | `intent`, optional `keyword`, `categoryId`, `deviceId`, `sort`, pagination |
| `detail` | `GET /api/v1/firmwares/{firmwareId}` | `firmwareId` |
| `versions` | `GET /api/v1/firmwares/{firmwareId}/versions` | `firmwareId`, `scope` |
| `devices` | `GET /api/v1/devices` | `developerId` |
| `device-by-slug` | `GET /api/v1/devices/by-slug/{slug}` | `slug` |
| `categories` | `GET /api/v1/firmware-categories` | `language` header, `deviceId`, `developerUserId` |
| `developers` | `GET /api/v1/developers` | `keyword`, `pageNum`, `pageSize` |
| `developer` | `GET /api/v1/developers/{developerId}` | `developerId` |
| `developer-firmwares` | `GET /api/v1/developers/{developerId}/firmwares` | `developerId`, `keyword`, `categoryId`, `deviceId`, `pageNum`, `pageSize` |
| `uiflow2` | `GET /api/v1/firmwares/uiflow2/latest` | none |
| `recommended` | `GET /api/v1/firmwares/recommended` | `limit` |
| `ranking --kind weekly` | `GET /api/v1/firmwares/rankings/weekly` | `limit` |
| `ranking --kind all-time` | `GET /api/v1/firmwares/rankings/all-time` | `limit` |
| `comments` | `GET /api/v1/firmwares/{firmwareId}/comments` | `firmwareId`, `pageNum`, `pageSize` |
| `recommend-device` | aggregate of public GET routes | `deviceId` or `deviceName`, `limit`, `sampleSize`, `detailLimit` |

The API also exposes a legacy UIFlow2 route, `/api/v1/firmwares/uiflow2/firmware`. It is intentionally not used by the CLI because the current `/latest` route provides direct CDN URLs.

Some deployments may leave `deviceSlug` empty or protect `/api/v1/devices/by-slug/{slug}` despite the documented public route. Prefer `devices` plus a `deviceId` for portable lookups; use `device-by-slug` only when the target deployment exposes it.

Verified production sort values for `GET /api/v1/firmwares` are `LATEST`, `MOST_DOWNLOADED`, and `MOST_LIKED`. Invalid guessed values such as `DOWNLOADS` or `MOST_COMMENTED` may return HTTP/API `400`.

The production `recommended` route can validly return an empty list. For user-facing recommendation questions, prefer `recommend-device` over `recommended` because it combines catalog search, popularity, likes, and detail metadata for the requested device.

## Response Shapes

Most responses use an envelope such as:

```json
{
  "code": 200,
  "msg": "查询成功",
  "data": [],
  "requestId": "..."
}
```

Paginated routes commonly return `rows` and `total` instead of a list in `data`:

```json
{
  "code": 200,
  "msg": "查询成功",
  "rows": [],
  "total": 0,
  "requestId": "..."
}
```

Useful public fields include:

- Firmware cards/details: `firmwareId`, `firmwareName`, `sourceType`, `currentVersion`, `supportedDevices`, `categories`, and `statistics`. Use `detail` to reliably fetch `sourceUrl` and fuller descriptions; list cards may omit them.
- Versions: `versionId`, `versionName`, `publishTime`, `visibility`, `status`, `binFileName`, `downloadCount`, and `current`.
- Devices: `deviceId`, `deviceCode`, `deviceName`, `deviceSlug`, `productUrl`, and `firmwareCount`.
- Categories: `categoryId`, `categoryCode`, `categoryName`, and `firmwareCount`.
- UIFlow2: `firmwareName`, `versionName`, `deviceType`, and `downloadUrl`.
- Rankings: `rank`, `firmwareName`, `developerName`, and either `weeklyScore` or `totalScore`.

`firmwareDescription` and `currentVersion.versionDescription` are sometimes plain text and sometimes JSON strings shaped like `{"format":"markdown","content":"..."}`. The CLI unwraps these fields for recommendation scoring, but JSON output preserves the original API payload for normal query modes.

`intent-search --intent ai` returns a derived result rather than the raw API envelope. It includes `candidateTotal`, `categoryCandidateTotal`, `matchedTotal`, `results`, `excludedTotal`, a bounded `notableExclusions` sample, and `warnings`. The AI classifier requires functional signals in the firmware name or description; a category label or a note such as “made with ChatGPT/Claude” alone is not sufficient.

An HTTP `200` response with `code: 200` and an empty list is a valid no-result response. HTTP `401` or `403`, or an error envelope with a non-success `code`, must be reported as an access/error condition rather than converted to an empty result.

## Scope Boundary

The public routes above do not require a Bearer token in the documented contract. Account, developer-editing, upload, review, admin, notification, follow/like, and private-share routes are outside this skill. Do not work around authentication or use a token supplied in chat.
