---
name: openclaw-regex-engine
version: 2.0.0
description: "Production-grade regex processing suite — test patterns with capture groups, explain any regex in plain English, build regex from natural language descriptions, browse 50+ battle-tested patterns, and find-replace with backreferences. Use when: (1) user says 'test this regex' or 'does this pattern match', (2) user asks 'explain this regex' or 'what does this regex do', (3) user needs to 'build a regex for emails' or 'create a pattern that matches URLs', (4) user wants a 'ready-made regex for phone numbers' or 'UUID pattern', (5) user requests 'regex find and replace' or 'search and replace with backreferences'. Supports all ES2024 flags, named groups, lookahead/lookbehind. Zero install, sub-100ms on Cloudflare Workers. Free + Pro $9/mo."
read_when:
  - "User pastes a regex pattern and wants to test it against sample text"
  - "User encounters a complex regex and asks what it does or how it works"
  - "User describes a matching goal in plain English and needs a regex built for them"
  - "User needs a common pattern for emails, URLs, IPs, UUIDs, phone numbers, or dates"
  - "User wants to perform regex-based find-and-replace with capture group references"
commands:
  - regex_test
  - regex_explain
  - regex_build
  - regex_library
  - regex_replace
metadata:
  openclaw:
    emoji: "\U0001F50D"
    homepage: https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers
    always: false
---

# OpenClaw Regex Engine v2.0

**Master regular expressions -- 5 tools to test, explain, build, browse, and replace patterns instantly.**

## Quick Reference

| Situation | Action | Tool |
|-----------|--------|------|
| Have a regex, need to test it | Run against text, get all matches + groups | `regex_test` |
| Found a scary regex in legacy code | Get plain-English breakdown of every token | `regex_explain` |
| Know WHAT to match but not HOW | Describe in English, get production regex | `regex_build` |
| Need a standard pattern (email, URL, IP) | Browse 50+ battle-tested patterns | `regex_library` |
| Need to transform text with regex | Find-replace with backreferences ($1, $2) | `regex_replace` |
| Complex pattern with capture groups | Test + Explain combo for full understanding | `regex_test` + `regex_explain` |

## What's New in v2.0

- :brain: **PatternForge Builder** -- Describe what you want in plain English. Get a production-ready regex with positive/negative test cases, flags, and explanation included.
- :book: **RegexLens Explainer** -- Break any regex into human-readable components token-by-token. Even nested lookaheads, possessive quantifiers, and Unicode categories.
- :file_cabinet: **BattleTest Library** -- 50+ curated patterns for email, URL, phone (international), IPv4/IPv6, UUID, JWT, credit card, date formats, file paths, and more. Every pattern includes test cases.
- :arrows_counterclockwise: **SmartReplace Engine** -- Full backreference support including named groups, global/first-match modes, and before/after diff preview.

## MCP Quick Start

```json
{
  "openclaw-regex": {
    "type": "streamable-http",
    "url": "https://regex-engine-mcp.yagami8095.workers.dev/mcp"
  }
}
```

Add to Claude Desktop, Cursor, Windsurf, VS Code, or any MCP-compatible client. No API key needed for Free tier. Works immediately.

## Detection Triggers

This skill activates when you say:

- "test this regex" / "does this pattern match" / "run this regex against"
- "explain this regex" / "what does this regex do" / "break down this pattern"
- "build a regex for" / "create a pattern that matches" / "regex for emails"
- "regex for URL" / "phone number regex" / "UUID pattern" / "IP address regex"
- "regex replace" / "find and replace with regex" / "search and replace with capture groups"
- "regular expression" / "pattern matching" / "capture groups" / "backreference"

## Tools (5)

### `regex_test` -- Match & Capture (PatternMatch Protocol)

Test a regex pattern against input text. Returns every match with full capture group detail, named groups, and exact index positions.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pattern` | string | required | Regex pattern to test |
| `text` | string | required | Input text to match against |
| `flags` | string | "g" | Flags: `g` global, `i` case-insensitive, `m` multiline, `s` dotall, `u` unicode, `v` unicodeSets |

**Output**: `{ matchCount, matches: [{ index, match, groups: [], namedGroups: {} }], executionTimeMs }`

#### WRONG vs RIGHT

**WRONG** -- Manually scanning text to check if a pattern works:
```
User: Does this regex match my test string?
Agent: *reads the regex visually, guesses "yes it should match"* — misses edge case with nested groups
```

**RIGHT** -- Use `regex_test`:
```
User: Does this regex match my test string?
Agent: calls regex_test → "3 matches found. Match 1 at index 15: 'user@example.com', group 1: 'user', group 2: 'example.com'"
```

---

### `regex_explain` -- Human-Readable Breakdown (RegexLens)

Break any regex into plain English, token by token. Each component gets a description, what it matches, and example matches.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pattern` | string | required | Regex pattern to explain |
| `flags` | string | "" | Active flags to include in explanation |

**Handles**: Character classes, quantifiers, anchors, groups (capturing, non-capturing, named), lookahead/lookbehind (positive and negative), backreferences, Unicode categories, and alternation.

**Output**: Array of `{ token, type, description, matches_example }` plus overall summary.

#### WRONG vs RIGHT

**WRONG** -- Staring at `^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%])[A-Za-z0-9!@#$%]{8,}$` and guessing:
```
User: What does this regex do?
Agent: *guesses* "It matches passwords maybe?" — no detail on the lookaheads or minimum length
```

**RIGHT** -- Use `regex_explain`:
```
User: What does this regex do?
Agent: calls regex_explain → "Password validator: requires at least 1 uppercase letter (lookahead 1), 1 digit (lookahead 2), 1 special char from !@#$% (lookahead 3), minimum 8 characters total from allowed set"
```

---

### `regex_build` -- Natural Language to Regex (PatternForge)

Describe what you want to match in plain English. Get a production-ready regex with recommended flags, explanation, and test cases (both positive and negative).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `description` | string | required | Plain English description of what to match |
| `options` | object | {} | `strict: boolean` for anchored patterns, `examples: string[]` for guidance |

**Output**: `{ pattern, flags, explanation, testCases: { shouldMatch: [], shouldNotMatch: [] } }`

**Example**: Input "match email addresses" produces a complete RFC-5322-lite pattern with 5 positive and 5 negative test cases.

---

### `regex_library` -- Pattern Collection (BattleTest Library)

Browse 50+ curated, production-tested regex patterns organized by category. Every pattern includes the regex string, description, recommended flags, and positive/negative test cases.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `category` | string | "" | Filter by category: `email`, `url`, `ip`, `phone`, `date`, `uuid`, `jwt`, `credit_card`, `password`, `html`, `file_path`, `css` |
| `search` | string | "" | Free-text search across pattern names and descriptions |

**Categories**: email, URL, IPv4, IPv6, phone (US, UK, JP, international), date (ISO, US, EU), UUID (v1-v5), JWT, credit card (Visa, MC, Amex), password strength, HTML tags, file paths (Unix, Windows), CSS selectors, color codes, semantic versioning.

---

### `regex_replace` -- Find & Replace (SmartReplace Engine)

Perform regex-based find-and-replace with full capture group reference support ($1, $2, named groups), global and first-match modes.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pattern` | string | required | Regex pattern to find |
| `replacement` | string | required | Replacement string with `$1`, `$2`, `$<name>` references |
| `text` | string | required | Input text to transform |
| `flags` | string | "g" | Regex flags |

**Output**: `{ result, replacementCount, diff: { before, after } }`

**Supports**: `$1`-`$9` numbered backreferences, `$<name>` named backreferences, `$&` full match, `` $` `` pre-match, `$'` post-match.

## What NOT to Do

| Don't | Why | Do Instead |
|-------|-----|------------|
| Use catastrophic backtracking patterns like `(a+)+$` | Will timeout on edge workers (~50ms limit) | Rewrite with atomic groups or possessive quantifiers |
| Expect PCRE-only features (conditional patterns, recursion) | Uses JavaScript ES2024 regex engine | Stick to JS-compatible syntax |
| Send input text over 100KB | Memory limits on edge workers | Split large texts into chunks |
| Rely on patterns for security validation alone | Regex is for format checking, not sanitization | Combine with server-side validation |
| Use `regex_build` for complex parsers | NL-to-regex handles single patterns, not grammars | Build complex patterns manually with `regex_explain` to verify |

## Security & Privacy

| What | Status |
|------|--------|
| Reads your input text and patterns | Yes -- for processing only |
| Stores your data | **No** -- zero persistence, stateless edge processing |
| Sends data to third parties | **No** -- processed entirely on Cloudflare Workers |
| Logs request content | **No** -- only anonymous usage counters |
| Executes patterns server-side | Yes -- sandboxed with 50ms timeout to prevent ReDoS |
| Requires authentication | Free tier: no. Pro: API key header only |

## Pricing

| Tier | Calls/Day | Price | What You Get |
|------|-----------|-------|--------------|
| Free | 20 | $0 | All 5 regex tools, no signup |
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
