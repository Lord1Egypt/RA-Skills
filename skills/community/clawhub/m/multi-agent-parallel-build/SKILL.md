---
name: multi-agent-parallel-build
description: Orchestrate multiple coding agents (Claude Code, Codex, etc.) in parallel waves to build UI pages, API endpoints, or features simultaneously. Use when building dashboards with 5+ pages, microservices, or any project where independent components can be built concurrently. Covers wave planning, shared shell/component libraries, agent spawning, merge conflict avoidance, and post-wave integration fixes.
---

# Multi-Agent Parallel Build

Spawn multiple coding agents in parallel to build independent components simultaneously. Reduces wall-clock time 3-5x for multi-page builds.

## When to Use

- Building 4+ UI pages that share a shell but have independent content
- Creating multiple API endpoint groups
- Any project with clearly separable, independent work units

## Wave Architecture

```
Wave 0 (Sequential — YOU do this):
  → Shared infrastructure: API, shell components, CSS, data layer
  
Wave 1 (Parallel — AGENTS do this):
  → Agent A: Page/Feature 1
  → Agent B: Page/Feature 2  
  → Agent C: Page/Feature 3
  → Agent D: Page/Feature 4
  → Agent E: Page/Feature 5

Wave 2 (Sequential — YOU do this):
  → Integration fixes, cross-component wiring, testing
```

## Step 1: Wave 0 — Build Shared Infrastructure

Before spawning agents, create everything they'll all need:

1. **API layer** with all endpoints agents will consume
2. **Shared shell** (nav, header, theme, CSS variables)
3. **Component library** (cards, charts, tables, modals)
4. **Data contracts** (JSON shapes agents should expect from API)

This is critical — agents that build against a shared shell produce consistent UIs. Agents that each invent their own shell produce chaos.

Example shared shell:
```javascript
// shell.js — agents import this
function createShell(pageTitle, navItems) { /* sidebar + topbar */ }
function createCard(title, content) { /* themed card component */ }
function mcFetch(endpoint) { /* API wrapper with base URL */ }
```

## Step 2: Plan Agent Assignments

Each agent gets:
- **One clear deliverable** (a page, a feature, a service)
- **Path to shared resources** (shell.js, shell.css, API base URL)
- **API contract** (which endpoints to call, expected response shapes)
- **No overlapping files** — each agent writes to its own directory/files

Write a task prompt for each agent:

```
Build {page_name} at {file_path}.
Import shared shell from {shell_path}.
Fetch data from these API endpoints: {endpoints}.
Expected data shapes: {json_examples}.
Use Chart.js/D3 for visualization. Dark theme. No frameworks — vanilla JS + HTML.
```

## Step 3: Spawn Agents

Use `sessions_spawn` or coding-agent skill to launch all agents simultaneously:

```
Agent A: "Build agents.html — display 215 AI agents in searchable grid..."
Agent B: "Build skills.html — display 197 skills with category filters..."
Agent C: "Build knowledge.html — display 6.8K knowledge records with search..."
Agent D: "Build tools.html — display 231 tools grouped by MCP server..."
Agent E: "Build workflows.html + archetypes.html — two pages..."
```

Key flags:
- Each agent gets its own working directory or clearly separate files
- Include the shared shell path and API contract in every prompt
- Set reasonable timeouts (10-20 min per page)

## Step 4: Wave 2 — Integration Fixes

Common issues after parallel build:

### Double-prefix bug
Agents often misconstruct API URLs: `/api/mc/api/mc/` instead of `/api/mc/`. Fix with sed:
```bash
sed -i '' "s|/api/mc/api/mc/|/api/mc/|g" static/mc/*.html
```

### Inconsistent mcFetch usage
Some agents inline `fetch()` instead of using the shared `mcFetch()`. Standardize.

### Missing StaticFiles mount
Server needs routes for the new static directories:
```python
app.mount("/static/mc", StaticFiles(directory="static/mc"), name="mc-static")
```

### Large payload timeouts
If tables have massive text columns (system_prompt, etc.), agents may have built queries that select everything. Fix API to use lightweight selects.

## Principles

1. **Wave 0 quality determines Wave 1 success** — spend 60% of effort on shared infrastructure
2. **No file overlap between agents** — if two agents touch the same file, one will clobber the other
3. **API-first** — build and test all API endpoints before spawning UI agents
4. **Expect 2-3 integration bugs per agent** — budget 20 min for Wave 2 fixes
5. **5 agents is the sweet spot** — more than 7 creates coordination overhead that exceeds time savings
