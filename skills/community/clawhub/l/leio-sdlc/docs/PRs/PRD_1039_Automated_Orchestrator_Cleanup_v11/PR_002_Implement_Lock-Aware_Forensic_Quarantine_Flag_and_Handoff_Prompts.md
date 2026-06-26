status: closed

# PR-002: Implement Lock-Aware Forensic Quarantine Flag and Handoff Prompts

## 1. Objective
Add a `--cleanup` flag to the orchestrator for lock-aware forensic quarantine of toxic branches, and update handoff prompts for various fatal exit scenarios.

## 2. Scope (Functional & Implementation Freedom)
- Add a new command-line argument `--cleanup` to the orchestrator.
- Implement a concurrency guard using exclusive, non-blocking locks (`fcntl.flock`). If another pipeline is active, exit with a fatal lock error.
- If the current branch is `master` or `main`, exit with an error.
- Implement the safe quarantine sequence: stage all modifications, create an empty WIP commit ("WIP: 🚨 FORENSIC CRASH STATE"), natively calculate a timestamp in Python, rename the crashed branch, checkout master, and safely delete ephemeral daemon locks (`os.remove()`).
- Add/update handoff prompter messages for git checkout errors, fatal crashes, and fatal interrupts.
- Ensure every `sys.exit(1)` in the orchestrator is mapped to a specific handoff prompt, including a success signal before exiting with code 0.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- `--cleanup` flag successfully acquires/fails `fcntl` locks and prevents destroying active pipelines.
- Toxic branches are correctly quarantined (WIP commit, timestamped rename, checkout master).
- Ephemeral locks are deleted via native Python `os.remove()`, NOT destructive git clean commands.
- Handoff prompts match the specified messages for fatal crash, git error, and interrupt.
- Tests must be written/updated to verify the `--cleanup` logic and handoff prompter mappings.
- All tests must pass (100% GREEN) before submitting.