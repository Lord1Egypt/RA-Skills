---
Affected_Projects: [leio-sdlc, pm-skill, leio-auditor]
---

# PRD: Universal Triad Adaptation & Toolchain Deployment

## 1. Context & Problem Definition (核心问题与前因后果)
Currently, the SDLC ecosystem suffers from **"Agentic Microservices Sprawl"**. We have successfully completed Phase 1 of the migration: physically moving the `pm-skill` and `leio-auditor` source code into the `leio-sdlc/skills/` directory and stripping their independent Git histories to form a cohesive **"Toolchain Monorepo"**.

However, Phase 2 (Code Refactoring & Deployment Pipeline) remains pending. The current issues are:
1. **LLM Driver Coupling:** `leio-auditor` still hardcodes `openclaw agent --message ...` via a Bash script (`prd_auditor.sh`). This prevents running it on environments with pure standalone LLM CLIs (e.g., `gemini` CLI) and exposes it to global prompt pollution ("Clone Identity Crisis").
2. **Production Deployment Crashing (ModuleNotFoundError):** While developing in the Monorepo, skills might try to use relative imports to share `agent_driver.py`. But when deployed to `~/.openclaw/skills/` via hard copy, they become physically isolated folders. A relative import will crash the production environment.

## 2. Requirements (需求说明)
The Orchestrator, PM, and Auditor MUST remain three distinct, independent tools (Triad Consensus Loop). Based on the absolute architectural mandate, the requirements are:

1. **Python Rewrite for Auditor & PM Import Fixes:**
   - Rewrite `skills/leio-auditor/scripts/prd_auditor.sh` into `skills/leio-auditor/scripts/prd_auditor.py`.
   - Ensure the `pm-skill` executable script is physically located at `skills/pm-skill/scripts/pm.py` (migrated from the root `scripts/pm.py`).
   - BOTH `skills/leio-auditor/scripts/prd_auditor.py` and `skills/pm-skill/scripts/pm.py` MUST utilize `leio-sdlc/scripts/agent_driver.py`.
   - Update the Python `sys.path` logic within `pm.py` and `prd_auditor.py` to dynamically resolve the `agent_driver.py` module (development vs. production isolation).

2. **Strict Red Team Prompt Isolation & Dual-Source Prompt Loading:**
   - **DO NOT DELETE `leio-sdlc/config/prompts.json`**. It MUST be retained for the core Orchestrator agents (coder, planner, etc.).
   - Remove the `pm` and `auditor` prompts from the shared `leio-sdlc/config/prompts.json`.
   - The PM prompt MUST reside within its own boundary: `skills/pm-skill/config/prompts.json`.
   - The Auditor's prompt MUST remain strictly isolated in its own physical boundary: `skills/leio-auditor/config/prompts.json`. Both skills will package their respective `config/prompts.json` during deployment in their `deploy.sh` scripts.
   - **Update `agent_driver.py`**: It MUST be modified to support loading the prompt from the skill's local `config/prompts.json` rather than from `SKILL.md` or a hardcoded string.

3. **Preflight CI Fix:**
   - Modify `skills/leio-auditor/preflight.sh` to validate the existence of `.py` instead of `.sh`.

4. **Strict Triad Symmetry & Single-Responsibility Deployment Layout:**
   - `leio-sdlc/deploy.sh` MUST ONLY deploy the `leio-sdlc` skill. It MUST support the `--no-restart` flag.
   - `skills/pm-skill/deploy.sh` MUST ONLY deploy the `pm-skill`. It MUST support the `--no-restart` flag. It must locally package its required dependencies (`agent_driver.py` and its local `skills/pm-skill/config/prompts.json`).
   - `skills/leio-auditor/deploy.sh` MUST ONLY deploy the `leio-auditor` skill. It MUST support the `--no-restart` flag. It must locally package its required dependencies (`agent_driver.py`).
   - **Strict Deployment Layout**: When the `deploy.sh` scripts package their dependencies, they MUST maintain the exact relative directory structures expected by the scripts (e.g., `dist/scripts/agent_driver.py` and `dist/config/prompts.json`) before swapping into the production directory.
   - **Backup Mandate**: Every individual `deploy.sh` script MUST generate a local physical backup archive (e.g., `tar.gz` in an `.old_versions` or `.releases` directory) BEFORE performing the atomic directory swap.

5. **Independent Symmetrical Rollbacks (NO KIT ROLLBACK):**
   - There is no global rollback orchestrator (`kit-rollback.sh`). Each skill (`leio-sdlc`, `pm-skill`, `leio-auditor`) relies ONLY on its own `rollback.sh`.
   - Create `leio-sdlc/rollback.sh`. It restores `leio-sdlc` from its local backup archive. It MUST support `--no-restart`.
   - Create `skills/pm-skill/rollback.sh`. It restores `pm-skill` from its local backup archive. It MUST support `--no-restart`.
   - Create `skills/leio-auditor/rollback.sh`. It restores `leio-auditor` from its local backup archive. It MUST support `--no-restart`.

6. **The Kit Installer (Global Orchestrators):**
   - Create `kit-deploy.sh` at the root. Its ONLY responsibility is to sequentially call `./deploy.sh --no-restart` for `leio-sdlc`, then iterate through `skills/` and call `bash deploy.sh --no-restart` for each sub-skill. Finally, it executes ONE `openclaw gateway restart`.

7. **Fix `SKILL.md` Command Templates**:
   - Update the "Invocation" sections in both `skills/pm-skill/SKILL.md` and `skills/leio-auditor/SKILL.md` to use the global installation paths (e.g., `~/.openclaw/skills/...`) or dynamically resolved paths that work post-deployment.

## 3. Architecture (架构设计)
- **Strict Triad Symmetry:** All three skills (`leio-sdlc`, `pm-skill`, `leio-auditor`) are peers and operate with absolute symmetry. They manage their own deployment and rollback logic physically. There is NO `kit-rollback.sh`.
- **Shared LLM Driver:** Extracts the LLM invocation logic into a shared `agent_driver.py` that can handle multiple CLI drivers (openclaw, gemini). Support is added for dual-source prompt loading.
- **Isolated Deployment & Red Team Isolation:** The deployment script resolves the monorepo-to-production impedance mismatch. Each skill's deploy script locally packages its required dependencies without global cross-contamination. Layout structure inside the distribution package is preserved. Red Team prompts are strictly kept in physical isolation and never merged into shared global JSON files.
- **Kit Global Orchestrators:** Simple root-level orchestrator (`kit-deploy.sh`) loops over the individual independent deployments and executes a single OpenClaw gateway restart at the end.

## 4. Acceptance Criteria (验收标准)
- [ ] `skills/leio-auditor/scripts/prd_auditor.py` replaces the bash script and natively invokes `agent_driver.py`.
- [ ] `skills/pm-skill/scripts/pm.py` properly utilizes `sys.path` logic to resolve `agent_driver.py` independently.
- [ ] `leio-sdlc/config/prompts.json` is retained but PM and Auditor prompts are removed. The PM prompt resides in `skills/pm-skill/config/prompts.json` and Auditor prompt resides in `skills/leio-auditor/config/prompts.json`.
- [ ] `agent_driver.py` successfully loads prompts dynamically from the local `config/prompts.json`.
- [ ] `skills/leio-auditor/preflight.sh` validates `.py` instead of `.sh`.
- [ ] Individual `deploy.sh` files exist for `leio-sdlc`, `pm-skill`, and `leio-auditor` that generate physical backup archives before atomic deployment, and support `--no-restart`.
- [ ] Deployments maintain the exact directory structure of shared files (e.g., `scripts/agent_driver.py`).
- [ ] Individual `rollback.sh` files exist for `leio-sdlc`, `pm-skill`, and `leio-auditor` that restore from backup archives and support `--no-restart`.
- [ ] `kit-deploy.sh` sequentially triggers all `deploy.sh --no-restart` scripts and restarts gateway once.
- [ ] `SKILL.md` templates use global or dynamic paths for invocation.

## 5. Framework Modifications (框架修改声明)
- `skills/leio-auditor/SKILL.md` (modified)
- `skills/pm-skill/SKILL.md` (modified)
- `skills/leio-auditor/scripts/prd_auditor.sh` (deleted)
- `skills/leio-auditor/scripts/prd_auditor.py` (created)
- `skills/pm-skill/scripts/pm.py` (modified)
- `leio-sdlc/config/prompts.json` (modified)
- `skills/pm-skill/config/prompts.json` (created)
- `skills/leio-auditor/config/prompts.json` (created)
- `scripts/agent_driver.py` (modified)
- `skills/leio-auditor/preflight.sh` (modified)
- `leio-sdlc/deploy.sh` (modified/created)
- `skills/pm-skill/deploy.sh` (created)
- `skills/leio-auditor/deploy.sh` (created)
- `leio-sdlc/rollback.sh` (created)
- `skills/pm-skill/rollback.sh` (created)
- `skills/leio-auditor/rollback.sh` (created)
- `kit-deploy.sh` (created)