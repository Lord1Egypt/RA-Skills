# Task-Type Profiles

Keep the package structure stable, but interpret implementation and validation according to the task type.

## 1. Bug repair

Include:

- minimal failure reproduction;
- root cause and affected call chain;
- frozen correct behavior;
- smallest repair;
- positive, negative, and regression validation;
- direct comparison with the original failure evidence.

Keep negative cases within the supported call path, documented input boundary, observed failure family, or material security/recovery risk. Do not turn unrelated parser or resource-exhaustion hardening into the repair.

Avoid vague items such as “fix code and run tests.”

## 2. Feature or refactor

Include:

- current and target behavior;
- invariants and compatibility or migration policy;
- model, service/API, caller, and documentation impact;
- closed implementation slices;
- behavior-preservation and new-capability validation;
- stale-symbol and stale-entry-point audit.

Review architectural and business invariants before defensive edge cases. Extreme malformed inputs outside the public contract are optional follow-up unless the feature explicitly owns them.

## 3. Test construction

Include:

- risk or evidence gap;
- fixture, oracle, isolation, and reproducibility;
- why the test reaches the target branch;
- expected failing and passing evidence;
- flakiness, environment dependencies, and time budget;
- independent review of the test itself.

## 4. Research and design

Include:

- question and decision objective;
- source version, commit, provenance, and evidence priority;
- common investigation matrix;
- separation of facts, inferences, recommendations, and open questions;
- reproducible scripts, queries, or samples;
- how conclusions feed later design gates.

Research completion does not imply implementation.

## 5. Complex run, experiment, or canary

Include:

- exact code, configuration, model, and provider baseline;
- run root, ports, processes, credential inheritance, and no-touch scope;
- preflight, admission or lease, monitoring, stop gates, and resume entry;
- per-stage observation, trace, and checkpoint evidence;
- success, blocked, failed, and aborted criteria;
- cleanup and complete archival of runtime, toolkit, workflow, and metadata—not source output alone.

The Reviewer inspects raw evidence rather than only the run summary.

## 6. Migration or operations

Include:

- exact target and destructive boundary;
- dry-run, backup, apply, and validation;
- idempotence and recovery;
- old/new schema acceptance policy;
- authorization for external-state changes;
- rollback or explicit irreversibility.

## 7. Documentation or policy

Include:

- documentation truth sources;
- target audience and navigation;
- consistency with current implementation and runtime facts;
- link, terminology, status, and duplication audit;
- protection against presenting future plans as current capability.

## 8. Mixed work

Select a profile per part. A research-to-design-to-implementation-to-canary task should have four dependent parts with distinct evidence and review criteria rather than forcing code-development language onto every item.
