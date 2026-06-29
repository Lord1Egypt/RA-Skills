---
name: init-program
description: Create or update the correct agent instruction file for the active coding assistant, then initialize a software project according to that file. Use when the user asks to initialize a new or existing repository, bootstrap project structure, create agent instructions, set coding rules, generate setup commands, choose between AGENTS.md and Claude Code instruction files, or align implementation work with an agent instruction contract before coding.
---

# Init Program

## Overview

Create the appropriate agent instruction file first, then use it as the project contract for initialization. Select the file by the active model or coding assistant, and treat that file as the source of truth for communication rules, coding conventions, project structure, setup commands, validation steps, code review expectations, and delivery requirements.

## Workflow

1. Inspect the workspace before writing files.
   - Read existing `AGENTS.md`, `README`, package manifests, build files, framework config, and directory structure.
   - Identify the project type, language, framework, package manager, test runner, and likely entry points.
   - Preserve user changes and avoid unrelated cleanup.

2. Choose the instruction file.
   - For Codex/OpenAI coding agents, create or update `AGENTS.md`.
   - For Claude Code, create or update the Claude Code instruction file used by that project, typically `CLAUDE.md`.
   - If the active assistant or expected instruction filename is unclear, ask before creating files.
   - If the repository already has an instruction file for the active assistant, update that file instead of creating a competing one.

3. Confirm the instruction language.
   - Ask the user which language to use for the generated instruction file before writing it.
   - Offer the user's current conversation language as the default when appropriate.
   - If the repository already has an instruction file, preserve its existing language unless the user asks to change it.

4. Create or update the instruction file.
   - If the selected file is missing, create it at the repository root unless the project already documents another location.
   - If it exists, update only the parts needed for project initialization.
   - Write concise, actionable instructions that future agents can follow without extra context.
   - Include concrete commands only after confirming they match the detected toolchain.
   - Require confirmation before proceeding on unclear or underspecified work, such as choosing a technology stack, runtime, database, package manager, deployment target, authentication method, or generated-file source.
   - Require the generated instruction file to tell future agents to ask the user to choose the technology stack before initializing a project when the stack is not already specified.

5. Initialize according to the selected instruction file.
   - Create the minimum project files and directories required by the requested stack.
   - Configure package/build/test tooling using the repository's existing conventions when present.
   - Add basic source, config, environment example, and validation files only when they are part of the requested initialization.
   - Avoid speculative features, unrelated refactors, or broad formatting passes.

6. Validate the initialized project.
   - Run the narrowest meaningful command first, such as dependency check, compile, lint, or focused tests.
   - If initialization changes shared contracts or generated code, run broader validation when feasible.
   - If a command fails because dependencies are missing or network access is blocked, report the exact command and reason.

7. Deliver a concise handoff.
   - Summarize the instruction-file contract, initialized files, validation commands, and any known gaps.
   - Mention unresolved assumptions only when they affect how the project should be used next.

8. Include code review rules in the instruction file.
   - Define how agents should review code before or after implementation.
   - Prioritize defects, regressions, security issues, maintainability risks, and missing validation.
   - Require findings to include file and line references when possible.

## Instruction File Selection

- Use `AGENTS.md` for Codex/OpenAI agents.
- Use `CLAUDE.md` for Claude Code unless the repository already uses a different Claude Code instruction path.
- If the user explicitly requests a filename, use that filename after confirming it matches their intended assistant.
- Do not create both `AGENTS.md` and `CLAUDE.md` unless the user explicitly wants multi-agent instructions.

## Language Selection

- Before creating a new instruction file, ask which language to use.
- Present the current conversation language as the default suggestion when it is suitable.
- For existing instruction files, keep the existing language unless the user explicitly requests another language.
- After the user chooses a language, write the instruction file in that language except for programming identifiers, commands, config keys, API names, and error text.

## Instruction File Template

Use this shape unless the existing repository clearly needs another structure:

```markdown
# AGENTS

## Communication

1. State conclusions first, then impact and next actions.
2. Use the user's preferred language unless project conventions require otherwise.
3. Keep delivery notes focused on changed files, validation, and risks.
4. Ask for confirmation before acting on unclear requirements or irreversible choices.
5. Before creating or rewriting this instruction file, ask the user which language it should use.

## Project Structure

1. Describe the main directories and ownership boundaries.
2. Identify generated files and their source commands.
3. Keep common logic in the appropriate shared package/module.

## Coding Rules

1. Follow existing naming, layering, error handling, and formatting conventions.
2. Keep changes scoped to the requested task.
3. Do not overwrite unrelated user changes.

## Setup

1. List install commands.
2. List required environment variables or `.env.example` fields.
3. List local run commands.
4. Require confirmation before choosing an unspecified technology stack, package manager, database, runtime, deployment target, or external service.
5. When initializing a project and the technology stack is not already specified, ask the user to choose the stack before creating project files.

## Validation

1. List focused checks for typical changes.
2. List broader checks for shared behavior or release work.
3. Require clear reporting when checks cannot run.

## Code Review

1. Review changes for correctness, regressions, security, maintainability, and test coverage.
2. Lead with findings ordered by severity, using file and line references when possible.
3. Keep summaries secondary to concrete issues; state clearly when no issues are found.
4. Call out unverified behavior, missing tests, or assumptions that affect release risk.
```

## Initialization Rules

- Prefer the detected package manager lockfile over choosing a new package manager.
- Prefer framework generators or official scaffolding only when they match the user's requested stack and can run safely in the workspace.
- If adding an HTTP API in a generated framework, update the source definition first, run the generator, then implement business logic.
- If the project has generated files, do not hand-edit generated output when a source schema or generator command exists.
- Keep secrets out of committed files; create `.env.example` with placeholder values when environment configuration is needed.
- Start a dev server only when the user needs to try a frontend/app and the project expects a server.
- Include code review expectations in the selected instruction file for every initialized project, even if the project has no review tooling yet.
- Ask the user which language to use before generating a new instruction file.
- Ensure the generated instruction file requires user choice of technology stack before project initialization when the stack is not already known.

## When Details Are Missing

- Make conservative assumptions from repository context when low risk.
- Ask one direct question when the instruction-file language, active assistant, instruction filename, technology stack, target runtime, database, package manager, deployment target, destructive action, or generated-file source cannot be inferred safely.
- If the user asks for a specific stack, use that stack even if the directory is otherwise empty.
