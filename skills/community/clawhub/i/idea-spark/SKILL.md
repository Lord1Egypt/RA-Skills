---
name: idea-spark
description: "Generate project ideas based on a domain or interest. Use when the user asks for project ideas, wants inspiration, says 'what should I build', 'give me ideas', 'project suggestions', or wants to find underserved niches. Complements idea-check for validation."
metadata: {}
---

# Idea Spark

Generates actionable project ideas by scanning real pain points from Hacker News, Reddit, and GitHub, then optionally validates them with idea-check.

## Workflow

### 1. Extract the domain

From the user's message, extract:

| Field | Notes |
|-------|-------|
| `domain` | Area of interest (e.g. "developer tools", "health tracking", "AI agents") |
| `count` | Number of ideas requested (default: 5) |
| `type` | Project type if specified: CLI tool, API, bot, app, library (default: any) |

If the domain is vague, ask for clarification before proceeding.

### 2. Research pain points

Run **3 searches in parallel** using the built-in `web_search` tool to find real problems people are complaining about or requesting:

```json
{ "tool": "web_search", "query": "site:news.ycombinator.com \"I wish\" OR \"someone should build\" OR \"why isn't there\" <domain> 2025 2026" }
```

```json
{ "tool": "web_search", "query": "site:reddit.com \"looking for\" OR \"is there a\" OR \"frustrated with\" <domain> tool" }
```

```json
{ "tool": "web_search", "query": "github.com trending <domain> OR \"help wanted\" OR \"good first issue\" <domain>" }
```

### 3. Synthesize ideas

From the search results, extract recurring themes and unmet needs. For each idea, produce:

| Field | Format |
|-------|--------|
| `name` | Short project name (2-4 words) |
| `pitch` | One-line description of what it does |
| `pain` | The real problem it solves (with source: HN/Reddit/GitHub) |
| `type` | CLI, API, bot, app, library, MCP server, OpenClaw skill |
| `effort` | low / medium / high |

Generate `count` ideas, ranked by how specific and actionable the pain point is.

### 4. Validate with idea-check (if available)

For each idea, run a quick validation:

```json
{
  "tool": "exec",
  "command": "mcporter call idea-reality.idea_check idea_text=\"<pitch>\" depth=quick"
}
```

If `mcporter` or `idea-reality` is not available, skip this step and note that validation was not performed.

Add the `reality_signal` score to each idea. Flag ideas with signal > 70 as "crowded".

### 5. Present the results

Format — **strict**:

```
💡 Idea Spark — <domain> — <count> ideas

1. <name>
   <pitch>
   Pain: <pain> (source)
   Type: <type> · Effort: <effort> · Signal: <score>/100 <status>

2. ...
```

Status mapping:
- Signal < 30: "open field"
- Signal 30-70: "some competition"
- Signal > 70: "crowded"
- Not checked: "not validated"

### 6. Follow-up

After presenting, suggest:
- "Want me to deep-check any of these?" → run `idea-check` with `depth=deep`
- "Want me to start building #N?" → proceed with development

### 7. Error handling

- If web searches return no results → broaden the domain, try without site filters
- If all ideas score > 70 → tell the user the space is saturated, suggest narrowing the niche
- If mcporter is not available → present ideas without validation, mention idea-check for later
- If the domain is too broad (e.g. "tech") → ask the user to narrow down

## Examples

| User says | Domain | Action |
|-----------|--------|--------|
| "Give me 5 project ideas for developer tools" | developer tools | Search HN/Reddit/GitHub, generate 5 ideas, validate each |
| "What should I build in the AI agent space?" | AI agents | Search for pain points, generate ideas, validate |
| "I want to build something with MCP servers" | MCP servers | Focus on MCP ecosystem gaps, generate ideas |
| "Startup ideas around health tracking" | health tracking | Search for unmet needs, generate ideas, flag crowded ones |
