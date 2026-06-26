---
name: mensa
description: Returns today's lunch menu of a German university canteen via the public OpenMensa API (no API key). One-time non-interactive setup picks a city; afterwards every canteen in that city is queryable by name substring.
version: 1.1.0
metadata:
  openclaw:
    homepage: "https://openmensa.org"
    requires:
      bins: ["python3"]
    tags: ["mensa", "food", "student", "openmensa"]
    categories: ["information", "productivity"]
    license: "MIT-0"
    keywords:
      - mensa
      - openmensa
      - canteen
      - lunch
      - student
      - campus
  clawdbot:
    homepage: "https://openmensa.org"
    requires:
      bins: ["python3"]
    tags: ["mensa", "food", "student", "openmensa"]
    categories: ["information", "productivity"]
    license: "MIT-0"
    keywords:
      - mensa
      - openmensa
      - canteen
      - lunch
      - student
      - campus
---

# Mensa

Returns the daily menu of a German university canteen, sourced from the public OpenMensa API (`https://openmensa.org`). No API key needed.

## When to use

Trigger this skill when the user asks for today's (or another day's) canteen / "Mensa" menu, e.g. *"What's for lunch at the Mensa today?"* or *"Mensaplan heute"*.

## Agent flow

1. **No config yet?** Ask the user for a city.
2. **List canteens in that city first** (do not save anything yet):
   ```bash
   python3 {baseDir}/mensa_today.py --list "<city>"
   ```
   Show the resulting list to the user and ask which canteen should be the default.
3. **Run setup with the user's chosen default:**
   ```bash
   python3 {baseDir}/mensa_today.py --setup "<city>" --default "<chosen-canteen-substring>"
   ```
   All canteens in that city are saved as aliases; the chosen one is marked as default. If the user does not pick (e.g. "egal"/"any"), call `--setup "<city>"` without `--default`; the first canteen returned by OpenMensa is then used.
4. **Menu queries:**
   ```bash
   python3 {baseDir}/mensa_today.py                       # default canteen, today
   python3 {baseDir}/mensa_today.py "UniCampus"           # any canteen in the city, by name substring
   python3 {baseDir}/mensa_today.py "Otto Hahn" --date 2026-06-02
   ```
   Substring matching is normalised — special characters (`-`, `,`, `.`) are ignored, so a query like *"Otto Hahn"* matches a canteen named *"Mensa Otto-Hahn-Straße"*.
5. **"No canteen matched"?** The query did not resolve to any saved alias. Show the user the available aliases (the script prints them) and offer to re-run `--setup` for a different city.

## Output rules (strict)

When rendering the menu back to the user, follow these rules verbatim:

- **Always present dishes as a bullet-point list**, one bullet per dish. No prose, no inline comma lists, no tables.
- **Never abbreviate, summarise, or truncate dish names.** Reproduce each dish name exactly as the script printed it (German umlauts, commas, parentheses included). Do not collapse a long name to "Pfann…" or "[---]".
- **Do not list Beilagen or Reste.** The script already filters out items whose category contains "Beilage" and items whose name contains "Restproduktion"; if such an item still slips through, omit it from the rendered list.
- Keep the script's header line (date) at the top, then the bullet list.

## Example output

```
2026-05-26 - Menu (student price)
- Spaghetti Bolognese - 2.80 EUR
- Couscous - 2.60 EUR (vegetarian)
- Türkische Linsensuppe, Fladenbrot - 1.80 EUR (vegan)
```

## Network egress

Outbound HTTPS to `openmensa.org` only. No credentials, no telemetry, no user data sent. The user's city and canteen choice stay in a local `config.json` next to the script.

## Files

- `mensa_today.py` — entry point (no third-party deps, stdlib only)
- `config.json` — created on first `--setup`, holds chosen canteen ids (gitignored, never uploaded)
- `README.md`, `LICENSE.md`
