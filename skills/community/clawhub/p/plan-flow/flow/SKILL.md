---
name: flow
description: Toggle autopilot flow mode - automatically orchestrates discovery, planning, execution, and review for feature requests
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---

# Flow: Autopilot Mode Toggle

Enables or disables autopilot flow mode. When enabled, feature requests automatically run the full plan-flow workflow without manual command invocation.

## Usage

```
/flow -enable       Enable autopilot mode
/flow -disable      Disable autopilot mode
/flow -status       Show current state
/flow               Same as -status
/flow -help         Show help
```

## How It Works

**State**: Stored in `flow/.autopilot` (empty marker file). Create to enable, delete to disable.

### When Enabled

Every user input is classified:

| Category | Signals | Action |
|----------|---------|--------|
| Slash Command | Starts with `/` | Run normally, no flow |
| Question/Exploration | Asking about code, explanations | Answer normally, no flow |
| Trivial Task | Single-file, obvious fix, complexity 0-2 | Execute directly, no flow |
| Feature Request | New functionality, multi-file, complexity 3+ | **Trigger full flow** |

### Full Flow (6 Steps)

1. **Check Contracts** → Look for relevant integration contracts
2. **Discovery** (PAUSE) → Gather requirements, ask user questions
3. **Create Plan** (PAUSE) → Create implementation plan, get user approval
4. **Execute Plan** → Implement phases with complexity-based grouping
5. **Review Code** → Review all uncommitted changes
6. **Archive** → Move artifacts to `flow/archive/`, prompt for cleanup

### Mandatory Checkpoints

Even in autopilot, these always pause for user input:

| Checkpoint | When | Why |
|------------|------|-----|
| Discovery Q&A | Step 2 | User must answer requirements questions |
| Discovery Gate | Step 2→3 | Discovery document must exist before plan. No exceptions. |
| Plan Approval | Step 3 | User must approve plan before execution |

### When Disabled

Commands run individually as normal:
`/discovery` → `/create-plan` → `/execute-plan` → `/review-code`

## Toggle Commands

### Enable
1. Create `flow/.autopilot` (empty file)
2. Confirm to user that autopilot is enabled

### Disable
1. Delete `flow/.autopilot`
2. Confirm to user that autopilot is disabled

### Status
1. Check if `flow/.autopilot` exists
2. Report current state (ENABLED/DISABLED)

## Critical Rules

| Rule | Description |
|------|-------------|
| **File-based state** | State is stored in `flow/.autopilot` - create to enable, delete to disable |
| **No other side effects** | This command ONLY manages the marker file. It does not run any workflow steps. |
| **Complete and stop** | After toggling state, STOP and wait for user input |
