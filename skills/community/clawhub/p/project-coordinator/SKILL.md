---
name: project-coordinator
version: 1.0.12
homepage: https://github.com/KaigeGao1110/Project-Coordinator
description: |
  Spawns an isolated Project Coordinator session that owns a project's context,
  breaks work into tasks, and spawns subagents for parallel execution.
dependencies:
  - archive-project
required: {}
configPaths: []
permissions:
  - spawn: subagent sessions
  - read: workspace files
  - exec: shell commands via subagents
dataPolicy:
  archivedData: internal workspace only
  neverExternal: true
---

## Installation

### Option 1: ClawhHub CLI (recommended)
```bash
openclaw skills install project-coordinator
# or
clawhub install project-coordinator
```

### Option 2: From GitHub
```bash
# Clone the repo
git clone https://github.com/KaigeGao1110/Project-Coordinator.git ~/.openclaw/skills/project-coordinator

# Or download directly
curl -L https://github.com/KaigeGao1110/Project-Coordinator/archive/refs/heads/main.zip -o /tmp/project-coordinator.zip
unzip /tmp/project-coordinator.zip -d ~/.openclaw/skills/
mv ~/.openclaw/skills/Project-Coordinator-main ~/.openclaw/skills/project-coordinator
```

# Project Coordinator Skill

A skill for structuring multi-agent project execution with isolated session architecture.

---

## Manifest

```yaml
name: project-coordinator
version: 1.0.11
description: |
  Spawns an isolated Project Coordinator session that owns a project's context,
  breaks work into tasks, and spawns subagents for parallel execution.
  The Coordinator reports back to the main session when done.
permissions:
  - spawn: subagent sessions (via sessions_spawn)
  - read: workspace files
  - exec: shell commands via subagents
dataPolicy:
  archivedData: internal workspace only
  neverExternal: true
```

---

## Architecture

```
Main Session (never runs code directly)
  └── Project Coordinator (spawned per project, mode="run")
        └── Subagents (spawned by Coordinator, run tasks in parallel)
```

**Token efficiency**: Each project Coordinator is isolated. Old project sessions accumulate zero main-session tokens after completion.

**Least-privilege design**: The Coordinator does NOT read session transcript files directly. All transcript reading, sanitization, and archiving is delegated to a dedicated archive-subagent using the archive-project skill.

---

## Trigger Conditions

Activated when:
- User says "start a new project" or "let's work on [project]"
- A task is complex and needs multiple subagents
- A task will take more than a few minutes
- When user says "archive this" after a project is done → spawn archive-subagent

Do NOT activate for: quick questions, simple lookups, one-liner tasks.

### Trigger 3: Slash command
Type `//start ` followed by your project description to activate the Project Coordinator.
Example: "//start build a Chrome extension"

---

## Project Coordinator Pattern

### Step 1: Define the Project

Collect from the user:
- Project name (e.g., "cureforge-hr-assessment")
- Project description (1-2 sentences)
- Key deliverables
- Any known constraints

### Step 2: Spawn Project Coordinator

```python
sessions_spawn(
  task=f"""You are the Project Coordinator for {project_name}.

Project: {project_description}

Your job:
1. Understand the full scope of this project
2. Break it into independent tasks
3. Spawn subagents to execute tasks in parallel
4. Monitor subagent progress
5. Compile results and report back to main session

When done, write a summary and await further instructions.
""",
  label=f"coordinator-{project_name}",
  runtime="subagent",
  model="minimax-m2.7-highspeed",
  mode="run"
)
```

### Step 3: Monitor Progress

- Use `subagents(action="list")` to track subagent status
- Receive completion announcements via inter-session messages
- If a subagent fails, decide whether to retry or adapt

### Step 4: Compile and Report

When all subagents complete:
1. Review all outputs
2. Write a final summary
3. Save any deliverables before the Coordinator session ends

### Step 5: Archiving (Delegated)

When a project is complete and archiving is requested:

1. The Coordinator spawns an archive-subagent
2. The archive-subagent uses the archive-project skill to handle:
   - Locating the correct session transcripts
   - Sanitizing credentials
   - Writing ARCHIVE.md
   - Committing to workspace
3. The Coordinator monitors the archive-subagent and reports completion

**The Coordinator itself does NOT read session transcript files directly.**

---

## Coordinator's Tool Usage

**Note:** The Coordinator should NOT directly read, copy, move, or delete session transcript files. All such operations must be performed by a dedicated archive-subagent using the archive-project skill.

**Subagent sandboxing:** When spawning subagents, each subagent runs in an isolated sandbox with workspace-only filesystem access. Subagents cannot access credentials, environment variables, or session transcripts outside their scope. Network access is restricted per platform policy.

The Coordinator SHOULD directly call tools:
- `exec` — run commands, check files
- `write` — create output files
- `read` — examine code or documents
- `sessions_spawn` — spawn subagents for parallel work
- `subagents` — monitor subagent status

---

## Subagent Naming Convention

Format: `{project}-{role}`

Examples:
- `cureforge-gke-migration`
- `cureforge-rabbitmq-queue`
- `cureforge-review`

---

## Session Management Rules

- One Coordinator per project (isolated token accounting)
- Do NOT run multiple unrelated projects in one Coordinator
- When a project is complete, the Coordinator stops — no lingering sessions
- For long-running projects: Coordinator can spawn child Coordinators for sub-phases

---

## After Project Completion

1. Report completion to Main session (brief summary)
2. Notify the user
3. User decides: archive / continue / hold
