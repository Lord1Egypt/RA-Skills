---
name: looop
description: Claude Automated Development Toolkit - Decompose requirements documents, single files, or inline text into detailed task lists and automatically execute in loops until project completion
requires:
  - claude-cli: Requires local Claude CLI installation
  - git: Modifies git repository (commits changes)
  - push: Optional git push to remote (--push flag)
permissions:
  - dangerous: Uses --dangerously-skip-permissions to bypass permission prompts
  - write: Writes files to specified src directory
  - git-commit: Automatically commits task completions
  - git-push: Optional push with --push flag
warning: This skill bypasses permission checks and automatically commits/pushes to git. Use with caution on trusted projects only.
---

# Claude Automated Development Toolkit

You are an automated development assistant responsible for decomposing project requirements (from documents, single files, or inline text) into executable task lists and automatically executing each task in loops until the project is complete.

## Parameters

| Parameter          | Required When              | Description                            |
|--------------------|----------------------------|----------------------------------------|
| `--docs <DIR>`     | Decomposing requirements directory | Requirements document directory path   |
| `--doc <FILE>`     | Decomposing single doc file | Single requirements document file path |
| `--requirement <TEXT>` | Decomposing inline requirement | Direct requirement text string |
| `--src <DIR>`      | Always required          | Code storage directory path            |

**Note:** `--docs`, `--doc`, and `--requirement` are mutually exclusive for decomposition. Use `--requirement` when you have a simple one-line requirement, `--doc` when you have a single requirements file, or `--docs` when you have multiple files in a directory.

## File Storage Location

All task-related files are stored in `<src_dir>/.looop/` directory:

| File         | Path                            | Description           |
|--------------|---------------------------------|-----------------------|
| tasks.json   | `<src_dir>/.looop/tasks.json`   | Task list data        |
| progress.txt | `<src_dir>/.looop/progress.txt` | Task progress records |
| *.log        | `<src_dir>/.looop/*.log`        | Task execution logs   |

## Log Files

Task execution logs are created per task, named by task ID, name and timestamp:

| Filename Pattern                            | When Created               |
|---------------------------------------------|----------------------------|
| `Task_#0_Decompose_YYYY-MM-DD_HH-MM-SS.log` | Requirements decomposition |
| `Task_#N_TaskName_YYYY-MM-DD_HH-MM-SS.log`  | Each task execution        |

**Log content:**

- Task start/end timestamps (second precision)
- Complete Claude CLI output (JSON stream)
- Debug information

**No log files for:**

- `--status` (status query)
- `--mark-manual` / `--list-manual` / `--resolve-manual` (manual operations)

## Execute Script

**Important**: Change to the skill directory first before running the script.

```bash
cd <skill_directory> && python run.py --src <DIR> [--docs <DIR> | --doc <FILE> | --requirement <TEXT>] [other parameters]
```

## Core Workflow

### Phase 1: Task Decomposition (requires docs/doc/requirement + src)

**Directory mode:** `python run.py --docs <requirements_dir> --src <code_dir> --decompose`

**Single file mode:** `python run.py --doc <requirements_file> --src <code_dir> --decompose`

**Inline requirement mode:** `python run.py --requirement "<requirement text>" --src <code_dir> --decompose`

The script will automatically:

1. Create `<src_dir>/.looop/` directory
2. Read requirement source (documents or inline text)
3. Call Claude to analyze and decompose into independent small tasks
4. Set ID, name, description, priority, dependencies, task_type, estimated_files, acceptance_criteria for each task
5. Save task list to `<src_dir>/.looop/tasks.json`

### Phase 2: Task Execution (only requires src)

Command: `python run.py --src <code_dir>`

The script will first check if `<src_dir>/.looop/tasks.json` exists:

- Not exists → Prompt to run `--decompose` first
- Exists → Automatically execute tasks in loops

Execution process:

1. Select next executable task from tasks.json
2. Call Claude to execute task, code goes into src directory
3. Record progress to progress.txt
4. Update task status, execute git commit
5. Continue next round until all tasks complete

## Optional Parameters

| Parameter               | Short     | Description                                     |
|-------------------------|-----------|-------------------------------------------------|
| `--decompose`           | `-d`      | Decompose requirements documents or text into task list |
| `--status`              | `-s`      | View task status statistics                     |
| `--max-tasks <N>`       | `-m <N>`  | Maximum N tasks to execute                      |
| `--push`                | `-P`      | Execute git push after completion               |
| `--mark-manual <ID>`    | `-M <ID>` | Mark task as needing manual intervention        |
| `--list-manual`         | `-L`      | List tasks needing manual intervention          |
| `--resolve-manual <ID>` | `-R <ID>` | Restore task to pending status                  |

## Usage Examples

```
# Decompose requirements from directory (requires docs + src)
python run.py --docs docs --src src --decompose

# Decompose from single document file
python run.py --doc docs/feature-x.md --src src --decompose

# Decompose from inline requirement text
python run.py --requirement "Implement a user login feature with form validation and JWT authentication" --src src --decompose

# Execute tasks (only requires src)
python run.py --src src

# View status
python run.py --src src --status

# Execute max 3 tasks and push
python run.py --src src --max-tasks 3 --push
```

## tasks.json Data Structure

```json
{
  "project": "Project name",
  "created_at": "YYYY-MM-DD",
  "docs_dir": "docs",
  "src_dir": "src",
  "requirements_docs": [
    "docs/xxx.md"
  ],
  "tasks": [
    {
      "id": 1,
      "name": "Task name (concise, imperative)",
      "description": "Detailed technical description including: what to build, files to create/modify, key implementation points",
      "priority": "high|medium|low",
      "dependencies": [],
      "task_type": "setup|core|feature|refactor|test|docs",
      "estimated_files": ["expected_file_path_1"],
      "acceptance_criteria": ["Specific verifiable criteria"],
      "status": "pending",
      "result": null,
      "issues": [],
      "completed_at": null
    }
  ]
}
```

**Task Fields:**
| Field | Description |
|-------|-------------|
| `id` | Unique task identifier |
| `name` | Concise imperative name (e.g. 'Create user model') |
| `description` | Detailed technical description with what/how/why/scope |
| `priority` | high (essential), medium (important), low (optional) |
| `dependencies` | Array of task IDs that must complete first |
| `task_type` | setup, core, feature, refactor, test, docs |
| `estimated_files` | Expected files to be created/modified |
| `acceptance_criteria` | Specific verifiable completion criteria |
| `status` | pending, in_progress, completed, blocked, needs_manual |

**Note:** When using `--requirement`, the structure will include `"requirements_text": "..."` and `"docs_dir": null` instead of `"requirements_docs"` and `"docs_dir"`.

## Task Status

| Status         | Description               |
|----------------|---------------------------|
| `pending`      | Pending execution         |
| `in_progress`  | Currently executing       |
| `completed`    | Completed                 |
| `blocked`      | Blocked                   |
| `needs_manual` | Needs manual intervention |

## Execution Flow

1. **Receive parameters** - Parse src (required) and optional docs/doc/requirement
2. **Build command** - Build python command based on parameters
3. **Execute script** - Change to skill directory, then run run.py using Bash tool
4. **Output results** - Display execution output and progress