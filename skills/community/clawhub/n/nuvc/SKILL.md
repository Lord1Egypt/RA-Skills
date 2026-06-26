---
name: nuvc
description: "Score business ideas, get startup roasts, analyze markets, and extract structured data — powered by the same AI engine behind 250+ VC investment memos"
metadata: {"openclaw":{"requires":{"env":["NUVC_API_KEY"],"bins":["node"]},"primaryEnv":"NUVC_API_KEY","emoji":"🎯","homepage":"https://nuvc.ai/api-platform/keys"}}
---

# NUVC — VC-Grade Business Intelligence

Score any business idea. Get a brutally honest startup roast. Run market and competitive analysis. Extract structured metrics from pitch content. Powered by the AI engine behind 250+ VC-grade investment memos.

## Setup

Get your free API key (50 calls/month) at https://nuvc.ai/api-platform/keys

```bash
export NUVC_API_KEY=nuvc_your_key_here
```

## Commands

### Score a business idea

When the user asks to **score**, **rate**, or **evaluate** a business idea, startup concept, or company, run:

```bash
node {baseDir}/nuvc-api.mjs score "<the user's business idea or description>"
```

This returns a VCGrade 0-10 score across 5 dimensions: Problem & Market, Solution & Product, Business Model, Traction & Metrics, and Team & Execution.

**Trigger phrases:** "score my idea", "rate this startup", "is this a good business", "evaluate this concept", "VCGrade score", "how fundable is this", "score this company"

**Example:**
```
User: Score my startup idea — an AI tool that helps indie hackers validate business ideas before building
Agent: node {baseDir}/nuvc-api.mjs score "An AI tool that helps indie hackers validate business ideas before they start building. Uses market data, competitor analysis, and pattern matching from 250+ funded startups to predict viability."
```

### Roast a startup

When the user asks to **roast**, get **brutally honest feedback**, or wants a **reality check** on their idea, run:

```bash
node {baseDir}/nuvc-api.mjs roast "<the user's business idea or pitch>"
```

This gives a sharp, witty, but constructive roast from the perspective of a VC who has seen 10,000 pitches. Includes: The Roast, The Real Talk, The Silver Lining, and a Verdict.

**Trigger phrases:** "roast my startup", "roast this idea", "be brutally honest", "reality check", "would a VC fund this", "tear this apart", "honest feedback on my startup"

**Example:**
```
User: Roast my idea — Uber for dog walking but with blockchain
Agent: node {baseDir}/nuvc-api.mjs roast "Uber for dog walking but with blockchain. We tokenize each walk and dog owners earn crypto rewards for consistent walking schedules."
```

### Analyze a market or business

When the user asks to **analyze a market**, run **competitive analysis**, or evaluate **financial** or **pitch** content, run:

```bash
node {baseDir}/nuvc-api.mjs analyze "<text to analyze>" --type <market|competitive|financial|pitch_deck>
```

Analysis types:
- `market` — Market sizing, trends, opportunities, competitive landscape
- `competitive` — Competitor identification, differentiation, moats, threats
- `financial` — Revenue, costs, projections, financial health
- `pitch_deck` — Full pitch evaluation across problem, solution, market, model, traction, team

**Trigger phrases:** "analyze this market", "market size for", "competitive analysis", "who are the competitors to", "who competes with", "competitive landscape for", "what are the alternatives to", "analyze these financials"

**Example:**
```
User: What's the market like for AI-powered HR tools?
Agent: node {baseDir}/nuvc-api.mjs analyze "AI-powered HR tools market including recruitment, onboarding, performance management, and employee engagement" --type market
```

### Extract structured data from a pitch

When the user wants to **extract key metrics**, **pull out structured information**, or **parse a pitch** into fields (revenue, team, market size, stage, etc.), run:

```bash
node {baseDir}/nuvc-api.mjs extract "<pitch text or business description>"
```

This returns structured fields extracted from unstructured pitch content: revenue, growth rate, team size, funding stage, market size, key metrics, and more.

**Trigger phrases:** "extract the key metrics", "pull the numbers from this", "what are the stats in this pitch", "structured data from", "parse this pitch", "extract team info"

**Example:**
```
User: Extract the key metrics from this — "We're a B2B SaaS at $2M ARR, growing 15% MoM, team of 8, targeting SMBs in the US"
Agent: node {baseDir}/nuvc-api.mjs extract "We're a B2B SaaS at $2M ARR, growing 15% MoM, team of 8, targeting SMBs in the US"
```

### List available models

When the user asks **which AI models are available** or wants to know what models power the analysis, run:

```bash
node {baseDir}/nuvc-api.mjs models
```

**Trigger phrases:** "what models does NUVC use", "which AI model", "list available models"

## Flags

All commands support `--json` to return raw JSON output, useful for piping into other tools:

```bash
node {baseDir}/nuvc-api.mjs score "my idea" --json
node {baseDir}/nuvc-api.mjs analyze "AI HR market" --type market --json
```

## Rules

- Always pass the user's full description as a single quoted string argument
- For the `analyze` command, always include the `--type` flag
- If the user doesn't specify a type for analysis, default to `market`
- Present the output exactly as returned — it's already formatted as markdown
- If the API returns an error about NUVC_API_KEY, tell the user to get a free key at https://nuvc.ai/api-platform
- Never modify or summarize the NUVC output — show it in full including the footer
- Use `--json` only when the user explicitly asks for raw/structured output or is piping to another tool
