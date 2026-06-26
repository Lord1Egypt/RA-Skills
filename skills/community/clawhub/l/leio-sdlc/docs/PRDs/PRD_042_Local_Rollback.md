# PRD_042: Local Skill Rollback & Blue/Green Deploy

## 1. Problem Statement
The current `deploy.sh` script executes an "overwrite" deployment, dropping files directly into `~/.openclaw/skills/<slug>/`. A flawed deployment causes immediate, irrecoverable failures to the Gateway and Skill. Rollbacks currently require recompiling or redownloading, which violates the CI/CD principle of Mean Time To Recovery (MTTR) minimization. Furthermore, mixing local deployment artifacts with `clawhub install` packages in the same directory structure creates conflicts.

## 2. Industry Best Practice: Capistrano-Style Symlink Deployment
We will adopt the industry-standard atomic symlink switching model (used by Capistrano, Envoyer, and Kubernetes ConfigMaps). 

**The Fix**: We will store release artifacts in a completely separate, dedicated storage directory outside the runtime path (`~/.openclaw/.releases/<slug>/`), and point the main skill runtime symlink (`~/.openclaw/skills/<slug>`) to the active release. This physically decouples artifact storage from runtime execution and prevents conflicts with `clawhub install`.

## 3. Architecture & Implementation
Update `deploy.sh` and create `scripts/rollback.sh` (both to be mirrored to `TEMPLATES/AgentSkill_Archetype/`).

### 3.1 `deploy.sh` (Blue/Green Deployment)
1. **Migration Safety**: If `~/.openclaw/skills/<slug>` exists and is a *directory* (legacy deployment) rather than a symlink, delete it (`rm -rf`) to make way for the new symlink architecture.
2. **Release Stamping**: Generate a release ID: `RELEASE_ID=$(date +"%Y%m%d_%H%M%S")`.
3. **Artifact Staging**: Copy `dist/` contents to the dedicated release path: `~/.openclaw/.releases/<slug>/$RELEASE_ID/`.
4. **Atomic Swap**: 
   - Create a temporary symlink: `ln -snf "$HOME/.openclaw/.releases/$SLUG/$RELEASE_ID" "$HOME/.openclaw/.releases/$SLUG/current_tmp"`
   - Atomically overwrite the main slug runtime symlink: `mv -T "$HOME/.openclaw/.releases/$SLUG/current_tmp" "$HOME/.openclaw/skills/$SLUG"`
5. **Gateway Reload**: Restart OpenClaw gateway (`openclaw gateway restart`).
6. **Auto-Cleanup (Pruning)**: Keep only the latest 3 releases. `ls -dt ~/.openclaw/.releases/<slug>/* | tail -n +4 | xargs -r rm -rf`.

### 3.2 `scripts/rollback.sh` (Instant Recovery)
1. Detects available releases in `~/.openclaw/.releases/<slug>/` sorted by time.
2. Identifies the *previous* release (the one just before the current symlink target).
3. Atomically swaps the `~/.openclaw/skills/<slug>` symlink back to that previous release.
4. Restarts the Gateway.
5. Fails gracefully if no previous release exists.

## 4. Testing Strategy (TDD)
Create `scripts/test_blue_green_deploy.sh` using an Ephemeral Sandbox (`TEMP_DIR=$(mktemp -d)`).

- **T1: Initial Deployment & Migration**:
  - Mock the OpenClaw skills directory to `$TEMP_DIR/skills`. Mock the releases directory to `$TEMP_DIR/.releases`.
  - Create a dummy *directory* at `$TEMP_DIR/skills/test-skill` to simulate legacy state.
  - Run `deploy.sh`. 
  - **Assert**: Legacy directory is destroyed. `$TEMP_DIR/.releases/test-skill/<timestamp>` exists. `$TEMP_DIR/skills/test-skill` is a symlink pointing to it.
- **T2: Atomic Version Progression**:
  - Sleep 1 second. Run `deploy.sh` again.
  - **Assert**: Two timestamped folders exist. Symlink points to the newer one.
- **T3: Instant Rollback**:
  - Run `scripts/rollback.sh`.
  - **Assert**: Symlink successfully points back to the *older* (first) timestamped directory.
- **T4: Auto-Cleanup Limit (Pruning)**:
  - Run `deploy.sh` 4 more times rapidly.
  - **Assert**: Exactly 3 timestamp folders exist in `$TEMP_DIR/.releases/test-skill/`. The oldest ones were purged.

## 5. Acceptance Criteria
- [ ] `deploy.sh` safely migrates legacy directories to symlinks.
- [ ] Releases are correctly decoupled into `~/.openclaw/.releases/` to prevent ClawHub/Gateway conflicts.
- [ ] `scripts/rollback.sh` achieves sub-second rollback.
- [ ] `test_blue_green_deploy.sh` thoroughly verifies migration, progression, rollback, and pruning.
- [ ] Files are mirrored to `TEMPLATES/AgentSkill_Archetype/` for future projects.