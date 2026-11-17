# Critique Rubric — 10 Dimensions

Evaluate each dimension on a 1-5 scale. Score honestly. A 3 is acceptable, not a failure.

Scoring guidance synthesized from: review-skill rubric v1.0, skill-architect
Quick Wins, agentskill.sh best practices, and OCAS authoring rules v3.1.0.

---

## D1: Frontmatter (Spec Compliance)

Does the YAML frontmatter follow the Agent Skills specification and Hermes conventions?

| Score | Criteria |
|-------|----------|
| **5** | `name` and `description` present and valid. Optional fields (`license`, `metadata`, `includes`, `triggers`) used where appropriate. Name matches directory, lowercase-hyphens only. `license` is a top-level frontmatter field. `metadata.hermes` present with `tags` and `category`. Env vars declared in `metadata.hermes.config` if the skill uses any. |
| **4** | Required fields valid. One minor issue (missing `category`, env vars only in body table). |
| **3** | Required fields present but one has issues (description too short, `metadata.hermes` missing). |
| **2** | Missing one required field, or name/description violate constraints. |
| **1** | No frontmatter, or both required fields missing/invalid. |

Core checks:
- `name`: 1-64 chars, lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens
- `description`: 1-1024 chars, non-empty
- No XML tags in name or description
- Name must not contain "anthropic" or "claude"
- `includes:` should list `references/**` if that directory exists
- `license:` must be a top-level frontmatter field
- `triggers:` present for agent-authored skills (enables slash command discovery)

Hermes-specific checks (from [Skills System docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)):
- `metadata.hermes.tags`: array of tag strings for `skills_list` grouping
- `metadata.hermes.category`: string — controls `skills_list` category grouping (e.g. `infrastructure`, `devops`, `productivity`). Must match an existing category; don't invent ad-hoc values
- `metadata.hermes.config`: if the skill uses env vars, declare them here with `key`, `description`, `default`. This enables `hermes config migrate` and `hermes config show`. Env vars only documented in a body table (not in `config`) is a D1-4 deduction
- `metadata.hermes.fallback_for_toolsets` / `requires_toolsets`: conditional activation — only set when the skill is a fallback or requires specific toolsets
- `metadata.hermes.fallback_for_tools` / `requires_tools`: same, for individual tools
- `platforms:` — optional OS restriction (`[macos]`, `[linux]`, `[windows]`, or combo). If omitted, skill loads on all platforms
- `required_environment_variables:` — formal declaration for secure setup prompts (env var name, prompt text, help URL, required_for level)
- Directory structure follows convention: `references/`, `templates/`, `scripts/`, `assets/` — no ad-hoc subdirectories
- `source:` field present for skills synced from external repos

Common rejection causes (from skill-architect):
- `tools:` instead of `allowed-tools:` — silently ignored
- YAML list in `allowed-tools:` — parse error; use comma-separated
- Brackets in `allowed-tools:` — parse error; no `[ ]`
- Invalid keys (`outputs`, `integrates_with`) — silently ignored
- Name with spaces/uppercase — may fail matching
- Name doesn't match directory — activation mismatch
- `category:` at top level instead of `metadata.hermes.category` — silently ignored by Hermes
- `tags:` only at top level without `metadata.hermes.tags` — works but misses Hermes grouping

---

## D2: Description Quality (Triggering)

Will agents select this skill for the right tasks?

| Score | Criteria |
|-------|----------|
| **5** | Follows `[What] [When] [Keywords]. NOT for [Exclusions]` formula. Third-person imperative voice. Under 1024 chars. Would trigger reliably on relevant prompts and not trigger on adjacent-but-different tasks. |
| **4** | Good coverage of what and when. Minor gap in trigger keywords or slightly broad scope. |
| **3** | Describes what but not when (or vice versa). Or uses first/second person. Or too generic to distinguish from similar skills. |
| **2** | Vague ("helps with files"), too short to be useful, or would false-trigger on unrelated tasks. |
| **1** | Empty, single word, or actively misleading. |

Key rules:
- Third person imperative: "Extracts text from PDFs" not "I can help you extract text"
- Include both what it does AND when to use it
- Include trigger keywords the user might say
- Include a NOT clause to prevent false activation
- Be specific enough to distinguish from similar skills
- Stay under 1024 characters

---

## D3: Conciseness (Token Efficiency)

Does every token justify its context window cost?

| Score | Criteria |
|-------|----------|
| **5** | No unnecessary explanations. Only includes what the agent wouldn't know without the skill. Every paragraph passes the "does the agent really need this?" test. |
| **4** | Mostly concise. One or two sections could be trimmed without losing value. |
| **3** | Some bloat. Explains concepts the agent already knows. |
| **2** | Significant bloat. Multiple paragraphs of unnecessary background. |
| **1** | Mostly filler. More explanation than instruction. |

Red flags:
- Defining common terms (PDF, API, CSV, JSON)
- Explaining how well-known libraries work
- Repeating the same instruction in different words
- Long introductory paragraphs before useful content
- "In this section, we will..." preamble text
- Inline credential paths or API key values (security scanner flag)

Code ratio target: SKILL.md body under 20% code (fenced-block lines / total lines).
Anything over 30% is a definite problem.

---

## D4: Structure (Progressive Disclosure)

Is the skill organized for efficient context loading?

| Score | Criteria |
|-------|----------|
| **5** | SKILL.md under 500 lines / 5000 tokens. Reference material in separate files. File references one level deep. Clear support file map with "When to read" column. Descriptive file names. |
| **4** | Good structure. One issue (SKILL.md slightly long, one deeply nested reference). |
| **3** | SKILL.md is 500-800 lines, or reference material mixed into SKILL.md. |
| **2** | SKILL.md over 800 lines, or deeply nested references (A links to B links to C). |
| **1** | Everything in one massive SKILL.md with no structure. |

Three-layer architecture (from skill-architect):
- Layer 1: Metadata (~100 tokens) — always in context at catalog scan
- Layer 2: SKILL.md (<5k tokens) — loaded on skill activation
- Layer 3: References (unloaded) — on-demand, per-file, only when relevant

Rules:
- SKILL.md body under 500 lines, ideally under 5000 tokens
- Split large content into `references/`, `scripts/`, `assets/`
- File references one level deep from SKILL.md
- Reference files over 100 lines should have a table of contents
- Use descriptive file names: `form_validation_rules.md` not `doc2.md`

---

## D5: Instruction Clarity

Can the agent follow the instructions without ambiguity?

| Score | Criteria |
|-------|----------|
| **5** | Steps are clear, sequential, and unambiguous. Input/output examples provided. Edge cases addressed. Consistent terminology throughout. Checklists for multi-step workflows. |
| **4** | Clear instructions with minor ambiguity in one area. |
| **3** | Generally understandable but requires interpretation in places. Inconsistent terminology or missing examples. |
| **2** | Ambiguous instructions that could be followed multiple ways. Key steps missing. |
| **1** | Instructions are contradictory, incomplete, or incomprehensible. |

Checks:
- One term per concept, used consistently
- Concrete examples, not abstract descriptions
- No time-sensitive information (dates, "before August 2025")
- Templates for output format where format matters
- Checklists for multi-step workflows
- Write in imperative form: "To accomplish X, do Y" not "You should do X"

---

## D6: Freedom Calibration

Is each part of the skill appropriately prescriptive for its fragility?

| Score | Criteria |
|-------|----------|
| **5** | Fragile operations have exact commands. Flexible tasks give direction without over-constraining. Defaults provided, alternatives mentioned briefly. |
| **4** | Generally well-calibrated. One area slightly over/under-constrained. |
| **3** | Presents multiple equal options where a default would be better. |
| **2** | Fragile operations lack guardrails, or flexible tasks are rigidly scripted. |
| **1** | No awareness of task fragility. Everything treated the same. |

Key rules:
- Pick defaults, don't present menus of equal options
- Fragile/destructive operations: exact commands, no flexibility
- Analysis/creative tasks: direction and criteria, not rigid scripts
- Explain "why" for rigid rules so the agent can adapt in edge cases

---

## D7: Error Handling

Does the skill handle failure gracefully?

| Score | Criteria |
|-------|----------|
| **5** | Scripts handle errors explicitly with helpful messages. Validation loops (do work, validate, fix, repeat). Error table or section covering common failures. |
| **4** | Good error handling in most paths. One gap in error coverage. |
| **3** | Some error handling but gaps. Scripts may fail silently. |
| **2** | Minimal error handling. Scripts punt errors without guidance. |
| **1** | No error handling. Scripts crash on edge cases. |

For skills with scripts:
- Scripts should handle errors explicitly, not punt to the agent
- Error messages should say what went wrong, what was expected, and what to try
- Include a validation step before destructive operations
- Constants should be documented (no magic numbers)

For skills without scripts:
- Include an error handling section or table
- Address common failure modes
- Provide fallback approaches

---

## D8: Progressive Disclosure

Does the skill load context efficiently?

| Score | Criteria |
|-------|----------|
| **5** | SKILL.md is a concise overview. Detailed material in separate files loaded only when needed. Clear signals telling the agent WHEN to load each file. Support file map uses "When to read" column with conditional language. |
| **4** | Good separation. One file could benefit from conditional loading. |
| **3** | Some material in SKILL.md that should be in references. Or support file map exists but uses static topic descriptions instead of conditional triggers. |
| **2** | Most content in SKILL.md. References exist but are poorly signaled. |
| **1** | Everything in SKILL.md. No separate files despite the skill being complex. |

**This is the most common failure across skill libraries.**

Rules:
- SKILL.md = overview + navigation
- `references/` = detailed material loaded on demand
- Tell the agent WHEN to load each file, not just that it exists
- "Read references/api-errors.md if the API returns non-200" > "See references/ for details"
- **Support file maps must use a "When to read" column** with conditional language ("Before X", "During Y", "When Z"), not just static topic descriptions

Conditional language patterns (from audit-support-file-maps):
- "Before [action]" — e.g., "Before running genie.py"
- "During [phase]" — e.g., "During Phase 2 discovery"
- "When [condition]" — e.g., "When bot detection blocks access"
- "If [situation]" — e.g., "If VPN Gate is blocked and VPS fallback is needed"

---

## D9: Scripts Quality

Are bundled scripts well-designed for agentic use?

Score N/A if the skill has no scripts.

| Score | Criteria |
|-------|----------|
| **5** | Scripts are self-contained with inline dependencies. No interactive prompts. Clear --help output. Structured output (JSON/CSV). Meaningful exit codes. Idempotent where possible. Error messages include what went wrong and what to try. |
| **4** | Good scripts. One minor issue. |
| **3** | Scripts work but have design issues (interactive prompts, unstructured output). |
| **2** | Scripts have significant issues (crash on edge cases, undocumented setup). |
| **1** | Scripts are broken, dangerous, or require extensive agent workarounds. |

Checks:
- No interactive prompts (agents can't respond to TTY input)
- `--help` documents usage, flags, and examples
- Structured output (JSON preferred) on stdout, diagnostics on stderr
- Meaningful exit codes for different failure types
- Dependencies declared inline (PEP 723 for Python, npm: for Deno)
- Idempotent operations (create-if-not-exists, not create-and-fail-on-duplicate)
- `--dry-run` for destructive operations

---

## D10: Completeness

Does the skill cover its stated scope?

| Score | Criteria |
|-------|----------|
| **5** | All features mentioned in the description are covered. Gotchas section captures non-obvious issues. Edge cases addressed. The skill is a coherent unit. |
| **4** | Covers the stated scope with one minor gap. |
| **3** | Missing coverage for part of the described scope. |
| **2** | Significant gaps between description and content. |
| **1** | Description promises features the skill doesn't deliver. |

**This is the second most common failure across skill libraries.**

Checks:
- Every capability in the description has corresponding instructions
- **Gotchas/Pitfalls section** present for non-obvious issues (environment-specific facts, naming inconsistencies, service quirks)
- Scope is a coherent unit of work (not too broad, not too narrow)
- Procedures generalize rather than solving one specific instance
- CHANGELOG.md tracks version history (if skill is in a repo)