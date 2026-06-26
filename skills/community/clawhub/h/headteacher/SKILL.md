---
name: headteacher-workbench
description: "Bootstrap and operate an AI-native headteacher workspace. Guide users through backend selection, environment-aware Feishu Base access routing, schema installation, data operations, and artifact generation. Use for class management setup, OpenClaw Feishu plugin onboarding, Feishu CLI onboarding, student records, grades, conduct logs, parent communication, schedules, and Word/Excel/PPT outputs. | 搭建并运行班主任 AI Native 工作台：引导用户选择后端、按运行环境路由飞书多维表格接入方式、初始化班级数据库、持续处理学生信息、成绩、德育、家校沟通与文件生成。"
argument-hint: "[task-or-class-name]"
version: "2.1.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: Detect the user's language from their first message and keep using it. The guidance below is written in English and Chinese for the same workflow.

# Headteacher Workbench

## When this skill should trigger

Trigger this skill when the user wants to do any of the following:

- Set up a headteacher workspace for the first time
- Install or verify `lark-cli`
- Install or verify the official OpenClaw Feishu plugin
- Connect Feishu Base, Notion, or Obsidian
- Bootstrap a class-management schema
- Inspect an existing Feishu Base and decide whether it is reusable
- Import student rosters or update grades, conduct records, parent communication, seat plans, duty schedules, or committee assignments
- Generate `.docx`, `.xlsx`, or `.pptx` artifacts from structured data
- Query an existing class workspace and update or summarize it

Do **not** treat this skill as:

- A persona simulator
- A teacher role-play prompt
- A colleague distillation workflow

## Default operating mode

This skill is **setup-first**. On first use, do not jump straight into task execution.

1. Check whether a local workspace manifest exists at:
   - `./.headteacher-skill/workspace_manifest.json`
2. If the manifest does not exist or is incomplete, enter setup mode.
3. Default-recommend `feishu_base` as the backend.
4. Only after setup is complete should normal runtime task routing begin.

After setup, treat the skill as two cooperating subsystems:

1. **Data record and retrieval**
   - write mode:
     - one-time import
     - dynamic append / update
   - read mode:
     - longitudinal read: follow one student across a timeline
     - horizontal read: inspect a cohort or the whole class at one time slice
2. **Artifact generation**
   - generate Office outputs from structured data
   - typical cases:
     - seat plan / duty schedule arranged by attributes
     - parent meeting PPT generated from scores plus daily records

## Setup workflow

### Step 1: Environment doctor

Run:

```bash
python3 tools/setup_doctor.py --format markdown
```

Use the result to decide:

- which agent runtime is currently hosting the skill
- whether Feishu should be accessed through the OpenClaw official plugin or through `lark-cli`
- whether `lark-cli` is installed
- whether Feishu is configured
- whether office artifact generation dependencies are present
- whether Notion MCP is available in the current agent environment
- whether Obsidian CLI is available
- whether the user still needs the official Obsidian skill / connector setup

### Step 2: Backend selection

Read [prompts/backend-selector.md](prompts/backend-selector.md).

Default recommendation order:

1. `feishu_base`
2. `notion`
3. `obsidian`
4. `local_only`

Use Feishu as the default unless the user explicitly prefers otherwise.

### Step 3: Workspace bootstrap

Read:

- [prompts/setup.md](prompts/setup.md)
- [prompts/schema-installer.md](prompts/schema-installer.md)
- [references/schema-manifest.md](references/schema-manifest.md)
- [references/backend-contract.md](references/backend-contract.md)

If backend is `feishu_base`, also read:

- [prompts/feishu-bootstrap.md](prompts/feishu-bootstrap.md)
- [references/feishu-model.md](references/feishu-model.md)

Then choose the Feishu access path:

1. If `tools/setup_doctor.py` reports `agent_runtime.runtime = openclaw`:
   - check whether the official OpenClaw plugin `openclaw-lark` is installed
   - if missing, guide installation first
   - then use the plugin's Feishu Base tools / API capabilities to create the base, tables, fields, views, and records
   - do **not** require `lark-cli` in this branch
2. If runtime is `codex`, `claude_code`, or another local agent:
   - use the existing local toolchain
   - run:

```bash
python3 tools/feishu_bootstrap.py bootstrap --workspace-name "<class-name>"
```

If the user provides an existing Base, inspect it first:

```bash
python3 tools/migration_inspector.py feishu --base-token "<base-token>" --format markdown
```

### Step 4: Runtime routing

Once setup is complete, read [prompts/runtime-router.md](prompts/runtime-router.md) and route the user's request into one of these intents:

- `setup workspace`
- `connect backend`
- `bootstrap schema`
- `inspect existing workspace`
- `migrate from subject-teacher base`
- `append records`
- `query student/class data`
- `generate artifact`
- `sync artifact`

## Runtime rules

### Capability split

Treat all runtime work as belonging to one of two families:

1. `data operations`
   - import existing roster / score / conduct material
   - append or update new records
   - read one student longitudinally
   - read multiple students horizontally
2. `artifact generation`
   - produce `.docx`, `.xlsx`, `.pptx` outputs from structured data
   - never treat Office files as the source of truth

### Data model

All runtime work should use the unified semantic model described in [references/schema-manifest.md](references/schema-manifest.md), not backend-specific ad hoc field guesses.

Core entities:

- student master
- exam batch
- score detail
- growth event
- parent communication
- seat assignment
- duty assignment
- committee assignment
- artifact registry

The model is intentionally object-event based:

- `student master` is the stable object layer
- scores, conduct, duties, observations, and parent communication are event or assignment layers
- artifacts are downstream products generated from those layers

### Backend rules

#### Feishu Base

The only fully supported backend in v1.

Always route access by runtime first:

- `openclaw` -> official OpenClaw Lark/Feishu plugin (`openclaw-lark`) + Feishu Base API tools
- `codex`, `claude_code`, or local agent -> `lark-cli` + local Python tools in this repository

Use local tools when the runtime is **not** OpenClaw:

- `python3 tools/setup_doctor.py`
- `python3 tools/feishu_bootstrap.py`
- `python3 tools/migration_inspector.py`
- `python3 tools/artifact_registry.py`

#### Notion

Supported as a planning target only in v1.

Read:

- [references/notion-model.md](references/notion-model.md)

Treat Notion as an external dependency:

- verify that Notion MCP is already connected
- if it is not connected, guide the user to install or connect Notion MCP first
- do not attempt to bundle Notion capability into this repository

You may produce the mapping plan and minimal bootstrap instructions, but do not claim full runtime parity with Feishu in v1.

#### Obsidian

Supported as a local-first planning target only in v1.

Read:

- [references/obsidian-model.md](references/obsidian-model.md)

Treat Obsidian as an external dependency:

- verify whether `obsidian` CLI is installed locally
- if missing, guide the user to install Obsidian CLI
- recommend that the user also installs the official Obsidian-related skill exposed by the agent environment
- do not attempt to bundle the Obsidian CLI or official skill into this repository

You may generate folder and note templates plus schema mapping guidance, but do not claim a full structured database experience in v1.

## Artifact generation

Use [prompts/artifact-generator.md](prompts/artifact-generator.md) and [references/artifact-spec.md](references/artifact-spec.md).

Supported artifact kinds in v1:

- `.docx`: parent visit records, class notices, student talk records
- `.xlsx`: seat plans, duty schedules, committee tables, deduction summaries
- `.pptx`: parent meeting slides

Before generating artifacts:

1. Confirm the workspace has already been initialized
2. Query structured data first
3. Choose a template or explain that a template is missing
4. Register the result with:

```bash
python3 tools/artifact_registry.py register ...
```

## Safety and change control

- Never overwrite an existing Feishu Base by default.
- If the user provides an existing Base, inspect and classify it before proposing migration.
- Preview destructive or schema-changing operations before applying them.
- Treat student contact details, addresses, and IDs as sensitive fields.
- Do not claim Notion or Obsidian parity that v1 does not implement.
- Do not imply that Notion MCP or Obsidian CLI are shipped by this repository; only guide installation or verification.

## Resource map

### Prompts

- [prompts/setup.md](prompts/setup.md)
- [prompts/backend-selector.md](prompts/backend-selector.md)
- [prompts/feishu-bootstrap.md](prompts/feishu-bootstrap.md)
- [prompts/schema-installer.md](prompts/schema-installer.md)
- [prompts/runtime-router.md](prompts/runtime-router.md)
- [prompts/artifact-generator.md](prompts/artifact-generator.md)
- [prompts/migration-guide.md](prompts/migration-guide.md)

### References

- [references/schema-manifest.md](references/schema-manifest.md)
- [references/backend-contract.md](references/backend-contract.md)
- [references/feishu-model.md](references/feishu-model.md)
- [references/notion-model.md](references/notion-model.md)
- [references/obsidian-model.md](references/obsidian-model.md)
- [references/artifact-spec.md](references/artifact-spec.md)

### Tools

- `tools/setup_doctor.py`
- `tools/schema_planner.py`
- `tools/feishu_bootstrap.py`
- `tools/migration_inspector.py`
- `tools/artifact_registry.py`
