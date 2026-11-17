# P0/P1 acceptance gate — DAVYLAB Knowledge Graph Skill 0.1.0

## P0 / source analysis
- [x] Repository architecture and source files mapped.
- [x] Hard/soft dependency semantics and diagnostic state model analyzed.
- [x] Licensing discrepancy and content-quality caveats recorded.
- [x] Independent implementation chosen; no upstream code/data copied.

## P1 / deliverable
- [x] `SKILL.md` contains triggers, workflow, commands, schema, guardrails.
- [x] Node.js, no third-party dependencies, portable engine and CLI.
- [x] Original AI-course demonstration with separate Design subject.
- [x] Validation rejects duplicates, dangling edges, self-edges, cycles, cross-subject edges.
- [x] Hard/soft ancestor paths, topological learning path, conservative diagnosis.
- [x] Regression tests for mastery threshold, immutability, scope and cause tracing.
- [x] Explicit human educational review and no question-answer scoring claims.

## Automated evidence
Run `node tests/engine.test.js` (18 tests) and 4 CLI commands listed in SKILL.md. All must exit zero. Demo `rootCauses` reflects unanswered prerequisites as untested rather than automatically weak.

## Exclusions (not P0/P1)
- No deployment to Academy / no production user data.
- No live end-to-end UI or classroom accuracy validation.
- No original cn-math-taxonomy data or question import.
- No claims of commercial licensing for upstream source.

**Exit:** P0 source-analysis gate passed. P1 local package/unit-test gate passed. Production integration gate is NOT claimed.
