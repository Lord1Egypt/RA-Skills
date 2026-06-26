# project-factory

Bootstrap a new OpenClaw automation project from a plain-language description using a four-phase workflow: LLM reasoning → flowchart confirmation → node configuration → scaffold generation.

## What It Does

1. **Phase 0** — LLM reasons about the project type, trigger, nodes, and skill recommendations from a plain-language description
2. **Phase 1** — Confirm or edit the generated Mermaid flowchart
3. **Phase 2** — Configure each node (skill, cron, credentials)
4. **Phase 3** — Generate the full project scaffold via `bootstrap_project.py`

## Trigger Words

- "创建新项目" / "new project" / "新建项目"
- "项目初始化" / "设计一个新流程"
- "帮我画个流程"

## Model Strategy

Phase 0 defaults to MiniMax-M2.5 (FAST). Automatically escalates to GPT-4.1 (SMART) for projects with 5+ nodes, multiple conditions, or non-standard sources.

## Output

- `projects/<project_key>/` directory with full scaffold
- `config/runtime.env`, `WORKFLOW.md`, `scripts/`
- Telegram routing + Cron registration

## Requirements

- OpenClaw workspace with `projects/` directory
- `skills/project-factory/scripts/bootstrap_project.py`
- Telegram bot token and target chat ID

## Files

- `SKILL.md` — Full skill definition
- `references/flow_design_language.md` — Node vocabulary
- `references/architecture.md` — Shared pipeline pattern
- `references/onboarding_checklist.md` — Setup checklist
- `references/shared_routing_group_schema.md` — Routing group schema