# Operations and Performance

## First Performance Check

Use `ollama ps` to confirm processor split, context, and residency before changing anything else.
If the model is partially or fully on CPU, performance advice must change immediately.

## Practical Levers

Tune in this order:
1. smaller or better-fit model tag
2. lower context size
3. fewer concurrent requests
4. non-streaming only when needed
5. copied model alias or Modelfile with known-good defaults

Do not jump straight to "need a bigger GPU" until those levers are checked.

## Context and Parallelism

Higher context uses more memory. Higher parallelism multiplies that pressure.
If latency spikes or the host starts swapping, reduce `num_ctx`, reduce concurrency, or move to a smaller model before changing application logic.

## Service Hygiene

Before upgrades or service-manager changes:
- note current version and working model tags
- protect disk headroom before large pulls
- capture how Ollama is started now: foreground, app, Docker, or service manager
- keep one rollback path that returns to the last known-good setup

## Remote Access Guardrail

Remote access is an operational feature, not a default.
Do not change bind address, reverse proxy, or firewall policy until the user explicitly approves the exposure plan and understands the trust boundary.
