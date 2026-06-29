# Agent Inventory

This inventory records platform facts for thin adapters. It is intentionally
conservative: unknown means the repository does not yet contain official or
observed evidence for that capability.

## Research Method

Use this priority order when updating an agent record:

1. Official platform documentation or manifest.
2. Runtime-provided tool list, help output, or observed tool behavior.
3. Local workspace configuration or plugin metadata.
4. Community notes, marked as community.
5. Unknown, with conservative fallback.

Do not convert product assumptions into hard requirements. Every agent must still
probe actual runtime capabilities.

## Agent Records

### generic

- Source status: baseline.
- Default optimization profiles: `prompt-agent`.
- Built-in tools: unknown.
- Skill/plugin mechanism: unknown.
- Likely strengths: portable prompt-only fallback.
- Required fallback: inline Markdown artifacts; no claimed file, shell, citation,
  or memory operations.
- Notes: use for new agents until a specific inventory record exists.

### codex

- Source status: observed in local agent-shell sessions; official verification
  still required before hardcoding product-specific claims.
- Default optimization profiles: `scripted-agent`, `file-agent`, `planner-agent`
  when matching tools are visible.
- Built-in tools: may expose file reads, file edits, shell commands, plans, local
  images, and sandbox/approval controls depending on session permissions.
- Skill/plugin mechanism: local skill folders with `SKILL.md`, `references/`,
  `scripts/`, and optional `agents/` metadata.
- Likely strengths: repository inspection, deterministic script execution, tests,
  and file-backed artifacts.
- Required fallback: if shell or write access is missing, use the generic
  Markdown fallback.
- Notes: treat exactly like any other file-capable agent; do not assume tools
  unless they are visible.

### claude

- Source status: unknown in this repository; verify with official Claude Code or
  Claude Desktop documentation before adding hard requirements.
- Default optimization profiles: `prompt-agent`; upgrade to `file-agent` or
  `scripted-agent` only after tools are visible.
- Built-in tools: commonly expected to vary by host; file, shell, browser, MCP,
  and project-context tools must be probed.
- Skill/plugin mechanism: unknown; MCP or project instructions may be available
  in some deployments.
- Likely strengths: long-form tutoring, codebase reasoning, and document review
  when files are exposed.
- Required fallback: use generic Markdown fallback until file and shell tools are
  confirmed.
- Notes: keep adapter prompt short; avoid hidden-reasoning requests. A local
  `.claude/settings.local.json` may allow specific Bash commands in this
  repository, but that is workspace-local evidence, not a general Claude
  capability.

### openclaw

- Source status: unknown in this repository.
- Default optimization profiles: `prompt-agent`; upgrade after file or shell
  tools are visible.
- Built-in tools: unknown; probe file, shell, search, and planning tools.
- Skill/plugin mechanism: unknown.
- Likely strengths: expected to be an agent-shell style coding assistant when
  file and shell tools exist.
- Required fallback: generic Markdown fallback.
- Notes: adapter must not assume compatibility with Codex or Claude tool names.
  If a current OpenClaw runtime exposes proactive-message or scheduler tools,
  use `reminder-agent` only after explicit user opt-in; otherwise keep daily and
  weekly knowledge digests on demand.

### hermes

- Source status: unknown in this repository.
- Default optimization profiles: `prompt-agent`; upgrade after file, shell,
  memory, search, or task tools are visible.
- Built-in tools: unknown; probe file, shell, memory, search, and task tools.
- Skill/plugin mechanism: unknown.
- Likely strengths: expected to be an agent-shell style assistant when local
  tools exist.
- Required fallback: generic Markdown fallback.
- Notes: preserve a strict "report failures, then downgrade" rule. If a current
  Hermes runtime exposes proactive-message or scheduler tools, use
  `reminder-agent` only after explicit user opt-in; otherwise keep daily and
  weekly knowledge digests on demand.

### workbuddy

- Source status: unknown in this repository.
- Default optimization profiles: `prompt-agent`; upgrade to `planner-agent` or
  `memory-agent` only after those tools are visible.
- Built-in tools: unknown; probe workspace files, command execution, task boards,
  memory, and retrieval.
- Skill/plugin mechanism: unknown.
- Likely strengths: project/workflow assistance when workspace context exists.
- Required fallback: generic Markdown fallback.
- Notes: if task-board tools exist, they are orchestration aids, not course
  state storage unless persistence is confirmed.

### qoder-work

- Source status: unknown in this repository.
- Default optimization profiles: `ide-agent` for programming-course review when
  IDE context is visible; otherwise `prompt-agent`.
- Built-in tools: unknown; probe IDE context, code index, file editing, shell,
  diagnostics, and task execution.
- Skill/plugin mechanism: unknown.
- Likely strengths: coding-course review and runnable demos when IDE tools are
  exposed.
- Required fallback: generic Markdown fallback.
- Notes: do not assume a code index can read PDFs or notes.

### trae

- Source status: unknown in this repository.
- Default optimization profiles: `ide-agent` for programming-course review when
  IDE context is visible; otherwise `prompt-agent`.
- Built-in tools: unknown; probe IDE context, file editing, shell, browser/search,
  diagnostics, and project commands.
- Skill/plugin mechanism: unknown.
- Likely strengths: IDE-assisted programming review, code demos, and project
  artifact generation when tools exist.
- Required fallback: generic Markdown fallback.
- Notes: add official Trae details here before tightening adapter behavior.

### openai

- Source status: local adapter metadata exists; runtime capability depends on the
  host using the prompt.
- Default optimization profiles: `prompt-agent`; upgrade to `retrieval-agent`,
  `scripted-agent`, or `visual-agent` only when host tools are visible.
- Built-in tools: unknown unless the host exposes files, code execution,
  retrieval, or browsing.
- Skill/plugin mechanism: prompt or custom GPT style configuration may be used.
- Likely strengths: portable runtime prompt and chat-native tutoring.
- Required fallback: generic Markdown fallback.
- Notes: do not assume the OpenAI host can read this skill folder.

### deepseek

- Source status: local adapter metadata exists; product-specific runtime tools are
  unknown in this repository.
- Default optimization profiles: `prompt-agent`.
- Built-in tools: unknown; model-only deployments may have no tools.
- Skill/plugin mechanism: prompt-level adapter.
- Likely strengths: strict grading, proof checking, and Chinese tutoring when
  paired with a capable host.
- Required fallback: generic Markdown fallback.
- Notes: avoid hidden-reasoning disclosure requests.

### ollama

- Source status: local adapter metadata exists; host tools are unknown.
- Default optimization profiles: `prompt-agent`.
- Built-in tools: usually model-only unless an agent shell wraps it; probe before
  using files or shell.
- Skill/plugin mechanism: prompt-level adapter.
- Likely strengths: local/offline tutoring and small-step outputs.
- Required fallback: generic Markdown fallback.
- Notes: keep outputs compact for smaller local models.

### ima

- Source status: local adapter and reference protocol exist.
- Default optimization profiles: `retrieval-agent`, `memory-agent`,
  `planner-agent`, and `delegating-agent` when ima-native tools are present.
- Built-in tools: documented in this repo as `ask_user`, `fetch`, `file_edit`,
  `file_read`, `file_write`, `provide_file`, `memory_recall`, `memory_write`,
  `match`, `search`, `shell`, `subagent_spawn`, `task_plan`, and `use_skill`.
- Skill/plugin mechanism: native skills such as `ima-knowledge`, `ima-note`,
  `ima-ppt`, `ima-report`, and `ima-skill-creator`.
- Likely strengths: knowledge-base retrieval, notes, memory, reports, PPT, and
  source-grounded review workflows.
- Required fallback: if ima tools are absent, use generic Markdown fallback.
- Notes: shell remains optional; only run local Python when shell exists.
