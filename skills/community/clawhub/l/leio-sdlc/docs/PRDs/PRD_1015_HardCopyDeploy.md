Status: Closed

# PRD-1015: Replace Symlink-based Deploy with Hard Copy for AgentSkills

## 1. Problem Statement
The current blue/green deployment strategy used in `deploy.sh` relies on symlinks pointing from the `~/.openclaw/skills/<skill_name>` directory to the release directory `~/.openclaw/.releases/<skill_name>/<timestamp>`. 
OpenClaw's security policy strictly prohibits symlinks that resolve outside the configured sandbox root to prevent path traversal vulnerabilities. As a result, newly deployed AgentSkills (e.g., `leio-sdlc`, `pm-skill`, `ams`) are rejected by the OpenClaw Gateway with the error: `[skills] Skipping skill path that resolves outside its configured root.`. This causes recent updates to disappear from the runtime environment after a deployment.

## 2. Solution Overview
Refactor the deployment logic for AgentSkills to strictly use **Hard Copy (Physical Sync) with Atomic Renaming**, eliminating all cross-directory symlinks. The scripts must handle both deployment (`deploy.sh`) and rollback (`rollback.sh`).

### Deployment Flow (`deploy.sh`)
1. **Backup Existing**: Compress the current running directory (`~/.openclaw/skills/<skill_name>`) into a `.tar.gz` and save it to the release history (`~/.openclaw/.releases/<skill_name>/backup_<timestamp>.tar.gz`).
2. **Stage New Code**: Copy the new release into a physical temporary directory inside the sandbox (e.g., `~/.openclaw/skills/.tmp_<skill_name>`).
3. **Atomic Swap**: Use an atomic `mv -T` command to instantly swap `.tmp_<skill_name>` to `<skill_name>`.
4. **Reload**: Restart the OpenClaw Gateway.

### Rollback Flow (`rollback.sh`)
1. **Find Backup**: Locate the most recent `.tar.gz` backup in `~/.openclaw/.releases/<skill_name>/`.
2. **Restore**: Extract the backup directly over `~/.openclaw/skills/<skill_name>` (after clearing the broken directory).
3. **Reload**: Restart the OpenClaw Gateway.

## 3. Scope Locking
**Target Repository Directory**: `/root/.openclaw/workspace/projects/leio-sdlc`

**Files to Modify/Create:**
- `/root/.openclaw/workspace/TEMPLATES/AgentSkill_Archetype/deploy.sh`
- `/root/.openclaw/workspace/TEMPLATES/AgentSkill_Archetype/rollback.sh` (Create if missing)
- `/root/.openclaw/workspace/projects/leio-sdlc/skills/pm-skill/deploy.sh`
- `/root/.openclaw/workspace/projects/leio-sdlc/skills/issue_tracker/deploy.sh`
- `/root/.openclaw/workspace/projects/leio-sdlc/deploy.sh`

*(Note: Ensure all sub-projects' deploy scripts mimic the archetype).*

## 4. Autonomous Test Strategy
**Test Type**: Bash Script Integration Testing with Mock Environment.

Create a test script (e.g., `scripts/test_deploy_hardcopy.sh`) that simulates the environment:
1. Define a mock `HOME` directory (e.g., `/tmp/mock_home`).
2. Create dummy `skills/<skill_name>` and `.releases/<skill_name>` directories.
3. Run `deploy.sh` with the mock `HOME` exported.
4. **Assert 1**: Check `[ ! -L "/tmp/mock_home/.openclaw/skills/<skill_name>" ]` (Must NOT be a symlink).
5. **Assert 2**: Check `[ -d "/tmp/mock_home/.openclaw/skills/<skill_name>" ]` (Must be a directory).
6. **Assert 3**: Verify a `backup_*.tar.gz` exists in the mock `.releases` directory.
7. Run `rollback.sh` and verify the directory is correctly restored from the tarball.
8. Call this test script from `preflight.sh`.

## 5. TDD Guardrail
**Mandatory Requirement**: The implementation of `deploy.sh`/`rollback.sh` and their failing integration test (`scripts/test_deploy_hardcopy.sh`) MUST be delivered in the same PR contract. Preflight must be green before merging.