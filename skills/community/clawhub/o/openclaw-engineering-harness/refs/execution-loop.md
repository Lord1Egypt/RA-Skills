# Execution Loop

## Phase 1: Clarify (Discovery & Shaping)

- **Goal**: Confirm the boundary of the request, eliminating vague assumptions.
- **Input**: User prompt.
- **Action**: Check if the goal, scope, and success criteria are complete. If not, use AskUserQuestion to supplement.
- **Output**: A structured task description.

## Phase 2: Map (Design & Constraint Check)

- **Goal**: Locate specific files and assess impact areas. Ensure the working tree is clean.
- **Input**: Structured task description.
- **Action**: Use code discovery tools to find entry points, dependencies, and validation scripts. Run `git status` to ensure you aren't stepping on uncommitted work.
- **Output**: The minimum working map and rollback plan (e.g., `git reset --hard`).

## Phase 3: Implement (Smallest Change)

- **Goal**: Perform the code modification exactly as planned.
- **Input**: Minimum working map.
- **Action**: Modify the code using file editing tools. Keep changes coherent and avoid out-of-scope refactoring.
- **Output**: Changed code files.

## Phase 4: Verify (Validation & Auto-Rollback)

- **Goal**: Prove the change is effective and does not break existing logic.
- **Input**: Changed code and validation scripts.
- **Action**: Run test commands or manually verify the criteria. If tests fail and you are stuck, you MUST auto-rollback using `git checkout -- <files>` or `git reset --hard`, and return to Phase 2.
- **Output**: Pass/fail evidence or rollback logs.

## Phase 5: Deliver (Closure & Snapshot)

- **Goal**: Package the results into publishable artifacts or a stable commit.
- **Input**: Validation evidence.
- **Action**: Summarize what was done, update memory, and use `git add` / `git commit` to seal the changes if the project allows.
- **Output**: Git diff summary, publishable artifacts, and a final delivery report.
