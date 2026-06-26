# L76 Core Architecture - Memory Items

Capture these items to MEMORY.md or daily notes after completing skill creation.

## Core Memory Items (1-8)

### 1. Skill Structure Template

**Category:** Skills / Architecture  
**Tags:** #skills #template #architecture  
**Content:**
A production-ready AgentSkills structure includes: `SKILL.md` (manifest + instructions), `index.js` (optional main logic), `references/` (examples, templates), and `scripts/` (validation, helpers). Frontmatter requires `name`, `description`, and `metadata` with author/version. Use `references/examples.md` for detailed usage patterns.

### 2. SKILL.md Frontmatter Standards

**Category:** Skills / Metadata  
**Tags:** #skills #frontmatter #standards  
**Content:**
SKILL.md frontmatter must include: `name` (kebab-case, unique), `description` (clear trigger conditions with "When to use" format), `metadata.author`, `metadata.version`. Optional: `metadata.emoji` for visual ID, `metadata.openclaw.requires.bins` for binary dependencies, `metadata.openclaw.install` for auto-install instructions. Version should be semver string.

### 3. Tool Integration Patterns

**Category:** Skills / Tools  
**Tags:** #tools #patterns #integration  
**Content:**
Five core tool integration patterns: (1) Sequential - chain tools linearly Read→Process→Write, (2) Conditional - check preconditions before acting, (3) Error Recovery - catch errors, log, attempt fallback, report, (4) Batch Processing - use Promise.all or loops for multiple items, (5) State Management - persist state to JSON files for cross-run continuity. Choose pattern based on workflow complexity.

### 4. Error Handling Strategy

**Category:** Skills / Error Handling  
**Tags:** #errors #recovery #strategy  
**Content:**
Categorize errors as: Recoverable (retry with backoff, fallback), User Action Required (prompt for input/permission), or Fatal (report clearly, suggest workaround). Return structured responses: `{status: 'error'|'partial'|'success', error: 'message', recovery: 'next step', details: {...}}`. Log errors to state file for debugging. Never expose sensitive data in error messages.

### 5. Skill Testing Checklist

**Category:** Skills / Testing  
**Tags:** #testing #quality #checklist  
**Content:**
Before publishing, verify: (1) Skill triggers correctly on described conditions, (2) All tool calls succeed in happy path, (3) Error paths are tested and handled, (4) Output is clear and actionable, (5) No sensitive data leaked, (6) Skill is idempotent (safe to re-run), (7) Documentation complete with examples. Run `scripts/validate.sh` for automated checks.

### 6. ClawHub Publishing Flow

**Category:** Skills / Publishing  
**Tags:** #clawhub #publishing #workflow  
**Content:**
Publish workflow: (1) Ensure SKILL.md frontmatter complete with name/description/version, (2) Login: `clawhub login`, (3) Publish: `clawhub publish ./skill-name --slug skill-name --name "Display Name" --version 1.0.0 --changelog "Description"`, (4) Verify: `clawhub list` or `clawhub search`. Default registry is clawhub.com. Override with `--registry` or CLAWHUB_REGISTRY env var.

### 7. State Management for Skills

**Category:** Skills / State  
**Tags:** #state #persistence #memory  
**Content:**
Skills needing cross-run state should use JSON files in skill directory or workspace. Track: `lastRun` (ISO timestamp), `runCount` (number), `errors` (array of last 10), `config` (user preferences). Use StateManager class pattern: load on init, save after updates, logError for failures. For workspace state, use `workspace/.skill-state.json` to avoid cluttering skill directory.

### 8. Skill Documentation Standards

**Category:** Skills / Documentation  
**Tags:** #docs #standards #best-practices  
**Content:**
SKILL.md body structure: (1) Brief intro (1-2 sentences), (2) "When to Use" with ✅/❌ lists, (3) Workflow steps numbered with bash code blocks, (4) Error Handling section, (5) Examples section with concrete commands, (6) References to related docs. Use markdown headers consistently. Include at least 3 concrete examples. Avoid placeholder text like `{your-value}`.

---

## Advanced Memory Items (9-16)

### 9. Troubleshooting Diagnostic Flow

**Category:** Skills / Troubleshooting  
**Tags:** #troubleshooting #diagnosis #debugging  
**Content:**
Standard diagnostic flow for skill issues: (1) Check SKILL.md frontmatter validity, (2) Validate file structure with scripts/validate.ps1, (3) Test in isolation with node index.js --verbose, (4) Check OpenClaw logs for tool call failures, (5) Review error categorization. Common issues: vague description, missing frontmatter, tool call failures, state corruption, performance degradation.

### 10. Performance Optimization Targets

**Category:** Skills / Performance  
**Tags:** #performance #optimization #metrics  
**Content:**
Target metrics for production skills: cold start <2s (acceptable <5s), tool call latency <500ms, memory usage <50MB, success rate >99%, error recovery <5s. Optimization strategies: batch tool calls, stream large files, implement concurrency limits (5-10 parallel), cache expensive operations, set explicit timeouts on all external calls, trim state arrays to prevent unbounded growth.

### 11. Tool Call Batching Pattern

**Category:** Skills / Performance / Patterns  
**Tags:** #performance #batching #tools  
**Content:**
Reduce tool call overhead (100-300ms per call) by batching: use exec('cat file*') instead of multiple read calls, combine read+process with inline Node.js, prefer web_fetch over browser for simple page reads, use mapWithConcurrency(items, fn, limit) for controlled parallelism with limit 5-10. For 100 files, batching reduces 30s overhead to ~3s.

### 12. Extension Point Architecture

**Category:** Skills / Architecture / Extensions  
**Tags:** #extensions #architecture #patterns  
**Content:**
Five extension points in L76 architecture: (1) Custom SkillExecutor - extend class and override preflight/process/finalize methods, (2) Custom StateManager - add versioned state, backups, rollback, (3) Tool Wrappers - create readWithRetry, execWithValidation, writeAtomic helpers, (4) Plugin System - implement SkillPlugin interface with onInit/onBeforeProcess/onAfterProcess/onError hooks, (5) Custom Validation - extend validate.ps1 with domain-specific rules.

### 13. Circuit Breaker Pattern for Skills

**Category:** Skills / Patterns / Reliability  
**Tags:** #reliability #patterns #circuit-breaker  
**Content:**
Implement circuit breaker for unreliable operations: three states (CLOSED=normal, OPEN=failing, HALF_OPEN=testing), threshold=5 failures triggers OPEN state, timeout=60s before attempting HALF_OPEN. Pattern prevents cascading failures and gives failing services time to recover. Use for API calls, network operations, external dependencies.

### 14. Multi-Stage Pipeline Pattern

**Category:** Skills / Patterns / Architecture  
**Tags:** #patterns #pipeline #architecture  
**Content:**
Multi-stage pipeline pattern: define stages array with name and function, iterate through stages with try-catch, update state after each stage for progress tracking, implement stage-specific recovery strategies, support partial completion with stageResults array. Use for ETL workflows, data processing, build pipelines. Each stage should be idempotent and independently testable.

### 15. Rate Limiting for API Integration

**Category:** Skills / API / Patterns  
**Tags:** #api #rate-limiting #integration  
**Content:**
Implement rate limiting for API calls: RateLimiter class with token bucket algorithm, track request timestamps, wait when limit reached, combine with exponential backoff retry (baseDelay=1s, maxDelay=30s, maxRetries=3). Retry on 429/503/timeout/ECONNRESET errors. Cache successful responses with TTL (default 1 hour) to reduce API calls.

### 16. Progress Tracking for Long Operations

**Category:** Skills / UX / State  
**Tags:** #progress #ux #state  
**Content:**
Track progress for long-running operations: update state after each unit of work with {current, total, percent, batch, totalBatches}, include timestamps for lastUpdate, report errors count separately, persist progress for resume capability. For batch processing, use Promise.allSettled to handle partial failures without stopping entire batch. Display progress as "Batch X/Y (Z%)" for user visibility.

---

## Usage

Copy relevant items to your `MEMORY.md` or `memory/YYYY-MM-DD.md` after completing skill work. Tag appropriately for future retrieval.

**Example:**
```markdown
### Skills Knowledge

{{Insert items 1, 2, 3, 6 from Core section}}
{{Insert items 10, 11, 13 from Advanced section}}
```

**Quick Reference by Category:**

- **Getting Started:** Items 1, 2, 5, 8
- **Tool Integration:** Items 3, 4, 7, 11
- **Performance:** Items 10, 11, 13, 15
- **Advanced Patterns:** Items 12, 13, 14, 15, 16
- **Troubleshooting:** Items 4, 9, 13
