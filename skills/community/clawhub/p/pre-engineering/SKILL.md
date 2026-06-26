---
name: pre-engineering
description: "PRE Engineering — Initialize a PRE (Plan-Review-Execute) multi-agent collaborative project. TRIGGER when: user wants to initialize a multi-agent collaborative project, mentions PRE system, PRE Engineering, wants to set up collaborative agents, wants to initialize project documents for agent collaboration, asks how to make multiple AI roles collaborate on a project, mentions Plan-Review-Execute, wants to use a collaboration log to drive multi-agent work, wants to create Planner/Executor/Reviewer guide documents, wants to start a PRE collaboration workflow, or expresses multi-agent collaboration intent without explicitly mentioning PRE."
---

# PRE Engineering

Guide the user to describe project requirements, interactively refine them, confirm and output project documents, then provide startup instructions.

## Overview

The PRE system operates through three agent roles — Planner, Executor, and Reviewer — using the collaboration log as the sole coordination medium, the project goals document as the driving core, and the project code as the decision foundation, enabling autonomous collaboration and continuous operation among agents.

This skill sets up the PRE collaboration framework for the user's project: collects project requirements through interactive Q&A, generates 5 collaboration documents upon confirmation, and provides instructions to launch the three agents. PRE is not a standalone project — it's a framework that adds multi-agent collaboration capabilities to an existing project.

## Interactive Requirements Collection

Use 2 steps to interact with the user, minimizing confirmation requests. During collection, proactively help refine requirements — remove duplicates, normalize descriptions, fill in missing technical constraints, automatically infer information.

### Step 1: Collect All Requirements At Once

Single AskUserQuestion collects all: project overview, features, technical constraints, special notes. Auto-scan project directory to infer available information, reducing manual input.

```json
{
  "questions": [{
    "header": "Project Requirements",
    "multiSelect": false,
    "options": [
      {"label": "Enter manually", "description": "Provide all project information directly (overview, features, constraints, notes)"},
      {"label": "Infer from existing docs", "description": "Auto-scan project directory (README, package.json, etc.) and infer information"}
    ],
    "question": "Please provide project information. You can describe separately:\n1. Project name and overview (1-2 sentences)\n2. Features (one per line)\n3. Technical constraints (tech stack, architecture, quality requirements) — or say 'no constraints'\n4. Special notes (third-party integrations, compliance, etc.) — or say 'none'\n\nExample:\nProject: E-commerce backend\nOverview: Build a backend supporting product management, order processing, and user auth\nFeatures: User registration/login, product lists, order management, payment integration\nConstraints: Python + FastAPI, PostgreSQL, RESTful API, ≥80% unit test coverage\nNotes: Payment integrates third-party API, PCI compliance required"
  }]
}
```

**Information Inference Rules**:
- Auto-scan README.md, design docs, package.json, requirements.txt, etc. to extract overview and tech stack
- If project directory has structured requirements (e.g., SPEC.md), extract feature list directly
- Present inferred results to user for confirmation or modification

After collection, refine requirements: remove duplicates, normalize descriptions, supplement missing dimensions (user management, error handling, etc.).

### Step 2: Confirm Draft & Generate Documents

Synthesize collected information into a project goals document draft and present to user for final confirmation. Upon confirmation, generate all 5 core documents.

```json
{
  "questions": [{
    "header": "Confirm & Generate",
    "multiSelect": false,
    "options": [
      {"label": "Confirm, generate all docs", "description": "Satisfied with the project goals document — start generating all 5 project documents"},
      {"label": "Needs revision", "description": "Not satisfied with some content — adjust it"}
    ],
    "question": "Here is the project goals document draft generated from your description:\n\n{Project goals draft content}\n\nAre you satisfied with it?"
  }]
}
```

If user selects "Needs revision", ask what to adjust, modify the draft, and re-present until confirmed.

Upon confirmation, write to `.pre/project-goals.md` in the project directory with the following format:

```markdown
# Project Goals

## Overview
{Project overview provided by the user}

## Feature Requirements
- {Feature requirements provided by the user, one per line}

## Technical Constraints
- {Technical constraints provided by the user, one per line}
- {If the user selected 'No special constraints', write: The Planner and Executor may choose an appropriate tech stack and architecture based on the project nature}

## Notes
- {Special notes provided by the user, one per line}
- {If the user selected 'No notes', write: No special requirements at this time}
```

**Important**: The project goals document does not include "current status" or "priority" fields. Project status is managed by the collaboration log; priority is determined by the Planner. Agents can only read this document — they must not modify it.

## Collaboration Log Initial Entry

Upon confirmation, write to `.pre/collaboration-log.md` in the project directory, creating the initial entry to drive the Planner to begin the first planning cycle:

```markdown
# Collaboration Log

## [{current_datetime}] Human — Project Launch
- Initialized project, Planner please begin first planning cycle
- Status: PLN_WAIT
```

Time format uses `[YYYY-MM-DD HH:MM]`, must execute `date +"%Y-%m-%d %H:%M"` to get the current system time — never fill in time from memory. **Timezone confirmation**: During initialization, confirm with the user the timezone to use (e.g., Shanghai UTC+8, Tokyo UTC+9, etc.). After confirmation, all log entries must consistently use that timezone, and the confirmed timezone should be recorded in the project goals document's Notes section.

## Agent Guide Document Generation

Upon confirmation, generate three agent guide documents. Each document is generated from the corresponding template file:

1. Read `references/planner-guide-template.md` → fill path placeholders → write to `.pre/planner-guide.md`
2. Read `references/executor-guide-template.md` → fill path placeholders → write to `.pre/executor-guide.md`
3. Read `references/reviewer-guide-template.md` → fill path placeholders → write to `.pre/reviewer-guide.md`

**Placeholder note**:

Templates already use default path values (collaboration-log.md, project-goals.md, ../src). If the user specifies a different code directory, replace all occurrences of `../src` in the template with the user-specified path during generation.

**Generation steps**:
1. Use the Read tool to read the corresponding template file
2. If the user specified a non-default code directory, replace `../src` with the user-specified path
3. Use the Write tool to write the content to the corresponding guide document in the `.pre/` subdirectory

**File existence check**: Before generating, check whether files with the same name already exist in the project directory. If they exist, prompt the user to choose overwrite or skip — do not auto-overwrite.

## Startup Instructions

After all documents are generated, present the startup instructions to the user:

---

**PRE Engineering initialization complete!** The following files have been generated:

- `.pre/project-goals.md` — Project requirements document (only humans can modify)
- `.pre/collaboration-log.md` — Initial PLN_WAIT entry written
- `.pre/planner-guide.md` — Planner role guide document
- `.pre/executor-guide.md` — Executor role guide document
- `.pre/reviewer-guide.md` — Reviewer role guide document

**IMPORTANT: Commit baseline before starting agents**

During subsequent reviews, the Reviewer will execute `git stash save` to stash code changes. If the `.pre/` collaboration documents are not committed, stash will sweep them away, causing agents to lose access to their files. **You must commit the generated documents as a baseline before starting the three agents**:

```bash
cd {project_directory_path}
git add .pre/
git commit -m "PRE initialization: collaboration documents baseline"
```

**Startup steps** (requires three separate terminals):

1. **Terminal 1 — Planner** (recommended: strong reasoning model, e.g. claude-opus-4-6):
   ```
   cd {project_directory_path}/pre
   claude --model claude-opus-4-6
   ```
   Then enter:
   ```
   /loop "Read planner-guide.md and follow its instructions as the Planner role. Each cycle starts by reading collaboration-log.md to check the latest status."
   ```

2. **Terminal 2 — Executor** (recommended: fast coding model, e.g. claude-sonnet-4-6):
   ```
   cd {project_directory_path}/pre
   claude --model claude-sonnet-4-6
   ```
   Then enter:
   ```
   /loop "Read executor-guide.md and follow its instructions as the Executor role. Each cycle starts by reading collaboration-log.md to check the latest status."
   ```

3. **Terminal 3 — Reviewer** (recommended: thorough review model, e.g. claude-opus-4-6):
   ```
   cd {project_directory_path}/pre
   claude --model claude-opus-4-6
   ```
   Then enter:
   ```
   /loop "Read reviewer-guide.md and follow its instructions as the Reviewer role. Each cycle starts by reading collaboration-log.md to check the latest status."
   ```

**IMPORTANT: Record Loop Task Job IDs**

After each `/loop` command is started, Claude returns a **job ID** (typically UUID format) displayed in the result. **Record all three job IDs immediately**:

```
Planner job ID:   <copy from planner startup result>
Executor job ID:  <copy from executor startup result>
Reviewer job ID:  <copy from reviewer startup result>
```

Suggested save locations:
- `.runner-ids.txt` file in project root, or
- Comment in the collaboration log header, or
- Local notes/document

**Usage**:
- **Pause single agent**: Execute `ScheduleCancel <job-id>` or provide job ID to cancel that loop
- **Pause all agents**: Cancel all three job IDs
- **Restart**: Re-run `/loop` command to generate new job IDs

See the "Loop Task Process Management" section in each agent's guide document for details.

**Project control methods**:

| Control intent | Operation | Agent response |
|---------------|-----------|----------------|
| Adjust direction | Modify feature descriptions or technical constraints in `.pre/project-goals.md` | Planner adjusts the plan in the next cycle based on the new direction |
| Reduce scope | Delete feature requirements in `.pre/project-goals.md` | Planner detects no requirements during PLN_WAIT and submits a "no new requirements" declaration |
| Add requirements | Add new items to feature requirements in `.pre/project-goals.md` | Planner identifies new requirements in the next cycle and proposes them |
| Pause project | Write "currently paused" in the Notes section of `.pre/project-goals.md` | Planner recognizes the pause marker during PLN_WAIT and does not act |

**DONE achievement condition**: Planner declares no new requirements → Reviewer confirms all project goals have been delivered → Reviewer writes DONE → Project complete.

---

## Loop Prevention (Deadlock Protection)

The PRE system has a built-in loop prevention mechanism to prevent infinite retry cycles when the Executor keeps getting rejected:

- **Blocking rule**: When the Reviewer rejects the Executor's submission for the same requirement **3 consecutive times**, the Reviewer marks a loop block and reverts the status to `PLN_WAIT`
- **Planner's response**: Upon receiving a loop block notice, the Planner should re-split or adjust the requirement proposal and submit a new plan
- **Executor's response**: Identify loop blockage marker in the log, stop retrying, wait for Planner's new requirements
- **Rejection count method**: Reviewer traces the log from the Planner's requirement submission entry, counting each rejection; when count reaches 3, mark blockage

## Version Recording Mechanism

The Reviewer is responsible for version management after each review cycle to ensure every delivered version is traceable:

- **When planning review passes**: Execute `git add <code_dir> && git stash save` to save a code snapshot (default src/, `.pre/` excluded via .gitignore)
- **When execution review passes**: Update `VERSIONS.md` and execute `git commit -m "V{date}-{time} V{version} - [description]"`
- **Version format**: `V{date}-{time} V{semantic-version}`（e.g., V20260511-2325 V0.0.6）
- **VERSIONS.md format**: Each record contains version number, change time, change summary (within 5 lines)

---

## Safety and Integrity Checks

1. **Do not overwrite existing files**: Check for existing files with the same name before generating documents; if they exist, prompt the user to choose overwrite or skip
2. **Collaboration log is append-only**: If the collaboration log already exists with entries, append new entries rather than rewriting the entire file
3. **Project goals document protection**: The generated project goals document is clearly marked "only humans can modify" — agents must not modify this file
4. **Code directory creation**: If the user-specified code directory (default `src/`) does not exist, create an empty directory