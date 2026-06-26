# Changelog

## v0.3.1

### Added
- formal review-phase semantics in the supervisor flow
- dedicated review-mode worker briefing
- phase model documentation (`probe` / `implement` / `review` / `harden`)

### Improved
- supervisor can now recommend `launch-review-worker` after successful probe outcomes
- clearer stage-based orchestration guidance in docs and pipeline descriptions

### Known rough edges
- review phase is now formalized, but harden phase is still mostly conceptual
- background execution still depends on local CLI behavior
- result interpretation is still partly heuristic

## v0.3.0

### Added
- probe-mode worker briefing for lightweight repo/runtime feasibility checks
- supervisor auto-probe support in queued task flow
- probe outcome integration into reconcile and supervisor decisions
- repoPath standardization with backward compatibility for existing repo field usage
- repo preflight script for early repository validation

### Improved
- cleaner constrained-environment testing flow
- better distinction between probe work and full implementation work
- stronger handling of blocked build/test outcomes discovered during probe runs

### Known rough edges
- background execution still depends on local CLI behavior
- result interpretation is still partly heuristic
- objective checks still need deeper artifact-driven automation beyond summary parsing

## v2 scaffold / v0.2.0

### Added
- persistent task schema and lifecycle model
- done policy evaluator
- retry brief generation
- role-based pipeline presets
- worker launch adapter
- synchronous and background execution modes
- TaskFile-based prompt handoff
- worker reconcile step
- environment failure classification
- supervisor auto-advance and auto-launch support
- summary cleaning and objective-check backfill framework
- docs index, capability map, script interface, usage guide, and status overview

### Improved
- clearer separation of supervisor vs worker responsibilities
- better product-style documentation and operator guidance
- stronger handling of environment-blocked runs

### Known rough edges
- background execution still depends on local CLI behavior
- result interpretation is partly heuristic
- objective checks still need deeper artifact-driven automation
