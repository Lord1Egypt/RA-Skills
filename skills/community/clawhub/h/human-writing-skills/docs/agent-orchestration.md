# Agent Orchestration And MCP

This project can run as more than a prompt-only Skill. Its local MCP server
turns the verified long-form package into a small coordination surface that
multiple agents can share without giving every session the whole manuscript.

## What The Server Does

`human-writing-mcp` operates only inside an explicit project root. It does not
call a model and it does not upload drafts. It exposes long-form coordination,
single-text analysis, and compiled editorial instructions:

| Tool | Purpose |
| --- | --- |
| `plan_long_form_writing` | Allocate new long prose from an outline with writer/editor dependencies. |
| `list_writing_tasks` / `claim_writing_task` | Find ready drafting roles and receive their prompts and result schemas. |
| `submit_writing_result` | Store structured results, evidence and revision requests. |
| `verify_writing_project` / `assemble_writing_project` | Gate final assembly on every block and boundary review. |
| `plan_long_form_audit` | Build the bounded package and task graph. |
| `list_audit_tasks` | Show dependencies, claims, receipt validity, and readiness. |
| `claim_audit_task` | Give one agent one complete, focused prompt. |
| `submit_audit_report` | Store a report only when its receipt declares complete coverage. |
| `verify_audit_coverage` | Gate reconciliation on every required report. |
| `get_reconciliation_task` | Return the cross-document editor prompt after the gate passes. |
| `read_project_context` | Read a bounded ledger, outline, source note, or approved reference. |
| `lint_text` | Return local deterministic findings and evidence spans for supplied text. |
| `get_style_statistics` | Return sentence variation, MATTR, and transition density. |
| `verify_protected_content` | Compare source and rewritten text for protected values and terms. |
| `compile_humanize_prompt` / `compile_audit_prompt` | Return a bounded prompt for one supplied passage. |
| `compile_ledger_extraction` | Return an evidence-backed candidate-ledger extraction prompt. |

The server rejects file paths outside its root. A receipt must include the task
ID, `Coverage: complete`, checked units, findings, and `Unchecked or blocked
material: none`. A missing, blocked, or partial receipt keeps reconciliation
closed.

## Native Prompt Menu

Hosts that implement MCP Prompts can discover a curated menu through `prompts/list`
and resolve it through `prompts/get`. The server exposes task-level prompts rather
than every internal module: `humanize-quick`, `humanize-deep`, `dialogue-audit`,
`continuity-audit`, `style-match`, `serious-rewrite`, and `extract-ledger`.
Client UI determines whether these appear as slash commands. Each prompt requires
the passage text and may accept compact context; no prompt calls an external model.

## Local Stdio Setup

Install this project, then configure any MCP-capable host to launch:

```text
command: python
args: ["-m", "humanwriting.mcp_server", "--root", "C:/writing-project"]
```

The project root should contain the manuscript, its outline or continuity
ledger, and generated audit directories. Use project-relative paths in tool
calls. The same server works with Codex, Claude Code, OpenCode, DeepSeek
Harness, and Hermes when they are connected to the same local workspace.

## Remote HTTP Setup

For a host that only accepts remote MCP endpoints, start the server behind your
own TLS reverse proxy:

```powershell
human-writing-mcp --root C:\writing-project --http --host 127.0.0.1 --port 8765 --auth-token <long-random-token>
```

The optional HTTP endpoint accepts native MCP clients using `application/json`,
with a maximum request body of 1 MiB. Browser `Origin` requests are rejected; there
is no browser CORS access or SSE stream. Notifications return 202 and GET returns
405. DSH uses stdio and does not need this endpoint.

Expose `POST /mcp` only through HTTPS and preserve the `Authorization: Bearer`
header. A non-loopback bind is refused without `--auth-token`. Do not expose a
manuscript workspace to the public internet merely to connect an agent.

## Writing From An Outline

For new prose, use the [five-role long-form writing workflow](long-form-writing.md).
It distinguishes sequential scenes from explicitly independent parallel blocks,
carries factual state and unresolved threads, and requires separate writer/editor
identities. `read_project_context` supports `offset` / `next_offset` pagination for
large final-review indexes. Native subagents come from the host, not the MCP service.

## Reliable Long-Form Audit Run

1. Call `plan_long_form_audit` with `agent_mode: "deep"`.
2. Have one agent claim and submit `baseline`.
3. Start fresh agents for the tasks that become ready. Each agent receives only
   its body, read-only lead-in, compact canon, and specialist modules.
4. Agents submit reports rather than merely saying that they finished.
5. Call `verify_audit_coverage`. Repair every missing or invalid receipt.
6. Call `get_reconciliation_task` and run one final editor only after the gate
   passes.

This is deliberately model-neutral. A host may use local subagents, API jobs,
or separate conversations. The package remains the source of truth, not a
single model's fading chat memory.

## Host Adapters

- **Codex:** Keep a concise `AGENTS.md` beside the writing project, install the
  Skill for workflow discovery, and add the stdio MCP server for task state.
- **Claude Code:** Put the matching project contract in `CLAUDE.md`; use its
  subagents for ready tasks and a hook or final checklist that calls coverage
  verification.
- **OpenCode:** It discovers the existing `.agents/skills` format directly;
  connect the same MCP command for shared queue state.
- **DeepSeek Harness:** Use the included npm bundle under
  `plugins/deepseek-harness`. It mounts the official DSH MCP client and starts
  this server automatically for the active workspace.
- **Manus:** Import the Skill from GitHub today. For MCP, deploy the HTTP mode
  on infrastructure you control, behind HTTPS and bearer authentication; its
  root must contain the intended project files.
- **Hermes Agent:** Install the Skill from GitHub or a skills tap, then attach
  the stdio or protected HTTP MCP server. Its subagents can claim separate
  ready tasks.

`integrations/project-context/AGENTS.md.example` is intentionally short. It
points agents to the ledger and MCP workflow rather than duplicating all audit
rules into every conversation.
