---
name: gta6wiki
description: Query the GTA6 Wiki (https://gta6wiki.wiki) encyclopedia, 3,843+ Leonida & Vice City interactive map landmarks (including 340+ enterable interiors and coordinates), 73+ story and side mission walkthroughs, all 61 built-in post-story cheat codes, and deep-dive analysis articles in English or Simplified Chinese. Use when the user asks any question about Grand Theft Auto VI locations, missions, characters (Jason Duval, Lucia Caminos, etc.), vehicles, weapons, 100% completion checklists, map pins, or cheats. No API key or login is required.
license: MIT
metadata:
  author: littleben
  homepage: https://gta6wiki.wiki
  mcp: https://gta6wiki.wiki/mcp
  cli: https://gta6wiki.wiki/cli/gta6wiki-cli.tgz
  documentation: https://gta6wiki.wiki/skill
  llms: https://gta6wiki.wiki/llms.txt
---

# GTA6 Wiki

Search and retrieve verified Grand Theft Auto VI encyclopedia entries, Leonida & Vice City interactive map coordinates, mission walkthroughs, 100% completion checklists, and cheat codes from [GTA6 Wiki](https://gta6wiki.wiki) with zero authentication or API keys.

## Scope & Sourced Facts

- **Bilingual knowledge base:** All core tools support `locale: "en"` (English) and `locale: "zh"` (Simplified Chinese with official Rockstar & in-game localized terminology).
- **Read-only & public:** No login, token, or API key is required across Remote MCP, CLI, or HTTPS JSON/Markdown endpoints.
- **Direct citations:** Always share the returned `canonicalUrl` or `mapPinUrl` (e.g., `https://gta6wiki.wiki/map?marker=L36`) so the user can open the interactive map or walkthrough directly.

## 1. Remote MCP Server (Recommended)

Connect any Streamable HTTP MCP client directly to:

```text
https://gta6wiki.wiki/mcp
```

Standard `mcpServers` JSON configuration (Claude Desktop, Claude Code, Cursor, Windsurf, Antigravity):

```json
{
  "mcpServers": {
    "gta6wiki": {
      "type": "http",
      "url": "https://gta6wiki.wiki/mcp"
    }
  }
}
```

Or add in one command with Claude Code:

```bash
claude mcp add --transport http gta6wiki https://gta6wiki.wiki/mcp
```

For legacy stdio-only MCP clients, bridge via the zero-dependency CLI:

```json
{
  "mcpServers": {
    "gta6wiki": {
      "command": "npx",
      "args": ["-y", "https://gta6wiki.wiki/cli/gta6wiki-cli.tgz", "mcp"]
    }
  }
}
```

### Available MCP Tools

1. **`search_wiki`** — `{ "query": "Vice City", "type": "locations", "limit": 10, "locale": "en" }`
   - Searches all reviewed GTA 6 Wiki entries across `locations`, `missions`, `characters`, `mechanics`, `vehicles`, `weapons`, and `items_collectibles`. Supports `intent` (`location`, `unlock`, `price_reward`, `mission_requirements`).
2. **`get_wiki_entry`** — `{ "slug": "jason-duval", "includeMarkdown": true, "locale": "en" }`
   - Retrieves a complete GTA 6 Wiki entry by `slug` or entity name: quick answers, walkthrough steps, attributes, verified claims, interactive map focus coordinates, related entries, and clean Markdown.
3. **`search_map_landmarks`** — `{ "query": "gun", "category": "shops_services", "enterableOnly": true, "limit": 20, "locale": "en" }`
   - Searches 3,843 verified Leonida & Vice City map pins (340+ enterable buildings, weapon shops, mod garages, safehouses, transit stations, 73 mission hubs). Supports `region`, `category`, `enterableOnly`, and exact `markerId` (such as `"L36"`), returning meter coordinates (`x`, `y`), real-world Miami/Florida counterparts, and fly-to `mapPinUrl` links.
4. **`list_missions`** — `{ "chapter": 1, "character": "Lucia", "missableOnly": false, "locale": "en" }`
   - Queries the GTA 6 playable story & side mission directory with chapter order (`0` Prologue through endgame), playable character, prerequisites, rewards, missable/optional flags, walkthrough URLs, and mapped landmark pins.
5. **`lookup_cheats`** — `{ "category": "vehicle", "storyAutoUnlockOnly": false, "locale": "en" }`
   - Searches all 61 built-in GTA 6 post-story cheats (`player`, `combat`, `vehicle`, `environment`, `filter`), returning D-Pad sequences, unlock challenges, phone input method (`L1/LB + R1/RB`), and session save/trophy rules.
6. **`list_articles_and_updates`** — `{ "kind": "all", "slug": "gta-6-leaks", "locale": "en" }`
   - Lists published deep-dive analysis articles and chronological Wiki updates, or returns the full Markdown body when `slug` is provided.

## 2. Official GTA6 Wiki CLI (Node.js 18+)

Run immediately via `npx` or install `gta6wiki` locally:

```bash
# Instant npx execution (zero dependencies)
npx -y https://gta6wiki.wiki/cli/gta6wiki-cli.tgz search "Vice City"

# Or install 'gta6wiki' into ~/.local/bin
curl -fsSL https://gta6wiki.wiki/cli/install.sh | sh

# Subcommands (append --json for structured JSON or --locale zh for Chinese)
gta6wiki search "Lucia Caminos"
gta6wiki entry vice-city --markdown --out vice-city.md
gta6wiki map "Ocean Drive" --enterable --limit 10
gta6wiki missions --chapter 1 --missable
gta6wiki cheats --category vehicle
gta6wiki articles gta-vice-city-collection
gta6wiki mcp
```

## 3. Bundled Python CLI Helper (Python 3.9+)

When this skill is installed locally, you can also run `scripts/gta6wiki.py` with the Python standard library only:

```bash
python3 scripts/gta6wiki.py search "Port Gellhorn"
python3 scripts/gta6wiki.py entry story-mission-guide --markdown
python3 scripts/gta6wiki.py map --region vice-beach --enterable --limit 15
python3 scripts/gta6wiki.py missions --missable
python3 scripts/gta6wiki.py cheats --category combat
python3 scripts/gta6wiki.py articles --kind blog
```

## 4. Clean Markdown Pages, `llms.txt` & Direct HTTPS APIs

Every page on GTA6 Wiki exposes a clean Markdown edition by appending `.md`:

- `https://gta6wiki.wiki/llms.txt` (structured English index)
- `https://gta6wiki.wiki/llms-full.txt` (complete single-file corpus)
- `https://gta6wiki.wiki/wiki/<slug>.md` & `https://gta6wiki.wiki/zh/wiki/<slug>.md`
- `https://gta6wiki.wiki/map.md`, `https://gta6wiki.wiki/cheats.md`, `https://gta6wiki.wiki/guides.md`

Direct read-only JSON endpoints (`{ "code": 0, "message": "ok", "data": ... }`):

- `GET https://gta6wiki.wiki/api/wiki/search?q=Vice+City&locale=en`
- `GET https://gta6wiki.wiki/api/wiki/entity?slug=vice-city&locale=en`
- `GET https://gta6wiki.wiki/api/wiki/landmarks?q=pawn&enterable=1&locale=en`
- `GET https://gta6wiki.wiki/api/wiki/missions?chapter=1&locale=en`
- `GET https://gta6wiki.wiki/api/wiki/cheats?category=player&locale=en`
- `GET https://gta6wiki.wiki/api/wiki/articles?kind=all&locale=en`

Website: https://gta6wiki.wiki · MCP, CLI & Skill Hub: https://gta6wiki.wiki/skill · Skill Archive: https://gta6wiki.wiki/skills/gta6wiki.zip
