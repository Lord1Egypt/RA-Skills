---
name: qwen-delegation
description: Delegates tasks to Qwen CLI via delegation-core for Alibaba's models
version: 1.9.8
triggers:
  - qwen
  - cli
  - delegation
  - alibaba
  - large-context
  - delegation-core selects Qwen or large-context batch processing is needed
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/conjure", "emoji": "\ud83e\udd9e", "requires": {"config": ["night-market.delegation-core"]}}}
source: claude-night-market
source_plugin: conjure
---

> **Night Market Skill** — ported from [claude-night-market/conjure](https://github.com/athola/claude-night-market/tree/master/plugins/conjure). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Smart Delegation](#smart-delegation)
- [Qwen-Specific Details](#qwen-specific-details)


# Qwen CLI Delegation

## Overview

This skill implements `conjure:delegation-core` for the Qwen CLI.
It provides Qwen-specific authentication, quota management,
and command construction.

For shared delegation patterns, see `Skill(conjure:delegation-core)`.

## When To Use

- After `Skill(conjure:delegation-core)` determines Qwen is suitable
- When you need Qwen's large context window (100K+ tokens)
- For batch processing, summarization, or multi-file analysis
- If the `qwen` CLI is installed and configured

## Prerequisites

**Installation:**
```bash
# Install Qwen CLI
pip install qwen-cli

# Verify installation
qwen --version

# Check authentication
qwen auth status

# Login if needed
qwen auth login

# Or set API key
export QWEN_API_KEY="your-key"
```
**Verification:** Run `python --version` to verify Python environment.

## Quick Start

### Using Shared Delegation Executor
```bash
# Basic file analysis
python ~/conjure/tools/delegation_executor.py qwen "Analyze this code" --files src/main.py

# With specific model
python ~/conjure/tools/delegation_executor.py qwen "Summarize" --files src/**/*.py --model qwen-max

# With output format
python ~/conjure/tools/delegation_executor.py qwen "Extract functions" --files src/main.py --format json
```

### Direct CLI Usage
```bash
# Basic command
qwen -p "@path/to/file Analyze this code"

# Multiple files
qwen -p "@src/**/*.py Summarize these files"

# Specific model
qwen --model qwen-max -p "..."
```

### Save Output
```bash
qwen -p "..." > delegations/qwen/$(date +%Y%m%d_%H%M%S).md
```

## Smart Delegation

The shared delegation executor can auto-select the best service:
```bash
# Auto-select based on requirements
python ~/conjure/tools/delegation_executor.py auto "Analyze large codebase" \
  --files src/**/* --requirement large_context
```

## Qwen-Specific Details

For Qwen-specific models, CLI options, cost reference,
and troubleshooting, see `modules/qwen-specifics.md`.
