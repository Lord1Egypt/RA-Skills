---
name: openclaw-json-toolkit
version: 2.0.0
description: "Enterprise-grade JSON processing suite — format, validate, deep-diff, JSONPath query, structural transform, and schema generation in one MCP server. Use when: (1) user says 'format this JSON' or 'pretty print this', (2) user asks 'validate my JSON' or 'is this valid JSON', (3) user needs to 'compare two JSON objects' or 'diff these configs', (4) user wants to 'query nested JSON' or 'extract with JSONPath', (5) user requests 'flatten JSON' or 'generate JSON Schema'. Supports draft-07 schema, recursive flatten, wildcard queries, filter expressions, array slicing. Zero install, sub-100ms on Cloudflare Workers. Free + Pro $9/mo."
read_when:
  - "User pastes raw or messy JSON and asks to format, pretty-print, or minify it"
  - "User asks to validate JSON, check syntax, or debug a parse error"
  - "User has two JSON objects and wants to compare, diff, or find changes"
  - "User needs to extract deeply nested values using JSONPath or dot notation"
  - "User wants to generate a JSON Schema from sample data or flatten nested structures"
commands:
  - json_format
  - json_validate
  - json_diff
  - json_query
  - json_transform
  - json_schema_generate
metadata:
  openclaw:
    emoji: "{}"
    homepage: https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers
    always: false
---

# OpenClaw JSON Toolkit v2.0

**The Swiss Army knife for JSON — 6 tools, zero install, instant results.**

## Quick Reference

| Situation | Action | Tool |
|-----------|--------|------|
| Messy single-line JSON from an API | Pretty-print with 2-space indent | `json_format` |
| Need to minify for production | Compress to single line | `json_format` (minify) |
| Pasted JSON won't parse | Find exact error line + column | `json_validate` |
| Two config files changed | See added/removed/changed paths | `json_diff` |
| Need one field from 500-line JSON | Query with JSONPath expression | `json_query` |
| Deeply nested keys hard to access | Flatten to dot-notation | `json_transform` |
| Building an API contract | Auto-generate draft-07 schema | `json_schema_generate` |

## What's New in v2.0

- :zap: **CloudEdge Protocol** -- All processing runs on Cloudflare's global edge network. Sub-100ms response worldwide, zero cold starts.
- :mag: **DeepQuery Engine** -- Full JSONPath with deep scan (`..`), wildcards (`*`), filter expressions (`?(@.price < 10)`), and array slicing (`[0:5]`).
- :shield: **Schema Draft-07 Intelligence** -- Auto-detects semantic formats: email, URI, date-time, IPv4, UUID. Infers `required` fields and `enum` candidates from sample data.
- :arrows_counterclockwise: **StructureMorph Transform** -- Recursive flatten/unflatten, key renaming with mapping objects, pick/omit projections on arbitrarily nested JSON.

## MCP Quick Start

```json
{
  "openclaw-json": {
    "type": "streamable-http",
    "url": "https://json-toolkit-mcp.yagami8095.workers.dev/mcp"
  }
}
```

Add to Claude Desktop, Cursor, Windsurf, VS Code, or any MCP-compatible client. No API key needed for Free tier. Works immediately.

## Detection Triggers

This skill activates when you say:

- "format this JSON" / "pretty print this" / "indent this JSON"
- "validate my JSON" / "is this valid JSON" / "why won't this parse"
- "compare these two JSON" / "diff these objects" / "what changed between these configs"
- "query this JSON" / "extract from JSON" / "JSONPath" / "get the nested value"
- "flatten this JSON" / "restructure this" / "rename these keys" / "unflatten"
- "generate a schema" / "create JSON Schema" / "schema from this sample"

## Tools (6)

### `json_format` -- Pretty-Print & Minify (CloudEdge Protocol)

Format any JSON string with configurable indentation or compress to a single line for production payloads.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json` | string | required | Raw JSON string to format |
| `indent` | number | 2 | Spaces per indent level (0-8) |
| `minify` | boolean | false | Compress to single line, strip whitespace |

**Output**: Formatted JSON string + byte count (before/after) + compression ratio when minifying.

#### WRONG vs RIGHT

**WRONG** -- Manually adding spaces to JSON in a text editor:
```
User: Can you add proper indentation to this JSON?
Agent: *manually edits text, misses nested arrays, breaks trailing commas*
```

**RIGHT** -- Use `json_format`:
```
User: Format this JSON
Agent: calls json_format → returns perfectly indented JSON with byte count in 12ms
```

---

### `json_validate` -- Validation with Diagnostics

Validate JSON syntax and get structural metadata on success, or precise error location on failure.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json` | string | required | JSON string to validate |

**On success**: `{ valid: true, type: "object"|"array", keyCount, depth, byteSize }`
**On failure**: `{ valid: false, error: "message", line: 3, column: 15, context: "near '...'" }`

#### WRONG vs RIGHT

**WRONG** -- Guessing where the JSON error is:
```
User: Why won't this JSON parse?
Agent: *scans visually, says "maybe line 12?"* — misses the real error on line 47
```

**RIGHT** -- Use `json_validate`:
```
User: Why won't this JSON parse?
Agent: calls json_validate → "Unexpected token at line 47, column 23: trailing comma after last element"
```

---

### `json_diff` -- Structural Comparison (DeepDiff Protocol)

Compare two JSON values and get a complete structural diff showing every added, removed, and changed path.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `left` | string | required | First JSON (the "before") |
| `right` | string | required | Second JSON (the "after") |

**Output**: `{ added: [...paths], removed: [...paths], changed: [{ path, from, to }], totalChanges }`. Every changed value shows the exact before/after values at that path.

- Use for: API response comparison, config drift detection, schema evolution tracking, deployment validation.

---

### `json_query` -- JSONPath Extraction (DeepQuery Engine)

Query JSON with full JSONPath support including dot notation, bracket notation, wildcards, deep scan, array slicing, and filter expressions.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json` | string | required | JSON data to query |
| `path` | string | required | JSONPath expression |

**Supported syntax**:
- `$.store.book[0].title` -- direct path
- `$.store.book[*].author` -- wildcard
- `$..price` -- recursive deep scan
- `$.store.book[0:3]` -- array slicing
- `$.store.book[?(@.price < 10)]` -- filter expression

**Output**: Array of matched values with their resolved paths.

---

### `json_transform` -- Structural Operations (StructureMorph)

Perform structural transformations: flatten nested JSON to dot-notation keys, unflatten back, pick/omit specific keys, or rename keys with a mapping object.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json` | string | required | JSON to transform |
| `operation` | string | required | `flatten`, `unflatten`, `pick`, `omit`, `rename` |
| `options` | object | {} | Operation-specific: `keys[]` for pick/omit, `mapping{}` for rename |

**Output**: Transformed JSON with operation summary (keys affected, depth change).

---

### `json_schema_generate` -- Schema from Samples (Schema Intelligence)

Generate a complete JSON Schema (draft-07) from any JSON value. Auto-infers types, detects semantic formats, determines required fields, and identifies enum candidates.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json` | string | required | Sample JSON value |

**Auto-detected formats**: `email`, `uri`, `date-time`, `ipv4`, `ipv6`, `uuid`, `hostname`.
**Output**: Complete JSON Schema with `$schema`, `type`, `properties`, `required`, `format` annotations, and `description` placeholders.

## What NOT to Do

| Don't | Why | Do Instead |
|-------|-----|------------|
| Send binary data (BSON, MessagePack, Protobuf) | Text JSON only | Decode to JSON string first |
| Send JSON over 1MB | Edge workers have memory limits | Split into chunks, process each |
| Expect streaming output | Each call returns complete results | Use for bounded payloads |
| Use as a database | Tools are stateless | Store results client-side |
| Send JSON with JS comments | Strict JSON spec only | Strip comments before sending |

## Security & Privacy

| What | Status |
|------|--------|
| Reads your JSON input | Yes -- for processing only |
| Stores your data | **No** -- zero persistence, stateless edge processing |
| Sends data to third parties | **No** -- processed entirely on Cloudflare Workers |
| Logs request content | **No** -- only anonymous usage counters |
| Requires authentication | Free tier: no. Pro: API key header only |

## Pricing

| Tier | Calls/Day | Price | What You Get |
|------|-----------|-------|--------------|
| Free | 20 | $0 | All 6 JSON tools, no signup |
| Pro | 1,000 | $9/mo | All 9 OpenClaw servers (49 tools), priority routing |
| x402 | Pay-per-call | $0.05 USDC | No account needed, crypto-native |

**Get Pro Key**: https://buy.stripe.com/4gw5na5U19SP9TW288

## The OpenClaw Intelligence Stack

| Server | Tools | Best For |
|--------|-------|----------|
| **JSON Toolkit** | 6 | Format, validate, diff, query, transform JSON |
| **Regex Engine** | 5 | Test, extract, replace, explain regex patterns |
| **Color Palette** | 5 | Generate, convert, harmonize, accessibility-check colors |
| **Timestamp Converter** | 5 | Parse, format, diff, timezone-convert timestamps |
| **Prompt Enhancer** | 6 | Optimize, rewrite, score, A/B test AI prompts |
| **Market Intelligence** | 6 | AI market trends, GitHub stats, competitor analysis |
| **Fortune & Tarot** | 3 | Daily fortune, tarot readings, I Ching |
| **Content Publisher** | 8 | MoltBook posts, social content, newsletter |
| **AgentForge Compare** | 5 | Compare AI tools, frameworks, MCP servers |

All 9 servers share one Pro key. **$9/mo = 49 tools.**
