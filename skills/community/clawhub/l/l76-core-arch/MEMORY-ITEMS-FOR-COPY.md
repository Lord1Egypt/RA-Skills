# Memory Items for Copy/Paste to MEMORY.md

Copy these items to your `MEMORY.md` or `memory/YYYY-MM-DD.md` after working with skills.

---

## 🏗️ Skills Knowledge

### Skill Structure Template
**Category:** Skills / Architecture  
**Tags:** #skills #template #architecture  
**Content:** A production-ready AgentSkills structure includes: `SKILL.md` (manifest + instructions), `index.js` (optional main logic), `references/` (examples, templates), and `scripts/` (validation, helpers). Frontmatter requires `name`, `description`, and `metadata` with author/version. Use `references/examples.md` for detailed usage patterns.

### SKILL.md Frontmatter Standards
**Category:** Skills / Metadata  
**Tags:** #skills #frontmatter #standards  
**Content:** SKILL.md frontmatter must include: `name` (kebab-case, unique), `description` (clear trigger conditions with "When to use" format), `metadata.author`, `metadata.version`. Optional: `metadata.emoji` for visual ID, `metadata.openclaw.requires.bins` for binary dependencies, `metadata.openclaw.install` for auto-install instructions. Version should be semver string.

### Tool Integration Patterns
**Category:** Skills / Tools  
**Tags:** #tools #patterns #integration  
**Content:** Five core tool integration patterns: (1) Sequential - chain tools linearly Read→Process→Write, (2) Conditional - check preconditions before acting, (3) Error Recovery - catch errors, log, attempt fallback, report, (4) Batch Processing - use Promise.all or loops for multiple items, (5) State Management - persist state to JSON files for cross-run continuity. Choose pattern based on workflow complexity.

### Error Handling Strategy
**Category:** Skills / Error Handling  
**Tags:** #errors #recovery #strategy  
**Content:** Categorize errors as: Recoverable (retry with backoff, fallback), User Action Required (prompt for input/permission), or Fatal (report clearly, suggest workaround). Return structured responses: `{status: 'error'|'partial'|'success', error: 'message', recovery: 'next step', details: {...}}`. Log errors to state file for debugging. Never expose sensitive data in error messages.

### Skill Testing Checklist
**Category:** Skills / Testing  
**Tags:** #testing #quality #checklist  
**Content:** Before publishing, verify: (1) Skill triggers correctly on described conditions, (2) All tool calls succeed in happy path, (3) Error paths are tested and handled, (4) Output is clear and actionable, (5) No sensitive data leaked, (6) Skill is idempotent (safe to re-run), (7) Documentation complete with examples. Run `scripts/validate.sh` for automated checks.

### ClawHub Publishing Flow
**Category:** Skills / Publishing  
**Tags:** #clawhub #publishing #workflow  
**Content:** Publish workflow: (1) Ensure SKILL.md frontmatter complete with name/description/version, (2) Login: `clawhub login`, (3) Publish: `clawhub publish ./skill-name --slug skill-name --name "Display Name" --version 1.0.0 --changelog "Description"`, (4) Verify: `clawhub list` or `clawhub search`. Default registry is clawhub.com. Override with `--registry` or CLAWHUB_REGISTRY env var.

### State Management for Skills
**Category:** Skills / State  
**Tags:** #state #persistence #memory  
**Content:** Skills needing cross-run state should use JSON files in skill directory or workspace. Track: `lastRun` (ISO timestamp), `runCount` (number), `errors` (array of last 10), `config` (user preferences). Use StateManager class pattern: load on init, save after updates, logError for failures. For workspace state, use `workspace/.skill-state.json` to avoid cluttering skill directory.

### Skill Documentation Standards
**Category:** Skills / Documentation  
**Tags:** #docs #standards #best-practices  
**Content:** SKILL.md body structure: (1) Brief intro (1-2 sentences), (2) "When to Use" with ✅/❌ lists, (3) Workflow steps numbered with bash code blocks, (4) Error Handling section, (5) Examples section with concrete commands, (6) References to related docs. Use markdown headers consistently. Include at least 3 concrete examples. Avoid placeholder text like `{your-value}`.

---

**Source:** l76-core-arch skill v1.0.0  
**Date:** 2026-03-22  
**Total Items:** 8
