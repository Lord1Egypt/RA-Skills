# OwlCoda RunKit Contract v0.2

Status: implementation candidate for repository-owned Core conformance

Date: 2026-07-13

Supersedes for new executions: [Contract v0.1](./OWLCODA_RUN_KIT_CONTRACT_V0_1.md)

## Purpose

Contract v0.2 hardens acceptance evidence. It keeps the project—not a chat
window, agent memory, or external dashboard—as the system of record, while
closing three gaps proven by Run008:

- an `accepted` closeout could be written without consuming a passing gate;
- source freshness did not prove verification-environment freshness;
- a descriptive shell or GUI label could be accepted without a replayable
  invocation description.

Contract v0.1 remains the historical interpretation contract for existing
artifacts. New accepted closeouts must use v0.2.

## Inherited principles

Contract v0.2 retains the v0.1 source fingerprint, safe path, profile impact,
append-only lineage, foreign-project zero-write, and explicit authorization
rules. In particular:

- `.owlcoda/runkit/**` is runtime truth and never product source;
- one execution pins one Core identity;
- uncovered change fails closed;
- stale source stops verification before command execution;
- only one active receipt leaf is valid;
- configuration and closeout state do not grant Git or release authority.

## D8: gate-bound accepted closeout

`closeout --decision accepted` must consume a Contract v0.2 gate input and
recompute the gate. A caller-supplied `accepted` string or a saved gate-output
summary is insufficient.

The recomputed gate must prove:

- `decision=accepted_passed`;
- one valid receipt lineage with one active leaf;
- the active receipt `runId` equals the execution being closed;
- the active receipt binds the current source fingerprint;
- the active receipt binds the current verification-context fingerprint;
- selected profile IDs match exactly;
- every command receipt uses replayable evidence and exited successfully;
- at least one writer lease exists and every lease is released.

The accepted closeout payload binds:

- Contract version;
- gate decision;
- gate-input file SHA-256;
- active receipt SHA-256;
- source fingerprint;
- verification-context fingerprint;
- selected profile IDs;
- released lease IDs;
- `authorizationGranted=false`.

`blocked` and `rejected` closeouts may be recorded without a passing gate so
failed work can still leave durable truth. They remain non-authoritative for
Git, release, publish, deploy, credential use, deletion, or foreign writes.

## D9: VerificationContextV1

Source equality alone is not enough to reuse verification. Contract v0.2 adds
`OwlCodaRunKitVerificationContextV1` and a canonical SHA-256 fingerprint kept
separate from the product source fingerprint.

The context contains:

- `reusePolicy`;
- material platform identity when bound;
- toolchain names and versions;
- lockfile paths and hashes;
- fixture identities and hashes;
- service identities;
- secret-safe environment value hashes.

Arrays are canonicalized by their canonical JSON value, object keys are sorted,
and duplicate primary identities are invalid. Raw secret values are forbidden;
only declared value hashes may enter the context.

### Reuse policies

- `portable`: platform is `null`; the receipt may be reused only when the full
  remaining context fingerprint matches.
- `platform_bound`: `platform.os` and `platform.arch` are required.
- `environment_bound`: platform is required and at least one fixture, service,
  or environment identity must be present.

A receipt whose declared context fingerprint differs from the recomputed
current context is rejected even when source files are unchanged.

## D10: replayable evidence

Every v0.2 command receipt contains
`OwlCodaRunKitReplayableEvidenceV1`. A natural-language command label is not
acceptance evidence.

Common required fields are:

- evidence kind: `shell` or `automation`;
- exact working directory;
- launcher executable and version;
- material tool versions;
- material input IDs and SHA-256 values;
- output artifact paths and SHA-256 values;
- command exit code plus stdout/stderr SHA-256 on the enclosing receipt.

Shell evidence additionally requires the exact argv array. It must not rely on
an ambiguous reconstructed command string.

Automation evidence additionally requires an automation-manifest SHA-256 and at
least one output artifact. The manifest may describe Computer Use, CDP,
Playwright, Electron, browser, or another deterministic runner, but acceptance
consumes its hash and outputs rather than a prose summary.

## Artifact chain

```text
GoalContract
  -> ExecutionPlan + engine pin
  -> WorkerLease
  -> ExecutionDeliveryPacket
  -> source gate + profile impact
  -> VerificationContextV1
  -> VerificationReceiptV2 + replayable evidence
  -> accepted_passed gate
  -> gate-bound CloseoutReceiptV2
```

## Compatibility

- v0.1 delivery fingerprints, profile resolution, and receipt lineage remain
  readable and retain their historical meaning.
- A closed execution is inspected against the immutable Core identity in its
  closeout receipt. Only an active execution is compared with the currently
  installed Core, so active engine drift still fails closed without making
  closed history unreadable.
- A v0.1 gate may still be inspected, but it cannot authorize a v0.2 accepted
  closeout.
- New project initialization writes `OwlCodaRunKitConfigV2` and pins Core
  `0.3.0`.
- Initialization upgrades a known V1 project config or an older v0.2 Core
  patch identity by atomically replacing `config.json` and writing an
  authorization-free local migration receipt. Unknown config versions fail
  closed and are not rewritten.
- Core artifacts emitted by the current Core use `RunKitCoreArtifactV2`;
  validators may still inspect historical V1 artifacts.

## Exit behavior

- accepted closeout with a complete current v0.2 gate: exit `0`;
- missing, rejected, mismatched, legacy, or lease-incomplete accepted gate:
  `closeout_gate_rejected`, exit `2`;
- malformed CLI input or unreadable JSON: `invalid_input`, exit `3`;
- active execution engine drift or an invalid historical closeout: inspect
  exit `2`;
- rejected or blocked record closeout: exit `0`, without acceptance binding.

## Authorization boundary

Accepted is not authorized. A valid v0.2 closeout records the control decision
for one source/context/profile combination. It does not authorize stage,
commit, push, tag, publish, deploy, delete, credential use, telemetry, or
foreign-project writes. Those actions require separate explicit authority.

## Core v0.3 provenance commands

Core `0.3.0` implements the first project-owned provenance workflow on top of
Contract v0.2:

- `runkit snapshot` records an exact executable/argv/cwd invocation, immutable
  stdout/stderr bytes and hashes, VerificationContext fingerprint, selected
  source manifest, and Git HEAD/status before and after. RunKit runtime paths
  are excluded from observed product status so evidence writes do not
  self-invalidate. Foreign mode is read-only and target drift fails closed.
- `runkit finalize` validates the current DeliveryPacket before consuming
  snapshots, recomputes profile impact, verifies replayable evidence and output
  hashes, appends receipt lineage, and emits the gate input/output.
- `runkit ready-for-commit` requires a fresh DeliveryPacket, accepted gate-bound
  closeout, released leases, and fresh selected root manifests. Its receipt
  keeps every Git/release action and authorization flag false.

These commands make the normal path tool-owned instead of hand-authored:

```text
snapshot
  -> finalize
  -> explicit accepted closeout
  -> fresh root snapshot
  -> ready-for-commit
```

## Core v0.4 recovery inspection

Core `0.4.0` makes `runkit inspect` the session-independent recovery entrypoint.
The top-level recovery summary distinguishes zero, one, and multiple active
executions. It selects a run only when exactly one active execution exists and
otherwise returns an explicit `plan_new_execution` or
`select_active_execution` action.

Every execution also reports a recovery view over the existing artifact
contract:

- validated engine-pin and closeout state;
- active and released worker leases;
- current DeliveryPacket freshness against the working tree;
- active receipt lineage and the one matching accepted gate;
- evidence trust level, issues, and one next allowed action.

Inspection does not infer acceptance from file presence. Multiple active runs,
malformed active artifacts, stale delivery, ambiguous packets or gates, and a
passed receipt without a recorded writer lease fail closed with exit `2`.
Closed historical executions remain readable through the Core identity bound
into their closeout receipt. Inspection remains read-only and grants no Git or
release authority.

## Core v0.5 visual-smoke evidence

Core `0.5.0` adds `runkit visual-smoke` as an executor-neutral evidence
orchestrator. A project supplies one explicit automation runner and exact argv;
RunKit does not embed a browser, Electron, CDP, Playwright, or Computer Use
driver.

The request freezes the visual surface, viewport, assertion ids, console
policy, denied external navigation, verification context, and selected source
manifest. The runner must write a structured result and at least one output
artifact inside the execution evidence root. RunKit recomputes all artifact
hashes, binds the canonical automation manifest, stdout, stderr and result to
`OwlCodaRunKitReplayableEvidenceV1`, and rejects failed assertions, policy
violations, malformed or missing artifacts, target writes, and post-run artifact
mutation.

The output remains an `OwlCodaRunKitSnapshotV1`, so the existing `finalize`,
receipt lineage, accepted closeout, and ready-for-commit gates consume visual
evidence without a parallel acceptance path. A passing visual smoke grants no
Git, release, credential, navigation, or foreign-write authority.

## Core v0.6 dependency-aware verification planning

Core `0.6.0` adds `runkit verify-plan` as the deterministic planning boundary
between a fresh DeliveryPacket and command execution. It does not weaken the
v0.2 source or acceptance gate. It records four separate facts:

- leased source drift invalidates receipts bound to the changed source;
- declared dependency drift invalidates receipts bound to the changed
  dependency identity;
- unrelated dirty-tree drift remains visible without invalidating unrelated
  local receipt evidence;
- global gate failure blocks the relevant acceptance decision without
  rewriting otherwise reusable receipts as stale or failed.

`OwlCodaRunKitEvidenceCoverageIndexV1` binds each candidate reusable receipt to
source-file hashes, declared dependency hashes, the verification-context
fingerprint, profile ids and command ids. The resulting
`OwlCodaRunKitVerificationPlanV1` records reusable and invalid receipts,
direct/transitive/supporting profile impact, one deterministic primary profile
or an ambiguity warning, uncovered paths, and the minimum pending command ids.
The plan also emits exact pending command definitions. A selected profile with
no command mapping blocks as `verification_mapping_required` instead of being
misreported as ready, and more than ten direct profile matches emit a
machine-readable breadth warning.

The Core recomputes workspace Git paths, current source hashes and declared
file-dependency hashes before writing the project-owned plan. Supporting-only
profile matches fail closed, and an uncovered path still requires the full
profile. A plan always records `authorizationGranted=false`; command execution,
Git, release, credentials, deletion and foreign writes require separate
authority.

## Core v0.7 receipt-backed coverage adoption

Core `0.7.0` adds `runkit coverage-adopt` as the provenance boundary between
accepted Contract v0.2 verification evidence and a reusable
`OwlCodaRunKitEvidenceCoverageIndexV1`. A request may select a project-owned
gate input by path and SHA-256 and map receipt command ids to project profile
commands or dependency ids to material inputs and VerificationContext entries.
It cannot supply receipt status, source hashes, dependency hashes, context
fingerprints, selected profiles, or command results.

The Core recomputes the gate artifact hash, validates its append-only lineage
and acceptance decision, selects only the active passed receipt, matches exact
cwd/launcher/argv and zero exit against the declared profile command, and
derives source and dependency coverage from bound evidence. The resulting
coverage artifact records its source gate path/hash, active receipt hash,
source run, current adopting run, the command/dependency selectors used for
derivation, and `authorizationGranted=false`.

`runkit verify-plan` in Core `0.7.0` consumes the coverage artifact through a
path and SHA-256, then re-derives it from the current gate bytes, active receipt,
project profiles, exact command evidence, and declared dependency evidence.
Changed source evidence or any mismatch between the derived result and the
stored index fails closed. Unbound inline coverage claims are rejected.
Coverage adoption and verification planning remain evidence operations:
neither grants command execution, Git, release, credentials, deletion,
telemetry, or foreign-write authority.

## Core v0.8 append-only native resume

Core `0.8.0` adds `runkit resume` after receipt-backed coverage adoption. The
CLI `--run-id` identifies the source execution and supports two explicit modes:

- an unclosed execution receives a new `OwlCodaRunKitResumeAttemptV1` in the
  same run only when its engine pin is current, it is the sole active execution,
  no writer lease remains active, and no finalized receipt lineage exists. An
  execution with finalized receipts must close before it can resume as a
  distinct continuation, so old verification cannot govern the resumed state;
- a closed execution creates a distinct continuation run atomically. The new
  execution preserves the exact parent goal bytes and binds the parent goal,
  closeout, decision, engine pin, source run id, and artifact hashes without
  modifying the parent execution.

Both modes derive a fresh `OwlCodaRunKitEvidenceCoverageIndexV1` through the
same accepted-gate and exact-command boundary as `coverage-adopt`. The request
may select coverage sources but cannot supply receipt status, hashes, profiles,
command results, or reusable receipt ids. Empty coverage is valid when the
source execution has no accepted evidence to inherit.

Inherited receipt ids remain provisional evidence, not a new acceptance
decision. The resume attempt requires the next workflow to acquire a writer
lease, prepare or replace the DeliveryPacket, and run `verify-plan`; that plan
re-derives the coverage index and determines which stages are still reusable.
Resume never rewrites a prior goal, lease, packet, snapshot, receipt, gate,
coverage index, event, or closeout, and every result keeps
`authorizationGranted=false`.

## Core v0.9 CLI-managed lease and delivery

Core `0.9.0` removes hand-authored lease and DeliveryPacket JSON from the
normal Codex adapter path while retaining the same project-owned artifacts.
`runkit lease acquire` accepts repeated explicit `--owned-path` values, rejects
the reserved runtime, and checks every active execution under a project-level
transaction lock before writing one `OwlCodaRunKitWorkerLeaseV1`. Active path
overlap, duplicate work items, malformed files, directories, and symlinked
lease truth fail closed. `lease inspect` reads those artifacts and `lease
release` is the only normal `active -> released` transition.

`runkit delivery create --from-lease` reads current Git porcelain status but
includes only changed regular files owned by the selected active lease. It
derives whole-file SHA-256 values, canonical source fingerprint, branch, HEAD,
Core identity, and a list of unrelated dirty paths. Unrelated dirty paths stay
visible but are not silently claimed by the lease. Reserved runtime paths,
deletions, renames, symlinks, an empty candidate set, released or ambiguous
leases, unsafe output directories, and duplicate packet ids fail closed.

These commands write only `.owlcoda/runkit/**`. Every result and generated
packet keeps `authorizationGranted=false` and all repository actions false;
lease or delivery state never grants Git, release, credential, deletion,
telemetry, or foreign-write authority.

## Core v0.10 high-level lifecycle composition

Core `0.10.0` adds `runkit start`, `runkit verify`, and `runkit finish` as the
normal Codex adapter path without replacing any atomic command or artifact.
`start` composes plan and lease acquisition under the project control lock; an
invalid or overlapping lease rolls back only the newly created execution.

`verify` accepts an exact executable and argv after `--`, including a
zero-argument executable or empty-string argument. It derives a bounded
DeliveryPacket from the selected lease, writes generated snapshot/finalize
requests under the execution, derives platform, Node, Git and recognized
lockfile identity, runs the snapshot, and finalizes only when that snapshot
passes without source drift. The complete high-level verify holds the project
control transaction, so `finish` cannot close while a command is running.
Finalize and accepted finish both require the snapshot selected-file map,
manifest fingerprint and material inputs to match the same DeliveryPacket;
an old snapshot cannot be relabeled with a new source fingerprint. A command failure preserves stdout, stderr,
exit code, request and snapshot artifacts and emits no passed receipt.

`finish accepted` first derives and validates the unique active receipt gate,
then releases active leases and writes the accepted closeout. Without that gate
it leaves leases active and fails closed. It accepts only a Contract v0.2 gate
whose execution, receipt, snapshot, evidence and DeliveryPacket directories are
real project directories without symlink ancestors. If closeout persistence
fails after lease release, the same control transaction restores those leases
before returning failure. `blocked` and `rejected` release the
execution's leases and close honestly without inventing verification.

These commands only compose existing project-owned truth. They do not parse a
shell string, adopt terminal history, schedule multiple commands, or grant Git,
release, credential, deletion, telemetry, deployment, or foreign-write
authority.

## Core v0.11 human-first inspect projection

Core `0.11.0` changes only direct `runkit inspect` presentation. Its default
stdout is a compact human summary of current execution, latest indexed
closeout, source and evidence status, active lease holders, dominant gap, next
allowed action and false release authority. The wording is deliberately
`latest indexed closeout`, not `most recent`, because Contract v0.2 closeout
artifacts do not carry an acceptance timestamp. A closed delivery remains
`historical`; inspect does not claim it is still fresh.

Machine consumers must call `runkit inspect --json`. That response preserves
the complete execution and recovery document and adds the deterministic
`OwlCodaRunKitInspectSummaryV1` projection. `--history` lists only indexed
closed executions, while `--run-id ID --verbose` focuses one execution's pin,
lease, source, evidence, trust, issues and next action. These views are derived
in memory and never write project state or create acceptance, Git or release
authority.

The projection is fail-closed. Every unclosed execution entry remains visible
even when its engine pin is malformed, multiple active executions never inherit
source or evidence state from closed history, and damaged closed truth points to
`repair_execution_artifacts`. Project config, execution, lease, delivery,
receipt, gate, engine pin and closeout truth must be regular project-owned files
and real directories without symlink ancestors. Config fields and authority
policy are validated before they enter the machine document. Symlinked,
redirected, dangling or non-regular truth is reported as invalid rather than
followed or silently treated as absent. Human output escapes control characters,
and indexed identifiers use locale-independent code-unit order.

## Core v0.12 typed model resource preflight

Core `0.12.0` adds `runkit resource-preflight` as the boundary before
model-intensive work. A project supplies a strict request containing one
hash-bound `OwlCodaRunKitVerificationPlanV1`, typed provider/model observations,
the remaining workload estimate, explicit unknown handling, and hard resource
limits. RunKit validates and totals this evidence; it does not query provider
billing, discover credentials, route a model, or execute the workload.

Receipt reuse is limited to workload entries whose `coveredByReceiptId` is
still present in the bound plan's `reusableReceiptIds`. The Core subtracts only
those entries, then deterministically totals pending calls, input/output/total
tokens, elapsed time, and cost. Cost remains typed unknown unless the project
supplies explicit USD input/output rates. Availability, remaining-call quota,
remaining-token quota, reset time, and pricing remain independent known or
unknown facts and preserve their adapter evidence kind, hash, reference, and
observation time. `maxObservationAgeMs` makes that evidence expire explicitly;
an expired latest artifact projects `run_resource_preflight` instead of model
readiness. Inspect revalidates the bound plan path, bytes, SHA-256, identity,
authority boundary, and reusable receipt set, and recomputes resource demand,
cost, freshness, blockers, warnings, and decision from the artifact rather than
trusting its projection fields.

The project policy separately chooses fail-open or fail-closed behavior for
availability, quota, reset time, and pricing. A required unavailable model,
insufficient known quota, exceeded limit, or fail-closed unknown returns
`blocked_by_resource` with `pause_at_deterministic_stage`. A model-optional gate
may return `ready_without_model_execution`; it never invents or selects a
fallback model. The append-only `OwlCodaRunKitResourcePreflightV1` artifact and
every CLI result keep authorization, Git, and release authority false.

Core `0.12.0` is the typed evidence and deterministic-estimate layer, not a
claim that every provider exposes reliable remaining quota, reset time, or
pricing. Live provider adapters require a separately verifiable source and may
legitimately report typed unknown fields.

## Core v0.13 standalone distribution, Quick verification and repair

Core `0.13.0` is distributed through the standalone `owlrunkit` package. The
RunKit package has an independent semantic version lifecycle from the
`owlcoda` CLI; a RunKit packaging or documentation patch does not change the
Contract `0.2` / Core `0.13.0` identity unless Core behavior or its bound
dependency closure changes.

Core `0.13.0` adds a bounded Quick Verification lane for one exact command
without a writer lease or Formal acceptance. `quick-verify` records the
pre/post workspace fingerprints, exact executable and argv, stdout/stderr
materials, exit result and an authorization-free
`OwlCodaQuickVerificationReceiptV1`. `quick-attest` recomputes the selected
workspace and receipt bindings. `quick-metrics --local` reads only the
project-owned receipt store and performs no telemetry or network access. A
Quick `GO` remains `captured_verification`; it cannot satisfy the Formal
Contract v0.2 acceptance gate.

Core `0.18.3` adds `OwlCodaQuickVerificationReceiptV2` only when the caller
uses `quick-verify --stdin-file`. RunKit copies at most 1 MiB from a regular
non-symlink file into the receipt store before execution, supplies those stored
bytes as exact stdin, and binds their workspace-relative path, byte size, and
SHA-256. V1 remains the no-stdin receipt and stays readable. Neither schema
binds undeclared ignored outputs or grants any authority.

Core `0.19.0` adds `OwlCodaQuickVerificationReceiptV3` for explicit isolation,
dependency-environment binding, and ignored-path binding. `--isolate` runs a
Git-visible candidate copy in a disposable consumer and records consumer source
versus discarded ignored-artifact deltas. `--dependency-root` binds an existing
dependency environment without installing it. `--bind-ignored` is the only
operation that emits `OwlCodaWorkspaceSnapshotV2` and claims those selected
ignored bytes. Workspace source, selected ignored paths, dependency metadata,
and consumer source mutations are distinct fail-closed facts. Disposable
ignored artifacts do not mutate or become evidence for the source checkout.

Core `0.19.0` also adds `OwlCodaQuickEvidenceReusePlanV1` and
`OwlCodaQuickEvidenceReuseReceiptV1`. A reuse plan verifies one earlier strict,
passed, source-unchanged Quick receipt from the same workspace, derives the
current candidate delta from Git objects plus both snapshots, and refuses any
path outside literal caller allowances before command execution. Byte-identical
dirty content later committed to Git remains unchanged evidence. Apply runs one
exact delta gate through Quick and records both receipt hashes; it grants no
authority and does not satisfy Formal or higher acceptance layers.

Quick output and Verification Envelope stdout/stderr evidence use a project-
global create-only SHA-256 object store. Existing Quick receipt-local material
paths remain valid; no historical tree is rewritten or deleted. Object reuse is
storage/provenance behavior, never additional assurance.

Core `0.19.0` can additionally bind external transition truth without changing
Quick Receipt V1/V2/V3. `quick-verify --capture-runtime` gives the exact child
an initially absent receipt-local `OWLRUNKIT_RUNTIME_REPORT` path. A strict
`OwlCodaRunKitExternalRuntimeReportV1` there is projected into a separately
hashed `OwlCodaRunKitRuntimeTransitionReceiptV1` that binds the Quick receipt
bytes, report bytes, derived workspace mutation, command-reported external
mutation, ordered stages, rollback outcome, final external state, and recovery
artifact `capturedBefore` / `restoresTo` semantics. A failed stage followed by
a successful rollback remains a failed transition with useful evidence; it is
not promoted to Quick, Formal, deployment, or business acceptance. Missing or
inconsistent runtime truth fails closed while preserving the base Quick
receipt. `quick-runtime-verify` rechecks stored bytes and projection integrity;
it does not independently re-observe the external runtime or grant authority.

Deterministic `repair` persists a reviewable plan before replay, reuses only
fresh receipt-bound coverage, replays pending exact argv, and appends
replacement lineage. Failed and orphaned attempts remain inspectable. Repair
cannot rewrite the parent receipt, lower risk, replace the executable after
planning, or activate a green leaf after source/profile drift.

`offline-export` and `offline-import` move exact receipt bytes through
`OwlCodaOfflineAttestationBundleV1`. Export refuses an existing destination.
Import is idempotent only when the stored receipt bytes match exactly and fails
closed on conflicts, symlinked paths or malformed bundles. The embedded
read-only attestation component is part of the standalone package; it does not
need a separate public package for the first adoption wave.

Formal cross-project adoption is registry-first. The installed package and
controller-owned `OwlCodaRunKitRegistryReleaseEvidenceV1` must bind the same
exact official npm registry version, 40-hex `shasum`, canonical SHA-512
`integrity`, and exact tarball URL. A local directory, `file:` dependency,
local tarball, symlink, workspace link, Git reference or mutable dist-tag can
exercise a release candidate but is not formal adoption evidence.

The canonical Codex Skill is assembled atomically with a content manifest that
binds its Skill text, Core, contracts and attestation files. Known valid
installations may be archived and replaced; unknown drift fails closed. Core
`0.13.0` does not grant Git, npm, release, or foreign-project authority.
Signing, keys, external anchors and GitHub Actions remain deferred.

## Core v0.14 self-service onboarding

Core `0.14.0` keeps Contract `0.2`, Quick/Formal lane separation, exact
registry binding, append-only execution lineage, independent review and all
authority boundaries unchanged. Its product change is the first-adoption
surface of the standalone `owlrunkit` package:

- top-level `--help` and `--version` follow ordinary CLI expectations and exit
  successfully without creating project state;
- `doctor` performs read-only Node, Core, config, package, registry, profile
  and project-script diagnostics with a short network timeout and a typed
  offline/DNS-timeout, authorization, missing-version and binding-mismatch
  taxonomy;
- `profiles detect --dry-run`, `profiles validate`, and
  `profiles impact --changed` provide deterministic official entrypoints
  without treating guessed profiles as authoritative configuration;
- `adopt --exact owlrunkit@0.14.0` accepts only the official npm registry exact
  version whose registry metadata and local install/lock binding pass the
  existing strict adoption evaluator; and
- `init` and `inspect` add a separate onboarding projection for
  `doctor -> profiles detect --dry-run -> adopt or Formal start`.

Read-only onboarding commands must not write project state or expose registry
credentials. Adoption evidence is written atomically only after eligibility.
Local directories, worktrees, `file:` or Git dependencies, local tarballs,
workspace links and mutable tags remain fail-closed. Profile detection never
overwrites existing config, and an implementation may omit `profiles apply`
rather than infer authority from a deterministic suggestion.

The onboarding projection is not the recovery state machine: a project with a
stale Packet, invalid evidence or engine drift must still follow the Core's
`nextAllowedAction`. Core `0.14.0` does not grant Git, npm, release, deploy or
foreign-project authority. Signing, keys, external anchors and GitHub Actions
remain deferred.

## Core v0.19 atomic onboarding

Core `0.19.0` keeps Contract `0.2` and all existing authority boundaries. The
versioned `OwlCodaRunKitOnboardingBootstrapPlanV1` dry-run binds the exact
project-local package and official registry release, checks upgrade safety,
previews profile reconciliation, reports shared Skill drift, and performs zero
writes. `bootstrap --apply` rechecks that plan under a project-owned lock, then
runs Core initialization, profile reconcile/validation, exact adoption and
doctor readback as one high-level transaction.

The transaction governs RunKit config, profiles, their migration/apply
receipts, and adoption evidence. A failure after mutation restores their exact
preimage before writing an append-only
`OwlCodaRunKitOnboardingBootstrapReceiptV1`. A concurrent bootstrap, active or
invalid project lifecycle, ambiguous project tool, exact-package mismatch, or
registry mismatch fails closed. The command does not modify package files,
source, Git, deployments, production, business state, or shared Skills, and it
never grants those authorities.

## Deferred work

Contract v0.2 still does not add a built-in browser or Electron driver, Plugin,
cloud, team, signing, or transparency-log services.
