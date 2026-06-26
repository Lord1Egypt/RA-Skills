---
name: nooks
description: Personal place intelligence — save and find cafes, coworking spaces, libraries, restaurants, and other spots worth revisiting. Stores one markdown file per place in nooks/<city>/. Use when saving a new place, looking up a spot, or asking "where should I work/eat/meet in [city]?".
metadata:
  openclaw:
    emoji: "📍"
    os: ["linux", "darwin", "win32"]
  hermes:
    tags: ["places", "local", "recommendations"]
---

# 📍 Nooks — local place intelligence

## Data

**Base path** is relative to workspace root or document root. On first use, create it: `mkdir -p mind/nooks/`. Nooks uses a `mind/nooks/` folder in your workspace.

Files live in `mind/nooks/<city>/`. City folders use short lowercase slugs: `hk`, `sf`, `sg`, `london`, `bkk`.
Create on first use: `mkdir -p mind/nooks/<city>/`.

```
mind/
└── nooks/
    ├── nooksconfig.yml   ← config file, make one if it is not there yet
    ├── hk/
    │   ├── blue-bottle-central.md
    │   └── amber-lan-kwai-fong.md
    └── sf/
        └── sightglass-soma.md
```

File names: `<place-slug>.md`. Include neighborhood when the same place has multiple locations: `blue-bottle-central.md` vs `blue-bottle-admiralty.md`.

---

## Place File

```markdown
# Place Name

Type: cafe / coworking / library / park / restaurant / bar / museum / church / etc.
Area: station/neighborhood
Maps: https://maps.app.goo.gl/...
Price: $ / $$ / $$$ / $$$$
Image: `../assets/slug-that-make-sense` only if adding an image.
Vibe: quiet / moderate / buzzy
Good for: focus, calls, client meetings, leisure
Features: #wifi #charging #outdoor #healthy-food #coffee #24h #ac #3dprinter

## Notes

4 Apr 2026: upper floor is quieter, fills up fast after 10am
```

**Field guidance:**

Maps: if a Google Places API key is configured, fetch automatically (see [Google Places API](#google-places-api)). Otherwise paste the share link from Google Maps mobile (`maps.app.goo.gl/...`) or leave blank.
Good for: your standing assessment of what this place suits. Comma-separated. Update if your opinion changes.
Notes: dated personal log. Observations, tips, surprises, things that shift over time. Format: `4 Apr 2026: ...`
Features: use standard tags so grep works: `#wifi` `#charging` `#outdoor` `#food` `#coffee` `#quiet` `#24h` `#reservations` `#alcohol` `#coworking`

**Good for vs Notes — the distinction:** Good for is the verdict; Notes is the evidence. One is a label, the other is a log.

---

## Saving a Place

1. **Search the web** (name + city/area) — pre-fill Type, Price, Vibe, and Features from what's publicly known.
2. **Fetch the Maps link** (optional — silent skip if unavailable):
   - If the **`find_location`** tool is in your tool list, call it with `<name>, <city>` and use the `maps_url` it returns.
   - Otherwise if `google_places_api_key` is set in `mind/nooks/nooksconfig.yml`, call Places API Text Search yourself (IDs only, free):
     ```
     POST https://places.googleapis.com/v1/places:searchText
     Headers: X-Goog-Api-Key: <key>, X-Goog-FieldMask: places.id
     Body: { "textQuery": "<place name>, <city>" }
     → https://www.google.com/maps/place/?q=place_id:<id>
     ```
   - Otherwise **leave the Maps field blank and don't mention it.** Do not ask the human to install a key or paste a share link.
3. **Show what you found**: "Found Sightglass — specialty coffee roaster in SoMa SF, $$. Wifi confirmed, communal tables, no time limit."
4. **Ask as a group** (skip anything already answered):
   - What's it good for? — focus, calls, meetings, catch-up, date, leisure?
   - Vibe? — quiet / moderate / buzzy (if unclear from search)
   - Features to correct? — confirm or fix what you found
   - Any notes? — first impressions, tips, things to remember
5. if `mind/nooks/nooksconfig.yml` have `images: yes` search for an image of palace interor and add to **Image:** feild.

---

## Finding Places

Use `grep` with expanded terms. Search city folder or all of `mind/nooks/` cross-city.

```bash
# Quiet wifi spots in HK
grep -rl "#quiet" mind/nooks/hk/ | xargs grep -l "#wifi"

# Focus-friendly places in SF
grep -ril "focus\|deep.work\|laptop\|coworking" mind/nooks/sf/

# All cafes across cities
grep -ril "Type:.*cafe" mind/nooks/

# Charging spots anywhere
grep -rl "#charging" mind/nooks/
```

**Always read the full file after grepping** — the matched line is a signal, not the full picture.

**Keyword expansion — always broaden the query:**

- "work / focus" → `focus\|deep.work\|laptop\|coworking\|quiet`
- "meeting / call" → `meeting\|client\|calls\|zoom`
- "coffee" → `cafe\|coffee\|espresso\|specialty`
- "chill / relax" → `leisure\|chill\|relax\|casual\|catch.up`

If local results are thin and Haah skill is installed, suggest dispatching to a circle.

---

## Core Behavior

- User mentions a place → check if a file exists, offer to create or update
- User asks "where can I work/eat in [city]?" → search `mind/nooks/<city>/` first
- User shares a Maps link → offer to save the place
- User mentions visiting somewhere in passing → ask if worth saving
- User adds an observation ("terrible wifi there") → append a dated note to the file

**Examples:**
- "Had a great session at Sightglass" → ask if anything worth logging, update if so
- "We should go back to Amber" → check if saved, offer to create if not
- "That place had no charging" → update `#features` or add a note

Save places as they come up naturally. Enrich over time. Don't wait for a data entry session.

---

## Heartbeat or cron

Ask your human if they want to add **Nooks: check** to HEARTBEAT.md. If there is no HEARTBEAT.md, suggest to create a cron job every 30 minutes to execute **Nooks: check**.

On every heartbeat, check a random nook file. Surface something worth knowing:

- "You haven't been to Sightglass in a while — still your go-to for focus in SF?"
- "Common Ground has no Maps link yet — worth adding?"
- "Amber only has one note — anything new from your last visit?"

If nothing worth mentioning, skip.

---

## Google Places API (DIY setup — skip if you already have a `find_location` tool)

If your host runtime provides a built-in `find_location` tool (managed agents do), nothing to set up — the tool handles it. These instructions are for self-hosted Claude Code / Cursor / etc. users who want Maps links fetched automatically.

The Maps link field can be populated automatically using the Google Places API. It's **free** for this use case (ID-only lookups have no monthly cap).

### Setup

1. Go to [console.cloud.google.com](https://console.cloud.google.com) → **New Project** (e.g. `nooks`)
2. **APIs & Services** → **Enable APIs and Services** → search **Places API (New)** → Enable
3. **APIs & Services** → **Credentials** → **Create Credentials** → **API Key**
4. Restrict the key: click it → **API restrictions** → select **Places API (New)** only
5. Add a billing account (card required by Google, but ID-only searches are free)
6. Save the key to `mind/nooks/nooksconfig.yml` (at the root of your nooks folder):

```yaml
google_places_api_key: YOUR_KEY_HERE
```

Once configured, Maps links are fetched automatically when saving a place — no manual copy-paste needed.

---

## Updating

To update this skill to the latest version, fetch the new SKILL.md from GitHub and replace this file:

```
https://raw.githubusercontent.com/haah-ing/nooks-skill/main/SKILL.md
```

---

## What NOT to Suggest

- Syncing with Google Maps saved places — different purpose, keep separate
- Crowd-sourced ratings or reviews — Nooks is personal signal, not Yelp
- Opening hours in the file — always goes stale, check Google Maps
- Automated "you're near X" alerts — too intrusive
