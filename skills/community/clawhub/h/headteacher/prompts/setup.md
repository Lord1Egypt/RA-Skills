# Setup Workflow

Use this prompt when the workspace has not been initialized yet.

## Goal

Turn a fresh installation into a usable headteacher workspace.

## Default behavior

1. Check whether `./.headteacher-skill/workspace_manifest.json` exists.
2. If missing, enter setup mode immediately.
3. Run:

```bash
python3 tools/setup_doctor.py --format markdown
```

4. Use the doctor result to identify the agent runtime and Feishu access mode.
5. Recommend `feishu_base` unless the user explicitly prefers another backend.
6. If the user accepts Feishu and the access mode is `openclaw_plugin`, guide them through:
   - verifying whether the official OpenClaw Lark/Feishu plugin (`openclaw-lark`) is installed
   - installing that plugin first if missing
   - using the plugin's Feishu Base API tools to create the workspace, tables, fields, views, and records
   - not requiring `lark-cli` in this branch
7. If the user accepts Feishu and the access mode is `lark_cli`, guide them through:
   - installing or verifying `lark-cli`
   - running `lark-cli config init --new` if needed
   - bootstrapping the workspace with `tools/feishu_bootstrap.py`
8. If the user selects Notion, verify that Notion MCP is connected. If not, stop at external setup guidance.
9. If the user selects Obsidian, verify that Obsidian CLI is installed and remind them to install the official Obsidian skill if needed.
10. After bootstrap, explain what tasks the user can run next.

## Required outputs

- environment status
- agent runtime
- Feishu access mode
- chosen backend
- whether the workspace is initialized
- next available actions

## Do not do

- do not role-play a teacher
- do not ask persona questions
- do not jump into file generation before setup is complete
- do not pretend this repository contains Notion MCP or Obsidian CLI capabilities
- do not force `lark-cli` when the skill is running inside OpenClaw with the official Feishu plugin path available
