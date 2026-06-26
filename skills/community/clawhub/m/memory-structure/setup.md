# Memory Structure Setup

This guide helps you set up the memory structure system in a new environment.

## Prerequisites

- File system write permissions
- Workspace directory path

## Quick Start

### Step 1: Create Directory Structure

Create the following structure in your desired memory location:

```bash
mkdir -p ~/self-improving/{domains,projects,archive}
```

### Step 2: Create Template Files

Manually create the following files:

**memory.md:**
```markdown
# Memory (HOT Tier)

## Preferences

## Patterns

## Rules
```

**corrections.md:**
```markdown
# Corrections Log

| Date | What I Got Wrong | Correct Answer | Status |
|------|-----------------|----------------|--------|
```

**index.md:**
```markdown
# Memory Index

| File | Lines | Last Updated |
|------|-------|--------------|
| memory.md | 0 | — |
| corrections.md | 0 | — |
```

**heartbeat-state.md:**
```markdown
# Self-Improving Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
```

### Step 3: Configure Heartbeat (Recommended)

Add to workspace HEARTBEAT.md for automatic 30-minute self-reflection:

```markdown
## Self-Improving Check
- Read ~/self-improving/heartbeat-rules.md
- Use ~/self-improving/heartbeat-state.md for state tracking
- If no changes since last check, return HEARTBEAT_OK
```

**Note:** The heartbeat interval (e.g., 30 minutes) is configured in OpenClaw's config file, not in this skill.

## Directory Structure

```
~/self-improving/
├── memory.md           # Main memory file (HOT Tier)
├── corrections.md      # Error correction log
├── index.md            # Memory index
├── heartbeat-state.md  # Heartbeat state
├── heartbeat-rules.md  # Heartbeat rules
├── domains/            # Domain knowledge directory
├── projects/           # Project-related memory
└── archive/           # Archived memory
```

## Verify Installation

Run to verify:

```bash
ls -la ~/self-improving/
```

## Security Notes

- Memory directory path can be adjusted as needed
- No automatic modification of any Agent configuration files
- All configurations require manual confirmation before execution
