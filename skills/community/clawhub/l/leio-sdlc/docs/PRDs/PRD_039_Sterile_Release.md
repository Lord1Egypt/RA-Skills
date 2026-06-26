# PRD_039: Sterile Release Pipeline (Artifact Packaging)

## 1. Problem Statement
Publishing or deploying the raw workspace directory copies massive test sandboxes, PRDs, local debug logs, and git history into the production environment (or ClawHub registry). This causes a 15-second timeout error during `clawhub publish` due to excessive file volume, and violates the principle of sterile, minimal production artifacts.

This issue is not unique to `leio-sdlc`; it affects all OpenClaw AgentSkills (e.g., AMS). We need a universal packaging standard that any project can adopt with zero code changes, driven by a configuration file.

## 2. Solution: Universal Packager driven by `.release_ignore`

We will abandon project-specific allowlists in favor of a universal, blacklist-driven packaging script utilizing `rsync`.

### 2.1 The Configuration File (`.release_ignore`)
Create a `.release_ignore` file in the project root. This acts exactly like `.npmignore` or `.dockerignore`.
- **Default Contents**:
  ```text
  .git/
  .sdlc/
  docs/
  tests/
  *.log
  *.diff
  .review_count
  memory/
  ```

### 2.2 The Universal Packager (`scripts/build_release.sh`)
Create `scripts/build_release.sh` to act as the universal bundler.
- **Logic**:
  1. Define `DIST_DIR="dist"`.
  2. Clean and recreate the `dist` directory.
  3. Ensure a `.release_ignore` file exists in the project root. If missing, warn but proceed or create a default one.
  4. Use `rsync` to copy everything from the project root (`./`) to `dist/`, strictly excluding files/directories listed in `.release_ignore`.
     - *Command Example*: `rsync -av --exclude-from='.release_ignore' --exclude='dist/' ./ dist/`
  5. The resulting `dist/` directory now contains a sterile, production-ready artifact.

### 2.3 Update Deployment (`deploy.sh`)
Modify the existing `deploy.sh` to hook into this new pipeline.
- **Logic**:
  1. Before syncing files, call `bash scripts/build_release.sh`. Ensure it exits on failure.
  2. Change the deployment source from `"$DEV_DIR"/*` to `"$DEV_DIR/dist/"*`.

### 2.4 Ecosystem Standardization
Once successfully implemented and tested in `leio-sdlc`, copy `build_release.sh`, `deploy.sh` (updated), and `.release_ignore` to `/root/.openclaw/workspace/TEMPLATES/AgentSkill_Archetype/` so future projects (like AMS) inherit this sterile pipeline by default.

## 3. Testing Strategy (TDD)
Create `scripts/test_build_release.sh`.

- **Sandbox Setup**: Create a temporary directory. Inside it:
  - Create a dummy `.release_ignore` containing `tests/` and `docs/`.
  - Create dummy files simulating a dirty workspace: `SKILL.md`, `scripts/main.py`, `docs/PRD.md`, `tests/test.sh`.
- **Execution**: Run `build_release.sh` against this sandbox.
- **Assertions**:
  - `dist/SKILL.md` MUST exist.
  - `dist/scripts/main.py` MUST exist.
  - `dist/docs/` MUST NOT exist.
  - `dist/tests/` MUST NOT exist.
- **Preflight Integration**: Append `bash scripts/test_build_release.sh` to the testing block in `preflight.sh`.

## 4. Acceptance Criteria
- [ ] A `.release_ignore` file is created at the project root.
- [ ] `scripts/build_release.sh` universally packages the project into `dist/`, respecting `.release_ignore`.
- [ ] `deploy.sh` correctly invokes the build script and deploys exclusively from `dist/`.
- [ ] `test_build_release.sh` thoroughly verifies the isolation boundary and is hooked into `preflight.sh`.
- [ ] The core scripts are mirrored to `TEMPLATES/AgentSkill_Archetype/`.
- [ ] Running `./preflight.sh` outputs `✅ PREFLIGHT SUCCESS`.