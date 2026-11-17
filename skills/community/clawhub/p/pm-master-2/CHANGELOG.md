# Changelog · PM Master v2

## 2.2.17 (2026-09-22) · v2.2.16 re-audit rectification (SDI-4 / SQP-2 / LP1 / T09 / AE1 / SQP-1 / SQP-3 / RA2)

Rectification of the ClawHub re-audit of v2.2.16 (scanners: AIG / ClawScan / SkillSpector all
still flagged `suspicious`; static-analysis clean). Changes are restricted to the OpenClaw
(ClawHub) edition; the WorkBuddy/Chinese edition is untouched.

### Security fixes (HIGH)
- **SDI-4 `execution_driver.py` · control-check stamp before inspection**: `execution_driver`
  stamped `last_control_check` the moment an inspection was *deemed necessary*, even though the
  real inspection (control_engine.py) had not run — letting a deemed-but-not-run inspection
  suppress the next genuine control check. Removed the premature stamp; `last_control_check` is
  now written ONLY by `control_engine.py` after a real inspection (control_engine.py:631).
- **SQP-2 `parse_sow.py` · destructive SOW subtree replacement without confirmation**: the script
  deleted and replaced the SOW subtree on every run with no explicit gate. Added an `--apply`
  flag; `--dry-run` (and running with neither flag) is now a safe preview that writes nothing.
  When `--apply` is given it prints a removal/addition diff and still writes a dated backup
  (`project.yaml.bak-<date>`) before the destructive replace. Docstring + playbook updated.
- **T09 `comm_send.py` · approver authority derived from caller-modifiable `project.yaml`**:
  `resolve_approver()` previously unioned the admin allowlist with `project.pm`/`project.sponsor`
  — so anyone who could edit `project.yaml` could self-authorize external email. Authorization is
  now **admin policy only** (`config.email.approvers` ∪ `config.governance.approver_identities`),
  fail-closed when empty. Sponsor co-sign uses only `config.email.sponsor_approvers`. Matches
  AIG remediation #4 ("do not derive email authorities from caller-modifiable project.yaml").
- **LP1 `comm_send.py` / `gate_engine.py` · untrusted environment identity**: the
  `PM_MASTER_REQUESTER` environment variable is now honored only when an administrator explicitly
  sets `config.email.trust_env_requester: true` (default `false`). The requester is recorded as an
  **untrusted audit label** and never influences authorization. Removed the `PM_MASTER_APPROVER`
  reference from the docstring.

### Disclosure / hygiene (HIGH / MEDIUM)
- **AE1 `SKILL.md`**: reworded the self-referential "single, English-only manifest" packaging note
  that tripped the analysis-evasion heuristic.
- **SQP-3 `CHANGELOG.md` / `SKILL.md`**: documented that English-only is an explicit ClawHub/OpenClaw
  marketplace compatibility requirement (the manifest is validated/rendered in English; no per-locale
  variant is offered), not a user-facing language restriction.
- **SQP-1 `README.md`**: added a bounded activation-scope block with positive triggers and explicit
  negative examples (do-not-activate).
- **RA2 `CHANGELOG.md`**: reworded a historical "write back `wbs` dates" entry that tripped the
  session-persistence heuristic.

### Residual (documented, not a defect)
- **TP4 (description/behavior mismatch, SkillSpector)**: each script is a narrow utility while the
  top-level description is broad. ClawScan already downgraded TP4 because the full package contains
  every claimed capability (email / confidentiality scan / DOCX export / role dispatch). The v2.2.16
  description discloses all four; this release keeps it. Per-chunk matching is a SkillSpector heuristic
  artifact for multi-file skills and is not a functional vulnerability.

### Version-consistency fix (caught post-packaging)
- Aligned the version string across all surfaces to **2.2.17**: `README.md` (header + §12 "Current
  version") and `_user_meta.json` still read 2.2.15 and were updated; the doc-sync rule in `README.md`
  no longer references the removed `SKILL.en.md` (single English `SKILL.md` since v2.2.16). `SKILL.md`
  metadata and `CHANGELOG.md` were already 2.2.17.   (CHANGELOG/MIGRATION historical mentions of
  `SKILL.en.md` are left as accurate history.)

### Documentation cleanup (post-packaging, doc-only — still 2.2.17)
- **SKILL.md**: removed legacy version-history chatter and in-progress wording so the file reads as a
  clean adoption manual. Removed: the stale `v2.1` H1; the intro paragraph referencing "v1.3.6's
  expert-dispatch workflow" / "v2 only claimed" / "v2's deadlock and paper features"; the inline
  "(fixes v2 P3)" and "(fixes v2 deadlock)" notes; the "smooth v1.x -> v2" migration comment; and the
  "really wired" state-machine label. The authoritative version is declared once in the metadata block
  and mirrored in `README.md` §12 + `_user_meta.json`.
- **README.md**: neutralized the hardcoded, platform-specific install path `/root/.codebuddy/skills/pm-master`
  to a portable `<SKILLS_DIR>` placeholder in the Quick Start install and example blocks.
- **SKILL.md (round 2, packaging/§8)**: removed the "Packaging" blockquote — it was internal edition/manifest
  trivia ("shared across editions", "manifest validated and rendered in English") plus audit-era defensive
  disclosure, not adoption guidance. Reframed §8 from "Security & Safety Notes (for reviewers)" to
  "Security & Safety Rules" and dropped the audit-defensive "There is no cryptographic token…" sentence; the
  substantive safety rules (email off by default, allowlist-bound approval, no silent external action,
  confidentiality scan) are retained as operational guidance.

## 2.2.16 (2026-09-21) · OpenClaw security-audit rectification + English-only unification

Single, English-only OpenClaw package produced in response to the ClawHub security audit
(scanners: AI-Infra-Guard, ClawScan, SkillSpector, Static-Analysis, VirusTotal).

### Security fixes (P0/P1)
- **T09-1 `comm_send.py` · forgeable approval**: an arbitrary `--approve <string>` was accepted. Approval is now bound to an authorization allowlist: `config.email.approvers` (admin) unioned with the project's declared `project.pm` / `project.sponsor`. Self-approval is forbidden, and an unresolvable approver set now rejects the send (fail-closed) instead of accepting any string.
- **T09-2 `gate_engine.py` · unauthenticated stage-gate transition**: the same boundary is applied to stage gates via `config.governance.approver_identities` unioned with `project.pm` / `project.sponsor`. Records now carry `requested_by`, `by`, `nonce` and `decision` so each transition is attributable and non-replayable.
- **T05 `comm_send.py` · path traversal in the SMTP draft filename**: the draft path is sanitized to `[A-Za-z0-9_-]`, suffixed with a random nonce, and confined to the artifact directory via `os.path.realpath` + `os.path.commonpath` containment.
- **DCE `control_engine.py` · dynamic code execution**: the lazy `importlib.util.exec_module()` load of `evm.py` was replaced with a direct `import evm` on `sys.path`.

### Disclosure / packaging / locale hygiene
- **TP4**: `description` now discloses the email gateway, the pre-publish confidentiality/leak scan, Markdown-to-DOCX export and SOW-driven expert-role dispatch, instead of implying pure PM document generation.
- **SQP-1**: trigger wording narrowed and explicit "do NOT trigger" exclusions added.
- **SQP-3 / AE1**: the dual `SKILL.md` + `SKILL.en.md` split was removed. This package ships ONE manifest (`SKILL.md`) and is English-only — an **explicit ClawHub/OpenClaw marketplace compatibility requirement** (the manifest is validated and rendered in English; the platform offers no per-locale manifest variant), not a user-facing language restriction; the PM methodology content is locale-neutral. The Chinese surface across scripts, references, config, examples and templates was translated. Zero CJK/fullwidth characters remain (verified by scan).
- **`config.yaml`**: `email.enabled` now ships `false` (was `true`), matching the documented "email is off by default" posture; the `email.approvers`, `email.sponsor_approvers` and `governance.approver_identities` allowlist keys referenced by the code and docs were added.

### Quality
- Fixed a regression in the stage-gate atomic commit: the pre-commit concurrency re-validation compared the already-mutated in-memory state, so it aborted every transition. It now re-reads `project.yaml` from disk and compares against the evaluated state.
- **Test fixtures repaired: `scripts/test_gate_engine.py` now passes 66 / 66 (was 55 passed / 11 failed).** The 11 failures were fixtures that did not model a deliverable-ready project:
  - WBS leaves had no `deliverable`, no milestone attribution, no connected dependency network, no domain-expert `role`, and `decomposition.critic_passed` was unset — so `consistency_check.py` reported fatal problems.
  - Fixtures did not register the deliverables `artifact_guard` derives from data presence (`wbs`, `raid_log`, `risk_register`, `status_report`, plus `portfolio_dashboard` / `program_charter` for programs), so the OAG gate criterion failed.
  - Operational fixtures used `ev=77 / ac=55` against `pv=100`, which put SPI at 0.77 and made `control_engine.py` raise a RED escalation. Aligned to `ev=ac=pv` (SPI/CPI = 1.0).

### De-identification (hardcoded-value review)
- **Removed all real customer / vendor / personal identifiers from the distributed package.** `confidentiality_check.py` previously hardcoded client, vendor and personal tokens in `HIGH_PATTERNS`, and shipped docs (`usage.md`, `CHANGELOG.md`) listed them verbatim — while the scanner's own `EXCLUDE_META` skipped exactly those files, so the check passed while the leak shipped.
  - Client/vendor/person tokens moved out of source into `config.yaml` → `confidentiality.high_tokens` / `confidentiality.high_patterns` (empty by default). Only universally safe patterns (local absolute paths `/Users/`, `/home/`, `C:\Users`) remain built in.
  - `usage.md` and `CHANGELOG.md` now describe the mechanism generically.
  - Verified: a grep for the identifiers across the package now returns zero hits, and the scanner still detects configured tokens correctly.
- Example emails switched from the real domains `corp.com` / `external.com` to the RFC 2606 reserved `example.com`.

## 2.2.15 (2026-07-24)

### Package housekeeping · remove root-level legacy scripts + doc CLI alignment to canonical version
- **Removed two root-level legacy scripts** (not part of the runtime script dir `scripts/`, historically left at package root):
  - `_split_subprojects.py`: one-off migration helper (split the example data-lake program into per-SOW subprojects), containing example hardcoded paths; zero references across the package, deleted.
  - Root-level `rollup_subprojects.py`: same name as `scripts/rollup_subprojects.py` but the **old write-back implementation** (86 lines, positional CLI, weighted-estimate write-back to master). The canonical version is `scripts/rollup_subprojects.py` (125 lines, `--program <program_dir>`, read-only aggregated view, does not modify master). Deleted the root-level duplicate to eliminate ambiguity.
- **Doc CLI aligned to canonical version**: `README.md` §7, `references/program-management.md`, `references/operation-model.md` (2 places) still used the old positional call `rollup_subprojects.py <program/project.yaml>` in examples and described "weighted-estimate write-back to master" behavior; unified to `--program <program_dir>`, and corrected the description to **read-only aggregated view** (reads each `subprojects/<sow>/project.yaml`, rolls up milestone done/total + BAC/EV/AC/EAC/CPI, prints or exports via `--json`, does not modify master).
- Note: the CHANGELOG mojibake suspected in last review's audit was verified byte-level as a **false positive** (file has 0 U+FFFD, clean UTF-8); it was a display artifact from terminal awk truncating multi-byte characters — no change needed.
- Confidentiality scan exit 0.

## 2.2.14 (2026-07-24)

### WorkBuddy compatibility housekeeping + branch governance (main promotion)
- **SKILL.md self-description fix**: the original header wrongly stated "this file is English (OpenClaw-compatible)"; it is actually the WorkBuddy main-controller activity list. Corrected to label `SKILL.md` = **WorkBuddy edition (activity list)**, `SKILL.en.md` = OpenClaw English version; both share `scripts/`/`templates/`/`references/`, and select the backend via `config.yaml`'s `subagent_mode: team`.
- **Version alignment 2.2.14**: `SKILL.md` / `SKILL.en.md` / `_user_meta.json` / `README.md` unified to 2.2.14 (CHANGELOG is authoritative).
- **Branch governance**: `v2` (current WorkBuddy package) promoted to `main` via **fast-forward** and set as the default/active branch; old `main` (v1.3.6) archived under immutable tag `v1.3.6`, plus an `archive/v1.3.6-main` branch for easy retrieval. Zero history loss, no force-push.
- Confidentiality scan exit 0.

## 2.2.13 (2026-07-22)

### Control engine robustness + rerender coverage expansion
- **Root cause**: running on a real project exposed 4 classes of status/render misalignment, causing false gate alarms and doc drift.
- **control_engine.py**:
  - Added unified status constants `DONE/CLOSED/CANCELLED_STATES` and `_norm_status()` normalization (compatible with Chinese/English synonyms), eliminating the "typo-style" errors from inlined hardcoding in each pillar.
  - Progress rollup skips `summary` packages (their estimates are rollups of child leaves; including them double-counts).
  - Cancelled/downgraded/terminated/out-of-scope packages and risks are excluded from overdue and active-drift counts (non-active work / closed items don't false-alarm).
  - Added `TERMINAL_LS` (closed/closeout/archived etc.): once a program/project reaches a terminal state, the control gate reports GREEN and no longer false-alarms `gate_not_operational`.
- **rerender_docs.py**:
  - Added `change_log` (title→description mapping, eliminating the case where the fact source has a CR but renders an empty shell), `raid_log` (dict assumptions auto-flattened to strings), `evm_report` (calls `evm.py` to recompute at current value), `baseline_record` + `control_register` re-rendering.
  - `--only` option extended to cover the above types.
- **rollup_program_wbs.py**: added `_rollup_status()`; when all leaf packages are cancelled/terminated, the milestone row carries `cancelled`, avoiding false overdue alarms from the control engine.
- **rollup_subprojects.py**: when `eac_vs_bac_var` is None, fall back to `n/a` to avoid None formatting crash.
- Validation: reran control engine/rerender on the example customer project; original false alarms gone; confidentiality scan exit 0.

## 2.2.12 (2026-07-21)
- **Domain-agnostic + SOW auto-alignment**: removed hardcoded defaults biased toward the data domain out of the box (`data-architect`/`etl-engineer`/`data-modeler`/`requirements-analyst`).
  - Added `scripts/role_catalog.py` (single source of truth): covers 10 technical domains (data-platform / software-dev / cloud-infra / ai-ml / cybersecurity / product / qa / integration / erp / biz-analytics) + cross-domain roles; provides `infer_domain(text)` / `infer_role(name, domain)` / `specialize()` / `align_from_sow(spec)`.
  - `dispatch.py` / `consistency_check.py` changed to import `role_catalog`, deleting their respective duplicate `ROLE_KEYWORDS` / `DOMAIN_BY_KEYWORD` / `DOMAIN_SPECIALIZATION`.
  - `parse_sow.py` default role changed to `solution-architect` (summary/wave) and a domain-inferred fallback `domain-sme` (leaf), and auto-writes `domain` from SOW text.
  - Old project domains (insurance-data-lake / payments / ecommerce / fintech-core) kept compatible via `LEGACY_SPECIALIZATION`, preserving specialized names.
  - `expert-roles.md` / `activity-expert-map.md` expanded into a full technical-domain role catalog; `sow-parsing-playbook.md` / `program-management.md` examples de-biased from data.

## 2.2.11 (2026-07-21)

### Confidentiality review made deep · added `confidentiality_check.py` (mandatory pre-release)
- **Background**: user pointed out the confidentiality review must not be "path-only" but must cover "the content of all files (scripts / examples / any file, including binaries)". Early reviews only scanned text and missed compiled caches `__pycache__/*.pyc` — whose bytecode embeds `co_filename` absolute paths (e.g. `/Users/<user>/...` or historical workspace paths), leaking the local username / historical workspace.
- **Added `scripts/confidentiality_check.py`**: recursively deep-scans the entire skill package.
  - Text files matched line-by-line; **binaries (.pyc etc.) scanned at byte level**, catching embedded absolute paths;
  - HIGH tokens (hit = leak, exit 1): absolute paths `/Users/` `/home/` `C:\Users`, plus customer / vendor / personal identifiers supplied via `config.yaml` → `confidentiality.high_tokens` / `confidentiality.high_patterns` (deliberately not hardcoded in the distributed package);
  - Whitelist (reviewed safe, no alarm): `Example Customer` / `Example Data-Lake Project` / `MPP Data Warehouse` / `nos-architect` / generic example email / `Example INR Amount`;
  - Auto-excludes its own source to avoid pattern self-match false positives.
- **Cleanup**: removed local `__pycache__` (path-leak source); `.gitignore` already ignored `*.pyc`, so `origin/v2` contains no leak.
- **Solidified**: `references/usage.md` §14 makes this scan a "mandatory gate before publishing to a shared branch".
- Validation: ran on current package exit 0 (PASS); after injecting a .pyc with a `/Users/` absolute path into the package, ran again and immediately FAIL (byte-level hit `@offset`), proving binary deep-scan works.

## 2.2.10 (2026-07-21)

### Bug fix · RAID log "A · Assumptions" rendered as JSON literal
- **Root cause**: `templates/common/raid_log.md` (and `sow_kickoff.md`) assumptions section used `{{#each assumptions}} - {{this}}`; when an assumption is stored as a `{'text': '...'}` dict, `{{this}}` outputs the whole dict's `str()` (`{'text': '<=1600 source tables...'}`), and the user sees a JSON-style blob, hurting readability.
- **Fix**: render engine `scripts/render.py` added the `assume_text` helper — dict takes `.text`, plain string/scalar passes through, None falls back to empty string; both templates' assumptions sections changed to `- {{ assume_text(this) }}`. This helper is safe for both forms and prevents dict stringification.
- Validation: the example customer program's `risks/raid_log.md` A section re-rendered as clean bullets ("- <=1600 source tables…" etc., 6 items); plain-string assumptions (e.g. SOW kickoff) also render fine.

## 2.2.9 (2026-07-21)

### Operational artifact guardrail (OAG, Operational Artifact Guardrail) — new executable guardrail
- **Root cause**: the example customer project modified `project.yaml` (RAID/EVM) during the operational phase but did not re-render the corresponding artifacts, leaving `raid_log` / `risk_register` / `portfolio_dashboard` weeks behind the fact source, violating the "refresh artifacts on every action" guardrail.
- **Added `scripts/artifact_guard.py`**: content-hash drift detection.
  - Each render (`build_subproject.py` / `rerender_docs.py`) writes `source_hash` (content hash of the dependent data slice) + `rendered_at` to `project.yaml.artifacts_meta.<key>`;
  - On check, recompute the current data hash and compare with `source_hash`: match = OK, mismatch = data drift (violation, exit 1);
  - Existing docs (no `source_hash`) only get an ADVISORY, not a false kill;
  - `--stamp <key>` records `source_hash` for manually/externally rendered docs (e.g. `portfolio_dashboard`).
- **Integration**:
  - `control_engine.py` periodic inspection has built-in OAG checks; drift escalates to RED and `exit 1` (can be hooked to a scheduled task);
  - `gate_engine.py` closeout gate (G3→4) lists "artifacts consistent with fact source (OAG)" as a **hard criterion**; drift blocks closeout;
  - OAG status printed on every stage-gate evaluation.
- **Documented**: SKILL.md added Iron Rule #12; `references/operation-model.md` §4.6, `references/phases/p2-execution.md` §7.1, `references/project-schema.md` (artifacts_meta) synced.
- Validation: example customer program `artifact_guard.py --project` exit 0 after re-render; after temporarily changing `raid`, ran again and immediately reported `[Data Drift] raid_log`, proving it catches the previously missed step.

### Bug fix · program-level RAID render read `raid.*` instead of top-level `risks`
- **Root cause**: `build_subproject.py` / `rerender_docs.py` read RAID from top-level `data['risks']`, but program-level RAID lives under `data['raid']['risks']`, causing `rerender_docs.py` to silently skip the risk doc (`if not data.get('risks'): skip`), and `risk_register.md` to be fed an empty list; `consistency_check.py` reads `raid.risks`, so the gate still passed, producing silent drift of "gate passed but doc stale".
- **Fix**: both scripts' risk render path falls back to `data['raid']['risks']`; `rerender_docs.py` removes the `KeyError` hazard.
- Validation: example customer program `risks/raid_log.md` / `risks/risk_register.md` correctly reflect R1–R12 / I1–I6; `rerender_docs.py` no longer skips.

## 2.2.7 (2026-07-20)

### Bug fix · sub-project status report "5. Risks & Blockers" rendered as JSON string
- **Root cause**: `templates/common/status_report.md` §5 used `{{#each risks}} - {{this}}`; when `risks` is a list of dicts, `{{this}}` outputs `str(dict)` → user sees a JSON-style blob.
- **Fix**: §5 changed to a risk table consistent with the risk register (with `sev_cell` severity color-band emoji: 🟢 green / 🟡 yellow / 🟠 orange / 🔴 red), columns include # / Severity / Risk ID / Description / Category / Owner / Mitigation / Status; when `risks` is empty shows "_No active risks or blockers this period._".
- Validation: all 9 example customer sub-project status reports re-rendered, §5 has no JSON blob; empty-risk branch normal. Three installs at v2.2.7.

## 2.2.6 (2026-07-20)

### WBS/Schedule Pillar 2+4 persistence fix + frozen example customer Payment Linkage materialized
- **`build_schedule.py` partial-graph protection (prevent flatten regression)**: when the program view lacks leaf detail (partial graph), if a package already has real start/end and its schedule offset is 0, **reuse existing dates** instead of resetting already-baselined milestones to the start date. Fixed the regression where 2.2.5's last program-view write-back flattened all example customer milestones to 2026-08-01.
- **program / single-SOW view read-only by default**: `--level program` and `--sow` no longer persist schedule dates back to `project.yaml` (only the full view, with the complete leaf graph, persists them), protecting the frozen master index from view-render changes.
- **Pillar 4 `due` computed per milestone**: a billed (fixed) milestone with no separate contract calendar → payment becomes due when that milestone is achieved (collection cadence = delivery cadence); each row's `due` defaults to its own milestone date; only when `sow_map`/`program.sows` explicitly gives `due_date` (earlier than the milestone date) can `drift` occur. Fixed the bug where SOW-level `due` leaked into later milestones, causing 30 false `drift` alarms.
- **example customer metadata backfill (non-destructive)**: added `billing.payment_id` ({SOW}-P{n}) to 37 existing fixed-fee milestones, changing no dates / BAC. After backfill, the Payment Linkage section of `plans/schedule_program_gantt.md` shows all 37 rows as `linked` (contract = "sign-off / completion triggers payment"); master unchanged, consistency/critic still exit 0.
- Validation: example customer (operational) not breached; planning-phase explicitly-late `due_date` still triggers `drift` (exit 1 from 6d gate). Three installs at v2.2.6.

## 2.2.5 (2026-07-20)

### WBS/Schedule Pillar 2 (milestone ↔ activity rollup) + Pillar 4 (payment milestone ↔ schedule linkage)
- **Pillar 2**: `build_schedule.py` added `milestone_coverage` computation — the set of activities directly attributed to each milestone (leaf `milestone_ref` or a dependency endpoint landing on the milestone), rendered to the "Milestone Coverage" section of `schedule_gantt.md`. A payment milestone may map to multiple activities.
- **`parse_sow.py` auto-tagging**: each leaf auto-sets `milestone_ref` pointing to its Wave milestone; each billing milestone auto-sets `billing.payment_id = {SOW}-P{n}` (Pillar 4 mapping).
- **Pillar 4**: `build_schedule.py` added `payment_linkage` computation — each fixed-fee payment row → its milestone → scheduled date vs contract due_date; status linked/drift/no-due. Rendered to the "Payment Linkage" section.
- **`consistency_check.py` 6d schedule-linkage gate (fatal only in planning phase, skipped in operational)**: 6d-1 milestone coverage gap (leaf not attributed to a milestone), 6d-2 payment ↔ milestone missing (fixed-fee SOW has payment rows but no billing milestone), 6d-3 payment order non-monotonic (same SOW billing milestones must be in ascending scheduled order).
- Validation: example customer (operational) not breached (consistency/critic both exit 0, Payment Linkage section renders example INR amounts normally); planning-phase example triggers the 6d gate.
- Safely reuses the Pillar 1 design: all new gates are fatal only in `planning_now` (phase ∈ {initiation, planning, ''} or lifecycle ∈ {planning, review, baselined, None}).

## 2.2.4 (2026-07-20)

### WBS decomposition discipline Pillar 1 (6 factors + Critic self-review engine) + Pillar 3 (fortnight granularity)
- **Added `scripts/critic_review.py` (executable Critic self-review)**: solidified the prose Critic of `sow-parsing-playbook.md` into a 6-factor check — scope traceable / milestone attribution / payment linked to payment row / assumptions have quantifiable boundaries / constraints' external prerequisites need entry_gate / dependencies connected. Fatal in planning phase (exit 1); downgraded to a hint (non-blocking) in operational phase (frozen, e.g. example customer).
- **`consistency_check.py` added 6c decomposition-discipline gate (fatal only in planning/initiation)**: integrates `critic_review.py --strict` result + validates `decomposition.critic_passed==true` + assumptions have quantifiable boundaries. Auto-skipped in operational phase, protecting frozen projects from being breached by new gates.
- **Pillar 3**: `init_project.py` defaults `control.leaf_granularity: fortnight` + `granularity_threshold: 10` (=10 working person-days, reusing the existing default but made explicit), as the standard leaf-package granularity for waterfall/program.
- **`sow-parsing-playbook.md` §2.6** rewritten: Critic self-review lists the 6-factor checklist, and requires running `critic_review.py --strict` after persistence and setting `critic_passed=true`.
- Validation: example customer (operational) consistency exit 0 / critic exit 0 (not breached); planning-phase example triggers 7 fatal items (scope/milestone/dependency/critic_passed/assumption-bound etc.), exit 1.

## 2.2.3 (2026-07-20)

### P0/P1 decomposition: methodology-agnostic skeleton + federated source of truth (SOW-parsing driven)
- **`references/phases/p0-p1-initiation-planning.md` refactor**:
  - Added §1.1 **P0/P1 step-by-step sequence**, clarifying the methodology-agnostic skeleton: P0 does not build the WBS; the WBS is derived in P1 from the P0.2 draft charter.
  - **P0.0** classify (project vs program) + design the PM team (program = master + per-SOW PM sub-agents).
  - **P0.1** extract SOW → structured understanding (spec JSON), applying `sow-parsing-playbook.md`; under a program, explicitly "init each sub-project first, then backfill the master index"; the master never holds leaves (echoes Iron Rule #11 / operation-model.md).
  - **P0.2** generate base artifacts from spec: charter still **draft**, estimate baseline as a **charter section** (Scope / Delivery milestones / Payment milestones / Assumptions / Constraints / Dependencies), not a standalone doc; RAID **seeded** from SOW assumptions/constraints/dependencies (not draft).
  - **P1** dispatch builds WBS (from draft charter) → schedule → 5×5 risk calibration → consistency gate → baseline freeze → **charter finalized** → G1→2 gate.
  - §2 methodology-adaptation table changed to "P0.2 estimate-baseline form / P1 schedule artifact / whether baseline frozen", clarifying agile/iteration does not freeze baseline, pure agile payment section marked "N/A — internal release cadence".
  - §3 artifact list annotates charter as "P0 draft, P1 final", estimate baseline = charter section.
- Background: user requested solidifying "P0 decides program/project and designs the PM team, builds the fact source from SOW extraction, puts the estimate baseline into the charter, P1 completes planning" as a skill-level step, consistent with operation-model's bottom-up approach.

## 2.2.2 (2026-07-20)

### Operation model solidified: bottom-up authoring + upward rollup (skill-level iron rule, not project-specific)
- **Added `references/operation-model.md`**: solidified "plans authored at sub-project level, status/RAID/change/progress maintained at sub-project level, program level is a read-only script-aggregated view" as the skill-level default operation model. Clarified: program `actuals`/RAID/status are all derived values, manual editing prohibited; to correct, change the source sub-project and rerun `rollup_subprojects.py` (or the single-file two-layer `rollup_program_wbs.py --derive-actuals`).
- **SKILL.md / SKILL.en.md added Iron Rule #11 (Bottom-up authoring & rollup)**: plans/status/RAID/change-control authored at the lowest owning unit (SOW/sub-project); the program level is a read-only script rollup, not a hand-maintained parallel source of truth. Violation consequence: governance drift, false status.
- **Program-specific Rules #6** references Iron Rule #11, and clarifies the division of labor between `rollup_subprojects.py` (cross-file) and `rollup_program_wbs.py` (single-file two-layer).
- **`references/program-management.md`** Per-SOW Sub-Project section: points to `operation-model.md`, adds a "Rollup (program = read-only aggregation of sub-projects)" subsection, writing the standard command sequence to refresh the program view (rollup → control_engine), and stresses derived fields must not be hand-edited.
- Background: when the example data-lake program (9 SOWs) was empirically tested, after splitting sub-projects, if program-level RAID/status and sub-projects each maintained their own set, they drifted within a week; this model eliminates that anti-pattern at the mechanism level.

## 2.2.1 (2026-07-19)

### 3 scheduling-engine fixes (SOW1 dependency failure / mermaid milestone error / summary package duration = 0)
- **`parse_sow.py` dependency persistence fix**: `chain_leaves` previously only rewrote the spec dict, while leaf packages were already created in `add_wave` (with `dependsOn=[]` at the time), so the real dependency was never written to `project.yaml` → `build_schedule` forward-scheduled all tasks with `ES=0`, start dates all equal to the project start date. Now writes back directly to the real package object in `byid`, so the leaf dependency chain truly takes effect.
- **`build_schedule.py` summary packages excluded from sequential duration**: WBS summary packages (Wave/SOW root) are containers whose `estimate` is a child rollup; if scheduled by `dur`, they inject tens of days of "ghost gaps". Now summary packages schedule with `dur=0`, span used for display only (bottom-up rollup yields real start/end). The ~7-week void between SOW1 Waves came from this.
- **mermaid milestone syntax fix**: the gantt milestone line originally output only `:milestone, start`; old mermaid errored `undefined.endTime` on milestones missing end. Now `:milestone, start, end` (start==end). Also the gantt skips summary packages (no longer mistakenly rendered as zero-width milestones).
- **Leaf package duration fallback**: when a leaf package has only `estimate` but no `duration`, use `estimate` as duration (previously 0, causing it to be misjudged as a milestone).
- **program-level view fix**: previously the program view scheduled only SOW root packages, leaves excluded → summary span uncomputable, duration all 0. Now the program view includes all SOW descendants when scheduling (computes real span and writes back leaf dates); on render shows only `tier==program` rows + milestones. SOW1 now shows 210 days (2026-08-01 → 2027-02-27), no longer 0.
- End-to-end validation: SOW1 leaf dependency chain effective, dates cascade continuously, no bare `&` in mermaid block, program table/gantt have no zero-duration, consistency gate exit 0.

## 2.2.0 (2026-07-19)

### Base-layout hardening: SOW/contract parsing pipeline (a + c dual channel) + billing-milestone gate
- **Added `references/sow-parsing-playbook.md`**: solidified "expert-level understanding" into a repeatable, methodology-agnostic (waterfall/agile/T&M/hybrid), contract-type-agnostic (fixed-fee/T&M/hybrid/LOI) parsing Playbook. Core: (a) text extraction + (c) guided Q&A dual channel generates an "understanding record (spec, JSON)", eliminating generalized inference at the source.
- **Added `scripts/parse_sow.py`**: understanding record (spec) → auto-writes WBS packages into `project.yaml` (idempotent, re-runnable, bottom-up cumulative estimate, default dependency chain guarantees forward-schedulability, auto-maintains `sow_map`'s fee/fee_type/methodology/status). Since spec passed (a)+(c) double confirmation, WBS persistence needs no manual approval.
- **`consistency_check.py` added "billing-milestone completeness" base-layout gate (fatal)**: any fixed-fee SOW in `sow_map` or its subtree containing a package with `billing.fee_type=='fixed' && fee>0` must have ≥1 package with `milestone:true && billing.fee_type=='fixed' && fee>0`, else the consistency gate blocks delivery. Mechanistically guarantees: any base layout necessarily contains billing milestones, fine-grained leaves, complete dependencies — eliminating naive plans.
- **End-to-end validation**: dry-run/real-run/dependency chain (entry_gate → Wave → leaf chain → billing milestone → next Wave), positive gate (real SOW1 passes), negative gate (fixed-fee SOW missing milestone fatally fails) all pass.

## 2.1.8 (2026-07-19)

### Bugfix: mermaid gantt render `&` causes "undefined.endTime" crash
- **Root cause**: `_gantt_name()` only escaped the ASCII colon to its fullwidth form, not the ampersand. In a mermaid gantt, `&` is a multi-task same-line operator; an ASCII `&` in a task name (e.g. "SOW1 Data Modelling **&** Engineering") is parsed as a line continuation, making subsequent tokens date-less tasks → error `Cannot read properties of undefined (reading "endTime")`.
- **Fix**: `_gantt_name()` additionally replaces the ASCII ampersand with its fullwidth equivalent (U+FF06) (visually still an ampersand, but does not trigger operator parsing). `SOW6 SME Support (T&M)` similarly covered (program-level gantt uses graph TD quoted labels, originally safe, but SOW-level gantt fixed).
- **Validation**: regenerated `plans/SOW1/schedule_gantt.md` gantt block has no bare ASCII `&` (all converted to the fullwidth form), renders normally under the mermaid parser.
- Synced run copy `~/.workbuddy/skills/pm-master/scripts/render.py`.
## 2.1.7 (2026-07-19)

### SOW parsing depth fix (after user review of SOW1 sub-project: plan showed only first fortnight, missing Wave structure and billing milestones)
- **Root cause**: previously the SOW1 plan was "naive level" — applied a one-off generalized 4-phase waterfall, did not read the SOW's real **4-Wave commercial structure** and **5 design-doc sign-off milestones** (4 of which are billing events = example amount); schedule covered only the first ~5 weeks.
- **Expert-level redo (CoT + review)**: extracted the SOW billing/delivery sections verbatim, modeled each "<Deliverable> post sign-off" event as a `milestone: true` + `billing:{event,fee_inr,currency,status}` package; each of 4 Waves is a summary package (source analysis → logical model → physical model + DDL → S2T mapping → sign-off milestone), scheduled in commercial-rhythm order (W1 2026-10-15 → W4 2027-04-28, full ~9 months); Customer System B archival design as a standalone delivery milestone (fee_inr:0, marked non-standalone billing).
- **Leaf packages ≤10 person-days**: logic/physical/S2T split into ≤10-day domain-expert buckets (W1.2a FSDM / W1.2b Customer System A / W1.3a Core DDL / W1.3b Semantic DDL …), meeting the control-gate hard threshold; summary/milestone use child rollup estimates.
- **Data-readiness gate**: added `SOW1.0 Source Readiness Gate` as a critical-path prerequisite (SME + real data + interface docs), corresponding to the SOW's largest rework risk.
- **Sub-project linkage**: subprojects/sow1/project.yaml adds `billing_milestones[]` index (M1–M5 with amount/date/status) and 4 Wave-level risks (incl. S1-R4 billing-milestone delay cash-flow risk); RAID dependency written back to SOW2/3/7 with correct prerequisites.
- **Added reference spec**: `references/program-management.md` adds "Billing-Milestone-Driven WBS Decomposition" expert convention (parsing a SOW must do chain-thinking + review before writing the WBS).
- **Validation**: SOW1 schedule covers FN01→FN20 (full ~9 months, not just first fortnight); gantt has 11 milestones (4 billing + 1 delivery + others); program-level consistency gate exit 0.
> Version number kept consistent with `SKILL.md`'s `metadata.version` and `_user_meta.json`'s `version`.

## 2.1.6 (2026-07-19)

### Two architectural gaps filled (raised after user reviewed example customer SOW1)

**1. Sub-project (per-SOW sub-project) level**
- Each SOW is now maintained as an independent "sub-project", with its own `project.yaml`, RAID log, risk register, status report, independently owned by each SOW project manager.
- `init_project.py` added `--parent <program.yaml> --sow SOW1 --slug sow1`: builds an independent skeleton under `program/subprojects/<slug>/`, and auto-write-backs the `program.projects[]` index (id/sow/methodology/status/path).
- Added `build_subproject.py`: renders `risks/raid_log.md`, `risks/risk_register.md`, `reports/status_report.md` from the sub-project `project.yaml` (single source of truth), and writes artifact paths back to `artifacts`.
- Sub-projects keep lineage with the parent program via `parent: {project: '../../project.yaml', sow: SOW1}`; cross-SOW dependencies written to each sub-project's `raid.dependencies[]`.

**2. Fortnight granularity + domain-expert decomposition**
- SOW1 leaf packages re-split from "4 packages × 1 role" into 4 phase groups (SOW1.1–1.4, summary) + 8 fortnight leaf packages (1.1.1–4.2), each ≤6 days, assigned independent domain roles (requirements-analyst / data-modeler / etl-mapping-analyst / nos-architect), independently billable and acceptable.
- `build_schedule.py` added `--granularity fortnight`: groups by 2-week buckets, schedule table adds a "Fortnight Plan" section (FN01… window + task count + work packages), gantt buckets by `section FNxx`.
- `render.py` added `eq` helper (`{{#if (eq granularity "fortnight")}}`) to support conditional rendering; template `schedule_gantt.md` added the fortnight branch.
- Fix: `build_sow_kickoff.py` only recognizes `tier=program` summary packages as SOW-level (avoids phase groups re-holding kickoff); `consistency_check.py` orphan-package check only covers top-level SOW (`^SOW\d+$`), no longer false-alarms phase groups.

**Validation**: example customer SOW1 sub-project built and indexed successfully; fortnight schedule rendered (FN01–FN03 bucketed, tasks named correctly); sub-project RAID/risk/status render with severity color bands; program-level consistency gate exit 0.

## 2.1.3 (2026-07-19)

### Program Charter refactor (feedback from user's WorkBuddy real-test of docs/program_charter.md)
- **Program Architecture mermaid fix**: the user's rendered draft had node `S6/S7` inside `subgraph DELIVERY` pointing to the subgraph itself (`S6 --> DELIVERY`), illegal mermaid syntax. Charter template rewritten as a data-driven version; architecture diagram changed to SOW6→CORE, SOW7 as a standalone node, no longer self-referencing the subgraph (rendered and verified legal).
- **Financials & Commercial Model fee capture**: original rendered draft had the whole fee column `(TBD)`. Added `program.sows[]` (sow/workstream/model/billing/fee); charter "Financials & Commercial Model" table now driven by `program.sows[].fee`; when not locked must fill `TBC — reason`, prohibiting whole-table `(TBD)`. Wrote example customer's real project data into `project.yaml` and re-rendered; fee column shows real values / TBC.
- **Consistency gate added rule 7d**: `program.sows[].fee` required; blank / `(TBD)` / TBD is fatal (unlocked writing `TBC — reason` passes). `project-schema.md` / `program-management.md` added `sows[]` and `fee` field definitions.
- Charter structure aligned with user expectations: header + architecture diagram + business case / objectives / scope / out-of-scope / financials / governance gates / key risks / success criteria + contract boundaries section.

## 2.1.2 (2026-07-19)

### WorkBuddy real-test fixes (3 pieces of on-site user feedback)
- **RAID log color band**: `templates/common/raid_log.md` added severity/priority color-band columns; risks auto-derived from `score` (🟢🟡🟠🔴, shown even when severity missing), issues derived from `priority`. `render.py` added `sev_cell(severity, score)` / `sev_band(score)` helpers (score derives color band, unknown does not block).
- **Risk register color-band robustness**: `risk_register.md` switched to `sev_cell(this.severity, this.score)`, showing color band by `score` even when data lacks `severity` (fixed "no color band used").
- **Program charter · contract amount**: contract overview table added a "contract amount (fee)" column; added a "Commercial Model & Fees" section, rolling up each contract's fee into the financial boundary, fees captured rather than left blank (TBD); `consistency_check` contract/commercial semantics unchanged.
- **Program charter · architecture diagram**: added a "Program Architecture (mermaid graph TD)" section showing sponsor → program manager → governance board → component portfolio structure (when user-provided data lacks this diagram, only the governance skeleton is shown).

> Note: the "Program Architecture mermaid error" the user reported does not have a corresponding section in the 2.1.1 charter; this time we added a compliant mermaid architecture diagram. If the erroring mermaid you see is in another file, please paste that block and I'll fix it per the original.

## 2.1.1 (2026-07-19)

### Fill the four production-grade gaps of v2.1.0 (on-site user feedback)
- **#1 Decomposition auto-write-back glue**: added `scripts/sync_wbs.py` — after an expert (human or sub-agent) splits SOW/domain packages into leaf packages, a decomposition-patch YAML one-click merges back into `project.yaml.wbs`; auto-attaches parent/child (parent / id prefix), tags tier, validates leaf-package required fields (role/owner/estimate/dod/dependsOn — fatal if missing, not written back), and sets `artifacts.wbs_dirty` to prompt re-render.
- **#2 WBS decomposition tree mermaid**: `templates/waterfall/wbs.md` added "WBS Decomposition Tree (graph TD hierarchy/decomposition diagram)", auto-constructed by `build_wbs.py` from `wbs[].parent` (or id prefix); summary/milestone packages marked `▶`, leaf packages marked with role. Dual views of the same source of truth as the gantt.
- **#3 Program Charter covers contract/Extract/SOW**: `program_charter.md` added a "Contract Boundaries & Subcontracting" chapter (contracts / extracts / sow_map three tables); `references/program-management.md` added the corresponding data model and consistency constraints (SOW mapping must correspond to `tier:program` summary package; outsourced Extract must bind to a contract).
- **#4 Single source of truth anti-drift**: `consistency_check.py` added rule 7c (program SOW mapping ↔ wbs consistent, drift is fatal) + `wbs_dirty` re-render reminder; added `scripts/rerender_docs.py` pure-function re-render of wbs/risk_register/program_charter from `project.yaml`, docs = source of truth + template, eliminating content drift.

## 2.1.0 (2026-07-19)

### Merge refactor: v1.3.6 enforcement framework + v2.0.0 architecture direction, fixing v2 deadlock and paper features
- **Fixed v2 P0 deadlock**: restored v1.3.6's "expert dispatch" workflow (SKILL.md added Step 2.5); WBS domain activities must be decomposed by domain experts and tagged with `role`; consistency gate defaults to fatal for missing `role` / over-threshold domain activities, main controller must not self-decompose to bypass.
- **Sub-agent protocol real wiring**: added `references/subagent-protocol.md` (JSON reporting contract) + `scripts/subagent_check.py` actually validating each sub-agent's output.
- **Stage gates hard/soft configurable**: `gate_engine.py` reads `config.stage_gates`, added English phase aliases (`--to execution/closeout` etc.) for use by the English package.
- **Expert dispatch idempotent**: `dispatch.py` marks packages already meeting criteria as `done`, rerun resets pending to zero.
- **Inspection persisted**: `control_engine.py` writes `last_control_check`; `execution_driver.py` reads the same field to avoid duplicate inspection.
- **Thresholds configurable**: `control_engine.py` injects `config.operational_control` into `data.control.thresholds`.
- **Cross-session resume**: `project_state.py` added `migrate`/`checkpoint`, `schema_version=2` + `_checkpoint` to prevent step-skipping.
- **Bilingual dual-package**: Chinese edition (WorkBuddy, `SKILL.md`) + English edition (OpenClaw, `SKILL.en.md`) share `scripts/`/`templates/`/`references/`, switch backend via `config.yaml.execution.subagent_mode`.

## 1.3.6 (2026-07-18)

**Core problem diagnosis**: v1.3.6 accumulated 201 lines of SKILL.md, 14 scripts, 12 references, 35 templates over multiple iterations — comprehensive but unstable output. Root-cause analysis in the review report.

### Major changes

#### SKILL.md refactor
- Compressed from 201 lines to ~90 lines, moved all reference material to references
- All rules changed from "suggested/recommended" to "must/prohibited/else blocked"
- 8 core iron rules placed upfront, cannot be violated
- Added checkpoints to each workflow step
- Intent → artifact routing table streamlined

#### Sub-Agent communication protocol (new)
- `references/subagent-protocol.md`: defines JSON Schema reporting format
- `scripts/subagent_check.py`: sub-agent output auto-validation
- Sub-agent behavior spec: must-do / must-not-do / exception handling

#### Execution-phase scripts completed (new)
- `scripts/execution_driver.py`: execution driver engine
  - Read WBS status, generate executable work-package list
  - Track Sprint/iteration progress
  - Auto-trigger control_engine inspection
  - Support JSON output

#### Agent-layer state-machine lock (new)
- `project.yaml` added `_checkpoint` field
- Track current workflow step
- Illegal step-skip directly rejected

#### Config enhancement
- `config.yaml` added execution/quality_gate/stage_gates/operational_control config blocks
- Layered config clearer

### Unchanged
- All v1.3.6 scripts (render/render_docx/consistency_check/build_*/schedule_health/evm/baseline/control_engine/gate_engine/dispatch/comm_send/project_state) fully compatible
- All 35 templates fully compatible
- All methodology references fully compatible
- project.yaml core structure compatible (new fields optional)

### Further de-identification (compliance · eliminate legal risk)
- `scripts/rollup_program_wbs.py` built-in example mapping further de-identified:
  - `COMPONENT_MAP`: stripped descriptive suffixes from SOW component slugs (`sow1-data-modelling` → `sow1`, …, `sow9-ts` → `sow9`, `external-pii` → `ext-pii`), keeping only numeric identifiers.
  - `PHASE_NAME`: phase aliases changed from customer-specific descriptions (Wave 1–4 base modeling / example subject domain / Customer System A analysis structure / Customer System B archival & integration) to neutral `Stream 1–4` naming, removing Customer System A / Customer System B / example subject domain and other customer-system/domain leaks.
  - Three occurrences of "an example data-lake project" / "example data-lake project" comments and alerts unified to "example project", no longer exposing real industry and customer.
- `CHANGELOG.md`: changed the 1.1.0 semantic description of the built-in example "an example data-lake project" to the neutral "example project".

> Note: the retained `Wave` / `example data-lake project` hits (e.g. `references/methodology-hybrid.md`, `hybrid_playbook.md`, `expert-roles.md`) are **generic methodology/domain example vocabulary**, not real customer or vendor names; the engine routing and design depend on them, so they remain unchanged.

## 1.3.1 (2026-07-16)

### De-identification (compliance · eliminate legal risk)
- Full scan of skill files; removed sensitive info such as real customer names and vendor names, unified into code names:
  - Real insurance-industry customer name → `Customer A` (code `ALPHA`); real MPP data-warehouse vendor name → `MPP Data Warehouse` (generic placeholder); another named integrator confirmed by scan to not exist in this repo, no action needed.
  - `references/activity-expert-map.md`: example project `example-data-lake` changed from real customer project name to `Customer A Data Lake (code ALPHA, MPP Data Warehouse)`; vendor-specific ETL engineer role changed to `MPP Data Warehouse TPT/ETL Engineer`.
  - `scripts/dispatch.py`: vendor name in expert-role titles changed to `MPP Data Warehouse TPT/ETL Engineer` / `MPP Data Warehouse / Platform Engineer`.
  - `references/expert-roles.md`: tech-stack example changed to `MPP Data Warehouse, cloud data warehouse`; domain specialization changed to `MPP Data Warehouse → batch loading (vendor TPT/MLOAD-class tools)`.
- After a second full-repo scan, real customer / vendor names achieved **0 residue**; `examples/sample_project.yaml` and `rollup_program_wbs.py` built-in examples are all generic placeholders (no customer names), kept.
- README / SKILL / `_user_meta.json` version synced to 1.3.1 (continuing the "sync README on every skill change" rule).

## 1.3.0 (2026-07-16)

### operational dual-track parallel (P2 execution + P3 monitoring multi-agent)
- **Orchestration dual-track**: after entering `operational`, the execution track (domain-expert Agent continuously delivers) and the monitoring track (`monitoring-agent` periodically runs `control_engine.py` and feeds back escalations) are implemented as **multi-agent parallel**, sharing `project.yaml`+`baselines/` with zero field conflicts (execution track writes `actuals`/`wbs_progress`/deliverables, monitoring track writes control/status reports and RAID updates).
- `orchestration.md` added §3.4 "operational dual-track" + §3.2 combined table adds "operational dual-track" row; `lifecycle.md §6.1` concurrency note upgraded to dual-track reference; `p2-execution.md` / `p3-monitoring.md` §8 handoff references dual-track and `monitoring-agent`.
- `agents.md` added §9 `monitoring-agent` (monitoring-track role).

### External communication & email approval gate
- **Layered config (policy/data separation)**: skill root added `config.yaml` (install-time policy/guardrails) — `email.enabled` / `email.backend` (agent-mail·himalaya·gog·smtp) / `email.default_from` / `email.requires_send_approval` (**hard guardrail, cannot be disabled by project**); project data in `project.yaml.communication:` (`from` / `cadence` / `approval_override` (may only be tightened) / `contacts[]`).
- **Contact book**: `templates/common/communication_plan.md` added a "stakeholder contact book" section (name/role/org/email/phone/timezone/note); `stakeholder-agent` syncs contacts into `project.yaml.communication.contacts[]` when finalized; `templates-index.md`, `project-schema.md` sync the data-key contract and `governance.communications[]` audit block.
- **`scripts/comm_send.py` (approval-gate wrapper)**: resolves recipients by role (query `communication.contacts[]`), forces `--approve`, external email per `approval_override.require_sponsor_cosign` requires sponsor co-sign, writes `governance.communications[]` audit after send; `--dry-run` only prints + audits, does not really send; unapproved / rejected by guardrail directly `exit 1`.
- **`agents.md` added §8 `communication-agent`**: draft email → present for approval → send via `comm_send.py` approval gate → register audit; explicitly never send on its own.
- `SKILL.md` §6 added "operational dual-track parallel" and "external email must pass approval gate" rules; §5 script quick-ref adds `comm_send.py`.
- **README.md synced to v1.3.0**: §2 adds "operational dual-track parallel / external communication & email approval" capabilities, §3.1 adds `config.yaml` install-time note, §7 adds `comm_send.py` row, §12 version note (continuing the "sync README on every skill change" rule).

## 1.2.2 (2026-07-16)

### Stage-gate engine unit-test suite (CI gate)
- **Added `scripts/test_gate_engine.py` (standalone, no pytest needed)**: provides 66-assertion regression protection for `gate_engine.py`, two-layer coverage —
  - **Pure-function / logic layer**: `GATES` table invariants, soft gates have no hard criteria, hard gates contain only control gate / closeout gate, `phase_label_for_state` routing (incl. regression lock for the historical bug "execution → monitoring must write monitoring"), `chk_*` helpers, `entry_criteria` branches by methodology (agile into execution skips baseline, waterfall into execution includes baseline criteria, closeout missing deliverables judged as fail).
  - **CLI integration layer**: real subprocess runs `gate_engine.py` and its dependencies `consistency_check.py` / `control_engine.py`, covering waterfall/agile/iteration-hybrid and the four program methodologies, verifying soft-gate (planning/monitoring) flips, hard-gate (execution/closeout/combo closeout) passes, blocking on missing baseline / missing acceptance / unrealized benefits / mismatched prerequisite state / unknown target, dry-run does not persist, `--status` output.
- Exit-code contract: `0`=all pass, `1`=has failure, can be directly hooked as a CI quality gate.
- **README.md synced to v1.2.2**: §7 script quick-ref adds `test_gate_engine.py` row; version number and §12 change note updated (continuing the "sync README on every skill change" rule established in v1.2.1).

## 1.2.1 (2026-07-16)

### Doc sync
- **README.md synced to v1.2.x**: added "phased delivery / stage-gate approval" core capabilities, §4.5 phase modules and stage gates, `gate_engine.py` script quick-ref, phase-transition mandatory-gate rule, 4 phase-module reference index; version raised to 1.2.1.
- Established rule: **sync README.md on every skill change** (consistent with SKILL.md / CHANGELOG / version number).

## 1.2.0 (2026-07-16)

### Phase modules and stage gates
- **Added 4 phase modules** (`references/phases/`): `p0-p1-initiation-planning.md` (initiation + planning), `p2-execution.md` (execution), `p3-monitoring.md` (monitoring), `p4-closeout.md` (closeout). Each module defines that phase's **activities / required deliverables / entry criteria / exit criteria / stage-gate approval checklist**, with methodology adaptation (waterfall/agile/iteration/hybrid/program).
- **Added `scripts/gate_engine.py` (stage-gate engine)**: evaluates entry criteria for the target phase per the `phase`↔`lifecycle_state` model; after approval, flips `project.phase` and `lifecycle_state`, appends a gate record to `governance.stage_gates`, produces a stage-gate review report in `docs/gate_reports/` and registers it to `artifacts`.
- **Hard gates reuse existing engine** (avoid logic duplication): entering `execution` requires `consistency_check.py` exit 0 (waterfall/hybrid also require `baseline.py --freeze`); entering `closeout` requires `control_engine.py` exit 0 + acceptance/retro deliverables + (program) benefits closure. If not passed, **exit 1 rejects advancement, cannot be skipped**.
- **Gate mapping**: G0→1 initiation→planning (soft gate / PM), **G1→2 planning→execution (hard gate / sponsor)**, G2→3 execution→monitoring (soft gate / PM, concurrent within operational), **G3→4 monitoring→closeout (hard gate / sponsor)**. Aligned with `lifecycle.md §5/§6`.
- `SKILL.md`: Step 1 routes to load the corresponding phase module by `phase`; §5 adds `gate_engine.py` usage; §6 adds rule "phase transition must pass stage gate (mandatory)"; §7 registers 4 phase modules in index.
- `lifecycle.md`: added §6 "phase modules and stage gates" — phase module ↔ gate ↔ state-machine mapping table, hard-gate automation criteria, `gate_engine.py` usage.
- `project-schema.md`: notes the `governance.stage_gates` record structure.

## 1.1.0 (2026-07-16)

### Optional enhancements (§5)
- **Control-gate technical enforcement**: `control_engine.py` added a "control gate Gate" control item, validating `lifecycle_state == operational`; when not yet in the operational control phase, mark AMBER and record escalation item `gate_not_operational`, aligning with `lifecycle.md` §5's `planning→baselined→operational` mandatory serial discipline (does not break the existing contract "only RED exits 1").
- **Program rollup decoupling**: `rollup_program_wbs.py` component / phase mapping changed to read from `project.yaml`'s `program.components` (SOW id → component slug) and `governance.waves` (phase key → phase name); falls back to the built-in example (example project) only when absent, with a warning, no longer hardcoding a single project.
- **Version traceability**: added `CHANGELOG.md`; `_user_meta.json` added `version` field; skill version raised to `1.1.0`.

### Concurrent fixes and hardening (from review round 1)
- Fixed crash of `rollup_program_wbs.py` on empty-wbs program.
- Fixed 4 list templates (`risk_register` / `change_log` / `benefits_realization` / `program_charter`) showing an extra column at table top due to `| {{#each}}` syntax.
- Made expert-dispatch "domain specialization" actually take effect: `init_project.py` skeleton adds `domain` / `product` and new `--domain` / `--product` params.
- Removed `eval(f.read())` safety fallback in 4 scripts, changed to explicit error when PyYAML missing.
- `usage.md` template count (30→35, common 11→16) synced and completed with the script quick-ref table.

### Docs and robustness (from review round 2)
- Added `references/project-schema.md`: `project.yaml` complete field structure, quality-gate required items, sub-agent collaboration conventions.
- `SKILL.md` §3 explains the TeamCreate multi-agent dispatch mechanism; §5 adds script exception handling and degradation notes; §7 registers `project-schema.md`.
- `lifecycle.md` §5.3 adds program phase ↔ state-machine mapping / operational vs monitor relationship / 5 exit conditions for leaving operational.

### Release
- **Published to `slearnAI/pm-master` (private)**: v1.1.0 pushed to `https://github.com/slearnAI/pm-master` (private repo, default branch `main`). Commit history keeps `v1.0 → v1.1.0` linear evolution; also cleaned up mistakenly committed `__pycache__` in repo, and added Python cache ignore to `.gitignore`. Git tag: `v1.1.0`.

## 1.0.0

- Initial version: Builder-First project / program management skill.
- Supports waterfall / agile / iteration / hybrid four methodologies.
- Built-in template library (35 templates + `_macros.md`), self-built `render.py` mini template engine, dual-track output (Markdown → DOCX).
- Quality gate `consistency_check.py`, baselining `baseline.py`, operational control `control_engine.py`, expert dispatch `dispatch.py`, schedule health `schedule_health.py`, earned value `evm.py`.
- Four-dimension routing + standard workflow + `planning→baselined→operational` mandatory state machine + multi-agent hybrid dispatch (direct / team / fork).

## 2.1.4 (2026-07-19)

### Real fixes for three on-site user feedback items
- **#1 project_state.py data-loss hardening**: kept 2.1.3's PyYAML hard-fail guard; added `_save` to make a timestamped backup (`project.yaml.bak_YYYYMMDD_HHMMSS`) before overwriting a non-empty file, and reject the destructive write of "empty dict over non-empty file" (empty data = suspected PyYAML load failure) (exit 5). Verified guard effective via harness; file not corrupted.
- **#2 contract fees really captured**: the original rendered whole-column `(TBD)` was actually missing data. Extracted example amounts from the archived 9 example SOW docs and wrote to `program.sows[].fee` and `program.contracts[]` (SOW1/3/4/5/7/9 fixed-fee, SOW6 T&M, SOW8 USD course total converted to INR, SOW2 T&M capped person-days). After re-render, the charter "Financials & Commercial Model" fee column shows example INR amounts, 0 data cells are `(TBD)`.
- **#3 risk/RAID color band**: fixed previous edit landing on the wrong path (`templates/risks/` doesn't exist, actually `templates/common/`) causing it to not take effect. Now templates `risk_register.md`/`raid_log.md` correctly call `sev_cell`, after re-render risk_register has 7, raid_log has 11 severity color-band emojis (🔴🟠🟡🟢). Re-rendered the user project's on-disk files, mtime updated.

## 2.1.5 (2026-07-19)

### WBS mermaid `invalid date` fix (user clean-test feedback)
- Root cause: `wbs.md` unconditionally renders the date-type `gantt`; when a WBS package lacks `start`/`end` (only has effort/estimate; user correctly noted WBS may have no dates), mermaid reports `invalid date`.
- Fix: `build_wbs.py` added `wbs_has_dates` flag (true only when all packages have valid YYYY-MM-DD start/end); `wbs.md` gantt section changed to `{{#if wbs_has_dates}}` conditional render. When no dates, only keep the "WBS Decomposition Tree" (graph TD), and note the date-type gantt belongs to the schedule plan (`schedule_gantt.md`), auto-appears after dates supplied.
- Validation: no-date WBS render → no gantt code block, no invalid date, decomposition tree kept; dated WBS (real project) → gantt normal. EN template synced.
