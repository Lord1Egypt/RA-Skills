# local-coding-orchestrator status

> Experimental v2 scaffold. Publishable for advanced users, but not yet a stable autonomous production orchestrator.

## Current maturity

The skill is in an advanced scaffold stage.
It has real orchestration components, but still needs hardening before fully autonomous production use.

## Implemented

- task schema and example
- task lifecycle/state machine
- done policy evaluator
- retry brief generation
- pipeline preset resolver
- worker launch preview
- synchronous worker execution adapter
- background worker launch metadata
- TaskFile-based prompt handoff
- background worker reconcile step
- environment failure classification
- supervisor auto-advance recommendations
- supervisor auto-launch support in safe cases
- supervisor auto-probe support for constrained repo/runtime validation
- early review-phase formalization with dedicated review-mode briefing
- repoPath standardization with backward compatibility for existing repo field usage
- stage-based execution model emerging across probe / implement / review / harden

## Still rough

- process/session tracking is not yet unified on OpenClaw process handles
- background reconcile uses lightweight heuristics
- objective checks now support limited backfill from worker summaries, but still need deeper artifact-driven automation
- some wrappers still inherit local CLI quirks and environment assumptions

## Recommended next hardening items

1. use OpenClaw process/session ids in workerRun where possible
2. enrich objective checks from actual command results
3. normalize result parsing and summaries
4. tighten worker completion classification
5. separate implementation workers from review workers more explicitly
