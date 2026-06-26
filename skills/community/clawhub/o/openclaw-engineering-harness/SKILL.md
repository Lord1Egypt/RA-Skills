***

name: openclaw-engineering-harness
description: A single skill for engineering workflow loop, responsible for request clarification, code discovery, tool-driven execution, smallest coherent changes, validation, and preparing publishable artifacts.
allowed-tools:

- Read
- LS
- Glob
- Grep
- SearchCodebase
- Edit
- MultiEdit
- Write
- TodoWrite
- AskUserQuestion
- Bash(git status:\*)
- Bash(git diff:\*)
- Bash(git checkout:\*)
- Bash(git add:\*)
- Bash(git commit:\*)
- Bash(git reset:\*)
- Bash(python3:\*)
  when\_to\_use: Use when the task requires a single skill that can clarify scope, inspect a codebase, implement the smallest coherent change, run validation, audit the publishable surface, and summarize delivery evidence.

***

# Engineering Workflow

This Skill combines request clarification, implementation execution, validation closure, runtime assistance, and artifact preparation into a single, independently distributable engineering loop.

## 🚀 How to Use This Skill

As a user, you can invoke this skill in your prompts using the following methods:

**Method 1: Explicitly by Name (Recommended)**
Simply mention the skill name and ask the AI to follow its workflow:

> "Please use the **openclaw-engineering-harness** skill to build \[your task]. Start from the **clarify** phase and confirm the goal and scope with me before proceeding."

**Method 2: Implicitly by Keywords**
Describe your task using the core concepts of this skill, and the AI will automatically trigger it:

> "Help me implement \[your task]. Before starting, please **clarify scope**, ensure you make the **smallest coherent change**, and finally **run validation** and **summarize delivery evidence**."

**Method 3: Enforcing the Phases**
You can command the AI to strictly follow the 5 phases defined in this skill:

> "Execute \[your task] by strictly following these phases: **clarify**, **map**, **implement**, **verify**, and **deliver**. Stop and wait for my approval after each phase."

***

## Always Start Here (For AI Agent)

1. Read `refs/request-shape.md` first to confirm the goal, scope, success criteria, and constraints.
2. Read `refs/capability-model.md` to understand the 3-layer runtime skeleton (tool/state/policy), tool priorities, and state progression rules.
3. Read `refs/execution-loop.md` to proceed in the exact order: discover -> design -> implement -> verify -> deliver.
4. When you need to generate a structured execution plan, run `scripts/run_workflow.py` with `policies/workflow-policy.json`, `tool/tool-config.json`, `state/state-policy.json`, and `policy/constraint-policy.json`.
5. **Memory System**: Read `refs/memory-system.md`. Always check `.claude/MEMORY.md` (if it exists) to learn user preferences and project context before starting. Update it during the deliver phase.
6. When you need to evaluate constraints independently, run `scripts/run_constraints.py` to output rule matches, passes, and blocking conclusions.
7. When preparing publishable artifacts, read `refs/export-policy.md` and `refs/release-checklist.md`, then run `scripts/run_audit.py` with `policies/export-audit-policy.json`.

## Core Workflow

- **Clarify the task shape first**: If the goal, boundary, validation criteria, or memory context are missing, ask or retrieve them first. Never modify code with vague assumptions.
- **Build a minimal working map first**: Entry points, dependencies, impact areas, validation points, and rollback points must come in pairs.
- **Make the smallest coherent change**: Reuse existing patterns. Avoid unrelated refactoring, naming drift, or introducing secondary mechanisms.
- **Verify immediately after changes**: Prioritize running checks that match the impact area. Record passed items, failed items, and uncovered risks.
- **Keep runtime and documentation consistent during delivery**: Verify first, summarize the results, extract new lessons learned to the `.claude/MEMORY.md` system, and only then generate publishable artifacts.

## Output Contract

- **Implementation Plan**: Goal, impact area, change strategy, rollback method.
- **Change Results**: What was done, why it was done, what areas were affected.
- **Validation Record**: What was executed, the results, remaining risks.
- **Distribution Summary**: Export directory, checklist, audit conclusions, and future recommendations.

## Runtime Surface

- `tool/tool-config.json`: Defines tool groups, tools required per phase, and the boundary between single-skill and standard library.
- `state/state-policy.json`: Defines state sequence, phase bindings, and minimum inputs required for each state.
- `policy/constraint-policy.json`: Defines deliverable constraint rules to determine if the 3-layer skeleton still satisfies boundaries.
- `scripts/run_workflow.py`: Reads structured requests, combines tool/state/policy layer results, and generates a minimal execution plan.
- `scripts/run_constraints.py`: Independently executes constraint evaluations, outputting rule matches, passes, and blocks.
- `scripts/run_audit.py`: Scans the target publish directory against audit policies to output matched items and blocking conclusions.
- `policies/workflow-policy.json`: Defines required fields, phase order, phase checkpoints, and default 3-layer configuration entries.
- `policies/export-audit-policy.json`: Defines audit file extensions and blocking patterns to prevent exposing host path signatures, URLs, or proprietary identifiers.

## Hard Boundaries (The Engineering Iron Laws)

- **DO NOT** commit or declare a task as 'done' if the validation (tests or execution) fails. Always return to the implement phase to fix the issue.
- **DO NOT** introduce massive refactoring, unrelated format changes, or new third-party dependencies unless explicitly approved by the user. Keep the PR/diff as small as possible.
- **DO NOT** leave debugging print statements, hardcoded mock data, or temporary comments in the final deliverable.
- **DO NOT** invent custom configurations or patterns if the project already has an established way of doing it (e.g., stick to the existing database ORM or UI component library).

