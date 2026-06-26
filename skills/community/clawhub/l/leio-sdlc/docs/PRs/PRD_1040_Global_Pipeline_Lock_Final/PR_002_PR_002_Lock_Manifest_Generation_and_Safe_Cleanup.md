status: closed

# PR-002: Lock Manifest Generation & Safe Cleanup

## 1. Objective
Generate a local lock manifest upon successful lock acquisition and update the cleanup process to safely release only the locks owned by the current pipeline run.

## 2. Scope (Functional & Implementation Freedom)
- Update the successful lock acquisition flow to write a `.sdlc_lock_manifest.json` file inside the invoking project's current working directory, recording exactly which locks are held.
- Modify the existing Orchestrator `--cleanup` functionality to read this manifest file.
- The cleanup process must only release the specific locks listed in the manifest (ensuring zero blast radius for other pipelines) and then delete the manifest itself.
- Ensure lock release remains the final step in the cleanup protocol.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Upon successful acquisition of all required locks, a `.sdlc_lock_manifest.json` is accurately generated containing the acquired locks.
2. The `--cleanup` command successfully reads the manifest and deletes ONLY the locks specified within it.
3. The manifest file itself is deleted after the locks are safely released.
4. The Coder MUST write or update tests for this specific functional slice. All tests MUST pass (GREEN) before submitting.
