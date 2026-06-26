# v2 summary

`local-coding-orchestrator` has been upgraded from a local tool router into a v2 orchestration scaffold.

## What changed conceptually

Before:
- route a task to Codex, Claude Code, or OpenCode
- collect or compare outputs

Now:
- persist task records
- supervise lifecycle transitions
- launch workers with structured briefs
- reconcile background runs
- classify environment failures
- generate retry briefs
- evaluate done policies
- recommend or apply next orchestration steps

## What exists now

- task ledger and schema
- lifecycle state machine
- objective check evaluation
- role-based pipelines
- worker launch adapters
- background worker metadata
- worker reconcile loop
- environment-aware blocking
- dedicated probe-mode execution path
- partial objective-check backfill from worker summaries
- docs and interface guide for continued iteration

## What still needs hardening

- stronger session/process integration with OpenClaw-native handles
- richer parsing of build/test/review outcomes
- better background completion signals
- less heuristic result interpretation

## Bottom line

The skill is now best understood as a local orchestration runtime scaffold, not just a routing helper.
