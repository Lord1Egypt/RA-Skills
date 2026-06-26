---
name: morning-briefing
description: "Aggregates weather, game updates, and concert data into a daily markdown briefing. Triggered by 'morning briefing', 'daily briefing', 'run my briefing', 'what's new today'."
metadata:
  openclaw:
    emoji: "🌅"
    os: [linux, darwin]
    requires:
      bins: [curl, jq]
---

# morning-briefing

A pure aggregator skill that reads data produced by other skills, filters and formats it, and writes a composed markdown briefing to `data/briefing.md`.

## Usage

1. **Initialize config** (first run only):
   ```bash
   bash scripts/init_config.sh
   ```

2. **Run the briefing**:
   ```bash
   bash scripts/morning_briefing.sh
   ```
   The script outputs the path to the generated markdown file.

3. **Read the file and present its contents verbatim to the user.** Do not summarize, reformat, paraphrase, add commentary, or editorialize. Output the entire markdown file exactly as written — the markdown IS the briefing. Do not wrap it in a code block. Do not omit sections. Do not change heading levels or link formatting.

## Data Sources

Weather is built-in (direct curl to wttr.in). Other sections are driven by external skills that write JSON data files:

- **steam-games-updates** — game news from Steam
- **upcoming-metal-concerts** — concert listings from concerts-metal.com

Each source has a jq template in `assets/templates/<source-id>.jq` that formats the raw JSON into markdown.

## Customization

Edit `~/.openclaw/config/morning-briefing.json` to:

- **Toggle weather** — set `weather.enabled` to `false`
- **Change location** — set `weather.location`
- **Enable/disable a source** — set `sources.<id>.enabled`
- **Filter game updates** — add `"games": ["CS2"]` to steam-games-updates preferences
- **Filter concerts by city** — edit `cities` array in upcoming-metal-concerts preferences
- **Change concert window** — edit `days_ahead` in upcoming-metal-concerts preferences

## Adding a New Source

1. Add an entry to `sources` in the config with `data_path` and `preferences`
2. Create `assets/templates/<source-id>.jq` that accepts the source's JSON schema
3. The template receives `$preferences` (argjson) and `$today`/`$cutoff` (arg) variables
