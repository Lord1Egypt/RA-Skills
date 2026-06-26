# Google Trends Skill - Command Reference

## Common options

| Option | Default | Description |
|--------|---------|-------------|
| `--geo` | `US` | Country/region code (e.g., `US`, `GB`, `DE`, `JP`) |
| `--hl` | `en-US` | Language code for results |

## daily-trends

Get daily trending search topics for a country.

```bash
node scripts/trends.mjs daily-trends [--geo GEO] [--lang LANG]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--geo` | `US` | Country code |
| `--lang` | `en` | Language code |

**Output:** Array of trending stories with title, traffic volume, articles, and timestamps.

## realtime-trends

Get real-time trending topics.

```bash
node scripts/trends.mjs realtime-trends [--geo GEO] [--hours HOURS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--geo` | `US` | Country code |
| `--hours` | `4` | Trending hours window: `4`, `24`, `48`, or `168` |

## autocomplete

Get autocomplete/search suggestions for a keyword.

```bash
node scripts/trends.mjs autocomplete "<keyword>" [--hl HL]
```

**Output:** Array of suggestion strings.

## explore

Explore trend widgets for a keyword. Returns widget metadata including tokens needed by other commands.

```bash
node scripts/trends.mjs explore "<keyword>" [--geo GEO] [--time TIME] [--category CAT] [--property PROP] [--hl HL]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--time` | `now 1-d` | Time range. Examples: `now 1-H`, `now 4-H`, `now 1-d`, `now 7-d`, `today 1-m`, `today 3-m`, `today 12-m`, `today 5-y`, or `YYYY-MM-DD YYYY-MM-DD` |
| `--category` | `0` | Category ID (0 = all categories) |
| `--property` | (empty) | Property filter: `""` (web), `images`, `news`, `froogle` (shopping), `youtube` |

## interest-by-region

Get search interest by geographic region for a keyword.

```bash
node scripts/trends.mjs interest-by-region "<keyword>" [--geo GEO] [--resolution RES] [--start-time DATE] [--end-time DATE]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--resolution` | `REGION` | Geographic resolution: `COUNTRY`, `REGION`, `CITY`, `DMA` |
| `--start-time` | `2004-01-01` | Start date (YYYY-MM-DD) |
| `--end-time` | today | End date (YYYY-MM-DD) |

**Output:** Array of objects with `geoCode`, `geoName`, `value`, `formattedValue`, and `hasData`.

## related-topics

Get topics related to a keyword.

```bash
node scripts/trends.mjs related-topics "<keyword>" [--geo GEO] [--start-time DATE] [--end-time DATE] [--category CAT]
```

**Output:** Ranked list of related topics with `title`, `type`, `value`, and `link`.

## related-queries

Get search queries related to a keyword.

```bash
node scripts/trends.mjs related-queries "<keyword>" [--geo GEO] [--start-time DATE] [--end-time DATE] [--category CAT]
```

**Output:** Ranked list of related queries with `query`, `value`, and `link`.
