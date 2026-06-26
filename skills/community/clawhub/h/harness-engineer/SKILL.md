---
name: harness-engineer
description: >
  A persistent autonomous engineering harness runtime that transforms any repository into a
  self-improving software system. Use this skill whenever the user wants to: build or run an
  autonomous coding agent, set up a self-healing engineering loop, orchestrate multi-agent
  software development, implement harness engineering principles, create a doc-driven
  development workflow, or run long-horizon autonomous software tasks. Trigger on phrases like
  "autonomous agent", "self-healing codebase", "harness engineering", "multi-agent pipeline",
  "continuous improvement loop", "OpenClaw skill", or any request for an agentic engineering
  system that runs without constant human input. Primarily designed for Claude Code and
  OpenClaw environments.

metadata:
  platform_enforcement: required
  platform_note: >
    This skill is instruction-only. Safe operation depends on the host platform
    enforcing: MCP tool router (blocked sensitive reads, protected writes, output
    redaction), sandboxed test execution, scoped git credentials (no direct push to
    main), and human approval gates. If these cannot be confirmed, run single-pass
    with manual oversight only. Full checklist in PLATFORM_REQUIREMENTS.md.
  required_platform_capabilities:
    - mcp_tool_router
    - sandboxed_test_execution
    - git_credential_scoping
    - human_approval_gates
  safe_defaults:
    - loop_mode: single-pass
    - verify_platform_requirements_before_first_use: true
---

# HARNESS ENGINEER

A production-grade skill for Claude Code and OpenClaw that transforms a repository into a
self-improving software system using six core harness engineering principles.

---

## SIX CORE PRINCIPLES

### P1: CONTEXT ENGINEERING
Treat context as a finite, precious resource. Curate aggressively.
See: runtime/context-engineering.md, runtime/compaction.md

### P2: TOOL USAGE
Each sub-agent receives only the tools it needs -- no more.
See: tools/TOOL_REGISTRY.md, references/mcp-tools.md

### P3: VERIFICATION MECHANISM
Every output is verified by someone other than who produced it.
See: agents/reviewer.md, references/testing-standards.md

### P4: STATUS MANAGEMENT
State lives outside the context window, in the repo.
See: runtime/status-management.md, templates/handoff.md

### P5: OBSERVABILITY AND FEEDBACK CLOSED-LOOP
Track what happens. Feed failures back into the harness, not the code.
See: runtime/observability.md, runtime/memory-system.md

### P6: HUMAN SUPERVISION
Humans approve high-impact events. The harness surfaces them explicitly.
See: runtime/autonomy-rules.md, runtime/prioritization.md

---

## NON-NEGOTIABLE RULES

1. CLAUDE.md / AGENTS.md IS GROUND TRUTH -- read it first, every session.
2. CODEBASE OVER DOCS -- when they conflict, trust the code.
3. 40% CONTEXT RULE -- compact or sub-agent before crossing 40% of context window.
4. NO IMPLEMENTATION WITHOUT a research output, a plan, and validation criteria.
5. GENERATION AND REVIEW ARE ALWAYS SEPARATE -- never the same agent.
6. FAILURE = HARNESS GAP -- fix the harness, not just the symptom.
7. OPTIMIZATION PRIORITY: Security => Correctness => Reliability => Performance =>
   Memory => Maintainability => Cost
8. MINIMAL SCOPE PER SUBAGENT — Estimate codebase size first (use platform file-count or line-count capability — never raw shell). If >5K lines, split into multiple subagents by module/feature/layer. Pin exact files to read (no wandering). One research doc + one code area per subagent max. If a subagent gets killed or times out, the scope was too large — split further.
   **Adaptive timeouts:** Default timeouts are guidelines, not hard kills. Check process logs before killing — if the agent is actively producing output, extend the timeout instead of killing. Only kill-and-split if the agent is silent/stuck for >10min or producing garbage. Scale timeouts by effort: S-effort=15min, M-effort=20min, L-effort=30-40min.
9. SUBAGENT PERMISSION MODE — Subagents are spawned by the platform using its native agent mechanism. The permission mode is set by the platform, NOT by this skill. The skill MUST NOT mandate any specific spawn command or permission mode — that decision belongs to the platform's enforcement layer (see PLATFORM_REQUIREMENTS.md Section 8). If the platform's default permission mode is insufficient, the platform operator configures it — the skill never overrides it.
10. ACTIVE MONITORING — Every time you launch a new batch of subagents, track session IDs, expected output files, and remaining queue. If the platform provides a cron/scheduler, use it to detect dead agents. If no scheduler is available, check agent status before each dispatch step. Dead agents stall the pipeline — detect them early.
11. MAX PARALLEL = 5 — Up to 5 Claude Code agents running simultaneously. If rate/API limit errors encountered, drop to 4, then 3, etc until no errors. Resume increasing after 5 clean minutes.
12. TOKEN EXHAUSTION RECOVERY: If ALL active agents hit rate/API limits (429/500), tokens are exhausted. Wait for token refresh before retrying. If the platform provides a scheduler, set a recovery job to resume after refresh. If no scheduler is available, the human operator must manually restart the cycle.
13. 10-MIN STUCK KILL — If any agent produces no output for >10 minutes, log the issue, kill it, and split the task into smaller subtasks before respawning. **MUST ALWAYS set a cron job when a subagent is given a command that will run for a while, to periodically check on its progress.**
14. TRACKING EVERYWHERE — Every phase, cycle, and step writes to tracking logs. DISPATCH-TRACK, error log, compact summaries, progress logs. Recovery must be able to pick up from any interruption point.

---

## SAFE START GUIDE

Before anything else: read PLATFORM_REQUIREMENTS.md and verify every item.
The harness depends on platform enforcement that cannot be checked from these files alone.

Step 1 -- Verify platform requirements (PLATFORM_REQUIREMENTS.md)
Run through the five platform capability checks before any other step.

Step 2 -- Sandbox first
Run on a throwaway branch. Observe one single-pass cycle before enabling continuous mode.

Step 2 -- Review CONFIG.yaml before every run
| loop_mode            | single-pass | Change after sandbox validation        |
| max_parallel_agents  | 3           | Increase after confirming behavior     |
| block_destructive... | true        | Never change                           |

PRs always require human approval. There is no auto-merge.

Step 3 -- Protect main branch
Require human reviewers on main/trunk in your git host.

Step 4 -- Graduation path: single-pass => maintenance => continuous

---

## HOW TO USE THIS SKILL

When activated in Claude Code or OpenClaw, read in this order:

1. CLAUDE.md or AGENTS.md if present (base context)
2. CONFIG.yaml (runtime settings)
3. runtime/loop.md (execution model)
4. runtime/context-engineering.md (context budget rules)
5. runtime/status-management.md (restore checkpoint if resuming)
6. MEMORY.md (prior failure context)
7. agents/dispatcher.md (task decomposition model, worktree agent)
8. Begin the loop

---

## REFERENCE FILES

| File                              | When to read                              |
|-----------------------------------|-------------------------------------------|
| CLAUDE.md / AGENTS.md             | First, every session -- base knowledge    |
| CONFIG.yaml                       | At startup                                |
| MEMORY.md                         | At startup and after every failure        |
| runtime/loop.md                   | Each loop cycle                           |
| runtime/context-engineering.md    | Continuously -- governs context budget    |
| runtime/compaction.md             | When compacting context within a phase    |
| runtime/status-management.md      | At startup (resume) and after each task   |
| runtime/observability.md          | After VERIFY phase                        |
| runtime/memory-system.md          | When writing or querying memory           |
| runtime/self-improvement.md       | After any failure                         |
| runtime/prioritization.md         | When selecting the next task              |
| runtime/autonomy-rules.md         | When blocked or at human gate             |
| agents/dispatcher.md              | Before decomposing any task (worktree agent) |
| agents/researcher.md              | Research phase (Q-Agent + R-Agent model)  |
| agents/planner.md                 | Plan phase (3-phase: design, outline, master plan) |
| agents/implementer.md             | Implement phase (worktree-driven execution) |
| agents/reviewer.md                | Review cycle                              |
| agents/debugger.md                | On any failure                            |
| agents/optimizer.md               | Optimization mode                         |
| agents/garbage-collector.md       | GC interval                               |
| tools/TOOL_REGISTRY.md            | Before any tool call                      |
| tools/tool-router.md              | Routing and redaction rules               |
| tools/execution-protocol.md       | Full tool call lifecycle                  |
| references/harness-rules.md       | Core constraints                          |
| references/testing-standards.md   | Before writing or running tests           |
| references/security-performance.md| Before any implementation                 |
| references/simplification-checklist.md | During review and refactoring        |
| references/git-workflow.md        | Before any commit or PR                   |
| references/mcp-tools.md           | MCP tool definitions and per-agent sets   |
| references/sensitive-paths.md     | Forbidden read paths -- enforced in-skill |
| references/constraints.md         | Active prevention rules                   |
| templates/                        | Plans, ADRs, handoffs, status docs        |
