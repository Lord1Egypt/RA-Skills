---
name: MCP Token Auditor
description: Analyze your MCP server config to estimate token consumption per tool. Identify which tools are blowing up your context window, get per-role groupings to keep subagents under the limit, and generate optimized role-specific MCP configs.
version: 1.0.0
author: abhinas90
tags: [mcp, claude-code, token-optimization, subagent, context-window]
price: 29
category: developer-tools
---

# MCP Token Auditor

**Stop your subagents from silently failing due to tool schema bloat.**

If you have 20+ MCP servers, your tool schemas alone can hit 209k tokens — exceeding Claude's context window before your subagent even starts working. The subagent dies. Silently. Zero error in the UI.

This tool audits your MCP config and gives you an exact breakdown.

## What it does

1. Reads your `mcp.json` (or any MCP config)
2. Estimates token consumption per tool based on schema complexity
3. Groups tools into logical roles (code-analysis, deployment, testing, data, communication, file-system)
4. Calculates total token footprint vs your target limit
5. Outputs per-role groupings you can copy directly into role-specific MCP configs

## Quick start

```bash
# Basic audit
python3 mcp-token-audit.py --config ~/.claude/mcp.json

# With custom token target (default: 60,000)
python3 mcp-token-audit.py --max-tokens 50000

# JSON output for scripting
python3 mcp-token-audit.py --json
```

## Example output

```
═══════════════════════════════════════════
  MCP TOKEN AUDIT REPORT
═══════════════════════════════════════════
  Config: ~/.claude/mcp.json
  Servers: 34
  Total tools: 566
  Total estimated tokens: 209,412
  Target limit: 60,000
  Utilization: 349.0%

───────────────────────────────────────────
  PER-ROLE BREAKDOWN
───────────────────────────────────────────
  communication      42,891 tokens  █████████████████████
  deployment         38,221 tokens  ███████████████████
  code-analysis      35,120 tokens  █████████████████
  data               28,450 tokens  ██████████████
  testing            24,310 tokens  ████████████
  general            40,420 tokens  ████████████████████

  🔴 Total tool schema tokens exceed target by 149,412 tokens
     Fix: Split MCP servers into per-role configs

───────────────────────────────────────────
  SUGGESTED ROLE GROUPINGS
───────────────────────────────────────────
  communication (mcp-communication.json) — 42,891 tokens ✅
  deployment (mcp-deployment.json) — 38,221 tokens ✅
  code-analysis (mcp-code-analysis.json) — 35,120 tokens ✅
  ...
```

## Why this matters

The #1 silent failure mode in multi-agent Claude Code setups isn't model quality. It's tool schema bloat. When your subagent's context window is 60% full before it even processes your prompt, you get: silent hangs, partial completions, and "prompt too long" errors with no diagnostic.

This tool catches the problem before your subagent crashes.

## Prerequisites

- Python 3.8+
- An MCP config file (works with any MCP-compatible format)
- No API keys required — runs entirely locally

## Files

- `scripts/mcp-token-audit.py` — Main audit script
- `SKILL.md` — This file