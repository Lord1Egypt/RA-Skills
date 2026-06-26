# Architecture

OpenClaw Manager is split into seven cooperating layers:

1. `src/skill/*`
   - OpenClaw-facing bootstrap, commands, and hooks
   - consent-gated sidecar startup checks, background maintenance, and skill wrappers
2. `src/api/*`
   - local loopback-only sidecar API by default
   - canonical ingress for thread shadows, sessions, connector updates, digests, and focus views
3. `src/control-plane/*`
   - `ThreadShadow` observation and promotion
   - `Session` and `Run` lifecycle
   - event log writes
   - checkpoint restore
   - attention scoring and snapshot orchestration
4. `src/storage/*`
   - filesystem-first durable state
   - append-only JSONL logs and generated indexes
5. `src/connectors/*`
   - source-specific adapters for Telegram, WeCom, Email, and GitHub
   - normalized inbound message generation
   - connector config and thread binding support
6. `src/telemetry/*`
   - skill traces
   - closure metrics
   - scenario signatures
   - capability facts
   - capability graph summary and anonymized export
7. `src/exporters/*`
   - snapshot HTML export
   - markdown reports for sessions, digests, and capability reports
