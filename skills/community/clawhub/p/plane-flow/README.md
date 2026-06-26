# plane-flow

Operate a local or self-hosted Plane workspace from OpenClaw.

## What it does

`plane-flow` helps an agent work with Plane for day-to-day PM flow:
- list projects, issues, states, labels, members, and cycles
- summarize project status
- create issues from notes or action items
- update issue descriptions
- move issues between states
- assign owners
- set priority and labels
- create cycles and add issues to cycles
- create comments and attach files
- add external links to issues

## Intended use

Use this skill when the user wants to:
- manage a backlog in Plane
- turn meeting notes into issues
- summarize project progress
- assign or triage work
- manage sprint / cycle flow in a self-hosted Plane instance

## Requirements

Python dependencies used by the bundled scripts:
- `requests`
- `PyYAML` (optional, only if using `PLANE_CONFIG_FILE`)
- `markdown` (optional, used for markdown-to-HTML rendering)

## Usage model: admin setup, business-team usage

This package is designed for two roles:

### 1) Administrators / technical owners
These people set up the Plane connection once for the environment.
They might be:
- the OpenClaw deployer
- an internal AI/platform owner
- an engineer supporting the workspace
- a technically comfortable PM/ops lead

Their job is to configure:
- `PLANE_BASE_URL`
- `PLANE_API_TOKEN`
- `PLANE_WORKSPACE_ID`
- optional local aliases / state mappings / priority mappings

### 2) Business users
These people use the skill in normal day-to-day work.
They might be:
- product managers
- operations teammates
- project managers
- delivery / coordination roles
- other non-technical collaborators

Their job is **not** to deal with environment variables or CLI tools.
Once the environment has been configured, they should be able to use the skill through normal natural-language requests.

The bundled Python scripts in `scripts/` are implementation helpers and admin/debugging tools. They are **not** the primary business-user interface.

## Administrator setup

### Required environment

Before the skill can talk to Plane, the host environment needs:

```bash
export PLANE_BASE_URL="https://your-plane.example.com"
export PLANE_API_TOKEN="your_api_token"
export PLANE_WORKSPACE_ID="your-workspace-id"
```

### Optional local config

You can also provide a small local YAML config for aliases and mappings:

```bash
cp scripts/sample_config.yaml ~/.plane_config.yaml
export PLANE_CONFIG_FILE="$HOME/.plane_config.yaml"
```

This optional config is useful for:
- default project alias
- project name aliases
- state name mapping
- priority mapping

### Optional admin helper: init wizard

For administrators, this skill also ships an optional helper script:

```bash
python3 scripts/init_config.py
```

It can generate a local `~/.plane_config.yaml`-style file and print the required `export` commands.

Notes:
- the real Plane API token is **not** written into the YAML file
- the token still lives in the shell environment
- this helper is for setup convenience, not the primary skill interface

### Optional admin helper: connection test

For debugging or first-time validation, administrators can run:

```bash
python3 scripts/test_connection.py
```

This verifies that the local environment is correctly configured and that the Plane API can be reached.

## Business-user experience

After an administrator has configured the environment, business users should be able to say things like:
- "帮我看看这个 Plane 项目的 backlog"
- "把这段会议纪要拆成几个 issue"
- "查一下这个项目现在有哪些高优先级任务"
- "把这个 issue 指派给某个人"
- "给这个 sprint 加几个 issue"
- "总结一下这个项目当前进展"

In other words, the normal user experience should be conversational, not command-line based.

## Local debugging / development helpers

For local debugging, development, or manual validation, the bundled CLI is also available:

```bash
python3 scripts/plane_cli.py projects list
python3 scripts/plane_cli.py projects summary --project "Your Project"
python3 scripts/plane_cli.py issues list --project "Your Project"
python3 scripts/plane_cli.py issues create --project "Your Project" --title "Draft requirement" --desc "Created from notes"
python3 scripts/plane_cli.py issues move --project "Your Project" --id <ISSUE_ID> --state todo
python3 scripts/plane_cli.py members list
```

### Inline images in issue descriptions

Issue descriptions now support text plus uploaded inline images.

Examples:

```bash
python3 scripts/plane_cli.py issues create \
  --project "Your Project" \
  --title "Requirement with screenshot" \
  --desc "This requirement includes a reference image." \
  --image ./screenshot.png
```

```bash
python3 scripts/plane_cli.py issues update-desc \
  --project "Your Project" \
  --id <ISSUE_ID> \
  --desc "Updated description with two inline images." \
  --image ./flow-1.png \
  --image ./flow-2.png
```

Behavior:
- images are uploaded as issue attachments first
- images are embedded using Plane's native `<image-component>` nodes with the `alignment` attribute
- supported alignments: `left`, `center` (default), `right`
- true text wrapping around images is not supported by Plane's editor (images are always block-level elements)
- if an embeddable URL is unavailable, the upload still succeeds and the skill falls back to attachment-only messaging in the description

## Notes

- This skill is designed for local or self-hosted Plane setups.
- The intended operating model is: administrators configure once, business users use it conversationally.
- Issue detail and issue update routes are handled as project-scoped.
- The bundled scripts are the implementation layer behind the skill, plus optional admin/debugging helpers.

## Files

- `SKILL.md` — skill instructions
- `scripts/` — bundled Plane integration
  - `init_config.py` — interactive config wizard
- `references/cli-usage.md` — command cookbook

## Skill changelog

### 0.1.3 — image alignment via Plane-native nodes
- use Plane's native `<image-component>` nodes instead of `<img>` tags for correct alignment support
- add `--image-align` flag to `issues create`, `issues update-desc`, and `comments create`
- alignment options: `left`, `center`, `right`

### 0.1.2 — inline images in comments
- `comments create --image` — supports repeatable `--image` for inline image embedding in comments
- same upload-then-embed pattern as issue descriptions

### 0.1.1 — metadata clarity
- clarify runtime requirements, required Plane environment variables, credential expectations, and admin-only local helper behavior

### 0.1.0 — initial release
- self-hosted Plane workflow skill with admin-first setup, conversational business-user workflow support, bundled issue/project helpers, interactive init helper, and publish-ready cleanup.

## Recommended fallback when not configured

If the skill is installed but the Plane connection is not configured yet, the user-facing response should guide the user toward an administrator handoff, for example:

> Plane 还没有完成连接配置，所以我暂时没法读取或更新你的项目。请让管理员或负责部署 OpenClaw 的同事先配置 Plane 连接（包括实例地址、API token 和 workspace ID）。配置完成后，你就可以直接用自然语言让我查询 backlog、创建 issue、安排 sprint 了。

This is usually better than exposing raw missing-env errors to non-technical users.

## Publishing hygiene

This package intentionally avoids shipping any real Plane URL, API token, workspace ID, project ID, or member ID.
