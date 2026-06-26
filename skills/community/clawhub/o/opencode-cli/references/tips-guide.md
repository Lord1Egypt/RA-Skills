# Practical Tips Guide

> OpenCode usage tips and shortcuts

---

## File Reference

Use `@filename` in prompt to quickly reference files:

```bash
opencode run "Analyze security issues in @src/auth.ts"
opencode run "Compare differences between @src/a.ts and @src/b.ts"
```

**Fuzzy search:** Just type part of filename after `@` to match.

---

## Undo/Redo

In TUI mode:

| Command | Description |
|---------|-------------|
| `/undo` | Undo recent change (stackable) |
| `/redo` | Restore undone change |

**Best practice:** Feel free to experiment, always `/undo` to rollback.

---

## Keyboard Shortcuts (TUI Mode)

| Shortcut | Function |
|----------|----------|
| `Tab` | Switch Build/Plan Agent |
| `@` | File fuzzy search |
| `Ctrl+C` | Cancel current operation |

---

## Slash Commands (TUI Mode)

| Command | Function |
|---------|----------|
| `/connect` | Configure API Key |
| `/init` | Initialize project AGENTS.md |
| `/undo` | Undo change |
| `/redo` | Redo change |
| `/share` | Create share link |
| `/title` | Change session title |
| `/summary` | Generate conversation summary |

---

## Best Practices

### Use Plan Mode First

Switch to Plan Agent to analyze implementation strategy, then switch to Build after confirmation.

### Maintain Session Continuity

Use `--continue` to maintain context and avoid repeated analysis.

### Leverage File References

Using `@` to reference files is more accurate than describing file paths.

---

*Tips Guide v1.0 - 2026-04-05*