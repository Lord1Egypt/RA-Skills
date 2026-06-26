# PRD_043: SDLC CWD Triple Lock Guardrail (--workdir)

## 1. Problem Statement
The SDLC Python scripts (`spawn_*.py`, `get_next_pr.py`, `create_pr_contract.py`) implicitly rely on the current working directory (`os.getcwd()`). When managing external projects (like `pm-skill`) via globally installed skill scripts, this creates a massive risk of context pollution, writing PRs to the wrong directory, and failing preflight checks.

Furthermore, cross-project orchestration introduces risks of toolchain path resolution failures and path traversal attacks (`../`), allowing sub-agents to escape their designated workspace.

## 2. Architecture Context (Monorepo)
Our workspace operates as a **Monorepo** (`itera.git` located at `/root/.openclaw/workspace/.git`). Sub-projects (`leio-sdlc`, `pm-skill`) do NOT have their own `.git` folders. 
*Constraint*: We CANNOT use Git ENV locks (like overriding `GIT_DIR`) because Git must be allowed to traverse up to the workspace root to find the repository. Git isolation relies entirely on directory-bound commands (`git add .` inside the locked directory) and strict path traversal defense.

## 3. Solution
Enforce an explicit, absolute, and heavily guarded `--workdir` constraint across all SDLC orchestrator scripts.

### 3.1 Scope of Changes
Update the following scripts to require `--workdir` (or `-w`):
- `scripts/spawn_planner.py`
- `scripts/spawn_coder.py`
- `scripts/spawn_reviewer.py`
- `scripts/create_pr_contract.py`
- `scripts/get_next_pr.py`

### 3.2 Requirements & Guardrails
1. **Mandatory Argparse**: Add `parser.add_argument("--workdir", required=True)`.
2. **Absolute Path Normalization**: Immediately resolve to an absolute path (`workdir = os.path.abspath(args.workdir)`).
3. **OS Level Lock**: Execute `os.chdir(workdir)` at the start of the script. 
4. **Auto-Scaffolding**: Run `os.makedirs("docs/PRs", exist_ok=True)` to prevent `FileNotFoundError` in virgin projects.
5. **Path Traversal Defense (Boundary Assertion)**: Any script processing file paths (like `create_pr_contract.py` or reading/writing PRDs) MUST assert that the resolved target path remains inside `workdir` using `os.path.commonpath([workdir, target_path]) == workdir`. If false, raise a `SecurityError`.
6. **Dynamic Engine Addressing**: In `spawn_planner.py`, calculate the path to `create_pr_contract.py` dynamically:
   `SDLC_DIR = os.path.dirname(os.path.abspath(__file__))`
   `contract_script = os.path.join(SDLC_DIR, "create_pr_contract.py")`
7. **Mind-Lock Prompting**: Inject the following into the agent's system prompt:
   `"ATTENTION: Your root workspace is rigidly locked to {workdir}. You are strictly forbidden from reading, writing, or modifying files outside this absolute path. Use 'git add .' to stage changes safely within your directory."`

## 4. Testing Strategy (TDD)
Create `scripts/test_cwd_guardrail.sh` using Ephemeral Sandbox Testing:

- **Sandbox Setup**: Use `TEMP_DIR=$(mktemp -d)` and `trap 'rm -rf "$TEMP_DIR"' EXIT` to ensure the sandbox self-destructs after testing, preventing dirty states.
- **T1: Fail-Fast Missing Arg**: Loop through all updated python scripts without passing `--workdir`. Assert `exit 1`.
- **T2: Relative Path Normalization**: Pass `--workdir ./tmp_test` and assert the scripts correctly resolve it to absolute paths.
- **T3: Strict Sandbox Isolation (Coder/Planner)**: Run `spawn_coder.py` with mock mode. Assert that mock output files are generated strictly inside the ephemeral sandbox and NOT in the `leio-sdlc` engine repository.
- **T4: Toolchain Dynamic Path Resolution**: Run `spawn_planner.py` and inspect its generated payload (via mock capture). Assert that it correctly instructs the Planner to use the absolute path to `create_pr_contract.py`.
- **T5: Path Traversal Rejection**: Attempt to call `create_pr_contract.py` with an output file path like `../../etc/passwd`. Assert that the Python script throws a `SecurityError` and exits.

## 5. Acceptance Criteria
- [ ] All SDLC scripts refuse to run without `--workdir`.
- [ ] Path traversal attempts (`../`) are actively blocked by Python assertions.
- [ ] `scripts/test_cwd_guardrail.sh` passes all 5 TDD scenarios in an ephemeral sandbox.
- [ ] `./preflight.sh` runs successfully (all legacy tests updated to inject `--workdir "$(pwd)"`).