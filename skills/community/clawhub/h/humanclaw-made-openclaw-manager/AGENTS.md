# OpenClaw Manager Agents Guide

OpenClaw Manager is an OpenClaw-native local control plane.

The repo is organized around these layers:

- `src/skill/*`: OpenClaw-facing bootstrap, commands, and hooks.
- `src/api/*`: local sidecar API.
- `src/control-plane/*`: session/run/event/checkpoint/attention/share logic.
- `src/connectors/*`: source-specific normalization for Telegram, WeCom, Email, and GitHub.
- `src/telemetry/*`: skill traces, closure metrics, capability facts, and capability graph export.
- `src/storage/*`: filesystem-first durable state.

Implementation rules:

- keep durable state filesystem-first under `~/.openclaw/skills/manager/`
- keep raw chat transcripts local by default
- treat `ThreadShadow` as the observation layer and `Session` as the promoted work object
- treat `Session` as the primary work object and `Run` as a concrete execution attempt
- append facts to JSONL logs instead of rewriting history

When extending the repo:

- prefer adding structured state and event coverage before UI copy
- keep connector adapters source-specific rather than sharing a generic shim
- keep exports read-only and redacted by default
- avoid introducing SQLite or cloud-primary state as a prerequisite
