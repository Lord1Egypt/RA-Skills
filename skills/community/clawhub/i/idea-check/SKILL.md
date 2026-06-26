---
name: idea-check
description: "Pre-build reality check before starting any new project or tool. Use when the user discusses a new idea, asks about competition, wants to know if something already exists, or says 'has anyone built', 'does this exist', 'check competition'."
metadata: {"openclaw":{"requires":{"bins":["mcporter"]}}}
---

# Idea Check

Scans GitHub, Hacker News, npm, PyPI, and Product Hunt to assess whether a project idea already exists before building it.

## Prerequisites

This skill requires the `idea-reality-mcp` MCP server registered in mcporter:

```bash
mcporter config add idea-reality --command "uvx idea-reality-mcp"
```

## Workflow

### 1. Extract the idea description

From the user's message, extract a clear, concise description of the project idea (1-2 sentences). Strip conversational filler.

### 2. Choose depth

| User intent | Depth |
|-------------|-------|
| Quick check, casual mention | `quick` (GitHub + HN only) |
| Serious project, "deep check", "thorough scan" | `deep` (all 5 sources in parallel) |
| Default | `quick` |

### 3. Run the reality check

```json
{
  "tool": "exec",
  "command": "mcporter call idea-reality.idea_check idea_text=\"<extracted idea description>\" depth=quick"
}
```

### 4. Interpret the result

The tool returns a JSON with `reality_signal` (0-100), `evidence`, `top_similars`, and `pivot_hints`.

Apply these rules:

| Signal | Action |
|--------|--------|
| **> 70** (crowded) | STOP. Report top competitors. Ask if the user wants to proceed, pivot, or abandon. |
| **30-70** (moderate) | Show results + pivot hints. Suggest a niche angle that existing projects don't cover. |
| **< 30** (open) | Green light. Mention the space is open and proceed. |

### 5. Format the response

```
<emoji> Idea Check — <signal>/100

<one-line verdict>

Top competitors:
1. <name> — <stars> stars — <description>
2. <name> — <stars> stars — <description>
3. <name> — <stars> stars — <description>

Sources: <list of sources checked>
<pivot hints if signal > 30>
```

Emoji mapping:
- Signal > 70: use a red indicator
- Signal 30-70: use a yellow indicator
- Signal < 30: use a green indicator

### 6. Error handling

- If the MCP tool is not available → tell the user to register `idea-reality-mcp` in `openclaw.json` (show the config snippet from Prerequisites)
- If the tool returns an error → report the error as-is, do not retry
- If `top_similars` is empty → note that no direct competitors were found but the signal score still reflects broader activity

## Examples

| User says | Depth | Expected behavior |
|-----------|-------|-------------------|
| "Has anyone built a CLI for tracking gym workouts?" | `quick` | Run check, likely high signal, show competitors |
| "I want to build an MCP server for pre-build validation" | `quick` | Run check, likely low signal, green light |
| "Deep check: AI-powered code review tool" | `deep` | Run deep scan, very high signal, suggest pivot |
| "Is there a market for a Telegram bot that tracks habits?" | `quick` | Run check, show results + pivot suggestions |
