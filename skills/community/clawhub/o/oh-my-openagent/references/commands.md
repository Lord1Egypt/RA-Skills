## Slash commands

OmO adds 8 slash commands to OpenCode.

### /ralph-loop

Start a self-referential development loop. The agent continues working autonomously until the task is complete, re-evaluating and adjusting as it goes.

### /ulw-loop

Start an ultrawork loop. Similar to ralph-loop but uses ultrawork mode for continuous completion without interruption.

### /cancel-ralph

Cancel an active Ralph Loop. Stops the autonomous loop.

### /start-work

Start a Sisyphus work session from a Prometheus plan. Flow:
1. Prometheus creates a detailed plan
2. Metis reviews for ambiguities (optional)
3. Momus validates completeness (optional)
4. Hephaestus executes the plan

### /refactor

Intelligent refactoring command. Uses LSP, AST-grep, architecture analysis, codemap, and TDD verification.

### /init-deep

Initialize a hierarchical AGENTS.md knowledge base. Creates structured documentation of the codebase for agent context.

### /handoff

Create a detailed context summary for continuing work in a new session. Captures current state, decisions made, files modified, and remaining tasks.

### /stop-continuation

Stop all continuation mechanisms (ralph loop, todo continuation, boulder) for the current session.

## Using commands

Commands are invoked in the chat:

```
/ralph-loop
/start-work
/refactor
```

Or loaded programmatically:

```
slashcommand(command="start-work")
slashcommand(command="refactor")
```
