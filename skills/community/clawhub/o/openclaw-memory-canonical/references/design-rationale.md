# Decision Rationale: Memory System v4

## Evolution Timeline

### 2026-04-04 — Session Start
- Baseline: 329-line AGENTS.md, 23KB MEMORY.md, 10 semantic files (many duplicates)
- System: OpenClaw 2026.4.2, Ubuntu 24.04, Qwen 3.6 Plus via OpenRouter

### Round 1: System Self-Audit
- Cut AGENTS.md 329→111 lines (-66%)
- Cut MEMORY.md 23KB→2.2KB (-90%)
- Removed stale files: ontology, tasks, monitoring, glossary
- Added: tiered loading (HOT/WARM/COLD), 3 memory types, grep tags, weekly review cron
- Added: episodic TTL, buffer rotation, freshness table, open questions

### Round 2: Second AI Consultation
AI feedback: "Structure near saturation — protect against 3 problems: duplicates, partial writes, stale knowledge."

Applied:
- **Atomic write script** (tmp → sync → mv)
- **Canonical Owner Rule** table (one home per fact type)
- **last_verified** in all WARM files
- **Frozen tag vocabulary** (no new tags)
- **Closure blocks** in episodic (Updated/Decisions/Open)

Removed: freshness from episodic (date already in filename), weekly digest conditional

### Round 3: DeepSeek Third Consultation
DeepSeek suggested: Signal Detection, Decision Registry, Friction Log, Boundaries

Applied:
- ✅ **Decision Registry** → `semantic/decisions.md` (8 decisions from audit)
- ✅ **Signal** added to closure blocks (Decision ≠ Signal)
- ✅ **Friction Log** added to working-buffer habit
- ❌ **Boundaries** not created (already in AGENTS.md safety rules)

### Round 4: Consolidation
- Final: 11 files, ~12KB, 10 mechanisms
- Frozen tag vocabulary codified
- All scripts tested
- Ready for ClawHub publication

## What We Rejected and Why

| Rejected | Reason |
|----------|--------|
| Separate decision DB | Already in MEMORY.md + decisions.md |
| Embedding/search layer | Overkill for single-user, grep works fine |
| Frontmatter schema | Adds ceremony without value |
| New memory "types" | 3 types at saturation, more = noise |
| Boundaries file | Already covered in AGENTS.md |
| Per-file intelligence scoring | Maintenance cost > query benefit |
| Separate open-questions file | Already a section in MEMORY.md |

## 2026-04-11 — Dual Thinking Publish-Readiness Recheck (6 alternating rounds)
- Trigger: user requested a 6-round alternating re-review using Qwen Orchestrator and AI Orchestrator, grounded in installed practical use on this host, then publication to ClawHub.
- Real host finding: packaged skill updates do not automatically overwrite deployed `memory/scripts/`, so published docs had to distinguish packaged reference state from active runtime state.
- Accepted fixes:
  - explicit `skills/openclaw-memory-canonical/` vs `memory/scripts/` contract
  - post-update re-sync + `health-check.sh` validation requirement
  - `.clawhubignore`, `CHANGELOG.md`, `UPGRADE.md`, `references/verification-evidence.md`, `references/reference-test-log.md`
  - deterministic `references/package-tree.sha256` generation for publish scope
  - explicit backup/restore guidance for local runtime script variants
- Rejected fix: cross-hash assertion between evidence docs and package-tree hash. Final DeepSeek closure round judged it unnecessary complexity because no concrete failure mode justified the extra layer.
- Rerun note: a later Qwen rerun proposed keyword-based machine routing heuristics for Canonical Owner Rule; DeepSeek rejected that as overfitted pseudo-determinism and the accepted clarification was narrower: if routing is still ambiguous after choosing the most specific primary nature, default to today's episodic note with a `#routing-note:` for weekly review.
- Signal: the real operational risk was lifecycle drift between packaged artifacts and deployed runtime scripts, not the core memory architecture.

## Key Design Principles

1. **Minimal ceremony** — grep, head, cat. No API, no library chain.
2. **Survive restarts** — everything on disk, nothing in "memory".
3. **Self-healing** — TTL archival, compaction recovery, buffer rotation.
4. **No duplicates** — Canonical Owner Rule enforced by weekly review.
5. **Small context** — 60-line HOT file fits in any prompt budget.

## Publication Traceability Note

For the current publish-ready line, local version-reporting artifacts must stay aligned with the visible skill heading and release evidence:
- `SKILL.md` heading version
- `_meta.json` `version`
- `.clawhub/origin.json` `installedVersion` when refreshed locally after install/update
- `references/package-tree.sha256` generated only after all accepted metadata/doc updates are complete

## 2026-04-11 — Dual Thinking Hardening Rerun from v4.6.9 (6 alternating rounds)
- Trigger: user requested another full 6-round alternating review via AI Orchestrator and Qwen Orchestrator, with publication only if real improvements survived validation.
- Accepted fixes:
  - required `health-check.sh` preflights now re-sync `memory/scripts/` first if the deployed script is missing or non-executable, then rerun the real script
  - Buffer Rotation Procedure step 3 now uses a deterministic terminal closure assertion
  - Buffer Rotation Procedure step 3 now explicitly handles both existing-closure reassembly and no-closure-yet closure creation with atomic rebuild semantics
  - Weekly Review step 7 now preserves exactly one terminal closure block instead of allowing duplicate closure blocks
- Rejected heavier idea: manual logical fallback in place of the real `health-check.sh` result when the script is missing; this was rejected as too structural and weaker than re-sync + real script validation.
- Signal: after v4.6.9, the remaining risk was not broad architecture but narrow executable seams around maintenance and recovery invariants at file endings and preflight script availability.

## 2026-04-11 — Dual Thinking Rerun from v4.6.10 under strict persistent-chat continuity
- Trigger: user requested another full 6-round alternating review and explicitly wanted consultant chats to persist across rounds unless a consultant degraded under context load.
- Review method: executed under `dual-thinking v8.4.0`, using one persistent DeepSeek chat across all valid AI rounds and one persistent Qwen chat until it degraded, then replacement recovery chats only when Qwen repeated already-fixed findings instead of honestly reviewing the current artifact.
- Accepted fixes:
  - publish chronology now explicitly finalizes hashed package files first, generates `references/package-tree.sha256` last among in-package content updates, and freezes hashed package files after generation until publish
  - Weekly Review now deletes stale `working-buffer.md.lock` before evaluating the active-session gate
  - Weekly Review numbering was restored to sequential order after the stale-lock patch
  - `.pending` recovery now validates the expected 4-line working-buffer header exactly, including field names, line order, valid ISO timestamps, and the required blank line
- Signal: the stricter persistent-chat method improved continuity for DeepSeek and exposed a real operational truth for Qwen: persistent chats are the default, but once a consultant starts repeating already-fixed findings against visible same-chat history, a recovery replacement chat is justified and should not be counted as normal continuity.

## 2026-04-14 — 8-round rerun from v4.6.11 to close remaining contract seams
- Trigger: user explicitly requested a fresh 8-round alternating review using AI Orchestrator and Qwen Orchestrator, then publication to ClawHub with a report of what changed.
- Review method: one persistent DeepSeek chat and one persistent Qwen chat were reused across the line; after convergence signs appeared, rounds 5-8 still ran because the user explicitly requested all 8 rounds.
- Accepted fixes:
  - `health-check.sh` now validates the exact 4-line `working-buffer.md` header contract, making the recovery invariant executable instead of documentation-only
  - the authoritative active-task-line definition was narrowed to bullet-list lines starting with `- ` after `## Active Task:` and the deterministic count command was aligned to `grep -c '^-[[:space:]]'`
  - the Buffer Rotation recovery note now matches the Runtime Decision Tree for stale-lock handling
  - the session-end cleanup clause now uses the same narrowed active-task-line definition as the rest of the runtime contract
- Rejected / non-accepted path: Qwen round 6 repeated the already-fixed session-end wording seam; it was treated as stale/non-meaningful rather than as justification for another patch.
- Signal: by v4.6.11 the remaining risk was no longer architectural; it was a cluster of narrow contract drifts where the skill text and executable validation logic were almost aligned but not perfectly identical. The 8-round rerun closed that last gap without adding complexity.

## 2026-04-14 — second 8-round rerun from v4.6.12 with no new patch
- Trigger: user explicitly requested another full same-style 8-round alternating review and another ClawHub publication.
- Review method: a fresh independent rerun was executed from the current 4.6.12 baseline, again using persistent DeepSeek and Qwen chats across the line.
- Accepted changes: no new runtime or contract patch was justified in this second rerun.
- Observed result: all 8 rounds converged on the same conclusion — the 4.6.12 artifact remained internally consistent, with no material current seam and no honest reason for another behavioral change.
- Publication consequence: if releasing again, the new version must be framed strictly as revalidation/evidence refresh, not as a fake functionality update.
- Signal: once the line had converged, repeating the full alternating process became valuable mainly as a confidence test. The system passed that test, which increases trust in stability but does not justify inventing more complexity.

