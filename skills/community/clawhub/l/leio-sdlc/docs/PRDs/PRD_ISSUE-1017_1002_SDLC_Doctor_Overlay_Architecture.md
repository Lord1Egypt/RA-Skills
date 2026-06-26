---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1017_1002_SDLC_Doctor_Overlay_Architecture

## 1. Context & Problem (业务背景与核心痛点)
Currently, configuring a project for LEIO SDLC requires manual setup of infrastructure files (preflight.sh, STATE.md, .gitignore rules, Git hooks). Missing any of these causes pipeline crashes or context leakage (pollution). Hardcoding checks inside the orchestrator causes configuration drift and technical debt, making it difficult to maintain framework-specific rules or extend SDLC to specialized project types (e.g., AgentSkills). A unified project generator ("creator") and boilerplate enforcer is required.

## 2. Requirements & User Stories (需求定义)
- The system must provide a `doctor.py` script to diagnose and automatically fix SDLC compliance for any target project directory.
- The system must use a "Template Overlay" (Manifest-Driven) architecture to manage boilerplate files without hardcoding names or contents in Python scripts.
- Overlays must be strictly modular:
  - `base/`: Universal SDLC requirements (e.g., `.gitignore.append`, `STATE.md`, `preflight.sh`).
  - `optional_hooks/`: Opt-in Git hooks (e.g., `pre-commit` lock to prevent human commits).
  - `profiles/<name>/`: Domain-specific overlays (e.g., `profiles/skill` for OpenClaw AgentSkills, adding `deploy.sh`, `SKILL.md`, `.release_ignore.append`).
- `doctor.py --fix` must be strictly idempotent: running it multiple times safely appends missing rules or skips existing files without destructive overwrites.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
> **[Instruction to Main Agent/Architect]**
- **File System as Single Source of Truth**: Create a `TEMPLATES/scaffold/` directory structure within the `leio-sdlc` project containing the `base`, `optional_hooks`, and `profiles` folders.
- **Doctor Implementation (`scripts/doctor.py`)**:
  - `check_vcs()`: Ensures `.git` exists; initializes and commits an empty baseline (`git commit --allow-empty`) if missing.
  - `apply_overlay(overlay_path)`: Iterates through files in the given template directory.
    - If a file ends with `.append` (e.g., `.gitignore.append`), intelligently merge/append lines avoiding duplicates.
    - Otherwise, copy the file to the target directory if it is missing.
  - Support CLI arguments: `--fix` (apply changes), `--profile <name>` (apply specific profile after base), `--enforce-git-lock` (apply `optional_hooks/pre-commit`).
  - Read-Only Mode (Default/`--check`): Scan the target directory and compare against required templates, outputting warnings/errors without modifying files.
- **Orchestrator Integration**: Remove hardcoded sandbox initialization logic (e.g., writing to `.git/info/exclude`) from `orchestrator.py` and replace it with a pre-flight call to `doctor.py --check` (which will fail fast if not compliant).

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Applying Base Scaffold to Empty Project**
  - **Given** an empty directory
  - **When** the user runs `doctor.py --fix`
  - **Then** Git is initialized with a baseline commit, `STATE.md` and `preflight.sh` are created, and `.gitignore` contains `.sdlc_runs/`.

- **Scenario 2: Applying Skill Profile**
  - **Given** a directory that already has the base scaffold
  - **When** the user runs `doctor.py --fix --profile skill`
  - **Then** `deploy.sh` and `SKILL.md` are created, and `.release_ignore` contains the appended ignore rules.

- **Scenario 3: Enforcing Git Lock**
  - **Given** an SDLC compliant project
  - **When** the user runs `doctor.py --fix --enforce-git-lock`
  - **Then** `.git/hooks/pre-commit` is created and prevents manual `git commit`.

- **Scenario 4: Orchestrator Fail-Fast**
  - **Given** a project missing `.gitignore` rules
  - **When** `orchestrator.py` is started
  - **Then** it immediately exits with a FATAL error instructing the user to run `doctor.py --fix`.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Unit Tests**: Test the `.append` logic to ensure it strictly respects idempotency (does not duplicate lines when run multiple times).
- **E2E Sandbox Tests**: Create a mock directory, run `doctor.py --fix --profile skill --enforce-git-lock`, and assert all overlay files (base + skill + hooks) are perfectly placed and Git is initialized.
- **Integration**: Verify `orchestrator.py` accurately crashes if the doctor's check mode fails, confirming the dependency inversion.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/doctor.py` (New script)
- `scripts/orchestrator.py` (Remove hardcoded init logic, add doctor check)
- `TEMPLATES/scaffold/*` (New template structures)

## 7. Hardcoded Content (硬编码内容)
### Exact Text Replacements:
- **`doctor_fail_message`**:
```text
[FATAL] Project is not SDLC compliant. Please run "python3 ~/.openclaw/skills/leio-sdlc/scripts/doctor.py --fix" to apply the required infrastructure.
```