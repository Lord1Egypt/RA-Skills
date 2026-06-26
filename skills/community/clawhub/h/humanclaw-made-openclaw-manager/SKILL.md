---
name: openclaw-manager
description: Install or operate a standalone local OpenClaw manager skill that adds shadow-first thread observation, durable session/run state, a loopback-only sidecar, attention management, snapshots, connector normalization, and capability reports for real work.
---

# OpenClaw Manager

Use this skill when the task is to operate, inspect, or extend the local OpenClaw Manager control plane.

## What this skill owns

- local `session / run / event / checkpoint / attention` state
- shadow-first `thread_shadow` observation and promotion queue
- append-only `events.jsonl` and `skill_traces.jsonl`
- local snapshot export
- connector normalization for Telegram, WeCom, Email, and GitHub
- capability graph and anonymized fact export
- standalone sidecar bootstrap and local command surface
- loopback-only sidecar by default
- consent-gated sidecar autostart

## Entry points

- bootstrap runtime: `src/skill/bootstrap.ts`
- local sidecar API: `src/api/server.ts`
- command registry: `src/skill/commands.ts`
- connector registry: `src/connectors/registry.ts`
- capability graph: `src/telemetry/capability-graph.ts`

## References

- architecture: `docs/architecture.md`
- session model: `docs/session-model.md`
- event schema: `docs/event-schema.md`
- connector protocol: `docs/connector-protocol.md`
- capability facts: `docs/capability-facts.md`
- security model: `SECURITY.md`
