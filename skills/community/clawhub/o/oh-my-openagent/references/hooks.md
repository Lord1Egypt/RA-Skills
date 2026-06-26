## Hooks

OmO includes 40+ built-in hooks that fire on various events. Hooks inject context, run checks, or modify behavior.

### Hook categories

#### Session hooks
- Fire on session start, resume, or end
- Examples: inject project context, load memory, set up environment

#### File hooks
- Fire on file save, create, or delete
- Examples: auto-format, lint check, update imports

#### Pre-commit hooks
- Fire before git commits
- Examples: run tests, check types, validate formatting

#### Keyword detector hooks
- Fire when specific keywords appear in conversation
- Examples: detect coding tasks, detect deployment requests

#### Todo continuation hooks
- Fire when todo items are completed
- Monitor task progress and trigger next steps

#### Error recovery hooks
- Fire on tool failures or agent errors
- Examples: retry logic, fallback behavior

### Hook configuration

Enable or disable hooks in `oh-my-opencode.json`:

```json
{
  "hooks": {
    "hook-name": {
      "enable": true
    },
    "another-hook": {
      "enable": false
    }
  }
}
```

### Custom hooks

Custom hooks can be defined with trigger conditions and actions:

```json
{
  "hooks": {
    "my-custom-hook": {
      "enable": true,
      "trigger": "keyword",
      "pattern": "deploy",
      "action": "prompt",
      "message": "Deployment detected. Running pre-deploy checks..."
    }
  }
}
```

### Notable built-in hooks

| Hook | Trigger | Behavior |
|------|---------|----------|
| TODO_CONTINUATION | Todo item completed | Continues to next task automatically |
| CODING_MODE | Coding keywords detected | Switches to appropriate coding agent |
| SESSION_CONTEXT | Session start | Injects project context |
| RALPH_LOOP | /ralph-loop command | Self-referential development loop |
| ULW_LOOP | /ulw-loop command | Ultrawork continuous loop |
