# Project Lifecycle Management

> Project pause, cancellation, resumption, cross-project dependencies, lead management, post-archive handling.

---

## Project Status

```
Active → Paused → Resume as Active / Cancelled
Active → Completed → Archived
Active → Cancelled
```

## Pause Process

1. Decision Maker instructs pause → Record pause reason and current progress
2. Notify all in-progress executors to pause work
3. Update project index status to "Paused"
4. Preserve all documents and outputs, don't clean up
5. When resuming: Read pause record, continue from breakpoint

## Pause Resumption Handling

When project paused with "In Progress" tasks, upon resumption the executor's session may no longer exist.

**When Pausing:**
1. Notify executor to save progress and intermediate output
2. Record progress at pause time in status tracking
3. Record intermediate output location

**When Resuming:**
1. Read pause record
2. "In Progress" tasks redispatch, add "continuation note":
   - Completed parts (don't redo)
   - Intermediate output location
   - Remaining parts to complete
3. Can dispatch to different executors

## Cancellation Process

1. Decision Maker instructs cancellation → Record cancellation reason
2. Notify all executors to stop work
3. Write simplified final-report (completed parts + cancellation reason)
4. Clean up temporary files
5. Update index status to "Cancelled"
6. Preserve valuable intermediate output, extract lessons learned

## Cross-Project Dependencies

- brief.md has "Cross-Project Dependencies" field, marking prerequisite projects
- Prerequisite not complete → Subsequent can initiate project and break down, but not dispatch for execution
- After prerequisite completes → Check and start subsequent project

## Project Lead Uniqueness

- Each project has only one lead at a time (written in brief.md)
- Only lead can: Update index, modify status, write review records, dispatch tasks
- Executor can only: Read spec, deliver output, feedback issues
- Change lead → Update brief.md, record handoff in status tracking
- Not limited who can be lead, but only one at a time

## Post-Archive Rework

- Don't reopen archived projects
- Create fix project, name `OriginalProjectName-fix`
- Fix project's brief.md references original project, explains problem
- After fix complete, add note to original project's final-report
