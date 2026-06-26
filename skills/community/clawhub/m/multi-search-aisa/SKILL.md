---
name: multi-search
description: "Run multi-source evidence gathering with confidence scoring across web, academic, Tavily, and synthesis layers via AISA. Use when: the user needs a comprehensive answer backed by multiple search sources instead of a single search pass."
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
# Multi Search

## When to Use

- Run multi-source evidence gathering with confidence scoring across web, academic, Tavily, and synthesis layers via AISA. Use when: the user needs a comprehensive answer backed by multiple search sources instead of a single search pass.

## When NOT to Use

- Do not use this skill for browser-cookie extraction, passwords, Keychain access, or other local sensitive credential access.
- Prefer a different skill when the user request is outside this skill's domain.

## Capabilities

- Aggregate multiple search sources into one confidence-scored answer.

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

- Research whether open-source coding agents improved in 2026 and cite multiple sources.

## Notes

- Invoke the Python client with the multi-search mode.
