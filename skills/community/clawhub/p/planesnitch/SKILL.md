---
name: planesnitch
description: Self-hosted aircraft monitor — watches one or more named locations for interesting aircraft (military/gov/police via plane-alert-db CSVs, emergency squawks 7500/7600/7700, custom ICAO hex/type lists, low-flyers by altitude, or literally everything) using free online ADS-B APIs (adsb.lol, adsb.fi, airplanes.live, adsb.one) or your own ultrafeeder — no SDR, no antenna, no hardware. Fires alerts to Telegram (with doc8643 aircraft-type photos) and/or webhooks (JSON array + base64 image), per-alert cooldowns, config-file driven (config.yaml), runs in Docker. Use when the user wants to monitor/alert on aircraft near a location, get pinged when a military/government/police plane flies overhead, watch for emergency squawks, or build their own plane-spotting radar without buying hardware.
homepage: https://github.com/psyb0t/docker-planesnitch
user-invocable: true
permissions:
  - "network: outbound HTTPS polling of public ADS-B APIs (adsb.lol/adsb.fi/airplanes.live/adsb.one) or a self-hosted ultrafeeder, plus outbound alert delivery to the Telegram Bot API and/or whatever webhook URL(s) you configure"
  - "shell: docker (run the container); curl (grab config/CSV files, optional Telegram getUpdates lookup)"
  - "filesystem: reads a local config.yaml (locations/coords, Telegram bot tokens, webhook URLs+headers); optionally reads local CSV watchlists and writes/reads a local image cache"
metadata:
  { "openclaw": { "emoji": "🛩️", "requires": { "bins": ["docker"] } } }
---

# 🛩️ planesnitch

Watches your configured locations and snitches the second something worth caring about flies within radius — military jets, government spooks, cops, emergency squawks, sketchy low-flyers, or whatever hex/type list you feed it. Pulls live ADS-B data from free public APIs (or your own ultrafeeder if you run one) — **no SDR, no antenna, no hardware, just a config file.** Alerts go to Telegram and/or a webhook.

For the full config schema, env vars, Docker run/compose, and Telegram bot setup, see [references/setup.md](references/setup.md).

## Security & safety

planesnitch sends data outbound on every poll cycle — know what you're pointing it at:

- **Location coordinates + radius leave your machine** on every poll, sent to whichever ADS-B source(s) you configure (public APIs by default — `adsb.lol`, `adsb.fi`, `airplanes.live`, `adsb.one`). If that's a concern, run your own `ultrafeeder` and point `sources` at it instead of the public endpoints.
- **External transmission on every alert, not just polling.** Every alert fired through a `telegram` notification target sends the matched aircraft's coordinates (`lat`/`lon`), squawk, registration, and (if `attach_image` is left at its default `true`) a doc8643 image to `api.telegram.org`. Every alert fired through a `webhook` notification target `POST`s the same data — plus `image_base64` when `attach_image` is on — to whatever `url` you set. In both cases the location's identity and the aircraft's tracked position leave your host to that third party on every match. Point `notify:` only at Telegram bots/chats and webhook `url`s you run or explicitly trust; treat the notification target list as part of your threat model, not just the ADS-B `sources`.
- **`config.yaml` holds a live Telegram bot token and/or webhook URL + auth headers in plaintext.** Treat it like a secret — don't commit it, don't paste it into chat, mount it read-only (`:ro`).
- **Alert content (aircraft position, squawk, registration, cached image) goes to every notification target you configure.** Only point `notify:` at Telegram chats and webhook endpoints you control. A webhook is an arbitrary outbound POST — vet the URL before adding it.
- **No inbound exposure by default** beyond the health endpoint (`:8080`) — planesnitch doesn't listen for anything else. It's a poll-and-push loop, not a server other things talk to.

## When To Use

- Get pinged the moment a military, government, or police aircraft flies within range of a location you care about.
- Watch for emergency squawks (7500 hijack / 7600 radio failure / 7700 general emergency) near an airport, home, or anywhere else.
- Track specific aircraft by ICAO hex (a plane you're curious about) or by type (any A400M, any C-17, any Rafale).
- Get alerted on anything buzzing low overhead (altitude-filtered proximity watch).
- Monitor multiple locations at once — home, office, grandma's house, wherever — each with its own radius and its own alert rules.
- Feed aircraft alerts into your own systems via webhook (Home Assistant, a Discord relay, whatever).

## When NOT To Use

- You want raw ADS-B reception off your own antenna — planesnitch is a *consumer* of ADS-B data, not a receiver. Run `ultrafeeder`/`dump1090` separately and point a `ultrafeeder` source at it if you want that.
- You need historical flight-track playback or analytics — this is a live watch-and-alert tool, not a flight database.
- You need sub-second latency — it polls on an interval (`poll_interval`, default `15s`), not a live stream.

## Config Walkthrough

Everything lives in one `config.yaml`. Five sections: locations, sources, watchlists, alerts, notifications.

**`display_units`** — how altitude/distance/speed render in alerts and webhook payloads. `aviation` (ft/nm/kts, default), `metric` (m/km/km·h), `imperial` (ft/mi/mph).

**`locations`** — named points with `lat`, `lon`, `radius`, optional `name` (falls back to the key). Distance/altitude values accept unit suffixes (`km`, `mi`, `nm`, `ft`, `m`) — `radius: 150km`, `radius: 50nm` both work. Plain numbers default to km (distance) / ft (altitude).

**`sources`** — where the ADS-B data comes from. Public APIs (`adsb_lol`, `adsb_fi`, `airplanes_live`, `adsb_one` — no config needed) or your own `ultrafeeder` (needs a `url`). Multiple sources fetch in parallel and dedupe by ICAO hex, keeping whichever entry has the most fields. `adsb_fi`/`airplanes_live`/`adsb_one` return enriched data (name, operator, year); `adsb_lol`/`ultrafeeder` are raw-fields-only.

**`watchlists`** — what to look for. Six types: `all` (everything in radius), `squawk` (transponder codes), `icao` (specific hex addresses), `icao_type` (ICAO type designators like `C17`/`B738`), `icao_csv` (hex list from a CSV file in `csv/` — see [plane-alert-db](https://github.com/sdr-enthusiasts/plane-alert-db)), `proximity` (altitude-filtered — the "low flyer" watch). All types still respect the location's radius regardless of type.

**`alerts`** — wires watchlists to notification targets. Optional `locations` filter (omit = all locations checked). `cooldown` (durations: `5m`, `1h30m`, `90s`, or plain seconds) stops the same aircraft from re-triggering the alert for a while.

**`notifications`** — `telegram` (`bot_token` + `chat_id`) or `webhook` (`url` + optional `headers`). Both support `attach_image: false` to skip the doc8643 aircraft-type photo (default `true`) — Telegram gets it as a photo attachment, webhooks get it as `image_base64` in the JSON payload. **Every alert sends location coordinates and aircraft tracking data off-host** — `telegram` targets to `api.telegram.org`, `webhook` targets to whatever `url` you set (see Security & safety above). Only add notification targets pointing at Telegram bots/chats and webhook endpoints you control or trust.

### Example config

```yaml
poll_interval: 1m
display_units: aviation

locations:
  home:
    name: "Home"
    lat: 38.8719
    lon: -77.0563
    radius: 150km

sources:
  - type: adsb_lol
  - type: adsb_fi
  - type: airplanes_live
  - type: adsb_one

watchlists:
  emergencies:
    type: squawk
    values: ["7500", "7600", "7700", "7400", "7777"]

  military:
    type: icao_csv
    source: plane-alert-mil.csv

  government:
    type: icao_csv
    source: plane-alert-gov.csv

  low_flyers:
    type: proximity
    min_altitude: 0ft
    max_altitude: 3000ft

alerts:
  - name: "Emergency Alert"
    watchlists: [emergencies]
    cooldown: 1m
    notify: [tg_main, my_webhook]

  - name: "Military Spotter"
    watchlists: [military, government]
    cooldown: 5m
    notify: [tg_main]

notifications:
  tg_main:
    type: telegram
    bot_token: "123456:ABC-DEF"
    chat_id: "-100123456789"

  my_webhook:
    type: webhook
    url: "https://example.com/hook"
    headers:
      Authorization: "Bearer xxx"
```

CSV watchlists (`icao_csv` type) need the matching file under `csv/` — military/government/police/civilian/PIA/everything lists are pulled from [plane-alert-db](https://github.com/sdr-enthusiasts/plane-alert-db), 15,000+ aircraft catalogued by the plane-spotting community. See [references/setup.md](references/setup.md) for the download commands and the full CSV list.

## How To Run

```bash
# grab the example config and edit it — locations, sources, watchlists, alerts, notifications
curl -sL \
  https://raw.githubusercontent.com/psyb0t/docker-planesnitch/main/config.yaml.example \
  -o config.yaml

# minimal run — no CSV watchlists, no persistent image cache
docker run \
  -v ./config.yaml:/app/config.yaml:ro \
  psyb0t/planesnitch

# with CSV watchlists (military/gov/police lists) + persistent image cache
docker run \
  -v ./config.yaml:/app/config.yaml:ro \
  -v ./csv:/csv:ro \
  -v ./images:/images \
  psyb0t/planesnitch
```

A health endpoint runs on `:8080`; the image ships a built-in Docker healthcheck against it.

Full config field reference, env var table, Docker compose, and Telegram bot-token setup: [references/setup.md](references/setup.md).
