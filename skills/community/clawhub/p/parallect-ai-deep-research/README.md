# Parallect Skill for OpenClaw

An [OpenClaw](https://openclaw.ai) skill that connects your autonomous agent to [Parallect.ai](https://parallect.ai) — a multi-provider deep research platform that queries Perplexity, Gemini, OpenAI, Grok, and Anthropic in parallel, then synthesizes results into a unified report with cross-referenced citations and conflict resolution.

## What it does

When installed, this skill teaches your OpenClaw agent to:

- **Run deep research** on any topic using multiple AI providers simultaneously
- **Manage budgets thoughtfully** — always discusses cost before spending your money
- **Poll asynchronously** — submits research, checks back with exponential backoff, and delivers results when ready
- **Present findings intelligently** — summarizes key insights first, then shares the full synthesis with citations
- **Suggest follow-ons** — offers next research directions from the synthesis engine
- **Track spending** — reports cost per query and cumulative session spend

## Quick Start

### 1. Get your API key

Sign up at [parallect.ai](https://parallect.ai) and go to **Integrations** (or **Settings > API Keys**) to create a key.

### 2. Install the skill

**Option A: ClawHub** (recommended)

```bash
clawhub install parallect
```

**Option B: Manual**

```bash
mkdir -p ~/.openclaw/skills/parallect/references
cp SKILL.md ~/.openclaw/skills/parallect/SKILL.md
cp references/*.md ~/.openclaw/skills/parallect/references/
```

### 3. Configure your API key

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "parallect": {
        "enabled": true,
        "env": {
          "PARALLECT_API_KEY": "par_live_YOUR_KEY_HERE"
        }
      }
    }
  }
}
```

### 4. Refresh OpenClaw

Ask your agent to "refresh skills" or restart the gateway.

## Usage

Just talk to your agent naturally:

- "Research the latest advances in quantum computing"
- "Deep dive on the competitive landscape for AI code editors"
- "Look up what's happening with CRISPR gene therapy clinical trials"
- "Find out about the regulatory implications of autonomous vehicles in the EU"

The agent will check your balance, discuss budget, submit the research, poll for results, and deliver a synthesis with citations.

## How it works

```
You: "Research X"
  │
  ▼
Agent checks balance ──→ Discusses budget tier with you
  │
  ▼
Agent calls research(query, tier) ──→ Gets jobId
  │
  ▼
Agent polls research_status(jobId) ──→ Reports progress
  │                                      "2 of 3 providers done..."
  ▼
Agent calls get_results(jobId) ──→ Delivers synthesis
  │
  ▼
Agent presents follow-on suggestions ──→ You pick one (or ask your own)
```

## Budget Tiers

| Tier | Max Cost | Providers | Best for |
|------|----------|-----------|----------|
| XXS | ~$1 | 1 | Quick factual lookups |
| XS | ~$2 | 1-2 | Brief overviews |
| S | ~$5 | 2 | Standard questions |
| M | ~$15 | 3-4 | Detailed research (default) |
| L | ~$30 | 4-5 | Comprehensive analysis |
| XL | ~$60 | All | Exhaustive multi-provider |

The agent will suggest an appropriate tier based on your question's complexity and confirm before spending.

## MCP Tools

This skill uses Parallect's hosted MCP server at `https://parallect.ai/api/mcp/mcp` with 9 tools:

| Tool | Purpose |
|------|---------|
| `research` | Submit a research query (async) |
| `research_status` | Poll job progress |
| `get_results` | Retrieve completed synthesis |
| `follow_up` | Pursue follow-on questions |
| `list_threads` | List recent research threads |
| `get_thread` | Get full thread context |
| `balance` | Check credit balance |
| `usage` | View spend analytics |
| `list_providers` | See available providers and tiers |

## Skill Frontmatter

The SKILL.md uses standard AgentSkills fields (`name`, `description`) plus OpenClaw-specific extensions:

| Field | Purpose |
|-------|---------|
| `user-invocable: true` | Tells OpenClaw this skill can be triggered by natural language, not just explicit tool calls |
| `metadata.openclaw.emoji` | Display icon in OpenClaw's skill list |
| `metadata.openclaw.primaryEnv` | Identifies the primary environment variable for setup prompts |
| `metadata.openclaw.requires.env` | OpenClaw validates these env vars are set before enabling the skill |

## Links

- [Parallect.ai](https://parallect.ai) — Dashboard, billing, research history
- [MCP Docs](https://parallect.ai/docs/mcp/overview) — Full MCP server documentation
- [API Reference](https://parallect.ai/docs) — REST API and tool reference

## License

MIT
