# Claude Code host capability mapping

Start with the current student question using the [SKILL entrypoint](../../SKILL.md). Necessary authorized setup, testing or wrapper maintenance stays quiet and can run while awaiting an answer when the host supports it. Track actual background work, retain one intake draft and resume without another start choice; only a blocker requiring user action interrupts. The mappings below are used when their capability is needed, not recited before intake.

Default delivery: after profile confirmation and start, follow [quick planning](../quick-planning.md) and call `brief`. Render its `report_text` directly in the fixed seven-part order: score/rank, local 3/4/5 schools, three pathway families with 1/1/1 examples, other feasible pathways, current actions. The deep research matrix need not finish before this planning reference. The stage mappings and receipt rules below describe optional deep verification with `finish`; do not apply their all-tasks-completed requirement to `brief`.
- Only for requested deep verification, when starting or resuming discovery, extraction, or evidence work, read the [retrieval playbook](../retrieval-playbook.md).
- For deep certification, before classifying, deduplicating, admitting, or resolving a source conflict, read the [source policy](../source-policy.md).
- When a tool, source or parser fails, read the [research recovery guide](../research-recovery.md) and continue within the verified evidence limits.

## Intake boundary

Follow the one-question-at-a-time intake in SKILL.md. Accept each answer as ordinary conversation text, retain the private draft across turns, and show only the current question and its choices. Wait for the reply before advancing. Use the bounded thematic questions in the questionnaire: related details share one question, already answered details are reused, and only decision-relevant gaps get one clarification per theme (six total). Preserve uncollected details separately from explicit unknown or refusal. Use a currently available choice control for one question when it can hold all choices, otherwise show lettered choices. Only the user selects or skips; an unanswered item stays pending.

Accumulate explicit answers under the twenty internal topic keys, then call `build_profile_from_questionnaire` only after collection is complete. `parse_numbered_questionnaire` is optional compatibility for a complete numbered document volunteered by the user, not a requirement for conversational replies. The mapping exists only inside the host; never ask the user for JSON or a path. An explicitly unknown readiness, strength, activity subtype, constraint, or preference remains `unknown` or empty instead of being inferred. Follow the separate profile confirmation gate before research.

Preserve the actual exam scope: school monthly/term/mock exams use school; confirmed joint exams use province_joint or city_joint. Use province_official only for an actual formal provincial gaokao result. A school-issued official report, a 750-point maximum or a calculation error never permits relabeling a school exam.

## Capability map

Examples are conditional on tools callable in the current session. Inspect them before declaring anything, then apply the linked policy/playbook unchanged.

| Capability | Use | Declare | Absent fallback |
|---|---|---|---|
| search | Callable web search/fetch discovery tools find candidate public pages. | Pass --host-capability search only when callable now. | With browse, read known official URLs in standard and disclose limited discovery; retain already authenticated material. Without a source reader, use offline mode. |
| browse | Callable web search/fetch page reading opens public pages and inspects citations. | Pass --host-capability browse only when callable now. | Try another available page or HTTP reader first. If none works, do not claim page verification; use already authenticated material or offline mode. |
| vision | Host vision inspects supplied public images or host-produced OCR and QR text only when exposed. | Pass --host-capability vision only when callable now. | Seek machine-readable HTML/XLS/XLSX/PDF/text or host-decoded QR payload, or mark the fact missing; the normal boundary remains local/host-native. |
| local_exec | Callable shell/local file tools run repository CLIs, adapters, and validators. | Workflow gate only; record its state in the handoff. | Without it, stop before deterministic calculation and disclose the limitation. Complete intake and profile confirmation first, then deliver the same seven-part reference using genuinely available evidence. Label uncomputed values unknown, disclose that calculation did not run, retain a resumable handoff, and never emulate a calculated result. |
| file_output | Callable shell/local file tools create the evidence workspace and anonymous Markdown or DOCX. | Workflow gate only; record its state in the handoff. | Retain a path-neutral structured handoff internally and explain permitted conclusions in chat; do not claim an evidence bundle or report was written. |
| offline | The explicit no-live-network branch consumes authenticated local material. | Pass no search or browse claim and record the offline branch. | Remain no-live-network, pass no search/browse claim, use only authenticated local inputs from the user or earlier retrieval in this session, and label current/live facts unavailable. |

Capability loss changes coverage only; it never relaxes the linked policy. The linked retrieval playbook is the only session-loop definition; this guide adds no separate step sequence.

Preflight declarations do not prove a browser launched or a website responded. Test the available original-source reader. With browse alone, standard can read known official URLs and public navigation; search loss limits discovery, not every source. Browse includes a working host page reader or HTTP reader. Chrome failure does not disable those alternatives, and no named search API is mandatory. Without any original-source reader, use the explicit offline branch; search snippets cannot establish facts. Follow the recovery guide to stop a failed tool branch, preserve other work and close only affected tasks with their actual unavailable reasons.

When an active QueryPlan pathway has missing, masked, partial, or conflicting policy evidence, pass the typed pathway observation through calculation instead of dropping that pathway. Preserve only real source IDs; a source-free missing observation stays source-free and must not acquire a policy year, target rank, deadline, or qualification conclusion.

After `finish`, read `delivery` and `research_summary` alongside the complete `report_text` and `sources` to deliver the detailed
reader-facing conclusions directly in the conversation, following SKILL.md and
references/conversation-output.md. Explain every school/pathway decision, its
reason, constraints, next actions and uncertainty. Keep the report file as an
optional attachment at the end; a file path, download link or short summary is
not a completed user-facing delivery.

All-unavailable can still reach finish and return sources=[] with profile_only. Explain a useful preparation version from the confirmed profile, label preparation advice clearly, and keep unsupported ranks, schools, deadlines and qualification judgments unknown. With partial evidence, deliver supported conclusions and specific gaps. Task closure is not evidence success. The older_year_resolution hints do not change tasks; only an explicit unavailable command with the verified newer receipt can close comparable old tasks. Do not make the family choose between repairing the environment and an unsupported estimate.

## Safety boundary

A text-only session follows the standard or offline fallback instead of inventing vision. Browser and search tools discover or read public content. Retrieved attachments cross `scripts.downloader`; QR adapters receive decoded text rather than images. Never silently use a third-party OCR service. External OCR or QR processing requires explicit user authorization and evidence disclosure; the default is local/host-native processing or a missing fact.

Use the scripts.host_workflow facade for start, next, ingest, unavailable and finish. The facade owns the journal; the Agent does not separately create, save or edit journal revisions. Its internal implementation uses the public `scripts.planning_session.PlanningSessionReplayJournal` in the private workspace: it saves the confirmed profile, then the preflight capability report and canonical QueryPlan. Before research, `bundle_path` is `None` and `task_outcomes` is empty. It checkpoints every `ingest` and `unavailable`, then `finalize_evidence` and `with_calculation`, retaining the current bundle and completed typed outcomes. These are implementation invariants, not a second host command sequence.

After process loss, run the same facade next command with the original `--workspace` and `--session`; then continue ingest, unavailable or finish. The facade's PlanningWorkflow.resume internally calls `journal.load(session_id[, revision])` and the existing finalize/calculate/publish context methods. The `profile_confirmed`, `preflight_complete`, `query_plan_ready` and `research_in_progress` checkpoints determine which internal work remains. A `status` snapshot is diagnostic only; never promote it or a digest into a completed receipt, and never double-write the journal through low-level APIs.

Keep search, logs, evidence IDs, and output names free of PII, credentials, private paths, raw local filenames, and student identifiers. Never claim live verification without opening the original source through an available reader, a written file without file output, or calculation without local execution and validation.
The host owns all session JSON, commands and paths. Never ask the user to author or locate them.
