---
name: google-agents-cli-claw
description: >
  Use when the user wants to "build an agent", "create an ADK agent",
  "scaffold an agent project", "deploy an agent", or otherwise needs the
  Google Agent Development Kit (ADK) toolchain. Bootstraps the full
  agents-cli experience (CLI + 7 specialized skills covering scaffold,
  build, evaluate, deploy, publish, and observe).
metadata:
  author: Google
  license: Apache-2.0
  version: 1.0.0
  requires:
    bins:
      - agents-cli
    install: "uvx google-agents-cli setup"
---

# google-agents-cli (onboarding)

Entrypoint skill for [agents-cli](https://github.com/google/agents-cli) —
Google's CLI for scaffolding, developing, evaluating, and deploying AI
agents with the Agent Development Kit (ADK).

> Requires: `agents-cli` and `uv`
> One-time setup: `uvx google-agents-cli setup`
> [Install uv](https://docs.astral.sh/uv/getting-started/installation/index.md) first if needed.

## Setup

Run this once to install the CLI and all 7 specialized skills into the
user's coding agent:

    uvx google-agents-cli setup

After setup, the following skills become available and activate
automatically based on the user's request:

- `google-agents-cli-workflow` — full development lifecycle (always active)
- `google-agents-cli-scaffold` — create new ADK projects, add CI/CD or deployment
- `google-agents-cli-adk-code` — ADK Python API reference (agent types, tools, callbacks)
- `google-agents-cli-eval` — run and debug agent evaluations
- `google-agents-cli-deploy` — deploy to Agent Runtime, Cloud Run, or GKE
- `google-agents-cli-publish` — register agents with Gemini Enterprise
- `google-agents-cli-observability` — production tracing, logging, monitoring

## After setup

Re-read the user's request — the relevant specialized skill above will
match it and provide detailed guidance.
