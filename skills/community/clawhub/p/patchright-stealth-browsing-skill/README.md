# Patchright OpenClaw Skill

This directory contains the instruction skill manual for the OpenClaw agent. It guides the LLM on how and when to invoke the stealth browser tools, and provides guidelines for remaining undetected.

---

## File Contents

* [SKILL.md](file:///save_data/projects/patch-right-extended/skill/SKILL.md): Declares the OpenClaw skill manifest header, YAML metadata, and core instruction prompts.

---

## Skill Configuration Metadata

The skill header defines execution dependencies:

```yaml
---
name: patchright-stealth-browsing
description: Perform stealth browser automation to bypass bot detection (Cloudflare, Akamai, Datadome) using Patchright.
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
---
```

* **`requires.bins`**: Requires `node` to be installed and available in the execution path, since the underlying MCP server runs on a Node runtime.

---

## Usage

When OpenClaw loads this skill, the guidelines in `SKILL.md` are appended to the agent's system prompt or tool-usage instructions. It teaches the agent:
1. To use the consolidated `patchright_*` toolset for protected target URLs.
2. How to bypass isolated context variable limitations using DOM state tracking.
3. How to perform optimized inputs via `bulk_fill` and wait synchronizations via `wait_for`.
4. Graceful handling of anti-bot blockers, capthas, or timeouts.
