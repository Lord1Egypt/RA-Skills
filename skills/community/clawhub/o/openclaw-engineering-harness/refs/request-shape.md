# Request Shape

Every task handled by this skill must be shaped into a structured format before implementation begins. This ensures that no work proceeds on vague assumptions.

## Required Fields

1. **Goal**: A concise statement of what needs to be achieved.
2. **Scope**: The exact files, components, or directories that will be affected by the change.
3. **Success Criteria**: The specific, verifiable conditions that must be met for the task to be considered complete.
4. **Memory Context**: The loaded relevant rules and constraints retrieved from `.claude/MEMORY.md` and related topic files.

## Optional But Recommended Fields

5. **Constraints**: Any technical or organizational limitations (e.g., standard library only, no external dependencies, performance budgets).
6. **Rollback**: The specific steps to take if the implementation fails (e.g., "revert commit XYZ", "delete the created directory").
7. **Verification**: The exact commands or scripts to run to prove the success criteria.
8. **Memory Extracted**: The new "Lessons Learned" derived from this task to be persisted into the memory system before closing.
9. **Deliverables**: The list of artifacts or outputs expected at the end of the task.

## Action Item

If any of the required fields are missing, use the `AskUserQuestion` tool to clarify the task shape before moving to the `map` phase.
