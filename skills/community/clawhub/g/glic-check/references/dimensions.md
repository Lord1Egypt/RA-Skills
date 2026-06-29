# GLIC / UGLIC Dimension Checklists

## Context Selection

Before starting, identify the target type:

| Type | Examples | Primary Lens |
|------|----------|-------------|
| **code** | .py, .js, .sh, .html, .ts | Programming best practices |
| **skill** | SKILL.md, skill directory | AgentSkill spec compliance |
| **config** | .json, .yaml, .env, app config files | Schema validity, security |
| **document** | .md, specs, docs | Clarity, completeness, accuracy |

Mixed targets (e.g., a skill with scripts) → apply both lenses.

**U dimension note**: U dimension applies best to skills and tools (anything with a user-facing surface). For code and config, apply U selectively using the sub-checklists below. For pure documents without a skill wrapper, Agent perspective is not applicable — skip it entirely; apply Human perspective only when the document is user-facing.

---

## U — Usability & User Experience

*UGLIC mode only. Examines the target from two perspectives:*
- **Agent perspective**: Can the LLM agent read and execute this reliably, without guessing?
- **Human perspective**: Can the human user complete the core task efficiently, especially on first use?

### skill

**Agent perspective (executability)**
- [ ] No vague directives: no `合理判断`, `适当处理`, `酌情考虑`, `按需调整`, `一般情况` or similar ambiguous wording that causes unpredictable agent behavior
- [ ] Step I/O explicit: every step's output is stated as input to the next step; agent does not need to guess connections
- [ ] All branches executable: every conditional path has concrete, objectively judgeable conditions and reachable actions
- [ ] Tool dependencies declared: required tools, APIs, and permissions documented before execution
- [ ] Error recovery path: on failure, agent has clear fallback/retry guidance, not a dead end
- [ ] Trigger precision: description avoids both false-positive triggers and missed real expressions
- [ ] No circular logic: skill does not send agent back to itself recursively or into infinite retry
- [ ] **SKILL.md length budget**: body stays within agent context limits — WARN if >500 lines, **ERR if >800 lines** (long SKILL.md silently degrades agent execution: agents may skim, miss critical instructions, or over-spend tokens before getting to the action steps)
- [ ] **Progressive read hint**: for skills with many references or long body, SKILL.md tells the agent *when* to lazy-load each reference (don't make agent load everything upfront)

**Human perspective (usability)**
- [ ] Implicit prerequisites surfaced: login, permissions, environment requirements stated upfront
- [ ] First-use success: first-time user can complete core task without trial and error; prerequisites documented
- [ ] Error messages actionable: user knows what happened, why, and what to do next
- [ ] Interaction rounds reasonable: no excessive back-and-forth or redundant confirmations
- [ ] No dead ends: every interaction step ends with a clear next action
- [ ] Output scannable: summary table, ERR-first ordering, clear hierarchy
- [ ] Terminology consistent: same concept uses same term throughout skill and output
- [ ] Reference file load timing: SKILL.md specifies *when* and *how* to load each referenced file

### code

**Agent perspective (executability)**
- [ ] Function/API intent clear from signature + docstring alone: agent can call it correctly without reading the body
- [ ] Parameter semantics documented: types, valid ranges, optional vs required, behavior when omitted

**Human perspective (usability)**
- [ ] CLI/API usage clear: all arguments, flags, exit codes, and invocation examples documented
- [ ] Error messages actionable: user knows what happened, why, and what to do next
- [ ] Progress visible: long-running operations show activity indicators, not silent waits
- [ ] Output scannable: key results visible without reading full output

### config

**Agent perspective (executability)**
- [ ] Field semantics self-explanatory or commented: agent reading the config can infer intent without external context

**Human perspective (usability)**
- [ ] Terminology consistent: same concept uses same term throughout
- [ ] Structure predictable: user knows what to expect from each section
- [ ] Prerequisites stated: required context, permissions, or dependencies documented upfront

### document

*Agent perspective: not applicable. Documents are primarily human-consumed; scenarios where an agent reads a document are covered under the skill that references it.*

**Human perspective (usability)**
- [ ] Terminology consistent: same concept uses same term throughout
- [ ] Structure predictable: user knows what to expect from each section
- [ ] Prerequisites stated: required context, permissions, or dependencies documented upfront

---

## G — Grammar（语法/格式/命名）

### code
- [ ] Syntax: file is parseable by its language runtime
- [ ] Naming: follows project conventions (check existing code first — same file, same project)
- [ ] Formatting: indentation, line endings, blank lines consistent with surrounding code
- [ ] No leftover debug artifacts: print(), console.log, debugger statements, commented-out blocks without explanation
- [ ] String quoting style consistent (project convention, not personal preference)
- [ ] Import order follows project pattern
- [ ] Docstring/comment format matches project style

### skill
- [ ] Frontmatter: `name` and `description` both present and non-empty
- [ ] Frontmatter: valid YAML, no extra fields beyond `name` + `description`
- [ ] No forbidden files: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc.
- [ ] Directory structure: SKILL.md at root, resources in correct subdirs
- [ ] File naming: lowercase, hyphens (no spaces, no underscores in skill name)
- [ ] Markdown: headings properly nested, links valid, no broken references
- [ ] Description quality: describes what + when, not vague ("Use when needed")

### config / document
- [ ] Valid format: JSON/YAML parseable, no syntax errors
- [ ] Field names match expected schema
- [ ] No broken internal links or anchors (for markdown docs)
- [ ] Consistent date/time/timestamp formats

---

## L — Logic（逻辑/流程/因果）

### code
- [ ] Control flow: all branches reachable? any dead code?
- [ ] Implicit dependencies: nonlocal, closures, global state — do they rely on side effects for correctness?
- [ ] Edge cases: empty input, null/None, zero, negative, extreme values
- [ ] Race conditions: shared mutable state in async/concurrent paths
- [ ] Retry/recovery: retry logic doesn't duplicate side effects; failures degrade gracefully
- [ ] Conditional completeness: if/elif chains cover all cases, else/default present where needed
- [ ] Loop invariants: termination guaranteed, no infinite loops on edge input
- [ ] Type consistency: variable types don't silently change (e.g., str → None → str)

### skill
- [ ] Workflow order: steps are in correct sequence (no step depends on a later step's output)
- [ ] Trigger description: specific enough to avoid false positives, broad enough to catch real uses
- [ ] Progressive disclosure: reference files linked from SKILL.md when their content is needed
- [ ] Conditional branches: if SKILL.md says "if X, do Y" → does Y actually work?
- [ ] No circular logic: skill doesn't send agent back to itself recursively

### config / document
- [ ] No contradictory settings: two fields that can't both be true
- [ ] Cross-field consistency: value in field A is compatible with value in field B
- [ ] Thresholds/limits: timeout values, retry counts, max sizes are reasonable
- [ ] Document flow: sections in logical order, no forward references without links

---

## I — Integrity（完整性/一致性/边界）

### code
- [ ] Error handling: all external calls (I/O, network, DB) have try/except or error returns
- [ ] Documentation alignment: comments, docstrings, README match actual behavior — check if recent changes broke existing docs
- [ ] Parameter coverage: all CLI args, function params, config keys documented
- [ ] Exit codes: non-zero on failure, zero on success
- [ ] Logging: important state transitions logged; sensitive data NOT logged
- [ ] Cache/stale state: caches have invalidation or expiry; stale data won't cause silent wrong behavior
- [ ] Cleanup: temporary files removed, connections closed
- [ ] Multi-target consistency: if code has multiple paths (single/group/broadcast), are all paths updated consistently?

### skill
- [ ] SKILL.md examples match actual scripts (parameter names, file paths, invocation syntax)
- [ ] All referenced files exist (scripts, references, assets) — no broken links
- [ ] Reference files are linked from SKILL.md (not orphaned)
- [ ] Parameter table covers all parameters; behavior for omitted params is clear
- [ ] No stale content: old descriptions, deprecated paths, removed features still mentioned
- [ ] **Cross-section references resolve correctly**: every "see Step X.Y" / "as in section Z" / "per X.Y.b above" must match an actual section heading in the same doc — broken section numbers are silent failures (agent will follow them and look for content that doesn't exist)
- [ ] **No build/runtime artifacts committed**: skill source dir should not contain `sign.key`, `.install-source.json`, `__skill_meta__.json`, `*.json.md`, `__pycache__/`, `.skill-data/`, build output, or test scratch files (these belong in `.gitignore` and are recreated at install/runtime)
- [ ] **Frontmatter field discipline**: only `name` + `description` should appear in frontmatter; `version` belongs in `package.json` / CHANGELOG, `metadata` / `author` / `tags` / `applicablePosition` etc. belong in README or Markdown body (extras in frontmatter break strict YAML parsers — e.g. Qoder reports "Invalid SKILL.md format", Cursor/Continue may also drop the skill)
- [ ] (Token budget for SKILL.md length is covered in **U-Agent** "SKILL.md length budget" — do not double-report here)

### config / document
- [ ] All required fields present per schema
- [ ] All referenced paths/files/IDs exist and are accessible
- [ ] No orphaned sections or unused fields that should be cleaned up
- [ ] User-facing content: no internal-only references leaked

---

## C — Containment（范围/副作用/安全）

### code
- [ ] Global state modification: does the code mutate shared objects (e.g., argparse Namespace in place)?
- [ ] File system side effects: writes to unexpected locations? overwrites existing files without warning?
- [ ] Network calls: are they intentional? do they leak data?
- [ ] Security: credential exposure (hardcoded keys, tokens in logs), path traversal, injection risks
- [ ] Backward compatibility: existing callers/importers unaffected; default behavior unchanged
- [ ] Scope match: does the change do more than what the commit message / PR description says?
- [ ] Input validation: user/external input sanitized; no trust without verification

### skill
- [ ] Token impact: is new content essential? does it justify its context window cost?
- [ ] No unnecessary files: backup copies, test scripts, temp output in skill directory
- [ ] No overlap: skill description doesn't conflict with other installed skills' trigger zones
- [ ] Description boundaries: doesn't over-claim capabilities it can't deliver
- [ ] Dependency boundaries: doesn't assume tools/env that may not exist on target agent

### config / document
- [ ] No sensitive data exposed: passwords, API keys, internal IPs, tokens
- [ ] System impact: config changes don't affect unrelated services
- [ ] Audience appropriate: internal-only content not published to public spaces
