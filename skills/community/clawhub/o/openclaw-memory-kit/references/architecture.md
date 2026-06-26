# OpenClaw Memory Kit Architecture

## Goal

Turn a personal OpenClaw setup into a shareable, privacy-safe memory framework that another person can install without inheriting the original operator's secrets, bindings, or local machine paths.

## Core Layers

1. `memory-lancedb-pro`
   Store short, stable, structured memory.
   Typical payloads: preferences, decisions, reusable rules, stable facts, agent-specific lessons.

2. Markdown mirror
   Mirror structured memory into Markdown so the workspace remains inspectable and easy to back up or search.

3. Shared task board
   Use task files under `workspace/shared/tasks/` as the execution ledger for collaboration, dispatch, status changes, and proof of completion.

## Default Scope Design

- `global`
  Shared long-term knowledge for the whole team.
- `project:team-default`
  Shared project memory for the current workspace.
- `user:owner`
  Stable preferences and facts about the primary operator of the workspace.
- `agent:<id>`
  Private memory for a specific agent role.

Each role gets access to `global`, `project:team-default`, `user:owner`, and its own private `agent:<id>` scope.

## Role Model

The generated kit defaults to seven active roles:

- `coordinator`
- `engineer`
- `strategist`
- `writer`
- `analyst`
- `operator`
- `collector`

The lineup is role-based rather than person-based so it can be shared without exposing the source user's identity or naming conventions.

## Runtime Defaults

- isolated target root
- loopback gateway
- token auth
- memory search enabled
- hybrid recall enabled
- automatic memory flush enabled
- markdown mirror enabled
- optional channel integrations left disabled by default

## Why This Is Safe To Share

The generated kit deliberately removes:

- raw secrets
- source `.env` values
- private usernames and home directories
- live Feishu or Telegram bindings
- personal scope names
- private LAN endpoints
