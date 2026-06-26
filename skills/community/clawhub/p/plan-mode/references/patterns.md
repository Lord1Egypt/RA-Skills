# Plan Mode Patterns Across AI Tools

Reference material on planning implementations. Load only when comparing approaches.

## Claude Code (Anthropic)

- **Activation:** `Shift+Tab` cycle or `/plan` prefix or `--permission-mode plan`
- **Behavior:** Read-only. Reads files, runs shell commands to explore, asks questions, writes plan. No source edits
- **Approval flow:** Approve + auto mode, approve + accept edits, approve + manual review, or keep planning. Can clear planning context
- **Key design:** Permission mode (structural tool restriction), not just a prompt

## Aider

- **Modes:** `/ask` (no changes), `/code` (execute), `/architect` (two-model)
- **Architect mode:** Reasoning model proposes → Editor model formats edits. Two LLM calls
  - Architect/Editor pairs significantly outperform solo models on editing benchmarks
  - Even same model as both architect and editor improves over solo baseline
- **Key insight:** Separating reasoning from editing lets each model focus on its strength

## OpenAI Codex CLI

- **Modes:** `suggest` (show diffs, per-change approval) vs `auto-apply`
- **AGENTS.md:** Repo-level instructions guide agent behavior
- **Key insight:** Granular per-change approval at diff level

## Cursor

- **Modes:** Agent (full autonomy) vs Ask (read-only)
- **Key insight:** Binary simplicity — no intermediate modes

## Windsurf (Cascade)

- **Modes:** Code (modify) vs Chat (questions, can propose insertable code)
- **Background planning agent:** Runs alongside execution, continuously refines long-term plan
- **Todo lists:** Visible in conversation, user-modifiable, auto-updating
- **Checkpoints:** Named project snapshots, revertible
- **Key insight:** Planning as background process, not mode switch. Living document

## Roo Code

- **5 modes:** Code, Ask, Architect (read + markdown-only edit), Debug, Orchestrator
- **Orchestrator:** No tools — delegates to other modes via `new_task`. Strategic coordinator
- **Per-mode model binding:** Each mode remembers its model
- **Custom modes:** Define tool access + persona + file permissions
- **Key insight:** Mode = tool restrictions + persona + model. Orchestrator = plan → delegate

## ExecPlan (tiann/execplan-skill)

- **Philosophy:** Plan as living document. Self-contained — reader needs zero prior context
- **Required sections:** Progress (checkboxes), Surprises & Discoveries, Decision Log, Outcomes & Retrospective
- **Plan to file:** Saved to `execplan/` directory, survives context resets
- **Milestones:** Each independently verifiable with observable outcomes
- **Key insight:** Plan is not a conversation artifact — it's a persistent file that tracks state across sessions. "Resolve ambiguities autonomously" during execution but document all decisions

## claw-superpowers (cutd)

- **7-step workflow:** Brainstorm → Plan → Execute → Test → Debug → Review → Finish
- **Hard gates:** "Do NOT write code until design approved" — non-negotiable
- **Plan format:** Saved to `docs/plans/YYYY-MM-DD-*.md`, includes exact file paths, complete code, exact commands
- **Subagent-driven execution:** Fresh subagent per task + two-stage review (spec then quality)
- **Execution handoff:** Plan offers two paths: subagent-driven (this session) or parallel session
- **Key insight:** Plans contain complete code (not "add validation"), assume implementer has zero context. Mandatory brainstorm before plan. Review after every task

## Universal Pattern

All tools converge on: Understand → Propose → Gate → Execute → Verify

**Gate placement differentiates:**
- **Plan-level:** Claude Code, Aider ask, Roo Architect, claw-superpowers
- **Change-level:** Codex suggest (per-diff)
- **Background:** Windsurf (concurrent plan + execute)
- **Delegation:** Roo Orchestrator, claw-superpowers subagents
- **Living document:** ExecPlan (file-persisted, session-independent)

**For conversational agents (OpenClaw):** Plan-level gating is most natural. Living-document pattern valuable for complex multi-session work. Subagent delegation useful for parallel independent tasks.

## Unique to this skill: Toolbox Audit

None of the tools above include a "what do I already have?" step in their planning phase. This skill adds:
- Scan installed skills before planning approach
- Search skill registries (ClawHub, GitHub) for relevant existing skills
- Surface "already installed" vs "available to install" in the plan

This prevents the common anti-pattern of agents reinventing capabilities that already exist in their skill library. Example: an agent asked to "make a PDF report" that writes raw Python instead of loading the installed `pdf-generator` skill.
