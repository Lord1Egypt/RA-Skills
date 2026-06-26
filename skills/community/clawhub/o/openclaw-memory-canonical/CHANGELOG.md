# Changelog

## 4.6.14 - 2026-04-14
- Fresh full 10-round Dual Thinking rerun from the `v4.6.13` baseline using alternating AI Orchestrator and Qwen Orchestrator, with one lawful Qwen recovery session after the original Qwen line repeated an already-rejected wording seam instead of engaging the accepted synthesis.
- All 10 rounds converged with no new material runtime, recovery, package-hygiene, or weak-model-execution seam in the skill artifact itself.
- The only accepted change in this line is release-honesty refresh: version/changelog/evidence/test-log surfaces now record the completed 10-round rerun instead of the older second 8-round rerun.
- The proposed `Tag Vocabulary (Frozen)` rename was explicitly reviewed and rejected as non-material wording churn.
- Final host `health-check.sh` evidence during this active publish session was FAIL only because the live workspace `memory/working-buffer.md` exceeded 80 lines; this was treated as current host state, not as a new packaged-skill defect.

## 4.6.13 - 2026-04-14
- Fresh second full 8-round Dual Thinking rerun from the `v4.6.12` baseline using alternating AI Orchestrator and Qwen Orchestrator with persistent same-topic sessions per orchestrator.
- All 8 rounds converged with no new material runtime seam, no justified behavioral patch, and no current contract/implementation drift.
- This release is an honest revalidation/evidence-refresh line, not a functional runtime change release.
- Refreshed release evidence, test log, rationale trail, and version surfaces to record the second independent full-rerun convergence result.

## 4.6.12 - 2026-04-14
- Fresh 8-round Dual Thinking rerun from the `v4.6.11` baseline using alternating AI Orchestrator and Qwen Orchestrator with persistent same-topic sessions per orchestrator.
- `scripts/health-check.sh` now validates the exact 4-line `memory/working-buffer.md` header contract (`# Working Buffer`, `created: <ISO-8601>`, `last_active: <ISO-8601>`, blank line), closing a real recovery/validation seam.
- Narrowed the authoritative active-task-line definition to bullet-list lines starting with `- ` after `## Active Task:` that contain non-whitespace content, and aligned the documented deterministic counting command to `grep -c '^-[[:space:]]' memory/working-buffer.md`.
- Aligned the Buffer Rotation recovery note so stale `working-buffer.md.lock` files are deleted unconditionally before `.pending` recovery or staleness evaluation, matching the Runtime Decision Tree.
- Aligned the session-end cleanup clause to the same narrowed active-task-line definition used elsewhere in the runtime contract.
- Final confirmatory rounds converged with no remaining material runtime seam; only release-surface refresh remained for publication.

## 4.6.11 - 2026-04-11
- Fresh 6-round Dual Thinking rerun from the `v4.6.10` baseline under the stricter `dual-thinking v8.4.0` same-chat continuity contract.
- Consultant continuity was kept persistently per orchestrator by default; Qwen required explicit recovery only when it demonstrably degraded and repeated already-fixed findings instead of reviewing the latest accepted state.
- Tightened publish chronology for `references/package-tree.sha256`: all hashed package files must be finalized first, the package-tree hash must be generated last among in-package content updates, and hashed files must not change after generation before publish.
- Weekly Review now deletes stale `working-buffer.md.lock` before evaluating the active-session gate, preventing orphaned lock files from deferring review indefinitely after a crash.
- Weekly Review checklist numbering was restored to clean sequential order after the stale-lock patch.
- `.pending` recovery now validates the 4-line working-buffer header exactly: exact field names, order, valid ISO timestamps, and required blank line.

## 4.6.10 - 2026-04-11
- Fresh 6-round Dual Thinking rerun from the `v4.6.9` baseline using alternating AI Orchestrator and Qwen Orchestrator.
- Tightened required `health-check.sh` preflight behavior: if the deployed script is missing or non-executable, bootstrap/re-sync `memory/scripts/` first and rerun the real script instead of substituting an informal manual pass.
- Hardened Buffer Rotation Procedure step 3 with a deterministic terminal closure-block assertion and explicit recovery branching for existing-closure reassembly vs no-closure-yet closure creation.
- Corrected Weekly Review step 7 so it preserves exactly one terminal 4-line closure block instead of potentially duplicating closure blocks in today's episodic file.
- Rejected heavier fallback proposals as unnecessary complexity for the current line; convergence was reached with narrow executable contract fixes.

## 4.6.9 - 2026-04-11
- Fresh 6-round Dual Thinking rerun from the `v4.6.8` baseline using alternating Qwen Orchestrator and AI Orchestrator.
- Added explicit session-start recovery remediation for recovered non-stale oversized active buffers: rotate immediately, then continue with a fresh working buffer.
- Clarified update/install drift handling: packaged skill updates do not change deployed `memory/scripts/` behavior until re-sync + `bash memory/scripts/health-check.sh` succeeds.
- Tightened oversized-buffer wording so mid-session deferral is explicitly separate from session-start recovery behavior.
- Made the mid-session oversized-buffer threshold deterministic: count active bullet lines under `## Active Task:` with `grep -c '^-'` and total lines with `wc -l`.
- Corrected the authority boundary: deployed scripts remain authoritative for host-side file operations, while the Markdown contract remains immediately authoritative for AI planning and decision logic.
- Rejected heavier ideas from the rerun as unnecessary complexity for the current line, including runtime auto-version enforcement and embedded self-referential version hashes.

## 4.6.8 - 2026-04-11
- Aligned release metadata and local version-reporting artifacts with the visible skill version after a fresh 6-round rerun.
- Made publish-evidence chronology explicit: current evidence files now state that they reflect the accepted rerun state after traceability fixes.
- Clarified Canonical Owner Rule ambiguity handling: when primary-nature routing still remains ambiguous, default to today's episodic note with `#routing-note:` for weekly review.
- Rejected keyword-based routing heuristics as unnecessary complexity during the rerun closure process.

## 4.6.7 - 2026-04-11
- Added explicit installed-runtime vs packaged-skill contract.
- Added mandatory post-update re-sync + validation flow for `memory/scripts/` after ClawHub installs/updates.
- Added publish-hygiene artifacts for release evidence (`.clawhubignore`, `UPGRADE.md`, `references/verification-evidence.md`, `references/reference-test-log.md`).
- Captured practical host finding: packaged script updates do not automatically overwrite deployed `memory/scripts/`, so runtime behavior must be trusted only after explicit re-sync + `health-check.sh` validation.
- Added operator-safety note to back up local script variants (for example `*.local.sh` wrappers) before overwriting deployed runtime scripts.
- Added deterministic post-patch packaging validation guidance and package-tree hash evidence for publish scope.
- Added explicit backup globs and deterministic restore snippet for deployed runtime script rollback.
- Clarified Canonical Owner Rule routing: added explicit ambiguity fallback to today's episodic note with `#routing-note:` instead of heuristic routing tables.
