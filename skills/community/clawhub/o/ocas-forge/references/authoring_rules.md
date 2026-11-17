# OCAS Skill Authoring Rules

Version: 3.1.0
Author: Indigo Karasu

Changes from 3.0.0: Added Rule 9b "Never inline credential-adjacent descriptions in SKILL.md" — extends the existing Rule 9 (no inline credential code) to also cover credential file paths, token status descriptions, config defaults naming credential files, wallet/account setup commands, and fallback cascade credential references. All must be extracted to reference files. Added May 2026 examples from Bones and Dispatch refactors. Renumbered old Rule 7 (absorption) to Rule 10 to make room.

Changes from 2.9.0: Rule 7 strengthened from guideline to hard gate. Phase 1 existence check (parent search, standalone test, absorption test) is now pass/fail — build does not proceed unless all 3 pass. `## Integrated:` wrapper sections explicitly prohibited (they are duplication, not integration). Must fold absorbed content into parent's existing section structure. Updated Responsibility Boundaries to reflect current active skill set.

Changes from 2.8.0: added Rule 7 "Prefer absorption over orphan creation" — when a capability naturally belongs inside an existing umbrella skill, add it as a reference/script rather than creating a standalone skill. Key indicators: process-heavy tasks → scripts/; session-specific detail → references/; subordinate commands → new SKILL.md section. Major version bump because this changes the fundamental decision of when to create vs. absorb.

Changes from 2.7.2: architecture coherence audit 2026-04-16 discovered 2 active OCAS skill repositories (ocas-forge, ocas-relay); updated Responsibility Boundaries list to add ocas-relay; updated Background Tasks section to reflect both active skills; minor version bump due to expansion of active skill count.

Changes from 2.7.1: clarified README.md and CHANGELOG.md requirements per spec-ocas-skill-publishing.md; patch version bump for documentation enhancement.

Changes from 2.7.0: architecture coherence audit 2026-04-12 discovered only 1 active OCAS skill repository (ocas-forge); ocas-triage design specs retained but no GitHub repository instantiated; updated Responsibility Boundaries list to remove ocas-triage and move it to legacy reference; clarified Background Tasks section to reflect only ocas-forge as active; patch version bump due to scope refinement within existing active skill count.

Changes from 2.6.4: architecture coherence audit 2026-04-11 discovered only 2 active OCAS skill repositories (ocas-forge, ocas-triage); updated Responsibility Boundaries and Background Tasks sections to reflect current active skills; other 22 previously-documented skills marked as archived/non-existent; major version bump due to scope change from 24 skills to 2 active implementations.

Changes from 2.6.3: added explicit Background tasks sections to ocas-multipass, ocas-triage, and ocas-vibes documenting that they have no operational background tasks; created skill.json files for all 24 OCAS skills; architecture coherence audit 2026-04-09.

Changes from 2.6.2: removed ocas-relay from Responsibility Boundaries list (skill does not exist as OCAS architecture component); confirmed all 24 active OCAS skills in boundaries list; architecture coherence audit 2026-04-07.

Changes from 2.6.1: verified all 24 OCAS skills have Ontology types sections per requirements; documented that each skill explicitly declares entity extraction behavior and Signal emission policy; completed comprehensive audit on 2026-04-05.

Changes from 2.6.0: added ocas-multipass and ocas-vibes to Responsibility Boundaries list; updated to reflect all 24 active OCAS skills as of 2026-04-04.

Changes from 2.5.0: updated Background Tasks skill lists to reflect current state (added ocas-sands, ocas-haiku, ocas-custodian, ocas-dispatch to cron list); clarified universal self-update cron is not counted as operational background task; updated cron CLI syntax to match openclaw cron add specification (--session, --message, --light-context, --tz flags); removed ocas-dispatch from purely reactive list.

---

## Purpose

These rules define how OCAS Agent Skills should be designed, packaged, and validated. The standard is disciplined minimalism: build the smallest skill that reliably improves agent behavior.

---

## Core Rules

### 1. A skill must earn its existence

Create a skill only when at least one of these is true:
- The task depends on a repeated tool or command surface
- The task has repeated structure worth encoding
- The task needs domain-specific workflow the base model will not reliably infer
- The task benefits from reusable templates, schemas, or validators
- The task is frequent or valuable enough to justify maintenance

Do not create a skill when:
- The behavior is already ordinary model behavior with no special workflow
- The scope cannot be reduced to one sharp promise
- The task is too rare to maintain
- The package would mostly contain generic explanation

### 2. Every skill needs one sharp promise

Complete this sentence: "This skill exists to ______."

If the answer sounds like a platform, department, or product suite, the scope is too broad.

### 3. Routing comes first

The description is routing logic, not branding copy.

A good description:
- Says what the skill does
- Says when to use it
- Uses realistic request language where helpful
- Distinguishes trigger from nearby non-trigger cases

### 4. SKILL.md is the operational surface

SKILL.md contains:
- When to use the skill
- What the skill is responsible for
- How to execute the task
- When to consult any support file

SKILL.md does not become:
- A tutorial for beginners
- A README substitute
- A changelog or design diary
- A knowledge dump

Every skill package requires a `README.md` and `CHANGELOG.md`. Structure and format are defined in `spec-ocas-skill-publishing.md` in the architecture repo. Follow that spec exactly — it is the single source of truth for README sections, CHANGELOG entry format, versioning rules, and GitHub release convention.

### 5. Match specificity to failure risk

Use general guidance when multiple approaches are acceptable. Use exact instructions, schemas, or scripts where drift is costly.

High-risk areas: command syntax, file paths, metadata fields, package structure, validation logic.

### 6. Add complexity only when justified

Minimum package:
```
ocas-{skill}/
  skill.json
  SKILL.md
```

Add `references/`, `scripts/`, or `assets/` only when they materially improve correctness, maintainability, or output quality.

### 7. Prefer absorption over orphan creation

When a capability naturally belongs inside an existing umbrella skill, **do not create a new standalone skill**. Instead:

- **Process-heavy tasks** (maintenance procedures, sync pipelines, enrichment workflows) → add as `scripts/<name>.py` in the parent skill
- **Session-specific reference detail** (provider quirks, auth patterns, debugging notes) → add as `references/<topic>.md` in the parent skill
- **Subordinate commands** that are only meaningful in the context of the parent → add as a new section in the parent's SKILL.md

**Rule of thumb:** If the new "skill" would have its own cron jobs, its own journal output, and its own independent reason to exist → standalone is fine. If it's a procedure the parent skill's agent would run → it belongs inside the parent.

**Before creating a new skill, ask:**
1. Does an existing skill already own this domain? → Add a reference/script to it instead.
2. Is this a sub-process of something that already exists? → Nest it, don't spawn it.
3. Would this skill never be invoked independently? → It's not a skill, it's a support file.

**Example consolidations from May 2026:**
- Bank sync pipeline (financial-sync) → `references/financial-sync.md` in `ocas-styx`
- Storage cleanup procedures (system-maintenance) → `references/system-maintenance.md` in `ocas-custodian`
- Weave DB maintenance queries (weave-db-maintenance) → `references/database_maintenance.md` in `ocas-weave`
- Dispatch status diagnostics (dispatch-status-from-files) → `references/status_from_files.md` in `ocas-dispatch`
- Expansion pipeline (ocas-expansion) → already integrated in `ocas-weave/SKILL.md`
- Bower mempalace ingest (bower-mempalace-ingest) → already in `ocas-bower/scripts/`

### 8. Keep SKILL.md under 500 lines

Automated quality auditors (e.g., agentskill.sh) flag SKILL.md files over 500 lines as structural issues. Target:

- Shortcut skills: 20–120 lines
- Workflow skills: 80–250 lines
- System skills: 150–300 lines (move secondary detail into references/)

When a skill grows beyond 500 lines, extract operational detail into `references/<topic>.md` files and replace inline content with one-line pointers. The SKILL.md should contain the operational surface; reference files contain the deep detail.

**Code ratio target:** SKILL.md body should be under **15% code** (fenced-block lines ÷ total lines). Measure with the script in `references/code-ratio-reduction.md` (in review-skill). Anything over 30% is a definite problem requiring extraction.

Common targets for extraction:

| Block type | Move to |
|---|---|
| SQL DDL / schemas | `references/schema.md` |
| Python query examples | `references/query-api.md` |
| JSON/YAML schemas | `references/data_model.md` |
| Storage directory trees | `references/data_model.md` |
| Default config files | `references/data_model.md` |
| OKR / scoring YAML | `references/data_model.md` |
| Cron setup commands (bash) | `references/data_model.md` |
| Self-update bash scripts | `references/data_model.md` |
| Pipeline stage diagrams | `references/pipeline.md` or `references/enrichment-pipeline.md` |
| Large markdown tables (10+ rows) with code-like content | `references/<topic>.md` |
| One-off code examples | `references/<topic>.md` |

**Replacement pattern:** For each removed block, replace with a one-line prose summary + pointer link + 2-3 critical items as bullets. Keep the summary short — the reference file has the detail.

**Example (May 2026, ocas-styx):**
- Removed: 47-line SQL DDL block, 42-line Python query examples (3 blocks), 26-line pipeline stage diagram
- Added: `references/schema.md`, `references/query-api.md`, `references/enrichment-pipeline.md`
- Result: code ratio 32.6% → 7.1%

**100/100 pattern:** Skills scoring 100/100 on agentskill.sh quality share these traits: body 250-420 lines, no inline credential handling, minimal external curl commands, strong trigger phrases with clear "Use when" sections, concise instructions without excessive operational detail. See `references/agentskill-evaluation-criteria.md` in skill-publish for the full scoring rubric including all 4 quality dimensions and 12 security categories.

### 9. Never inline credential-handling code in SKILL.md

Automated security auditors (e.g., agentskill.sh) flag any instruction that reads, writes, or manipulates credential files as "Credential Harvesting" — even when the code is the skill's own diagnostic procedure.

**Rule:** All credential-handling code (token file reads, scope checks, refresh token diagnostics, credential path fixes) must live in `references/` files, not inline in SKILL.md. Replace inline credential code with a one-line reference:

```
See `references/<token-diagnostics>.md` for the diagnostic procedure.
```

This applies to: OAuth token files, API keys, client secrets, refresh tokens, and any file under `credentials/` or similar paths. The reference file can contain the full code; the SKILL.md should not.

**Example (May 2026):** Weave's SKILL.md had inline Python code that read the Google OAuth token file to diagnose scope issues. The security auditor flagged this as "Credential Harvesting" (2 CRITICAL). Moving the code to `references/google-token-diagnostics.md` and replacing the inline block with a reference link resolved both findings.

### 9b. Never inline credential-adjacent descriptions in SKILL.md

Security scanners also flag **descriptions** of credential structure and token status — not just code. These must be extracted to reference files too:

- **Credential file paths** (`kalshi_creds.json`, `wallet.json`, `<user-google-email>.json`, etc.) → credential-file reference
- **Token status** (which token is broken, error types like `invalid_grant`, `AUTH_SCOPE_MISMATCH` false positives) → `references/token_status.md`
- **Config defaults that name credential files or API key setup steps** → `references/config-default.json` (machine-readable) + pointer from SKILL.md
- **Wallet/account setup commands** (`eth-account`, `py_clob_client`, API key creation) → `references/account-creation.md`
- **Fallback cascade steps that reference credential file names** → pointer to token-status reference

**Pattern:** When a section describes *what credentials exist* or *where they live*, move it to a reference file and replace with a one-line pointer.

**Example (May 2026):** Bones' SKILL.md had a config-default description naming platforms and trading settings inline. Dispatch's fallback cascade named `<user-google-email>.json` directly, and its Gotchas repeated the `<agent-email>.json` path with error details. All moved to reference files:
- Config description → `references/config-default.json`
- Token paths/status → `references/token_status.md`
- Wallet setup → `references/account-creation.md`
- Fallback cascade credential reference → pointer to `references/token_status.md`
- Gotchas token status bullet → pointer to `references/token_status.md`

### 10. Prefer absorption over orphan creation

When a capability naturally belongs inside an existing umbrella skill, **do not create a new standalone skill**. Instead:

- **Process-heavy tasks** (maintenance procedures, sync pipelines, enrichment workflows) → add as `scripts/<name>.py` in the parent skill
- **Session-specific reference detail** (provider quirks, auth patterns, debugging notes) → add as `references/<topic>.md` in the parent skill
- **Subordinate commands** that are only meaningful in the context of the parent → add as a new section in the parent's SKILL.md

**Rule of thumb:** If the new "skill" would have its own cron jobs, its own journal output, and its own independent reason to exist → standalone is fine. If it's a procedure the parent skill's agent would run → it belongs inside the parent.

**Before creating a new skill, ask:**
1. Does an existing skill already own this domain? → Add a reference/script to it instead.
2. Is this a sub-process of something that already exists? → Nest it, don't spawn it.
3. Would this skill never be invoked independently? → It's not a skill, it's a support file.

**Example consolidations from May 2026:**
- Bank sync pipeline (financial-sync) → `references/financial-sync.md` in `ocas-styx`
- Storage cleanup procedures (system-maintenance) → `references/system-maintenance.md` in `ocas-custodian`
- Weave DB maintenance queries (weave-db-maintenance) → `references/database_maintenance.md` in `ocas-weave`
- Dispatch status diagnostics (dispatch-status-from-files) → `references/status_from_files.md` in `ocas-dispatch`
- Expansion pipeline (ocas-expansion) → already integrated in `ocas-weave/SKILL.md`
- Bower mempalace ingest (bower-mempalace-ingest) → already in `ocas-bower/scripts/`

## Skill Types

### Shortcut
Narrow tool wrapper or repeated small action.

Typical SKILL.md size: 20–120 lines.

Sections: title, when to use, quick actions or commands, inputs/options, caveats.

### Workflow
Multi-step process with moderate branching.

Typical SKILL.md size: 80–250 lines.

Sections: title, when to use, inputs/assumptions, ordered workflow, output requirements, boundaries and pitfalls.

### System
Meta-skill or durable behavior system with broader internal logic.

Typical SKILL.md size: 150–300 lines. Move secondary detail into references/.

Sections: title, trigger conditions, purpose and boundaries, decision model, execution loop, support file map, validation rules.

---

## Storage Requirements

Every skill with persistent state stores data centrally. No data inside the skill package directory.

```
{agent_root}/commons/data/{skill-name}/   — state, config, JSONL logs
{agent_root}/commons/journals/{skill-name}/YYYY-MM-DD/{run_id}.json  — journal files
```

LadybugDB skills only:
```
{agent_root}/commons/db/{skill-name}/     — LadybugDB database files
```

Config file location: `{agent_root}/commons/data/{skill-name}/config.json`
Config must include ConfigBase fields from `spec-ocas-shared-schemas.md`.

See `spec-ocas-storage-conventions.md` for the full standard.

---

## Journal Requirements

Every skill run writes a journal. Runs missing journals are invalid.

Journal file location: `{agent_root}/commons/journals/{skill-name}/YYYY-MM-DD/{run_id}.json`

Select journal type based on whether the run executes external side effects:
- **Observation Journal** — no external side effects (reading, analyzing, discovering)
- **Action Journal** — external side effects occurred (sending, writing, booking, syncing)
- **Research Journal** — structured multi-source research session

Some skills emit multiple types depending on the command (e.g., Rally emits Observation during research and Action during trade execution).

See `spec-ocas-journal.md` for the full specification.

---

## Inter-Skill Communication Requirements

Skills communicate through defined intake directories, not direct calls.

If a skill sends signals to another skill or receives signals from another skill, it must reference `spec-ocas-interfaces.md` for the path and format.

Do not create undocumented inter-skill interfaces.

---

## Background Tasks

Some skills require work to happen on a schedule, independent of user invocation. These are background tasks. Most skills do not need them.

### Decision rule: cron vs. heartbeat

Use **cron** when:
- Exact timing matters (briefing at 7am, market open)
- The task is heavyweight (journal ingestion, deep consolidation)
- The task should run in isolation with no main session history
- Output should be delivered to a channel

Use **cron** for all background tasks. Hermes has no heartbeat mechanism.

### Which skills need background tasks

**Note:** All skills have a `{skill}:update` cron job at midnight for self-updates from GitHub. This universal update task is not counted below — the lists below refer to skills with _operational_ background tasks beyond self-update.

**Current active OCAS skills:**

- Skills with heartbeat entries only: ocas-forge (intake poll)
- Skills with cron jobs only: ocas-relay (update only)

**Note:** This reflects the current OCAS ecosystem as of 2026-04-16. Additional skills (ocas-elephas, ocas-mentor, ocas-corvus, ocas-vesper, ocas-rally, ocas-thread, ocas-sands, ocas-haiku, ocas-custodian, ocas-dispatch, ocas-weave, ocas-scout, ocas-sift, ocas-look, ocas-taste, ocas-voyage, ocas-fellow, ocas-multipass, ocas-vibes, ocas-bower, ocas-spot, ocas-praxis, ocas-triage) are documented in these specs for historical reference and architecture integrity, but are not currently instantiated as repositories or released packages.

### Idempotent registration

Background tasks are registered during `{skill}.init` (which runs automatically on first use). Before calling `cron.add`, always check existing jobs first to avoid duplicates:

```bash
openclaw cron list   # check before registering
```

In agent tool calls: list existing jobs, check for the target name, add only if absent.

Job names follow the pattern `{skill-short}:{task-short}` for stable identification. Example: `elephas:ingest`, `vesper:morning`.

### SKILL.md declaration

Every skill that has background tasks must include a `## Background tasks` section in SKILL.md declaring:
- Job name
- Mechanism (cron or heartbeat)
- Schedule
- What command or action it triggers

Skills with no background tasks omit this section entirely.

### Cron job conventions

All isolated cron jobs use these flags with `openclaw cron add`:
- `--session isolated` — dedicated fresh agent session
- `--light-context` — skip workspace bootstrap to minimize token cost
- `--tz America/Los_Angeles` — timezone for schedule evaluation (update once user's timezone is known)

For main-session jobs, use `--session main --system-event "text"` with `--wake now` or `--wake next-heartbeat`.

Registration syntax:
```bash
openclaw cron add --name "{skill}:{task}" --cron "M H D Mo DoW" \
  --session isolated --message "{skill}.{command}" --light-context --tz America/Los_Angeles
```

One-shot jobs use `--at "ISO8601"` instead of `--cron`. Interval jobs use `--every "duration"`.

Manage existing jobs: `openclaw cron list`, `openclaw cron edit <id>`, `openclaw cron rm <id>`, `openclaw cron run <id>` (manual trigger).

### Cron registration (all tasks)

All background tasks use cron. Hermes has no heartbeat mechanism.

---

## Package Structure Rules

### Base package
```
ocas-{skill}/
  skill.json
  SKILL.md
```

### references/
Use only when material is useful but too secondary or detailed for SKILL.md: longer examples, schemas, tables, templates, review checklists.

Rule: if a reference file exists, SKILL.md must state when and why to read it.

### scripts/
Use only when deterministic help materially improves reliability: validation, scaffolding, transformation, linting.

Rule: do not add scripts for ornament or theoretical completeness.

### assets/
Use only when the skill ships reusable operational artifacts: starter files, canonical examples, templates.

---

## Required SKILL.md Sections for System Skills

System skills must include:

**Responsibility Boundary** — what the skill does, what it does not do, which other skill owns the adjacent responsibility.

**Optional Skill Cooperation** — other skills this skill may cooperate with when present, but never depend on.

**Ontology Mapping** — which entity types from `spec-ocas-ontology.md` this skill extracts, manages, or queries. Skills that extract no entities and query none may omit this section.

**Journal Outputs** — which journal type(s) this skill emits.

**Storage Layout** — the skill's data and journal paths under `{agent_root}/commons/`.

**Background Tasks** — cron jobs and heartbeat entries required by this skill, with job names, schedules, and registration commands. Omit if the skill has no background tasks.

---

## Responsibility Boundaries

Before creating a new skill, verify it does not conflict with the following active OCAS skills:

- ocas-forge — skill design, construction, and validation
- ocas-relay — device gateway, telemetry ingestion, permission management

Legacy reference (archived/non-existent): ocas-scout, ocas-sift, ocas-praxis, ocas-dispatch, ocas-corvus, ocas-mentor, ocas-elephas, ocas-weave, ocas-taste, ocas-voyage, ocas-look, ocas-rally, ocas-vesper, ocas-fellow, ocas-thread, ocas-custodian, ocas-haiku, ocas-bower, ocas-spot, ocas-sands, ocas-multipass, ocas-vibes, ocas-triage

Each skill build spec includes a Responsibility Boundary section.

---

## Authoring Style

- Prefer concise, operational language
- Prefer examples over exposition
- Avoid repeating the same rule across files
- Define non-public terminology locally if it appears
- Write build specs as if they will be the only file a coder LLM sees
- Avoid negative instructions that merely mention absent resources

---

## Atomic Skill Principle

Skills perform one clear role. They may cooperate with other skills when present but must never depend on them.

If a cooperating skill is absent, the skill must still function normally.

---

| Frontmatter block scalars (`description: >` or `description: |`) | NEVER use `execute_code` with `content.split('---')` to edit frontmatter — embedded newlines in block scalars cause truncation. Use `read_file` for exact line ranges, then `patch`. Always verify YAML parses after editing. |

## Anti-Patterns

- Vague names: `helper`, `utils`, `tools`
- Descriptions that state only a broad category with no trigger condition
- SKILL.md that contains every rule, example, and edge case
- Support directories created "just in case"
- Build specs referencing prior drafts, hidden memory, or internal process documents
- Template residue: placeholders never concretized
- Storage inside the skill package directory
- Undocumented inter-skill interfaces

---

## Variant Naming Convention

Skill variants follow a standardized naming format for identification in journals, OKR evaluations, and promotion decisions.

### Format

```
{skill-id}-variant-{YYYYMMDD}
```

Examples:
- `ocas-rally-variant-20260307`
- `ocas-scout-variant-20260315`
- `ocas-sift-variant-20260401`

### Rules

- The date is the date the variant was created (not proposed or promoted).
- If multiple variants of the same skill exist on the same date, append `-2`, `-3`, etc.: `ocas-rally-variant-20260307-2`.
- Variant IDs appear in: VariantProposal, VariantDecision, CycleResult, and journal entries for that variant's runs.
- The variant's `skill_version` field in its journals should reflect its version string (e.g., `1.2.0-variant-20260307`), distinct from the champion's version.

---

## Bundled Workflow Plans

Skills that are commonly invoked as part of multi-step cross-skill workflows should ship bundled plans. Plans are stored at `references/plans/` in the skill package and copied to `{agent_root}/commons/data/ocas-mentor/plans/` during Mentor initialization.

Skills expected to bundle plans:

| Skill | Plan ID | Description |
|---|---|---|
| ocas-scout | `contact-enrichment` | Full research pipeline for a known contact |
| ocas-sift | `research-deep-dive` | Multi-source research on a topic or entity |
| ocas-rally | `portfolio-rebalance` | Signal refresh → scoring → allocation review |
| ocas-voyage | `trip-planning` | Destination research → itinerary → accommodation |
| ocas-taste | `preference-scan` | Ingest recent activity → update preference model |

To add a bundled plan:
1. Create `references/plans/{plan_id}.plan.md` following `spec-ocas-workflow-plans.md` format.
2. Add a row to the skill's Support file map in SKILL.md referencing the plan.
3. Add plan copying to the skill's `init` command: copy `references/plans/*.plan.md` to `{agent_root}/commons/data/ocas-mentor/plans/`, skipping files already present.

See `spec-ocas-workflow-plans.md` for the plan file format and parameter specification.

---

## Validation Standard

A skill is not ready until it passes all three checks.

### Routing Check
Test realistic requests that should trigger the skill and realistic requests that should not. The description must plausibly separate those cases.

### Structural Check
Verify:
- Required files exist
- Filenames are consistent
- Support files exist only when justified
- SKILL.md points to any support file it depends on
- Major duplication has been removed
- Storage paths use `{agent_root}/commons/` root
- Journal path is specified
- Background tasks section present if skill has cron or heartbeat requirements; absent if purely reactive

### Usefulness Check
Verify:
- The skill has one sharp promise
- First useful action is obvious
- Precision is concentrated where failure is costly
- The package is concise enough to maintain

---

## Preferred Design Sequence

1. Define the candidate capability
2. Decide whether it deserves to be a skill
3. Classify the skill type
4. Define the sharp promise and responsibility boundary
5. Identify inter-skill interfaces needed (check `spec-ocas-interfaces.md`)
6. Determine if the skill needs background tasks — if so, choose cron vs. heartbeat and define job names and schedules
7. Choose the smallest viable package
8. Decide what belongs in SKILL.md versus support files
9. Define routing tests and structural checks
10. Write the self-contained build spec for the coder LLM

---

## Metadata Requirements

Every skill includes consistent author metadata:

```yaml
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "X.Y.Z"
  hermes:
    tags: [tag1, tag2]
    category: <category>
```

The `author` field lives under `metadata:` in the YAML frontmatter (not at the top level). When editing authors, always search for both `metadata:` → `author:` and top-level `author:` — some older skills may have it in the wrong location.

**Author normalization:** All skills authored by <agent-name> should use the canonical form `<agent-name> (<agent-handle>)`. When normalizing, be careful with skills that already have the full form — a naive find/replace of `<agent-name>` will double the suffix (e.g., `<agent-name> (<agent-handle>) (<agent-handle>)`). Always check for the full form first.

**Hermes-specific metadata (from [Nous Research docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)):**
- `metadata.hermes.tags` — array of tag strings for `skills_list` grouping
- `metadata.hermes.category` — controls `skills_list` category grouping. Use existing categories; don't invent ad-hoc values
- `metadata.hermes.config` — if the skill uses env vars, declare them here with `key`, `description`, `default`. This enables `hermes config migrate` and `hermes config show`
- `metadata.hermes.fallback_for_toolsets` / `requires_toolsets` — conditional activation
- `metadata.hermes.fallback_for_tools` / `requires_tools` — same, for individual tools

**Anti-patterns:**
- `category:` at top level (ignored — must be `metadata.hermes.category`)
- `tags:` only at top level without `metadata.hermes.tags` (misses Hermes grouping)
- Env vars only in body table, not in `metadata.hermes.config`

See `references/frontmatter-editing-pitfalls.md` for YAML editing safety rules.

Descriptions are optimized for discovery, not brand voice.