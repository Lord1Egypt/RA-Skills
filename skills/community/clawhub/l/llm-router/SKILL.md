---
name: llm-router
description: 'Use AIsa for model routing, provider setup, and Chinese LLM access. Use when: the user needs model configuration, provider guidance, or routing workflows. Supports setup and model operations.'
author: AIsa
version: 1.0.0
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🤖
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 🤖
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# LLM Router

Use AIsa for model routing, provider setup, and Chinese LLM access. Use when: the user needs model configuration, provider guidance, or routing workflows. Supports setup and model operations.

## When to use

- The user needs model routing, provider setup, or Chinese LLM access.
- The user wants one place for provider configuration or model selection.
- The user wants setup guidance for AIsa-hosted model workflows.

## High-Intent Workflows

- Configure an AIsa provider path.
- Inspect supported models or routing options.
- Prepare a runtime for Chinese-model access.

## Quick Reference

- `python3 scripts/llm_router_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Prefer explicit CLI auth flags when a script exposes them.

## Example Requests

- Help me configure AIsa for Qwen
- List the supported routed models
- Choose a model for Chinese long-form analysis

## Guardrails

- Do not ask for extra credentials beyond the shipped flow.
- Do not advertise setup paths that the public bundle does not ship.
- Keep setup instructions aligned with the actual runtime.
