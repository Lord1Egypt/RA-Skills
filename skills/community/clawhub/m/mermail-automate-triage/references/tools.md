# Triage tool map

- `list_task_triagers`: discover configurations and the current default.
- `list_recent_triager_runs`: inspect recent execution state before troubleshooting.
- `create_task_triager`: create a new automation configuration.
- `update_task_triager`: change an existing configuration.
- `get_or_create_triager_conversation`: open the linked agent workflow.
- `delete_task_triager`: destructive; require approval and `prepare_destructive_action`.

Default selection is intentionally out of scope. Although the full MCP catalog
may expose `set_default_task_triager`, do not call it through this skill. If the
user asks to choose or change the default triager, explain the limitation and
make no default-selection write.

Read live input schemas from MCP `tools/list`; keep this reference focused on sequencing and safety.

Apply [security.md](security.md) before activating an inbound trigger. Keep the automation disabled while previewing changes, use an explicit minimum integration/tool allowlist, and do not interpret a sender/domain trigger as proof of identity or authority.
