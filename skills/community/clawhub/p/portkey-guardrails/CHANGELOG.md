# Changelog — portkey-guardrails

## v1.0.0 — 2026-04-03

Initial release.

- G-01: Prompt injection detection (block)
- G-02: PII leakage prevention — AU-first (redact)
- G-03: Off-scope response filter (flag)
- G-04: Budget guard — reads BUDGET.json (block)
- G-05: Context length guard (warn)
- Declarative per-agent YAML config layer with schema validation and live-reload watcher
- Semantic cache (nomic-embed-text via Ollama + SQLite) with graceful degradation
- Per-agent guardrail overrides via agent-config.yaml
- Audit logging to markdown per agent
- Fail-open hook design — gateway continues if module unavailable
- Live production validation: deployed on OpenClaw gateway (2026-04-03)
