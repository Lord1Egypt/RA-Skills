# longarm HTTP API Reference

Remote gesture, screenshot, app launch, overlay, and batch automation for Android.

Base URL: `http://<device-ip>:<port>`. If token auth is enabled, send `Authorization: Bearer <token>` on every request. Missing or invalid tokens return `401`.

## Tiers

Free: `tap`, `long_press`, status, screen info, screenshots, overlay show/hide, app launch, intent launch, and batch infrastructure.

Plus: `swipe`, `pinch`, `two_finger_swipe`, and `rotate`, including when used inside batch tasks. Without Plus, these return `403` with `{"error":"Plus subscription required"}`.

## Coordinates

Screen origin is top-left. `x` increases rightward and `y` downward. Gesture position fields are optional where documented; omitted start positions default to the floating bubble's current coordinates. Durations are milliseconds.

## Core Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/status` | Health, version, Plus state, and available gesture endpoints. |
| GET | `/api/screen/info` | Screen width, height, and density. |
| POST | `/api/gesture/tap` | Tap at `x`, `y`; `duration` defaults to `50`. |
| POST | `/api/gesture/long_press` | Long press at `x`, `y`; `duration` defaults to `1000`. |
| POST | `/api/gesture/swipe` | Plus swipe from `startX,startY` to `endX,endY`; `duration` defaults to `300`. |
| POST | `/api/gesture/pinch` | Plus pinch/zoom at `x,y`; `startSpread`, `endSpread`, optional `angle`, `duration`. |
| POST | `/api/gesture/two_finger_swipe` | Plus two-finger swipe with optional `spread` and `duration`. |
| POST | `/api/gesture/rotate` | Plus two-finger rotation with `radius`, `startAngle`, `endAngle`, optional `duration`. |
| GET | `/api/screenshot` | PNG screenshot, optionally with grid/scale labels. |
| POST | `/api/overlay/show` | Show floating control button. |
| POST | `/api/overlay/hide` | Hide floating control button. |
| POST | `/api/app/open` | Open an installed Android app by package name. |
| POST | `/api/intent/open` | Open an Android intent. |

Example bodies:

```json
{ "x": 540, "y": 1200, "duration": 50 }
```

```json
{ "startX": 540, "startY": 1800, "endX": 540, "endY": 600, "duration": 300 }
```

```json
{ "packageName": "com.android.settings" }
```

```json
{
  "action": "android.intent.action.VIEW",
  "data": "https://example.com",
  "packageName": "com.android.chrome",
  "categories": ["android.intent.category.BROWSABLE"],
  "extras": { "fromLongarm": true }
}
```

## Screenshot Grid

`GET /api/screenshot` accepts query parameters:

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `gridSize` | Required when enabling grid | none | Cell size: pixels (`8`-`4096`), cm (`0.1cm`-`100cm`), or inches (`0.05in`-`40in`). |
| `gridColor` | No | `80FF0000` | `RRGGBB` or `AARRGGBB`; URL-encode `#` if included. |
| `gridWidth` | No | `1` | Grid line width, `0.5`-`32` px. |
| `coordinates` | No | `false` | Adds column/row labels. |
| `scale` | No | `false` | Adds measurements; cannot combine with `coordinates`. |

Labels add top/left margins, so returned PNG dimensions may be larger than the raw screen.

## Batch Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/batch` | List saved batch tasks. |
| POST | `/api/batch` | Create a saved batch task. |
| GET | `/api/batch/<id>` | Get one saved task. |
| PUT | `/api/batch/<id>` | Replace one saved task. |
| DELETE | `/api/batch/<id>` | Delete one saved task. |
| POST | `/api/batch/<id>/run` | Start a saved task run. |
| POST | `/api/batch/run` | Start an inline unsaved task run. |
| GET | `/api/batch/status` | Current runner state and progress. |
| GET | `/api/batch/history` | List run history entries. |
| GET | `/api/batch/history/<runId>` | Get one run history entry. |
| DELETE | `/api/batch/history/<runId>` | Delete one history entry and screenshots. |
| DELETE | `/api/batch/history` | Delete all history entries and screenshots. |
| GET | `/api/batch/history/<runId>/screenshots/<screenshotId>` | Download one run screenshot PNG. |
| GET | `/api/batch/history/<runId>/export` | Export all screenshots from a run as zip. |

Only one batch task can run at a time; concurrent starts return `409`.

### Batch Task Shape

```json
{
  "name": "Open Google News and scroll",
  "variables": { "packageName": "com.google.android.apps.magazines" },
  "steps": [
    { "type": "open_app", "params": { "packageName": "{{packageName}}" }, "delayAfterMs": 2500 },
    { "type": "swipe", "params": { "startX": 540, "startY": 1900, "endX": 540, "endY": 650, "duration": 700 } }
  ]
}
```

Step fields: `type`, `params`, optional `repeat`, optional `delayAfterMs`, optional `continueOnError`, and optional `children` for `loop` steps.

Common step types: `tap`, `long_press`, `swipe`, `pinch`, `two_finger_swipe`, `rotate`, `screenshot`, `open_app`, `open_intent`, `overlay_show`, `overlay_hide`, `delay`, `set`, and `loop`.

String params can reference variables with `{{name}}`; whole-value references preserve the original JSON type.

Batch runs return `{ "runId": "run_...", "status": "processing" }`. Poll `/api/batch/history/<runId>`. Terminal statuses are `finished`, `failed`, and `aborted`.
