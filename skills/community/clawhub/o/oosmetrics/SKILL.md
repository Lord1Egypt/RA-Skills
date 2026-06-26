---
name: oosmetrics
description: Search, compare, and analyze 330K+ open-source GitHub repos by growth rate, acceleration, and originality. Discover trending projects, find alternatives, check licenses, and get AI-powered analysis.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins: ["npx"]
      env: ["OOSMETRICS_API_KEY"]
    primaryEnv: "OOSMETRICS_API_KEY"
    install:
      npm: "@oosmetrics/mcp@1.0.1"
---

# oosmetrics - Open Source Momentum Intelligence

Query growth metrics, compare repos, discover trending projects, find alternatives, and get AI-powered deep analysis for 330,000+ GitHub repositories tracked by oosmetrics.com.

## How it works

This skill runs the `@oosmetrics/mcp` npm package (source: https://github.com/AlessandroFlati/GitHubMetrics/tree/main/mcp) as a local MCP server over stdio. The server makes HTTPS requests only to `api.oosmetrics.com` using your API key. It does not listen on any ports, does not run in the background after the agent session ends, and does not collect telemetry or send data anywhere other than the oosmetrics API.

## Setup

1. Get your API key at https://oosmetrics.com/profile (Pro or AI tier required). The key is scoped to your account and can be rotated or deleted at any time from your profile page.
2. Set the environment variable: `export OOSMETRICS_API_KEY=oosm_your_key_here`
3. The MCP server is installed via `npx @oosmetrics/mcp@1.0.1` and starts automatically when this skill is loaded. It communicates with the agent over stdio (no network ports opened locally).

## Tools

The available tools depend on your subscription tier. The server fetches the tool list from the oosmetrics API at startup, so Pro users see 7 tools and AI users see all 10.

### Pro + AI tier tools

**search** - Find repos by natural language query, language, or sort criteria.
**get_repo** - Get detailed metrics, grades, and description for a specific repo.
**compare** - Compare 2-5 repos side by side with full metrics.
**trending** - Get the hottest repos right now, optionally filtered by language.
**alternatives** - Find similar repos to a given one using embedding similarity.
**history** - Get historical metrics time series (stars, growth, acceleration over time).
**analyze** - Get or trigger an AI analysis of any repo (tech stack, health signals, alternatives, creative build ideas).

### AI tier only tools

**existence_check** - Describe a project idea, get back similar existing repos ranked by relevance.
**dependency_discovery** - Describe what you want to build, get recommended dependencies with health signals.
**license_check** - Check license compatibility for a list of dependencies.

## Example prompts

Use these as a guide for how to interact with the tools:

### Discovery
- "What are the fastest-growing Rust projects this week?"
- "Find me Python ML frameworks that are gaining traction"
- "Show me trending repos in Go"

### Research
- "Get the metrics for facebook/react"
- "Compare Express.js, Fastify, and Hono by growth and acceleration"
- "Show me the 90-day growth history for astral-sh/uv"
- "What are the best alternatives to Prisma?"

### Due diligence
- "Analyze denoland/deno - focus on ecosystem maturity"
- "Is there already a project like X? I want to build a real-time collaborative markdown editor"
- "Check the licenses for these deps: facebook/react, vercel/next.js, prisma/prisma"
- "What libraries can help me build a CLI tool for Kubernetes management?"

### Comparisons and decisions
- "I'm choosing between SQLx and Diesel for a new Rust project. Compare them."
- "Which React state management library has the best momentum right now?"
- "Compare the top 3 Python web frameworks by acceleration"

## Workflow patterns

### Evaluate a technology choice
1. Use `search` to find candidates in the domain
2. Use `compare` to see them side by side
3. Use `analyze` on the top pick for a deep dive
4. Use `history` to check if growth is sustained or a spike

### Check before you build
1. Use `existence_check` with your project description
2. If similar projects exist, use `get_repo` to understand their approach
3. Use `alternatives` to map the full landscape
4. Use `license_check` to verify compatibility

### Stay informed
1. Use `trending` to see what's hot globally or in your language
2. Use `search` with specific domains ("AI agent frameworks", "database engines")
3. Use `analyze` on anything that catches your eye
