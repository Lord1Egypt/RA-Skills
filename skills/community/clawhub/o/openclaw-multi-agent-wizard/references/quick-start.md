# Quick Start

Use this file when you need a compact, install-ready summary of how the wizard should behave.

## What this skill is

This skill is a beginner-friendly installation wizard for OpenClaw multi-agent.

Its job is not to teach the user OpenClaw internals. Its job is to help the user finish setup with the least confusion possible.

## The two main paths

### Path 1: `多 bot 多 agent`

Use this when the user wants:

- one bot for work
- one bot for life
- one bot per assistant

Best default for beginners.

### Path 2: `单 bot 多 agent`

Use this when the user wants:

- one Feishu bot
- different assistants in different Feishu groups

V1 supports only group-based routing.

## The advanced path

### Path 3: `A2A collaboration`

Use this when the user wants:

- one main assistant to talk publicly
- one or more specialist assistants to help in the background

Recommended Feishu pattern:

- one public main agent
- background worker agents

## Core success rule

Do not build too much at once.

For high success:

- one bot at a time
- one group at a time
- one small config addition at a time
- verify before moving on
- if the user is lost in Feishu, anchor on visible page titles or left-side menu labels

## The default run order

1. preflight
2. recommend a mode
3. collect the minimum inputs
4. create or confirm one agent
5. auto-suggest a persona kind from the agent name
6. write the starter profile files for that agent
7. guide one Feishu app setup
8. bind one route
9. restart if needed
10. verify
11. summarize

If there are more agents, bots, or groups, repeat the same pattern instead of doing everything in parallel.

## The default beginner recommendation

If the user is unsure:

- recommend `多 bot 多 agent`

If the user wants one shared Feishu bot:

- recommend `单 bot 多 agent`
- but start with only one target group

If the user asks for collaboration between agents:

- recommend the A2A pattern where one main agent speaks and worker agents help privately

## The default persona rule

If the agent name already strongly suggests a role:

- infer the starter persona kind automatically
- do not ask the user to choose unless the name is ambiguous
- for A2A worker names, also recognize obvious specialist roles like `data`, `writing`, `project`, and `research`

## The one sentence promise

When the user is anxious or overwhelmed, anchor on this:

- "You do not need to understand the technical details. I will guide you one small step at a time."
