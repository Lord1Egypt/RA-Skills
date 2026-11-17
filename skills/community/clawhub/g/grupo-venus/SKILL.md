---
name: grupo-venus
description: Natal charts, transit forecasts and, with a ticket, written reports from the third-party site grupovenus.com. Use for Grupo Venus or carta astral readings.
user-invocable: true
metadata: {"openclaw":{"emoji":"♀","homepage":"https://github.com/apresmoi/grupo-venus","requires":{"bins":["node"]},"envVars":[{"name":"GRUPO_VENUS_HOME","required":false,"description":"Folder for the people file, cache and ticket. Default: ~/.grupo-venus"},{"name":"GRUPO_VENUS_TICKET","required":false,"description":"Optional grupovenus.com ticket, sent only to grupovenus.com. Overrides the stored one."}]}}
---

# Grupo Venus

Use this skill to fetch free natal charts, transit forecasts, and transit interpretations from **grupovenus.com**, store people across sessions, and read their charts conversationally. Users with a grupovenus.com ticket can also read and create its written reports (see Paid Reports).

> **Unofficial skill.** Not affiliated with or endorsed by Grupo Venus. Uses the public free tier of grupovenus.com as-is.

All work goes through one bundled helper, [scripts/gv.mjs](scripts/gv.mjs) (Node.js 18+, built-in modules only, readable source). In the commands below, `gv` means `node "{baseDir}/scripts/gv.mjs"`, where `{baseDir}` is the folder holding this file. Any working directory works. Its only other file is the time zone table [data/zone.tab](data/zone.tab), plain text from the IANA time zone database.

## Privacy and consent (hard rules)

Birth data (name, exact birth date and time, place, sex) is personal. Before the first request or the first save for a person:

1. Tell the user, in one or two lines, that their birth data will be sent to **grupovenus.com**, an unofficial third-party astrology site, and that the city name goes to **photon.komoot.io** to find coordinates.
2. Ask whether to **save the person** for later sessions. `gv add` writes nothing to disk unless you pass `--save`, so pass it only on a yes. Without it, use the printed `line` with `--line` on `chart` and `transits`: that person is not added to the people file and their forecasts are not cached. The one thing written is the chart image, as a temporary file in the data folder: delete it once shown. The helper also deletes it on any run after an hour, and `gv forget` removes it.
3. Suggest a first name or alias instead of a full name. The name only labels the chart.
4. Add other people (partners, friends, family) only when the user says they have that person's permission.
5. Load only the person being discussed, not the whole list, unless the user asks for comparisons.

Deleting: `gv remove KEY --yes` deletes one person and their cached charts, forecasts and reports. `gv forget --yes` deletes all people, the cache, the stored ticket and the exports in the data folder (an export written to a path the user chose is theirs to delete). Offer these whenever the user asks about their data, and **confirm with the user before running either**: `--yes` records that confirmation.

Shell safety: pass every user-supplied value as one single-quoted argument (`--city 'São Paulo'`), escaping any single quote inside it. Never paste user text into a command unquoted. The helper itself runs no shell.

## Network and data

- **Hosts contacted:** `grupovenus.com` (charts, forecasts, interpretation texts, reports) and `photon.komoot.io` (city coordinates, only when adding a person from birth data). Nothing else: the helper refuses a redirect to any other host.
- **Data sent:** the person's name, birth date and time, city and coordinates, which are the inputs of the requested report. Numerology also sends the full birth name and, if given, the signature text, for that request only. No API keys. The only credential is an optional grupovenus.com ticket, sent only to grupovenus.com. The ticket status check sends a fixed placeholder person ("X"), never a real one, because the site hides the counters for an empty person list. The environment variables read are the optional `GRUPO_VENUS_HOME` and `GRUPO_VENUS_TICKET`.
- **Data written:** for people saved with consent: the people file, the cache folder and exports, plus the ticket if the user shares one. For an unsaved person: only a temporary chart image, which the next helper run deletes once it is an hour old. It is all in the data folder and readable by the owner only. Interpretation texts in the cache contain no personal data; chart images, forecasts and reports do, and `gv remove` deletes them. Option values are checked against fixed lists, so no option can write outside the data folder. The one exception is `gv export FILE`, which writes the list where the user says.
- **Nothing is installed or executed** besides the bundled [scripts/gv.mjs](scripts/gv.mjs). It downloads no code.

---

## Server etiquette (hard rules)

grupovenus.com is a small server shared with its own users. Be a light client.

- **Every grupovenus.com request goes through `gv`.** Never call the site with curl or any other tool. The helper queues requests (parallel calls wait their turn), pauses 2 seconds between them, and caches the responses for saved people (nothing is cached for an unsaved one).
- **Never run requests in parallel**, and never prefetch "just in case". Fetch only what the current reply needs.
- **Never add people to the site's person list.** People come from an imported list, or from birth data with coordinates from Photon (see Adding People). A report made with a ticket is kept by the site under that ticket (see Paid Reports).
- **Reuse the cache.** Interpretation texts are the same for everyone and are cached forever. Chart images are cached per person. A 1-year forecast is reused for 14 days.

Requests per action, before caching:

| Action | Requests |
|---|---|
| Add or import people | 0 |
| Natal chart image | 1 (then cached) |
| Forecast graph | 1 |
| Interpretation text | 1 per transit and style (then cached forever) |
| Paid: ticket status | 2 |
| Paid: list reports | 1 |
| Paid: read a report | 1 (cached with `--for KEY`) |
| Paid: create a report | 1 to 3, plus one ticket credit |
| Numerology | 1 or 2 |

---

## People Storage

People live in `~/.grupo-venus/grupo-venus.json`, with the cache next to it in `grupo-venus-cache/`. Existing OpenClaw data in `~/.openclaw/workspace/memory/grupo-venus.json` keeps being used where it already exists. Set `GRUPO_VENUS_HOME` to choose another folder. `gv --help` prints the folder in use.

Example record (Luis Alberto Spinetta is the example throughout, because he's from another planet):

```json
{
  "people": {
    "spinetta": {
      "name": "Luis Alberto Spinetta",
      "birthdate": "1/23/1950 4:35:00 PM",
      "city": "Buenos Aires",
      "country": "Argentina",
      "sex": "V",
      "tz_offset": "3",
      "lat_dms": "34S37",
      "lon_dms": "58W23",
      "lat_decimal": -34.6167,
      "lon_decimal": 58.3833,
      "style": "deep"
    }
  }
}
```

- **sex:** `V` = varón (male), `H` = hembra (female). This is the site's own convention.
- **tz_offset:** hours west of UTC: `3` = UTC-3 (Argentina), `-1` = UTC+1 (Madrid). It is the offset in force at the birth date and place, daylight saving time included.
- **lat_dms / lon_dms:** degrees and minutes, `34S37` = 34°37′S, `58W23` = 58°23′W.
- **lat_decimal / lon_decimal:** South is negative, **West is positive** (the server's convention).
- **style:** `casual`, `deep`, or `practical`. See Voice & Style.

Commands: `gv list` shows everyone, `gv style KEY casual|deep|practical` saves a style, `gv remove KEY --yes` deletes a person, `gv forget --yes` deletes everything (after the user confirms).

---

## Adding People

Follow Privacy and consent first. Then offer the import:

> "Do you already have people saved on grupovenus.com? Open https://grupovenus.com/perso2.asp (English: https://grupovenus.com/perso2i.asp), press **Download the list** and attach the file here. Otherwise just tell me the name, birth date, exact birth time, city, country and sex, and I'll add them myself. If you have a grupovenus.com ticket, you can share it and I'll also read those reports."

Mention the ticket only in this one clause, once. See Paid Reports for what to say if the user asks about it.

### Option A: import the downloaded list

```bash
gv import "/path/to/Lista de N Personas.html"
```

The file holds one person per line in the site's own format, already with coordinates and time zone. A pasted copy of those lines saved to a text file imports the same way. Existing people keep their `style`.

### Option B: add from birth data

```bash
gv add --name 'Luis' --date 1950-01-23 --time 16:35 \
  --city 'Buenos Aires' --country 'Argentina' --sex V --key spinetta --save
```

- The city and country are sent to Photon (photon.komoot.io, OpenStreetMap data) for coordinates. The time zone is computed locally from the bundled table. No grupovenus.com request.
- `--save` stores the person. Leave it out when the user did not agree to saving (see Privacy and consent).
- `--time` is local clock time on the birth certificate, 24h.
- The output lists `matches`. **Confirm the matched city with the user** when the name is common ("Córdoba: Argentina or Spain?"). If the first match is wrong, run the same command again with `--pick N`.
- If the birth time is unknown, say the Ascendant and houses will be unreliable, and use 12:00.

### Export for the browser

Why it exists: people saved here can also be opened on grupovenus.com itself, for example to read a full report there. The file holds only the person lines already stored (name, birth date and time, city, country, sex, time zone, coordinates). It is written locally and sends nothing.

```bash
gv export
```

The file goes to the `exports/` folder inside the data folder, where `gv forget` also deletes it. A path given as argument is outside that cleanup; say so.

This writes the same list format the site downloads. Opening it and pressing **Modificar** loads everyone into the user's browser on grupovenus.com. It replaces the list saved in that browser, so tell the user before they press it and suggest downloading their current list first as a backup.

---

## Natal Chart Image

```bash
gv chart spinetta            # prints the PNG path
gv chart spinetta --lang I --zodiac S2
```

`--lang`: `E` Spanish (default), `I` English, `F` French. `--zodiac`: see Zodiac Types.

---

## Transit Forecast

```bash
gv transits spinetta                 # 1 year, Saturn to Pluto, from today
gv transits spinetta --report=-1     # 3 days, Moon to Jupiter
gv transits spinetta --top 5
```

Output is JSON, transits sorted by peak intensity:

```json
{"code": "PLUOPOASC", "peak_height": 50, "peak_date": "2027-01-26", "peak_orb": "0°0'",
 "intensity": 0.91, "windows": [{"from": "2026-12-25", "to": "2027-02-27", "retro": false},
                                {"from": "2027-07-23", "to": "2027-10-31", "retro": true}]}
```

- `peak_height` is the bar height on the site's graph, the intensity proxy (`intensity = height / 55`).
- `windows` are the active periods. A transit that returns by retrograde motion shows several windows.
- Forecasts must start today or later. Past start dates need a ticket; the helper says so.

### Free forecast reports

| `--report=` | Server label | Transiting planets | Period |
|---|---|---|---|
| `8` (default) | `1 año Sat-Plu` | SAT, URA, NEP, PLU | 1 year |
| `-1` | `3 días Lun-Júp` | LUN, SOL, JUP | 3 days |
| `0` | `1 semana Luna,Sol-Júp` | LUN, SOL, JUP | 1 week |
| `1` | `2 semanas Sol-Plu` | SOL, MAR, JUP, SAT, URA, NEP, PLU | 2 weeks |

`8` is the richest free dataset: every transit of the 4 outer planets to the natal planets, Ascendant and Midheaven, with orbs every 2 days for a full year. Ticket-only forecasts (`7`, `6`, `4`, ...) go through `gv make`, see Paid Reports.

---

## Paid Reports (ticket)

A grupovenus.com ticket (the code in `info.asp?tic=CODE`) gives access to the written reports. Use this section only when the user shares a ticket or asks about one.

### Neutrality (hard rules)

This skill is independent and has no stake in whether anyone buys a ticket.

- The onboarding clause in Adding People is the only time you bring up the ticket. Never raise it again unless the user does.
- If the user asks what a ticket adds, answer plainly and factually, without recommending it:
  > "Without a ticket: natal chart image, 1-year outer-planet forecast, short-range forecasts, transit interpretations and numerology. With a ticket you can also get the written reports (natal, vocational, karmic and others), solar and lunar returns, progressions, and forecasts for longer periods or past dates."
- No persuasive wording ("unlock", "premium", "full potential", "go deeper with"), no prices, no links to purchase pages, no suggestion to buy.
- Never present the free reading as partial or incomplete. Answer every question as well as the free data allows.
- When a question would need a paid report and the user has no ticket, answer from the free data. Mention the ticket only if they ask how to get more.

```bash
gv ticket set 'CODE'      # stored owner-only; output shows it masked
gv ticket                 # status: credits_left, reports_created, expires, days_left, valid (2 requests)
gv ticket --offline       # only whether one is stored (masked), no request
gv reports                # reports made with the ticket in the last 180 days: id, person, type, plus expiry
gv read 'ID' --for KEY    # full text of one report, as markdown; no credit used. --for keeps a local copy under that saved person
gv make KEY --report=62 --yes            # create a report: uses ONE ticket credit
gv make KEY --with KEY2 --report=16 --yes  # two-person report (synastry)
gv make KEY --report=13 --start 2027-01-01 --city 'Madrid' --country 'España' --yes   # solar return for 2027, living in Madrid
```

Rules:

- **The ticket is a credential.** Never print it, echo it back, or put it in a file outside the helper. It appears once on the command line, in `gv ticket set`, and from then on only masked. `GRUPO_VENUS_TICKET` overrides the stored one.
- **Check the ticket once per conversation** with `gv ticket` when the user first wants paid reports, and tell them the credits left and expiry. If `valid` is false, say why (no credits or expired) and stay on the free tier. Don't re-check after every report: a new `make` returns `credits_left`.
- **Read before you make.** Run `gv reports` first; if the person already has that report type, `gv read` it for free.
- **Confirm every `make`** with the user, naming the report and that it uses one credit; `--yes` records that confirmation. Report `credits_left` from the output. A report already made here comes back as `cached`: no request, no credit.
- Returns and progressions are cast for where the person **is** at that date. Ask where they live (or will be) if it may differ from the birth place, and pass `--city`/`--country` in the site's spelling (Spanish country names, US states by name). The birth place is the default.
- Asking again for the same person, report and date is free: the site recognizes it and the output says `existing`.
- A created report is kept by grupovenus.com under the ticket for 180 days, then deleted there; say so when confirming a `make`. `gv read` keeps a local copy only with `--for KEY`, under that saved person, and `gv remove KEY` deletes it. Without `--for` nothing is kept.
- Two-person reports take the second person with `--with KEY2` (or `--line2 'LINE'`). Both people go to grupovenus.com, so the second one needs the same consent as anyone else.
- Reports come in the language of `--lang` (E is Spanish). Answer in the user's language anyway.

| `--report=` | Report |
|---|---|
| `62` | Carta Natal (full natal reading, ~35 sections) |
| `170` / `61` | Natal con Quirón / Carta SuperNatal |
| `69` | Informe Indra (psychological mirror, ~145 sections) |
| `66` / `174` | Vocacional / Vocacional simple |
| `63` / `171` | Infantil / Infantil coloquial |
| `65` / `64` / `67` | Espiritual / Kármica / Astrología y Tarot |
| `50` | Pronóstico para hoy |
| `13` / `173` / `15` / `14` | Revolución Solar (year of `--start`) / Solar coloquial / Lunar (first return on or after `--start`) / Progresiones (at `--start`) |
| `16` / `172` / `17` | Two people: De Pareja / De Pareja coloquial / De Amistad |
| `90` | Two people: Carta Compuesta |
| `22` / `23` | Two people: couple forecast, 2 months Sol-Plu / 12 months Mar-Plu (from `--start`) |
| `7` / `6` / `4` | Forecasts: 2 years Sat-Plu / 1 year Jup-Plu / 3 months Mar-Plu (from `--start`, past dates allowed); also returns parsed `transits` |

The text is markdown: `##` chapters, `###` the astrological factor (for example "Sol en Géminis") or the transit with its code and dates ("Plutón Trígono Mercurio (PLUTRIMER), 8/11/2026"), then its interpretation. The Indra report has no factor headings on the site, only text. Read the sections relevant to the question rather than pasting the whole report, and keep the person's reading style.

---

## Numerology (free)

Two numerology reports are free, with or without a ticket: `945` Básica and `947` Avanzada. They need no `--yes` and use no credit.

```bash
gv make KEY --report=945 --fullname 'Juan Cruz Pérez'
gv make KEY --report=947 --fullname 'Juan Cruz Pérez' --signature 'J. Pérez'
```

- Numerology is computed from the **full birth name** (as on the birth certificate), so a saved alias gives a different result. Ask for the full name, say it goes to grupovenus.com, and pass it with `--fullname`. It goes into that one request only: a report made with `--fullname` or `--signature` is never written to disk, because its text repeats them. Without either option the saved name is used and the report is cached like any other.
- `--signature` (947 only, optional) adds an analysis of the letters the person writes when signing.
- The output has the same `text` markdown as the other reports.

---

## Transit Interpretation Texts

```bash
gv interp PLUOPOASC                      # colloquial (default)
gv interp PLUOPOASC --style tratsp       # technical, classical
gv interp PLUOPOASC --style starsolues   # potentials, higher expression
```

Texts are in Spanish. Synthesize them in the user's language; never paste them raw.

### Transit codes

Format `[TRANSITING][ASPECT][NATAL]`, for example `SATCUAASC` = ♄ □ ↑ (Saturn square Ascendant).

| Code | Server name | English | Symbol |
|---|---|---|---|
| `SOL` | Sol | Sun | ☉ |
| `LUN` | Luna | Moon | ☽ |
| `MER` | Mercurio | Mercury | ☿ |
| `VEN` | Venus | Venus | ♀ |
| `MAR` | Marte | Mars | ♂ |
| `JUP` | Júpiter | Jupiter | ♃ |
| `SAT` | Saturno | Saturn | ♄ |
| `URA` | Urano | Uranus | ♅ |
| `NEP` | Neptuno | Neptune | ♆ |
| `PLU` | Plutón | Pluto | ♇ |
| `ASC` | Ascendente | Ascendant | ↑ |
| `MC` | Medio Cielo | Midheaven | MC |

| Code | Server name | English | Degrees | Symbol |
|---|---|---|---|---|
| `CJC` | Conjunción | Conjunction | 0° | ☌ |
| `SEX` | Sextil | Sextile | 60° | ⚹ |
| `CUA` | Cuadratura | Square | 90° | □ |
| `TRI` | Trígono | Trine | 120° | △ |
| `OPO` | Oposición | Opposition | 180° | ☍ |
| `QUI` | Quincuncio | Quincunx | 150° | ⚻ |

| Server name | English | Symbol |
|---|---|---|
| Aries | Aries | ♈ |
| Tauro | Taurus | ♉ |
| Géminis | Gemini | ♊ |
| Cáncer | Cancer | ♋ |
| Leo | Leo | ♌ |
| Virgo | Virgo | ♍ |
| Libra | Libra | ♎ |
| Escorpio | Scorpio | ♏ |
| Sagitario | Sagittarius | ♐ |
| Capricornio | Capricorn | ♑ |
| Acuario | Aquarius | ♒ |
| Piscis | Pisces | ♓ |

---

## Zodiac Types

| `--zodiac` | System |
|---|---|
| `T` | Tropical (default) |
| `S1` | Sidereal, Fagan-Bradley |
| `S2` | Sidereal, Lahiri |
| `S3` | Sidereal, Sassanian |
| `S4` | Sidereal, Krishnamurti |
| `S5` | Sidereal, Hipparchos |

Default to Tropical. Mention sidereal only if the user asks.

---

## Comparing Two People

Compare from data you already have:

1. `gv transits A` and `gv transits B` (usually cached).
2. Find overlapping windows: periods where both are under major transits at once.
3. Highlight shared themes (both under Pluto? both under Neptune?), clashing periods, and supportive overlaps.

If the user has shared a ticket, the two-person reports (synastry, friendship, composite chart, couple forecast) are also available through `gv make --with`, see Paid Reports. Otherwise compare as above, without bringing up the ticket.

---

## Voice & Style

### General tone

You're an astrologer who knows the craft but talks like a person, not like a mystical pamphlet. Avoid:
- "the stars are telling you..." (too mystical, cliché)
- degree lists with no context (too raw)
- "this is a powerful time for growth" (vague, useless)

Be direct, be specific, use the symbols, name the tension or the gift without overselling it.

### Per-person styles

Read the person's `style` before writing about them. If it isn't set, ask (see First Reading).

#### `casual`

Like a friend who knows astrology. No jargon, no degrees, no house numbers unless asked. Lead with feeling and situation, not planet names.

> "Right now something is shaking your sense of identity: who you are and how you show up. It's not comfortable, but it's not pointless either. What's falling apart probably wasn't representing you anymore."

Use `transiaw` texts only. Offer depth only if asked.

#### `deep`

Full astrological language: aspects, houses, orbs, retrograde phases, symbols (♇ ☍ ↑). Structure the reading clearly.

> "♇ Pluto is exactly opposite (☍) your natal ↑ Ascendant, orb 0°. A long transit: active from late December through February, then again by retrograde from late July to October."

Synthesize all 3 styles (`tratsp`, `starsolues`, `transiaw`). Give timing windows explicitly.

#### `practical`

Skip the poetry: what to do and when. Windows, peaks, warnings. Calendar-friendly.

> "**April 3 to 17:** good window to start physical projects (♄ △ ♂).
> **Watch June:** tension between what you want to change and what the context allows (♄ □ ♅)."

Dates, peaks and one action line per transit. No extended interpretation unless asked.

---

## First Reading

The recommended flow for someone new. **Do not dump all the data at once.** Each step is one conversation beat.

### Step 1: add them and show the chart

1. Follow Privacy and consent, then add the person (see Adding People).
2. If `style` is not set, ask:
   > "How would you like me to read your chart?
   > - **Casual:** like a friend who knows astrology, no jargon
   > - **Deep:** full aspects, houses and timing
   > - **Practical:** straight to the point, what to do and when"

   Save it with `gv style`.
3. `gv chart KEY` (or `--line` for an unsaved person) and show the image.
4. A **brief profile** from the chart, 3 or 4 sentences: Sun (core drive), Ascendant (how they show up), Moon (emotional nature), and any tight conjunction or stellium that stands out.
5. `gv transits KEY --top 3` and a **current snapshot** in 2 to 4 sentences: the transits whose windows include today. Fetch the matching interpretation only for those (`transiaw` for casual and practical).

### Step 2: offer next steps

At most 4 options:

> What would you like to explore?
> - **Year forecast:** the key transits month by month
> - **A specific transit:** go deeper on something I mentioned
> - **Someone else:** compare your year with another person's
> - **This week:** the short-range sky

### Step 3: go deep on demand

Only when asked: fetch the 3 interpretation styles for that one transit, synthesize 1 to 3 paragraphs, and say when it's exact, when it fades and whether it returns retrograde.

---

## Conversational Suggestions

- **Several people stored:** offer comparisons. "I also have [name] saved. Want me to compare your years?"
- **Language:** answer in the user's language, whatever `--lang` was used.
- **Past dates:** full-year readings for past dates need a ticket. Without one, don't offer retrospective year readings, and don't bring up the ticket.
- **Ticket errors:** if `gv` reports a ticket is required or refused, say so plainly and continue with the free alternative.
