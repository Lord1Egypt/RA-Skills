---
name: perplexity-research
description: "Produce citation-backed deep research answers through Perplexity Sonar models via AISA. Use when: the user needs synthesized research, comparative analysis, or long-form cited answers instead of raw link lists."
author: aisa
version: "1.0.0"
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  env:
    - AISA_API_KEY
  bins:
    - python3
metadata:
  openclaw:
    primaryEnv: AISA_API_KEY
    requires:
      env:
        - AISA_API_KEY
      bins:
        - python3
---
# Perplexity Research

## When to Use

- Produce citation-backed deep research answers through Perplexity Sonar models via AISA. Use when: the user needs synthesized research, comparative analysis, or long-form cited answers instead of raw link lists.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Generate cited research answers with configurable Sonar model depth.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Primary Runtime

Use the bundled Python client as the canonical ClawHub runtime path:

```bash
python3 scripts/search_client.py
```

## Example Queries

- Research global AI regulation trends and return a cited summary.

## Notes

- Best when synthesis matters more than raw result recall.
