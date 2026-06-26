# Mentor Evolution Engine

## Improvement Detection
Detect from journal trends: high retry rate, low OKR performance, rising latency, poor model pairing, recurring bottlenecks, unstable decision quality.

## Proposal Generation
Each proposal follows the VariantProposal schema from spec-ocas-shared-schemas.md. Fields: target skill, base version, observed problem, evidence, proposed changes, expected improvement, evaluation plan, minimum runs, critical non-regression conditions.

Write proposals to: `~/openclaw/data/ocas-forge/intake/{proposal_id}.json`

## Promotion Criteria
Promote when: sufficient runs completed, aggregate scores exceed champion, no non-regression failures. Continue testing if inconclusive. Archive if consistently worse.

Write decisions to: `~/openclaw/data/ocas-forge/intake/{decision_id}.json` using VariantDecision schema from spec-ocas-shared-schemas.md.

See spec-ocas-interfaces.md for full handoff contracts.

## Self-Improvement
Mentor analyzes its own orchestration journals. May improve: task decomposition heuristics, dependency ordering, retry policy, skill routing preferences, evaluation thresholds, heartbeat cadence.
