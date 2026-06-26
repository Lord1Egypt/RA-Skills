# Mensa

An OpenClaw skill that returns the daily lunch menu of a German university canteen — student prices, vegan/vegetarian tags, no API key, stdlib only.

## Quickstart

```bash
# 1. Install
clawhub install mensa

# 2. Pick your city + canteen (one-time)
python3 ~/.openclaw/workspace/skills/mensa/mensa_today.py --setup "<your-city>"

# 3. Ask your OpenClaw agent
```

> What's on the menu at the Mensa today?

That's it.

## Talking to it in chat

Once configured, the agent dispatches to this skill whenever you ask about today's (or another day's) canteen menu. Examples:

> What's for lunch at the Mensa today?

> Show me tomorrow's Mensa menu.

> Mensaplan heute.

The reply lists dishes with student prices and tags vegan/vegetarian items:

```
2026-05-26 - Menu (student price)
- Spaghetti Bolognese - 2.80 EUR
- Couscous - 2.60 EUR (vegetarian)
- Soup - 1.80 EUR (vegan)
```

## First-run setup

The agent will ask for your city, list all canteens OpenMensa knows in that city, and let you pick one as the default. Under the hood that's two CLI calls:

```bash
# 1. Preview the canteens in a city (no config written)
python3 ~/.openclaw/workspace/skills/mensa/mensa_today.py --list "Magdeburg"

# 2. Save the config with your chosen default (substring match)
python3 ~/.openclaw/workspace/skills/mensa/mensa_today.py --setup "Magdeburg" --default "UniCampus"
```

`--setup` saves **every canteen in that city** as an alias; the `--default` substring picks which one is used when you don't name a canteen. Without `--default`, the first canteen returned by OpenMensa is used. The result is cached in a local `config.json` next to the script and is never sent anywhere.

```
Searching canteens in 'Magdeburg' via OpenMensa...
Saved 3 canteen(s) for Magdeburg. Default: Mensa UniCampus (id=109).
All canteens in this city are now queryable by name substring.
```

Re-run `--setup` any time to switch city.

## CLI usage (advanced / debugging)

The script can be called directly. Useful for testing without going through the agent:

```bash
# Today's menu for the default canteen
python3 ~/.openclaw/workspace/skills/mensa/mensa_today.py

# Any canteen in your configured city by name substring
python3 ~/.openclaw/workspace/skills/mensa/mensa_today.py "UniCampus"
python3 ~/.openclaw/workspace/skills/mensa/mensa_today.py "Herrenkrug"

# A different date
python3 ~/.openclaw/workspace/skills/mensa/mensa_today.py --date 2026-06-01
```

Substring matching is **normalised** — `-`, `,`, `.` are treated as spaces, so a query like *"Otto Hahn"* matches a canteen named *"Mensa Otto-Hahn-Straße"*.

Vegan/vegetarian tags are derived heuristically from the meal's `notes` array — OpenMensa does not expose dedicated flags, so detection depends on the canteen labelling its dishes.

Side dishes (any meal whose `category` contains "Beilage") and leftover items (any meal whose name contains "Restproduktion") are filtered out before the menu is printed, so only main dishes are shown.

## Upgrading from 0.1.x

1.1.0 renames the skill from `mensa-today` to `mensa`, adds a `--list` preview step before setup, and filters Beilagen/Restproduktion out of the printed menu. After updating, delete the old `config.json` and re-run setup so the new alias map is written.

## Network egress

Outbound HTTPS to `openmensa.org` only. No credentials, no telemetry, no user data sent. Your city and canteen choice stay in `config.json` on your machine.

| URL                                                  | Method | Data sent |
|------------------------------------------------------|--------|-----------|
| `https://openmensa.org/api/v2/canteens?page=N`       | GET    | none      |
| `https://openmensa.org/api/v2/canteens/{id}/days/{date}/meals` | GET | none |

A `User-Agent: mensa-openclaw-skill/1.1.0` header is sent with every request so OpenMensa can identify and contact this client if needed.

## Trust

By using this skill, your requests go to **openmensa.org** (a community-run open data project). Install only if you trust that service to receive your canteen and date lookups.

## Attribution

Menu data comes from the community project [OpenMensa](https://openmensa.org). This skill is not affiliated with OpenMensa.

## License

MIT-0 (MIT No Attribution) — see [LICENSE.md](LICENSE.md). Use freely in any project, attribution not required.
