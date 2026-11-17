# Completion Criteria

Declare success only after the layers relevant to the requested outcome have passed. An earlier layer cannot substitute for a later one.

## Acceptance Layers

1. **Invocation:** the intended command or request was submitted with the reviewed target and inputs.
2. **Task:** the OBD task or asynchronous product task reached a successful terminal state. A caller exit or timeout is not the task state. A trace is correlated log evidence, not a state machine and not proof of success by itself; reconcile an interrupted caller through the shared failure workflow.
3. **Control plane:** registered configuration, deployment/component/tenant state, and actual artifact identity match the plan.
4. **Runtime:** intended processes, listeners, paths, service manager units, or containers exist; objects that should be stopped or removed do not.
5. **Data plane:** an authenticated SQL, HTTP/API, metrics, backup-catalog, replication, or test-result check proves the requested capability. When SQL supplies the evidence, follow [version-adaptive SQL evidence](sql-evidence.md) rather than assuming a variable, view, or column exists.
6. **Isolation:** unselected objects remain unchanged and no unexplained residual object or task remains.

Use only the applicable layers, but explicitly mark a skipped layer and why it is not needed.

## Report Verdict Vocabulary

When a test, audit, or operation report uses uppercase verdicts, apply them consistently:

- **`UNSUPPORTED`:** installed public help/schema and the version-matched plugin/workflow prove that the exact operation is absent, or the standard repository probe conclusively proves that no compatible artifact exists for the resolved product/version/platform. A disabled, stale, inaccessible, or incompletely probed repository is not unsupported.
- **`BLOCKED`:** every safe, authorized, in-scope probe and compatible alternative has been completed, but an external condition such as network access, credentials, missing authorization, unavailable TTY, or conflicting live state prevents continuation. Name the blocking condition and completed probes.
- **`FAIL`:** a supported path exists but the attempted behavior, required acceptance layer, or test procedure does not meet the expected result. Skipping a required safe probe and then stopping is an incomplete or failed test execution, not blocked.
- **`PASS`:** every acceptance layer applicable to the exact case succeeds. If cleanup is part of the test case, its selected-object removal and retained-object checks must also succeed; command exit alone never passes a case.

`partial` and `unknown` remain valid observed states while a mutation or asynchronous task is being reconciled, but neither can be promoted to `PASS`. The final report must preserve that uncertainty or resolve it to the vocabulary above without relabeling an omitted probe as a product limitation.

## Common Lifecycle Outcomes

| Operation | Required outcome |
|---|---|
| Deploy | exact artifacts and registered configuration; verified `deployed` state for an ordinary deploy; require processes, listeners, and data-plane readiness only when the authorized operation also includes start |
| Start | every selected target running; dependencies healthy; representative data-plane check |
| Stop | every selected target stopped; listeners closed; unselected targets unchanged |
| Restart | stop/start transition completed for selected targets; runtime identity is new where expected; data plane recovered |
| Reload/configure | registered, generated, and effective runtime values agree; restart-required values are not reported as dynamically applied |
| Upgrade/reinstall | actual per-node artifact version/release/hash matches the target; mixed versions are only those allowed by the reviewed path; data plane remains usable |
| Add/remove Observer servers from an existing deployment | `UNSUPPORTED`; make no mutation. Product-side topology change with stale OBD registration is `partial`/`FAIL`, never `PASS` |
| Component add/delete | registration and runtime agree with the new topology; deletion verifies `config.yaml`, `inner_config.yaml`, dependencies, processes, listeners, paths, component data plane, and retained data, with no unexplained residual reference or service |
| Destroy/drop/overwrite | the exact authorized runtime/data object is absent or replaced; separately owned or external data is preserved unless explicitly included; expected retained parent directories, controller registration, traces, and package repositories are reported separately from unexpected residue |

## Domain Additions

Domain workflows must add their own proof:

- tenants: login with the intended credential, topology/resources, allowlist, role, or restored data;
- backup/restore: terminal task, manifest/catalog identity, SCN/time coverage, and representative restored data;
- monitoring: exporter metric, Prometheus target/query, Grafana datasource/dashboard, and alert delivery when requested;
- OCP: process, authenticated API/UI, MetaDB, terminal background task, and correct managed-cluster identity;
- benchmarks: required phases, result files, failure counts, metrics, and post-test database health;
- diagnostics: artifact integrity and independently corroborated findings.

Report `partial`, `not completed`, or `unknown` when a required layer is missing. Never collapse a mixed state into a single healthy status.
