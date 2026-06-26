---
name: parallel-findall
description: "Discover entities (companies, people, products) matching a natural-language description via the Parallel FindAll API. Use when the user wants to 'find all X' or 'list every Y that…' — different from web search (returns webpages) and deep research (returns a narrative report). Returns a structured list of entities."
homepage: https://parallel.ai
---

# Parallel FindAll

Discover entities matching a natural-language description. FindAll is for "give me a list of things that match this criteria" tasks — companies, people, products, papers, anything enumerable. Returns structured entities, not webpages or prose.

## When to Use

Trigger this skill when the user asks for:
- "find all [X]", "list every [Y] that…"
- "discover [companies / people / products] matching…"
- "give me a list of [SaaS in vertical Z / YC W24 dev tools / Series A AI startups]"
- Bulk entity discovery where the answer is a structured list, not a narrative

**Use Search for "what is X?"; use FindAll for "list every X that matches Y".**

## Quick Start

```bash
parallel-cli findall run "AI startups that raised Series A in 2026" --json
```

## CLI Reference

### Basic Usage

```bash
parallel-cli findall run "<objective>" [options]
parallel-cli findall status frun_xxx --json
parallel-cli findall poll frun_xxx --json
parallel-cli findall result frun_xxx --json
parallel-cli findall extend frun_xxx <n> --json
parallel-cli findall cancel frun_xxx
```

### Common Flags

| Flag | Description |
|------|-------------|
| `-g, --generator` | Generator tier: `preview`, `base`, `core` (default), `pro` |
| `-n, --match-limit` | Max matched candidates, 5-1000 (default: 10) |
| `--exclude '<json>'` | Entities to exclude (JSON array of `{name, url}`) |
| `--no-wait` | Return immediately with `frun_xxx`; poll separately |
| `--dry-run` | Preview the schema FindAll will use, without creating a run |
| `--json` | Output as JSON |
| `-o, --output <file>` | Save full result to file |

### Examples

**Basic discovery:**
```bash
parallel-cli findall run "Find roofing companies in Charlotte NC" --json
```

**Larger result set with `core` generator:**
```bash
parallel-cli findall run "AI startups that raised Series A in 2026" -n 50 --json
```

**`pro` tier for deeper coverage:**
```bash
parallel-cli findall run "YC W24 dev tools companies" -g pro -n 100 --json
```

**Preview the schema before running:**
```bash
parallel-cli findall run "Find Series B fintechs in Latin America" --dry-run --json
```

**Exclude already-known entities:**
```bash
parallel-cli findall run "Find AI startups in healthcare" \
  --exclude '[{"name": "Hippocratic AI", "url": "hippocraticai.com"}]' \
  --json
```

**Async — launch then poll separately:**
```bash
parallel-cli findall run "AI startups that raised Series A in 2026" --no-wait --json
# returns frun_xxx
parallel-cli findall status frun_xxx --json
parallel-cli findall poll frun_xxx --json    # waits and returns result
```

**Extend an existing run with more matches:**
```bash
parallel-cli findall extend frun_xxx 50 --json
```

**Cancel a running job:**
```bash
parallel-cli findall cancel frun_xxx
```

## Best-Practice Prompting

### Objective
1-3 sentences describing:
- The entity type (companies / people / products / papers / etc.)
- The matching criteria (vertical, geography, time range, status)
- Any quality filters ("active", "publicly listed", "open-source")

### Generator Tier
- `preview` — fast scan, low coverage. Useful only for quick sanity checks.
- `base` — broad and fast, but **noisy** (query echoes, no-URL entries, category placeholders). Use only when the user explicitly accepts noise.
- `core` (default) — best balance of coverage and quality.
- `pro` — deeper coverage, slower. Use for high-stakes discovery where missing matches is costly.

### Match Limit
Pick the smallest `-n` that satisfies the user's intent. Default 10 is fine for "show me a few"; bump to 50–100 for "list every X". Max 1000.

## Response Format

`findall run` returns JSON with:
- `findall_id` — `frun_xxx`
- `status` — `running` / `completed` / `cancelled` / `failed`
- `schema` — the JSON Schema FindAll built for the matches
- `matches[]` — array of entities, each with fields per the schema (typically `name`, `url`, plus skill-specific extracted fields)

## Output Handling

When relaying matches to the user:
- **Filter noise**: drop entries with empty `url`, query-echo names, or category placeholders. Especially important on `-g base`.
- **Group by source domain** if the result set is large — helps the user spot duplicate sources.
- **Echo `findall_id`** so the user can `extend` or `cancel` later.

## Running Out of Context?

For large result sets (`-n` ≥ 50), save and use `sessions_spawn`:

```bash
parallel-cli findall run "<objective>" -n 100 --json -o /tmp/findall-<topic>.json
```

Then spawn a sub-agent:
```json
{
  "tool": "sessions_spawn",
  "task": "Read /tmp/findall-<topic>.json and produce a deduplicated table grouped by category.",
  "label": "findall-summary"
}
```

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Unexpected error (network, parse) |
| 2 | Invalid arguments |
| 3 | API error (non-2xx) |

## Prerequisites

Requires `parallel-cli` (installed and authenticated). If `parallel-cli --version` fails, or if a later command fails with an authentication error, tell the user to see https://docs.parallel.ai/integrations/cli and stop.

## References

- [API Docs](https://docs.parallel.ai)
- [FindAll API Reference](https://docs.parallel.ai/api-reference/findall)
