#!/usr/bin/env python3
"""Claude Automated Development Toolkit - Main Controller Script"""
import argparse
import io
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add skill directory to path for imports
_skill_dir = os.path.dirname(os.path.abspath(__file__))
if _skill_dir not in sys.path:
    sys.path.insert(0, _skill_dir)

from task_utils import (
    init_looop_dir, load_tasks, save_tasks, get_next_task,
    update_task_status, get_task_summary, mark_task_manual,
    STATUS_PENDING, STATUS_COMPLETED, STATUS_NEEDS_MANUAL
)
from logger import init_logger, get_logger, close_logger


def get_looop_dir(src_dir: str) -> str:
    """Calculate .looop directory path from src directory"""
    return os.path.join(src_dir, ".looop")


def get_tasks_file(src_dir: str) -> str:
    """Calculate tasks.json file path from src directory"""
    return os.path.join(get_looop_dir(src_dir), "tasks.json")


def get_progress_file(src_dir: str) -> str:
    """Calculate progress.txt file path from src directory"""
    return os.path.join(get_looop_dir(src_dir), "progress.txt")


def check_claude_installed() -> bool:
    """Check if Claude CLI is installed"""
    try:
        result = subprocess.run(
            'claude --version',
            capture_output=True,
            text=True,
            shell=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def ensure_claude_md(src_dir: str) -> bool:
    """Check if CLAUDE.md exists in project directory, if not run init"""
    claude_md_path = os.path.join(src_dir, "CLAUDE.md")

    # Check parent directory too
    parent_dir = os.path.dirname(src_dir)
    parent_claude_md = os.path.join(parent_dir, "CLAUDE.md")

    if os.path.exists(claude_md_path) or os.path.exists(parent_claude_md):
        print("[Info] CLAUDE.md found")
        return True

    print("[Warn] CLAUDE.md not found, initializing...")

    try:
        result = subprocess.run(
            'claude init',
            capture_output=True,
            text=True,
            shell=True,
            cwd=src_dir,
            timeout=120
        )
        if result.returncode == 0:
            print("[Info] CLAUDE.md generated")
            return True
        else:
            print(f"[Warn] Init failed: {result.stderr}")
            return True
    except subprocess.TimeoutExpired:
        print("[Warn] Init timed out")
        return True
    except Exception as e:
        print(f"[Warn] Init error: {e}")
        return True


def run_claude(prompt: str, cwd: str = None, timeout: int = 600) -> str:
    """Invoke Claude CLI to execute command"""
    logger = get_logger()
    logger.info("Claude executing...")

    env = os.environ.copy()
    if sys.platform == 'win32' and 'CLAUDE_CODE_GIT_BASH_PATH' not in env:
        try:
            result = subprocess.run('where bash', capture_output=True, text=True, shell=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    path = line.strip()
                    if 'Git' in path and 'bash.exe' in path:
                        env['CLAUDE_CODE_GIT_BASH_PATH'] = path
                        break
        except (subprocess.TimeoutExpired, Exception):
            pass

    cmd = 'claude -p --dangerously-skip-permissions --verbose --output-format stream-json'
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        shell=True,
        env=env,
        cwd=cwd
    )

    process.stdin.write(prompt)
    process.stdin.close()

    output_lines = []
    spinner_chars = ['.', '..', '...']
    spinner_idx = 0
    dots_printed = 0

    try:
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                logger.claude(line)  # Log to file
                output_lines.append(line)
                # Show progress dots (real-time feedback)
                dots_printed += 1
                if dots_printed % 10 == 0:  # Every 10 lines
                    print('.', end='', flush=True)
                    if dots_printed % 50 == 0:  # Line break every 50 dots
                        print()
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        process.terminate()
        process.wait(timeout=5)
        return "Execution interrupted by user"

    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout after {timeout}s")
        process.terminate()
        process.wait(timeout=5)
        return f"Execution timeout after {timeout} seconds"

    stderr = process.stderr.read()
    if process.returncode != 0:
        logger.error(f"Claude failed: {stderr}")
        return f"Execution failed: {stderr}"

    # Clear progress dots and show completion
    if dots_printed > 0:
        print()  # New line after dots
    logger.info("Claude completed")

    return ''.join(output_lines)


def decompose_requirements(docs_source: str, src_dir: str, push: bool = False, is_single_doc: bool = False) -> None:
    """Let Claude decompose requirements documents and write to tasks.json"""
    # Create task-specific logger for decompose
    looop_dir = get_looop_dir(src_dir)
    init_logger(looop_dir, task_id=0, task_name="Decompose")
    logger = get_logger()

    today = str(__import__('datetime').datetime.now().date())

    # Handle single doc vs directory
    if is_single_doc:
        if not os.path.isfile(docs_source):
            logger.error(f"Document file not found: {docs_source}")
            close_logger()
            return
        doc_files = [docs_source]
        docs_dir = os.path.dirname(docs_source) or "."
    else:
        if not os.path.exists(docs_source):
            logger.error(f"Docs directory not found: {docs_source}")
            close_logger()
            return
        doc_files = []
        for f in os.listdir(docs_source):
            if f.endswith('.md') or f.endswith('.txt') or f.endswith('.json'):
                doc_files.append(os.path.join(docs_source, f))
        docs_dir = docs_source

    if not doc_files:
        logger.warning(f"No documents found in {docs_source}")
        close_logger()
        return

    ensure_claude_md(src_dir)
    init_looop_dir(src_dir)
    tasks_file = get_tasks_file(src_dir)

    doc_list = "\n".join(f'"{f}"' for f in doc_files)

    git_cmds = f'- git add "{tasks_file}"\n   - git commit -m "<decide commit message based on task decomposition>"'
    if push:
        git_cmds += "\n   - git push"

    # Build JSON example string with detailed fields
    json_example = f''' {{
  "project": "Project name",
  "created_at": "{today}",
  "docs_dir": "{docs_dir}",
  "src_dir": "{src_dir}",
  "requirements_docs": ["{docs_dir}/xxx.md"],
  "tasks": [
    {{
      "id": 1,
      "name": "Task name (concise, imperative, e.g. 'Create user model')",
      "description": "Detailed technical description including: what to build, specific files to create/modify, key implementation points",
      "priority": "high|medium|low",
      "dependencies": [],
      "task_type": "setup|core|feature|refactor|test|docs",
      "estimated_files": ["expected_file_path_1", "expected_file_path_2"],
      "acceptance_criteria": ["Specific verifiable criteria 1", "Criteria 2"],
      "status": "pending",
      "result": null,
      "issues": [],
      "completed_at": null
    }}
  ]
}}'''

    prompt = f"""You are an expert project manager and technical architect. Analyze all requirements documents in the "{docs_dir}" directory and decompose them into a detailed, executable development task list.

Requirements document paths:
{doc_list}

Code storage directory: "{src_dir}"
Task file storage path: "{tasks_file}"

## Task Decomposition Guidelines

### 1. Granularity Principle
- Each task should be completable in 1-3 Claude sessions (typically 1-3 hours of meaningful work)
- Target: 3-15 tasks for a typical project, NOT 30+ tiny tasks
- **Anti-patterns to avoid:**
  - "Create file X" - too narrow, just a file operation
  - "Write function Y" - too narrow, should be part of a module task
  - "Add validation for field Z" - too narrow, validation belongs to the feature task
  - "Setup dependency A" - too narrow, combine all setup into ONE setup task
- **Good granularity examples:**
  - "Implement user authentication module" (includes: model, routes, validation, session handling)
  - "Build data processing pipeline" (includes: input parsing, transformation, output formatting)
  - "Create REST API for resource X" (includes: endpoints, validation, error handling, basic docs)
  - "Setup project infrastructure" (includes: config, dependencies, folder structure, basic scaffolding)

### 2. Task Consolidation Rules (IMPORTANT)
Before splitting a task, ask: "Can this be part of a larger related task?"

**Combine when:**
- Multiple tasks share the same file/module → merge into ONE module task
- Sequential tiny tasks (A→B→C) with no branching → merge into ONE pipeline task
- Setup tasks < 5 files → merge into ONE setup task
- Related features used together → merge into ONE feature module task

**Split only when:**
- Truly independent components with NO shared files
- Parallel work paths (different developers could work simultaneously)
- Large feature that genuinely needs 3+ hours AND has clear sub-components

### 3. Task Breakdown Strategy (Layer Guidelines)
Each layer typically produces ONE consolidated task, NOT multiple tiny tasks:

**Layer A - Setup & Infrastructure (ONE task):**
- Combine: project init + config + dependencies + folder structure + database setup
- Example: "Setup project infrastructure" covers ALL setup in ONE task

**Layer B - Core Data & Models (ONE task per major domain):**
- Combine all models/schemas for a domain into ONE task
- Example: "Create data models for user and order domain" (NOT separate tasks per model)

**Layer C - API/Interface Layer (ONE task per resource):**
- Combine: all endpoints + validation + error handling for ONE resource
- Example: "Build REST API for user resource" (NOT separate tasks per endpoint)

**Layer D - Features & Business Logic (ONE task per feature module):**
- Combine related feature components into ONE cohesive task
- Example: "Implement user authentication feature" (includes: login, logout, session, validation)

**Layer E - Integration & Utilities (ONE task or merge into Layer D):**
- Combine helpers/services into ONE task, or merge into related feature tasks
- Example: "Add utility helpers and middleware" (NOT separate tasks per helper function)

**Layer F - Testing & Documentation (ONE task at END):**
- ONE unified test task covering all features, NO per-feature tests

### 3. Test Task Consolidation Rule (IMPORTANT)
- DO NOT create test tasks for individual features (e.g., "Test user model", "Test login API")
- Create ONE comprehensive test task at the end with dependencies on ALL feature tasks
- Example: "Write comprehensive tests for all completed features" (depends on all core/feature task IDs)
- This ensures faster development iteration and unified test coverage verification

### 3. Dependency Analysis
- Identify hard dependencies (must complete before another task)
- Order tasks so foundational work comes first
- Mark dependencies clearly - use task IDs from earlier tasks

### 4. Priority Assignment Rules
- **high**: Core functionality, blocking other tasks, setup essentials
- **medium**: Important features, can be delayed briefly
- **low**: Nice-to-have, polish, documentation, optional enhancements

### 5. Description Quality Requirements
Each task description must include:
- **What**: Specific deliverable (file names, function names, components)
- **How**: Key implementation approach, technology choices
- **Why**: Connection to requirements (which requirement this addresses)
- **Scope**: Clear boundaries - what's included and excluded

### 6. File Prediction
- List expected files to be created/modified
- Use realistic paths matching project structure
- If uncertain, use descriptive placeholders like "src/models/user.py"

### 7. Acceptance Criteria
Each task must have 1-3 specific, verifiable acceptance criteria:
- Example: "User can register with valid email" (not: "Registration works")
- Example: "API returns 200 for valid requests" (not: "API is functional")
- Example: "Tests pass with >80% coverage" (not: "Tests are written")

## Execution Steps

1. Read and deeply analyze all requirements document content
2. Identify all major features and components mentioned
3. Apply decomposition layers to create fine-grained tasks
4. Set logical dependencies following the layer order
5. Assign priorities based on criticality and dependency position
6. Write detailed descriptions with technical specifics
7. Predict files and define acceptance criteria for each task
8. Save the complete task list to "{tasks_file}" in JSON format:

{json_example}

## Output Requirements

After completing, provide a summary:
- Total tasks created
- Tasks by type (setup, core, feature, test, etc.)
- Tasks by priority (high/medium/low)
- Dependency chain overview
- Estimated project scope and complexity assessment
"""

    run_claude(prompt, cwd=src_dir)
    close_logger()


def decompose_requirement_text(requirement_text: str, src_dir: str, push: bool = False) -> None:
    """Let Claude decompose a requirement text string and write to tasks.json"""
    looop_dir = get_looop_dir(src_dir)
    init_logger(looop_dir, task_id=0, task_name="Decompose")
    logger = get_logger()

    today = str(__import__('datetime').datetime.now().date())

    ensure_claude_md(src_dir)
    init_looop_dir(src_dir)
    tasks_file = get_tasks_file(src_dir)

    git_cmds = f'- git add "{tasks_file}"\n   - git commit -m "<decide commit message based on task decomposition>"'
    if push:
        git_cmds += "\n   - git push"

    # Build JSON example string with detailed fields
    json_example = f''' {{
  "project": "Project name",
  "created_at": "{today}",
  "docs_dir": null,
  "src_dir": "{src_dir}",
  "requirements_text": "Original requirement text",
  "tasks": [
    {{
      "id": 1,
      "name": "Task name (concise, imperative, e.g. 'Create user model')",
      "description": "Detailed technical description including: what to build, specific files to create/modify, key implementation points",
      "priority": "high|medium|low",
      "dependencies": [],
      "task_type": "setup|core|feature|refactor|test|docs",
      "estimated_files": ["expected_file_path_1", "expected_file_path_2"],
      "acceptance_criteria": ["Specific verifiable criteria 1", "Criteria 2"],
      "status": "pending",
      "result": null,
      "issues": [],
      "completed_at": null
    }}
  ]
}}'''

    prompt = f"""You are an expert project manager and technical architect. Analyze the following requirement and decompose it into a detailed, executable development task list.

Requirement:
{requirement_text}

Code storage directory: "{src_dir}"
Task file storage path: "{tasks_file}"

## Task Decomposition Guidelines

### 1. Granularity Principle
- Each task should be completable in 1-3 Claude sessions (typically 1-3 hours of meaningful work)
- Target: 3-15 tasks for a typical project, NOT 30+ tiny tasks
- **Anti-patterns to avoid:**
  - "Create file X" - too narrow, just a file operation
  - "Write function Y" - too narrow, should be part of a module task
  - "Add validation for field Z" - too narrow, validation belongs to the feature task
  - "Setup dependency A" - too narrow, combine all setup into ONE setup task
- **Good granularity examples:**
  - "Implement user authentication module" (includes: model, routes, validation, session handling)
  - "Build data processing pipeline" (includes: input parsing, transformation, output formatting)
  - "Create REST API for resource X" (includes: endpoints, validation, error handling, basic docs)
  - "Setup project infrastructure" (includes: config, dependencies, folder structure, basic scaffolding)

### 2. Task Consolidation Rules (IMPORTANT)
Before splitting a task, ask: "Can this be part of a larger related task?"

**Combine when:**
- Multiple tasks share the same file/module → merge into ONE module task
- Sequential tiny tasks (A→B→C) with no branching → merge into ONE pipeline task
- Setup tasks < 5 files → merge into ONE setup task
- Related features used together → merge into ONE feature module task

**Split only when:**
- Truly independent components with NO shared files
- Parallel work paths (different developers could work simultaneously)
- Large feature that genuinely needs 3+ hours AND has clear sub-components

### 3. Task Breakdown Strategy (Layer Guidelines)
Each layer typically produces ONE consolidated task, NOT multiple tiny tasks:

**Layer A - Setup & Infrastructure (ONE task):**
- Combine: project init + config + dependencies + folder structure + database setup
- Example: "Setup project infrastructure" covers ALL setup in ONE task

**Layer B - Core Data & Models (ONE task per major domain):**
- Combine all models/schemas for a domain into ONE task
- Example: "Create data models for user and order domain" (NOT separate tasks per model)

**Layer C - API/Interface Layer (ONE task per resource):**
- Combine: all endpoints + validation + error handling for ONE resource
- Example: "Build REST API for user resource" (NOT separate tasks per endpoint)

**Layer D - Features & Business Logic (ONE task per feature module):**
- Combine related feature components into ONE cohesive task
- Example: "Implement user authentication feature" (includes: login, logout, session, validation)

**Layer E - Integration & Utilities (ONE task or merge into Layer D):**
- Combine helpers/services into ONE task, or merge into related feature tasks
- Example: "Add utility helpers and middleware" (NOT separate tasks per helper function)

**Layer F - Testing & Documentation (ONE task at END):**
- ONE unified test task covering all features, NO per-feature tests

### 3. Test Task Consolidation Rule (IMPORTANT)
- DO NOT create test tasks for individual features (e.g., "Test user model", "Test login API")
- Create ONE comprehensive test task at the end with dependencies on ALL feature tasks
- Example: "Write comprehensive tests for all completed features" (depends on all core/feature task IDs)
- This ensures faster development iteration and unified test coverage verification

### 3. Dependency Analysis
- Identify hard dependencies (must complete before another task)
- Order tasks so foundational work comes first
- Mark dependencies clearly - use task IDs from earlier tasks

### 4. Priority Assignment Rules
- **high**: Core functionality, blocking other tasks, setup essentials
- **medium**: Important features, can be delayed briefly
- **low**: Nice-to-have, polish, documentation, optional enhancements

### 5. Description Quality Requirements
Each task description must include:
- **What**: Specific deliverable (file names, function names, components)
- **How**: Key implementation approach, technology choices
- **Why**: Connection to requirements (which requirement this addresses)
- **Scope**: Clear boundaries - what's included and excluded

### 6. File Prediction
- List expected files to be created/modified
- Use realistic paths matching project structure
- If uncertain, use descriptive placeholders like "src/models/user.py"

### 7. Acceptance Criteria
Each task must have 1-3 specific, verifiable acceptance criteria:
- Example: "User can register with valid email" (not: "Registration works")
- Example: "API returns 200 for valid requests" (not: "API is functional")
- Example: "Tests pass with >80% coverage" (not: "Tests are written")

## Execution Steps

1. Deeply analyze the requirement text
2. Identify all major features and components implied
3. Apply decomposition layers to create fine-grained tasks
4. Set logical dependencies following the layer order
5. Assign priorities based on criticality and dependency position
6. Write detailed descriptions with technical specifics
7. Predict files and define acceptance criteria for each task
8. Save the complete task list to "{tasks_file}" in JSON format:

{json_example}

## Output Requirements

After completing, provide a summary:
- Total tasks created
- Tasks by type (setup, core, feature, test, etc.)
- Tasks by priority (high/medium/low)
- Dependency chain overview
- Estimated project scope and complexity assessment
"""

    run_claude(prompt, cwd=src_dir)
    close_logger()


def main():
    parser = argparse.ArgumentParser(description="Claude Automated Development Toolkit")
    parser.add_argument("--docs", "-D", metavar="DIR",
                        help="Requirements document directory path")
    parser.add_argument("--doc", metavar="FILE",
                        help="Single requirements document file path")
    parser.add_argument("--requirement", "-r", metavar="TEXT",
                        help="Direct requirement text string")
    parser.add_argument("--src", "-S", required=True, metavar="DIR",
                        help="Code storage directory path")
    parser.add_argument("--decompose", "-d", action="store_true",
                        help="Decompose requirements documents")
    parser.add_argument("--status", "-s", action="store_true",
                        help="Show current task status")
    parser.add_argument("--mark-manual", "-M", type=int, metavar="ID",
                        help="Mark task as needing manual intervention")
    parser.add_argument("--list-manual", "-L", action="store_true",
                        help="List tasks needing manual intervention")
    parser.add_argument("--resolve-manual", "-R", type=int, metavar="ID",
                        help="Restore task from manual intervention")
    parser.add_argument("--max-tasks", "-m", type=int, default=0,
                        help="Maximum tasks to execute (0 = unlimited)")
    parser.add_argument("--push", "-P", action="store_true",
                        help="Git push after task completion")
    args = parser.parse_args()

    # Initialize directories
    init_looop_dir(args.src)
    looop_dir = get_looop_dir(args.src)
    tasks_file = get_tasks_file(args.src)
    progress_file = get_progress_file(args.src)

    # === Non-task operations: direct console output, no log file ===

    # Status mode
    if args.status:
        data = load_tasks(tasks_file)
        summary = get_task_summary(data)
        print("=" * 60)
        print(f"Project: {data.get('project', 'Unnamed')}")
        print(f"Requirements: {data.get('docs_dir', 'N/A')}")
        print(f"Source: {data.get('src_dir', args.src)}")
        print()
        print(f"Total: {summary['total']} | Done: {summary['completed']} | "
              f"Pending: {summary['pending']} | Manual: {summary['needs_manual']}")
        print("=" * 60)
        return

    # Mark manual
    if args.mark_manual:
        data = load_tasks(tasks_file)
        if mark_task_manual(data, args.mark_manual, "User marked", tasks_file):
            print(f"[Done] Task #{args.mark_manual} marked for manual intervention")
        else:
            print(f"[Warn] Task #{args.mark_manual} not found")
        return

    # List manual
    if args.list_manual:
        data = load_tasks(tasks_file)
        manual_tasks = [t for t in data["tasks"] if t["status"] == STATUS_NEEDS_MANUAL]
        if not manual_tasks:
            print("[Info] No tasks need manual intervention")
        else:
            print("[Info] Tasks needing manual intervention:")
            for t in manual_tasks:
                print(f"  #{t['id']}: {t['name']}")
        return

    # Resolve manual
    if args.resolve_manual:
        data = load_tasks(tasks_file)
        for t in data["tasks"]:
            if t["id"] == args.resolve_manual:
                t["status"] = STATUS_PENDING
                if "manual_reason" in t:
                    del t["manual_reason"]
                save_tasks(data, tasks_file)
                print(f"[Done] Task #{args.resolve_manual} restored to pending")
                return
        print(f"[Warn] Task #{args.resolve_manual} not found")
        return

    # === Task execution operations: create log file ===

    # Check Claude CLI
    if not check_claude_installed():
        print("[Error] Claude CLI not installed")
        print("[Info] Install: https://claude.ai/code")
        return

    # Decompose mode
    if args.decompose:
        # Check which source is provided
        sources_provided = sum(1 for x in [args.docs, args.doc, args.requirement] if x)
        if sources_provided == 0:
            print("[Error] --docs, --doc, or --requirement required for decomposition")
            return
        if sources_provided > 1:
            print("[Error] Only one of --docs, --doc, or --requirement can be used")
            return

        if args.requirement:
            # Direct requirement text mode
            decompose_requirement_text(args.requirement, args.src, args.push)
        elif args.doc:
            # Single document mode
            if not os.path.isfile(args.doc):
                print(f"[Error] Document file not found: {args.doc}")
                return
            decompose_requirements(args.doc, args.src, args.push, is_single_doc=True)
        else:
            # Directory mode
            if not os.path.exists(args.docs):
                print(f"[Error] Docs directory not found: {args.docs}")
                return
            decompose_requirements(args.docs, args.src, args.push, is_single_doc=False)
        return

    # Main execution loop
    if not os.path.exists(tasks_file):
        print(f"[Error] Task file not found: {tasks_file}")
        print("[Info] Run --decompose first")
        return

    data = load_tasks(tasks_file)
    if not data.get("tasks"):
        print("[Warn] No tasks. Run --decompose first")
        return

    ensure_claude_md(args.src)

    summary = get_task_summary(data)
    total = summary['total']
    print(f"[Info] Starting: {total} tasks")
    print()

    task_count = 0
    try:
        while True:
            data = load_tasks(tasks_file)
            task = get_next_task(data)
            summary = get_task_summary(data)

            if task is None:
                print(
                    f"[=====>          ] {summary['completed']}/{total} ({int(summary['completed'] / total * 100 if total > 0 else 0)}%)")
                if summary["pending"] > 0:
                    print("[Warn] Pending tasks blocked by dependencies")
                elif summary["needs_manual"] > 0:
                    print(f"[Warn] {summary['needs_manual']} tasks need manual intervention")
                else:
                    print("[Info] All tasks completed!")
                break

            if args.max_tasks > 0 and task_count >= args.max_tasks:
                print(f"[Info] Max limit reached: {args.max_tasks}")
                break

            task_count += 1

            # Create task-specific logger
            init_logger(looop_dir, task['id'], task['name'])
            logger = get_logger()

            logger.progress(summary['completed'], total, task['name'])
            logger.task_start(task['id'], task['name'], task.get('priority', 'medium'))

            update_task_status(data, task["id"], "in_progress", tasks_file=tasks_file)

            # Build context hint for progress file
            context_hint = ""
            if os.path.exists(progress_file):
                context_hint = f'\nProgress file: "{progress_file}"'

            # Build context from previous completed tasks
            completed_context = ""
            if os.path.exists(progress_file):
                with open(progress_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Get last 50 lines for context
                    recent_progress = ''.join(lines[-50:]) if len(lines) > 50 else ''.join(lines)
                    if recent_progress.strip():
                        completed_context = f'\n\n## Recent Progress (Last Completed Tasks)\n```\n{recent_progress.strip()}\n```'

            # Build acceptance criteria section
            acceptance_section = ""
            if task.get('acceptance_criteria'):
                criteria_list = '\n'.join(f'- {c}' for c in task['acceptance_criteria'])
                acceptance_section = f'\n\n## Acceptance Criteria\nVerify these criteria before marking complete:\n{criteria_list}'

            # Build estimated files section
            files_section = ""
            if task.get('estimated_files'):
                files_list = '\n'.join(f'- {f}' for f in task['estimated_files'])
                files_section = f'\n\n## Expected Files\nFocus on these files:\n{files_list}'

            now = __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            git_cmds = '- git add all\n- git commit -m "<decide commit message based on task content>"'
            if args.push:
                git_cmds += "\n- git push"

            prompt = f"""Execute this development task with high quality and completeness.

## Task Information

**Task #{task['id']}: {task['name']}**
- **Type**: {task.get('task_type', 'feature')}
- **Priority**: {task.get('priority', 'medium')}
- **Description**: {task.get('description', 'None')}{files_section}{acceptance_section}

## Working Directory
Target: "{args.src}/"{context_hint}{completed_context}

## Execution Guidelines

### 1. Before Coding
- Review the task description and acceptance criteria carefully
- Check progress file for related completed work (patterns, conventions)
- Plan your implementation approach

### 2. During Coding
- Follow existing project conventions and patterns
- Use appropriate technology stack for the task type
- Write clean, maintainable code with proper naming
- Include necessary error handling
- Keep functions focused and modular

### 3. File Organization
- Create files in "{args.src}/" directory
- Use logical folder structure (models, controllers, services, utils, etc.)
- Name files descriptively following project conventions

### 4. Testing Strategy (CRITICAL)
{f'''- This is a TEST task: Write comprehensive tests for ALL completed features
- Test coverage should verify functionality from previous tasks
- Include unit tests, integration tests, edge cases, and error handling tests''' if task.get('task_type') == 'test' else f'''- This is NOT a test task: DO NOT write tests during this task
- Focus ONLY on implementing the core functionality described above
- Testing will be handled in a separate unified testing phase at the end
- Skip any "write tests" requirements in acceptance criteria - they will be deferred'''}

### 5. Verification
{f'''- Run all tests to ensure they pass
- Verify test coverage meets requirements''' if task.get('task_type') == 'test' else f'''- Verify basic functionality works (manual smoke test if needed)
- DO NOT write automated tests - just ensure code is functional
- Check for obvious errors or missing implementations'''}

### 6. Completion Documentation
Append summary to "{progress_file}":

```
========================================
Task #{task['id']}: {task['name']}
Time: {now}
Status: completed or needs_manual
----------------------------------------
Done:
- [List specific files created/modified]
- [Key implementation decisions]
{f'- [Test coverage summary]' if task.get('task_type') == 'test' else '- [Tests deferred to unified testing phase]'}
----------------------------------------
Issues:
- [None or specific blockers encountered]
----------------------------------------
Manual reason:
- [None or why needs manual intervention]
========================================
```

### 7. Git Operations (if completed successfully)
{git_cmds}

### 8. Status Reporting
End your output with:
---STATUS---
completed or needs_manual
---END---

## Important Notes

- If blocked by external dependencies, API keys, or decisions requiring human input: mark needs_manual with clear reason
- If partially complete but blocked: document what was done and what remains
- If fully complete: ensure core functionality works before marking completed
"""

            output = run_claude(prompt, cwd=args.src)

            final_status = STATUS_COMPLETED
            try:
                if "---STATUS---" in output and "---END---" in output:
                    status_part = output.split("---STATUS---", 1)[1]
                    if "---END---" in status_part:
                        val = status_part.split("---END---", 1)[0].strip().lower()
                        if val in ("needs_manual", "needs manual"):
                            final_status = STATUS_NEEDS_MANUAL
                elif "Execution failed" in output or "Execution timeout" in output:
                    final_status = STATUS_NEEDS_MANUAL
            except Exception:
                final_status = STATUS_NEEDS_MANUAL

            data = load_tasks(tasks_file)
            if final_status == STATUS_NEEDS_MANUAL:
                mark_task_manual(data, task["id"], f"See {progress_file}", tasks_file)
                logger.task_end(task['id'], task['name'], "needs_manual")
                logger.info(f"See {progress_file}")
            else:
                update_task_status(data, task["id"], STATUS_COMPLETED, tasks_file=tasks_file)
                logger.task_end(task['id'], task['name'], "completed")

            close_logger()

    except KeyboardInterrupt:
        print("[Warn] Interrupted")


if __name__ == "__main__":
    main()