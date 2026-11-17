# planesnitch setup

## Requirements

- Docker
- A config file (`config.yaml`) — nothing else. No SDR, no antenna, no hardware.
- A Telegram bot token (if using Telegram alerts) or a webhook endpoint you control (if using webhook alerts) — at least one notification target.

## Quick Install

```bash
# grab the example config
curl -sL \
  https://raw.githubusercontent.com/psyb0t/docker-planesnitch/main/config.yaml.example \
  -o config.yaml

# edit config.yaml: locations, sources, watchlists, alerts, notifications

# run — without CSV watchlists
docker run \
  -v ./config.yaml:/app/config.yaml:ro \
  psyb0t/planesnitch

# run — with CSV watchlists (military/gov/police tracking)
mkdir -p csv
BASE=https://raw.githubusercontent.com/sdr-enthusiasts/plane-alert-db/main
curl -sLo csv/plane-alert-mil.csv $BASE/plane-alert-mil.csv
curl -sLo csv/plane-alert-gov.csv $BASE/plane-alert-gov.csv
curl -sLo csv/plane-alert-pol.csv $BASE/plane-alert-pol.csv

docker run \
  -v ./config.yaml:/app/config.yaml:ro \
  -v ./csv:/csv:ro \
  psyb0t/planesnitch

# full setup — CSV watchlists + persistent aircraft-type image cache
docker run \
  -v ./config.yaml:/app/config.yaml:ro \
  -v ./csv:/csv:ro \
  -v ./images:/images \
  psyb0t/planesnitch
```

**Verify:** logs show `planesnitch starting`, `health endpoint listening on :8080`, and one `watchlist <name>: N aircraft loaded` line per `icao_csv` watchlist. Then `fetched N aircraft` lines start showing up every poll cycle.

## Docker Compose

```yaml
services:
  planesnitch:
    image: psyb0t/planesnitch
    restart: unless-stopped
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - ./csv:/csv:ro
      - ./images:/images
    ports:
      - "127.0.0.1:8080:8080"   # health endpoint, loopback-only
```

## Full Config Schema (`config.yaml`)

Top level:

| Field | Default | Description |
|---|---|---|
| `poll_interval` | `15s` | How often to fetch aircraft data and re-check watchlists. Accepts `s`/`m`/`h` durations or plain seconds. |
| `display_units` | `aviation` | Unit preset for altitude/distance/speed in alerts + webhook payloads. See table below. |
| `locations` | — | Map of named locations to watch. Required, at least one. |
| `sources` | — | List of ADS-B data sources to poll. Required, at least one. |
| `watchlists` | — | Map of named watchlists (what to match on). Required, at least one. |
| `alerts` | — | List of rules wiring watchlists to notification targets. Required, at least one. |
| `notifications` | — | Map of named notification targets (Telegram / webhook). Required, at least one. |

### Display units

```yaml
display_units: aviation  # aviation (default), metric, or imperial
```

| Preset | Altitude | Distance | Speed |
|---|---|---|---|
| `aviation` | ft | nm | kts |
| `metric` | m | km | km/h |
| `imperial` | ft | mi | mph |

### Locations

```yaml
locations:
  home:
    name: "Home"          # optional — pretty display name; falls back to the map key
    lat: 38.8719
    lon: -77.0563
    radius: 150km
  area51:
    name: "Area 51"
    lat: 37.2350
    lon: -115.8111
    radius: 50nm
```

| Field | Required | Description |
|---|---|---|
| `name` | no | Display name used in alerts. Falls back to the location's map key. |
| `lat` | yes | Latitude, decimal degrees. |
| `lon` | yes | Longitude, decimal degrees. |
| `radius` | yes | Search radius around the point. Accepts unit suffix (`km`, `mi`, `nm`) — plain numbers default to km. |

Any distance/altitude value anywhere in the config accepts a unit suffix (`km`, `mi`, `nm`, `ft`, `m`) — they all convert internally. Plain numbers without a suffix default to km for distances, ft for altitudes.

### Sources

```yaml
sources:
  - type: adsb_lol
  - type: adsb_fi
  - type: airplanes_live
  - type: adsb_one
  - type: ultrafeeder
    url: http://ultrafeeder:80/tar1090/data/aircraft.json
```

| Type | Config | Data richness |
|---|---|---|
| `adsb_lol` | none | Raw ADS-B fields only |
| `adsb_fi` | none | Enriched (name, owner/operator, year) |
| `airplanes_live` | none | Enriched (name, owner/operator, year) |
| `adsb_one` | none | Enriched (name, owner/operator, year) |
| `ultrafeeder` | `url` (required) | Raw ADS-B fields only |

Multiple sources fetch in parallel per location and dedupe by ICAO hex — the entry with the most fields wins when the same aircraft is seen by more than one source.

### Watchlists

```yaml
watchlists:
  emergencies:
    type: squawk
    values: ["7500", "7600", "7700"]

  military:
    type: icao_csv
    source: plane-alert-mil.csv

  my_planes:
    type: icao
    values: ["4ca123", "a12345"]

  cool_jets:
    type: icao_type
    values: ["A400", "RFAL", "AJET"]

  everything:
    type: all

  low_flyers:
    type: proximity
    min_altitude: 0ft
    max_altitude: 3000ft
```

| Type | Matches on | Config fields | Source |
|---|---|---|---|
| `all` | Every aircraft in radius | none | Location radius |
| `squawk` | Transponder squawk code | `values` (list of squawk codes) | Inline list |
| `icao` | ICAO hex address | `values` (list of hex strings) | Inline list |
| `icao_type` | ICAO type designator ([doc 8643](https://www.icao.int/publications/DOC8643/Pages/Search.aspx)) — e.g. `C17`, `B738` | `values` (list of type codes) | Inline list |
| `icao_csv` | ICAO hex, loaded from a CSV | `source` (CSV filename under `csv/`) | Local file, [plane-alert-db](https://github.com/sdr-enthusiasts/plane-alert-db) format |
| `proximity` | Altitude window | `min_altitude`, `max_altitude` | Location radius + altitude limits |

All watchlist types respect the owning location's `radius` regardless of type — an aircraft outside the radius never matches, no matter what watchlist rule it would otherwise trip.

### Alerts

```yaml
alerts:
  - name: "Emergency Alert"
    watchlists: [emergencies]
    cooldown: 1m
    notify: [tg_emergencies, my_webhook]

  - name: "Military Spotter"
    watchlists: [military, government]
    cooldown: 5m
    notify: [tg_spotting]

  - name: "Everything at Home"
    locations: [home]           # optional — omit to check all locations
    watchlists: [everything]
    cooldown: 1m
    notify: [tg_main]
```

| Field | Required | Description |
|---|---|---|
| `name` | yes | Display name for the alert, used in Telegram/webhook payloads. |
| `watchlists` | yes | List of watchlist names this rule checks. |
| `locations` | no | List of location names to restrict this rule to. Omit = every configured location is checked. |
| `cooldown` | yes | Suppresses repeat alerts for the same aircraft. Durations: `5m`, `1h30m`, `90s`, or plain seconds. |
| `notify` | yes | List of notification target names (keys from the `notifications` map) to fire. |

### Notifications

**External transmission.** Every alert sends the matched aircraft's coordinates (`lat`/`lon`), squawk, registration, and other tracking metadata — plus a cached doc8643 image when `attach_image` is left at its default `true` — to the notification targets below. `telegram` targets deliver via `api.telegram.org`; `webhook` targets `POST` a JSON payload (including `image_base64` when image attachment is on) to whatever `url` you configure. That data leaves your host to those third parties on every match. Only configure `bot_token`/`chat_id` pairs and webhook `url`s you control or explicitly trust — see [SKILL.md Security & safety](../SKILL.md#security--safety).

**Telegram:**

```yaml
notifications:
  tg_emergencies:
    type: telegram
    bot_token: "123456:ABC-DEF"
    chat_id: "-100123456789"
    # attach_image: false   # text-only, skip the doc8643 photo (default: true)
```

| Field | Required | Default | Description |
|---|---|---|---|
| `type` | yes | — | `telegram` |
| `bot_token` | yes | — | Bot token from @BotFather. |
| `chat_id` | yes | — | Target chat/channel ID. |
| `attach_image` | no | `true` | When `true` and the aircraft has a resolvable ICAO type, sends the doc8643 image as a photo (caption = alert text). Set `false` for text-only alerts. |

**Webhook:**

```yaml
notifications:
  my_webhook:
    type: webhook
    url: "https://example.com/hook"
    headers:
      Authorization: "Bearer xxx"
    # attach_image: false   # omit base64 photo from payload (default: true)
```

| Field | Required | Default | Description |
|---|---|---|---|
| `type` | yes | — | `webhook` |
| `url` | yes | — | POST target. |
| `headers` | no | — | Map of extra headers sent with every request (auth, etc). |
| `attach_image` | no | `true` | When `true` and resolvable, embeds the doc8643 image as base64 in `image_base64`. Set `false` to cut payload size / avoid the doc8643 fetch. |

If every notification target attached to an alert has `attach_image: false`, planesnitch skips the doc8643 fetch entirely for that alert (no wasted bandwidth/disk).

Webhook delivery is a JSON array POST per poll cycle, even for a single alert:

```json
[
  {
    "alert": "Military Spotter",
    "location": "Home",
    "match": {
      "reason": "icao_csv_match",
      "watchlist": "military",
      "info": { "Registration": "94-0067", "Operator": "USAF", "Type": "BOEING C-17A Globemaster III" }
    },
    "units": { "altitude": "ft", "distance": "nm", "speed": "kts" },
    "image_base64": "/9j/4AAQSkZJRgABAQ...",
    "aircraft": {
      "hex": "ae07e1", "flight": "TEDDY64", "registration": "94-0067",
      "type": "C17", "description": "BOEING C-17A Globemaster III",
      "owner_operator": "USAF", "year": "1994", "squawk": "1613",
      "emergency": "none", "altitude": 12350, "lat": 37.9306, "lon": -78.7019,
      "speed": 413, "track": 245.3, "distance": 98.9
    }
  }
]
```

`match` shape varies by watchlist type:

| Watchlist type | Match fields |
|---|---|
| `squawk` | `{"reason": "squawk", "watchlist": "...", "squawk": "7700", "distance_km": 12.3}` |
| `icao` | `{"reason": "icao_match", "watchlist": "...", "distance_km": 12.3}` |
| `icao_type` | `{"reason": "icao_type_match", "watchlist": "...", "type": "C17", "distance_km": 12.3}` |
| `icao_csv` | `{"reason": "icao_csv_match", "watchlist": "...", "info": {...}, "distance_km": 12.3}` |
| `all` | `{"reason": "all", "watchlist": "...", "distance_km": 12.3}` |
| `proximity` | `{"reason": "proximity", "watchlist": "...", "distance_km": 12.3}` |

`image_base64` is `null` when no image is cached / `attach_image: false`.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `LOG_LEVEL` | `INFO` | Set to `DEBUG` for verbose output. |
| `PLANESNITCH_CONFIG` | `config.yaml` | Path to config file. |
| `PLANESNITCH_CSV_DIR` | `/csv` | Path to CSV watchlist files. |
| `PLANESNITCH_IMAGES_DIR` | `/images` | Path to cached doc8643 aircraft-type images. |

## Telegram Bot Setup

1. Message [@BotFather](https://t.me/BotFather), send `/newbot`, get a token — that's `bot_token`.
2. **Personal alerts:** send your bot a message first, then check `https://api.telegram.org/bot<TOKEN>/getUpdates` — your `chat_id` is in there.
3. **Channel alerts:** add the bot as admin on the channel, post something, then check `getUpdates` for the channel ID (starts with `-100`).

Multiple Telegram notification targets can use the same `bot_token` with different `chat_id`s to route different alerts to different chats/channels.

## Plane-Alert-DB CSV Lists

`icao_csv` watchlists read from [sdr-enthusiasts/plane-alert-db](https://github.com/sdr-enthusiasts/plane-alert-db) — 15,000+ community-catalogued aircraft.

| List | Count | File |
|---|---|---|
| Military | 8,709 | `plane-alert-mil.csv` |
| Government | 1,743 | `plane-alert-gov.csv` |
| Police | 932 | `plane-alert-pol.csv` |
| Civilian | 4,530 | `plane-alert-civ.csv` |
| Privacy (PIA) | 94 | `plane-alert-pia.csv` |
| Everything | 15,914 | `plane-alert-db.csv` |

```bash
mkdir -p csv
BASE=https://raw.githubusercontent.com/sdr-enthusiasts/plane-alert-db/main
curl -sLo csv/plane-alert-mil.csv $BASE/plane-alert-mil.csv
curl -sLo csv/plane-alert-gov.csv $BASE/plane-alert-gov.csv
curl -sLo csv/plane-alert-pol.csv $BASE/plane-alert-pol.csv
curl -sLo csv/plane-alert-civ.csv $BASE/plane-alert-civ.csv
curl -sLo csv/plane-alert-pia.csv $BASE/plane-alert-pia.csv
curl -sLo csv/plane-alert-db.csv  $BASE/plane-alert-db.csv
```

`plane-alert-db.csv` contains everything (mil + gov + pol + civ + pia) in one file — use it alone if you want to watch all 15,000+ aircraft and skip the individual lists. Re-download anytime for fresh data, or write your own CSV — it just needs an ICAO hex column first.

## Ports

| Port | Service |
|---|---|
| 8080 | Health endpoint. The Docker image ships a built-in healthcheck against it. |

No other inbound ports — planesnitch only makes outbound requests (ADS-B source polling, Telegram/webhook delivery).

## Volumes

| Container path | Purpose | Persist? |
|---|---|---|
| `/app/config.yaml` | Config file. Mount `:ro`. | Required, host file |
| `/csv` | CSV watchlist files (`icao_csv` type). Mount `:ro`. | Only needed if using `icao_csv` watchlists |
| `/images` | Cached doc8643 aircraft-type images. | Optional — persists the image cache across restarts; without it, images re-download every restart |

## Image Cache

When an aircraft has a resolvable ICAO type designator and at least one notify target has `attach_image: true` (the default), planesnitch fetches the matching image from [doc8643.com](https://doc8643.com) and caches it under `/images`. Misses are recorded as `.notfound` markers so types without an image aren't re-fetched every time. The cache never expires on its own — delete the mounted `images/` dir on the host to force a refresh.
