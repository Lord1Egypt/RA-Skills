# OwlCoda RunKit Contract v0.1

Status: **frozen for Codex-side project execution**
Frozen at: 2026-07-13
Runner prerequisite: Node.js 20+

## Purpose

RunKit Contract v0.1 defines the smallest reusable execution contract proven while developing OwlCoda inside Codex. It coordinates project-owned truth, bounded workers, delivery evidence, stage verification, invalidation and replacement without relying on chat history or agent memory.

This is a control and evidence contract. It is not an OwlCoda product API, a workflow designer, a memory system or a release system.

## Frozen principles

1. **Project-owned truth** — goals, packets, profiles, receipts and decisions live as project artifacts. Agent memory may help locate them but is never authoritative.
2. **One owner per write scope** — every work item has an explicit lease and owned paths. Parallelism is allowed only across non-overlapping scopes.
3. **Complete a phase before stage verification** — implementation lanes may batch a coherent phase and stop at `ready_for_stage_verification`; the stage gate runs once after all dependencies are fresh.
4. **Evidence travels with delivery** — a delivery packet records scoped whole-file hashes, canonical fingerprint, commands already run and repository actions. The controller verifies hashes instead of repeating covered commands.
5. **Stale evidence fails before execution** — a scoped source mismatch returns `invalidated_by_concurrent_write`; verification commands must remain at zero until a fresh replacement packet is valid.
6. **Uncovered change fails closed** — if no profile covers a changed path, the decision is `full_profile_required`, never an empty successful selection.
7. **Lineage validity is not verification success** — a structurally valid receipt graph becomes accepted only when the active receipt binds the current source fingerprint, exact selected profiles and real command receipts.
8. **Append-only replacement** — invalidated receipts remain immutable. A replacement references the parent receipt SHA-256 and becomes the only active leaf.
9. **Foreign projects remain project-owned** — read-only shadow runs may read another repository but must write all runner artifacts and scratch outside that repository and prove its start/end state is unchanged.
10. **Runtime truth beats transcript appearance** — gate decisions consume files, hashes, exit codes and receipts, not worker summaries.

### Additive clarifications

These rules narrow unsafe or ambiguous inputs without changing the frozen v0.1 semantics:

1. **Runtime state is never product source** — `.owlcoda/runkit` and every descendant are reserved. They are forbidden in delivery `changedFiles`, verification profile path rules and lease owned paths. A violation is `invalid_input` / exit `3`, never a source change or profile match.
2. **One execution pins one engine** — execution creation records `contractVersion`, `coreVersion`, `coreManifestSha256` and an immutable or content-addressed `coreSourceRef`. Every later core invocation compares this pin before acting. A mismatch fails closed as `engine_changed_during_execution` / exit `2`; it cannot silently mix implementations inside one lineage.
3. **Core and producer data are separate** — acceptance semantics consume the contract version, pinned core identity and core payload. Producer identity is provenance. Adapter-specific extensions are namespaced and cannot add authority or change acceptance.
4. **Configuration is data, not authority** — project configuration, profiles and command declarations never authorize Git, publish, deploy, destructive actions, credential use or foreign-project writes.

## Artifact chain

```text
GoalContract
  -> ExecutionPlan
  -> WorkItem + WorkerLease
  -> ExecutionDeliveryPacket
  -> VerificationProfile selection
  -> Stage VerificationReceipt
  -> GateDecision
  -> CloseoutReceipt
```

`events.jsonl` is the append-only transition ledger. `execution-plan.json` is a derived mutable snapshot and must not override contradictory events or receipts.

## Delivery source contract

An `ExecutionDeliveryPacket` contains exactly one source hash map:

- `changedFiles.files`, or
- `changedFiles.wholeFileSha256`.

Both shapes present is malformed. Paths must be safe repository-relative paths: no absolute path, Windows rooted or drive-relative path, backslash, NUL, empty segment, `.` or `..`. Selected sources must be regular files inside the physical workspace root; symlinks and root escapes are rejected. The reserved `.owlcoda/runkit` subtree is rejected even though it is otherwise repository-relative, preventing receipts from recursively changing the fingerprint they describe.

Canonical stream:

```text
<path><TAB>sha256:<lowercase-whole-file-sha256><LF>
```

Rows are ordered by ascending Unicode code units, independent of locale and ICU. The source fingerprint is SHA-256 of the UTF-8 bytes of the canonical stream.

Source gate results and process exit codes:

- `valid` — exit `0`
- `invalidated_by_concurrent_write` — exit `2`
- `malformed_packet` — exit `3`

## Verification profile contract

A profile has a stable `id` and path rules. v0.1 supports only:

- exact safe repository-relative path;
- safe non-empty `directory/**` prefix.

For legal inputs the resolver returns deterministic, de-duplicated profile IDs. Any uncovered changed path returns:

```json
{
  "decision": "full_profile_required",
  "profileIds": [],
  "uncoveredPaths": ["..."]
}
```

Unsafe input is `invalid_input` / exit `3`; it is not converted into a profile decision. Profiles may not name `.owlcoda/runkit`, `.owlcoda/runkit/**` or a descendant exact path.

## Receipt lineage contract

Each lineage entry contains:

- a 64-hex `receiptSha256` matching canonical receipt content;
- a receipt object;
- optional 64-hex `parentReceiptSha256` referencing an earlier invalidated receipt.

Receipt SHA values are globally unique. The lineage rejects malformed entries, hash mismatch, missing or non-prior parent, parent with the wrong state, cycles, branches and multiple active leaves.

Lineage CLI exit codes:

- structurally valid — exit `0`
- well-formed but invalid — exit `2`
- malformed input — exit `3`

## Joint verification gate

The active receipt must bind:

- a current source gate with `status=valid` and exit `0`;
- the exact recomputed source fingerprint;
- the exact targeted profile IDs;
- a valid single-leaf receipt lineage.

For `status=passed`, `commandRuns` must be greater than zero and equal the number of command receipts. Every command receipt requires a non-empty command, exit `0`, and SHA-256 for stdout and stderr.

A zero-command receipt may remain `shadow_validated` or `ready_for_verification`, but it cannot be accepted as passed.

## Stage verification economy

- Implementation lanes complete a coherent phase before testing when the round contract selects stage verification.
- A stage owner consumes all fresh packets and runs one declared top-level profile.
- The controller validates the packet and receipt hashes and does not repeat covered commands.
- A failed stage is classified before repair. Only the affected stage is rerun after a replacement packet; unrelated profiles remain valid.
- Full regression belongs at an integration, merge or release boundary, not every feature delivery.

## Foreign-project read-only mode

Before and after the stage, record at minimum:

- foreign HEAD;
- raw Git status bytes and SHA-256;
- a declared workspace manifest fingerprint appropriate to the project;
- selected file hashes.

All foreign build scratch and receipts must be redirected to the controller project's artifact directory. Any start/end mismatch is `foreign_workspace_changed_during_shadow`, even when the verifier itself passed.

## Provenance

- Run001 proved leases, receipt-first handoff, targeted repair and controller economy.
- Run002 proved a packaged provider-backed synthetic coding loop and restart recovery.
- Run003 proved stale packet invalidation, minimal affected profile selection and append-only replacement.
- Run004 proved the contract against the foreign Swift/macOS OwlOps project with one stage command, one focused Swift verifier and zero foreign repository writes.

The exact evidence hashes are recorded in the Run004 manifest and closeout receipt.

## Versioning rule

The semantics above are frozen as v0.1. New optional fields are allowed when they do not weaken these invariants. Any change to path grammar, canonicalization, exit meanings, invalidation timing, receipt parentage, acceptance evidence or foreign-write policy requires a new contract version.

## Not yet included

- reusable npm package or global installation;
- Codex plugin or skill distribution;
- remote worker transport;
- UI/workflow designer;
- cloud/team memory;
- automatic commit, publish or deployment authority.
