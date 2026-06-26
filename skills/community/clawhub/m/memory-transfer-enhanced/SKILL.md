---
name: memory-transfer
description: Transfer memory files between OpenClaw agents with support for topic-specific transfers and two modes: memory sharing (with role transformation) and memory cloning (verbatim copy). Use when: (1) Migrating memory from main agent to sub-agent, (2) Sharing specific topic memories between agents, (3) Copying user preferences to new agents, (4) Backing up agent memory before resets.
metadata:
  {
    "openclaw": { "emoji": "📦" }
  }
---

# Memory Transfer Skill

Transfer memory files and context between OpenClaw agents with advanced filtering and transformation options.

## Core Features

1. **Topic-Specific Transfer** - Transfer only memories related to a specific topic/keyword
2. **Memory Sharing** - Share memories with role/perspective transformation (I → you, my → your)
3. **Memory Cloning** - Clone memories verbatim without any transformation

## Mode Differences

### Memory Sharing (share mode)
**Best for knowledge/context transfer between agents**

This mode:
1. **Filters out user information** - Removes personal data about the user:
   - User names: "我叫小明", "我的名字是..."
   - User preferences: "我喜欢...", "我讨厌..."
   - User personal info: email, phone, address, birthday
   - About user: "关于我..."

2. **Transforms to target agent's identity** - Converts references to match the target agent:
   - "I am Agent Main" → "I am Agent Skill Master" (adopts target identity)
   - "Agent Main's workspace" → "Agent Skill Master's workspace"
   - "I work as a helper" → "I work as Agent Skill Master"
   - First-person pronouns (I, my, me) remain as first-person

**Use when**: Sharing project knowledge, workflows, or task context. The target agent adopts the knowledge as their own experience.

### Memory Cloning (clone mode)
Copies memory exactly as-is without filtering or transformation:
- All content preserved verbatim
- User information remains
- Original context maintained

**Use when**: Full backup/migration or preserving original author's voice.

## Commands

### List available agents

```bash
ls /home/node/.openclaw/
```

### Transfer all memory from source to target

```bash
node memory-transfer.js transfer <source-agent-id> <target-agent-id>
```

### Transfer with mode selection (interactive)

```bash
node memory-transfer.js transfer <source> <target> --mode interactive
```

This will prompt for:
1. Topic filter (optional - press Enter to transfer all)
2. Mode selection: share or clone
3. Confirmation before proceeding

### Transfer specific topic memory

```bash
node memory-transfer.js transfer <source> <target> --topic "claude"
```

### Force memory sharing (with transformation)

```bash
node memory-transfer.js transfer <source> <target> --mode share
```

### Force memory cloning (verbatim)

```bash
node memory-transfer.js transfer <source> <target> --mode clone
```

### Preview transfer (dry run)

```bash
node memory-transfer.js transfer <source> <target> --dry-run
```

### List agent memories

```bash
node memory-transfer.js list <agent-id>
```

### Search memories by topic

```bash
node memory-transfer.js search <agent-id> <topic>
```

## Interactive Workflow

When running without explicit flags, the skill will:

1. **Prompt for source agent** - Select which agent's memory to transfer
2. **Prompt for target agent** - Select destination agent
3. **Prompt for topic** (optional) - Enter keyword to filter, or press Enter for all
4. **Prompt for mode** - Choose:
   - `share` - Filter user info + transform pronouns (recommended for knowledge sharing)
   - `clone` - Keep original verbatim (for backup)
5. **Show preview** - Display what will be transferred
6. **Confirm** - Require explicit confirmation before executing
7. **Execute or cancel** - Proceed or abort based on user decision

## Examples

### Transfer all memories as sharing (with transformation)

```bash
node memory-transfer.js transfer main coder --mode share
```

### Transfer specific date memory as clone

```bash
node memory-transfer.js transfer main coder 2026-03-01.md --mode clone
```

### Transfer topic-filtered memory with preview

```bash
node memory-transfer.js transfer main coder --topic "preferences" --dry-run
```

### Interactive mode (recommended for first-time use)

```bash
node memory-transfer.js transfer main coder --mode interactive
```

## Target Agent Adaptation Rules

When using **share mode**, the memory is transformed to match the target agent's identity:

### Agent Identity

| Source | Target |
|--------|--------|
| I | Agent Main (source agent name) |
| me | Agent Main |
| my | Agent Main's |
| I bought | Agent Main bought |
| I think | Agent Main thinks |

### Role Statements

| Source Pattern | Target |
|----------------|--------|
| I work as helper | Agent Skill Master works as helper |
| I serve as | Agent Skill Master serves as |

**Result example**: "I bought a phone" → "Agent Main bought a phone"

This way the target agent knows this is the source agent's experience, not their own.

| Source | Target |
|--------|--------|
| I think | you think |
| I believe | you believe |
| I know | you know |
| I understand | you understand |
| I remember | you remember |
| I prefer | you prefer |
| I like | you like |
| I want | you want |
| I need | you need |

**Important**: The transformation converts both pronouns AND role descriptions so the target agent doesn't inherit confused identity. For example:
- "I am Agent Skill Master" → "you are Agent Skill Master"
- "My role is to create skills" → "your role is to create skills"
- "I was created to help you" → "you were created to help me"

## Agent Workspaces

OpenClaw agent workspaces are typically at:
- `/home/node/.openclaw/workspace-<agent-id>/`
- Main agent: `/home/node/.openclaw/workspace-main/`

Memory files:
- `MEMORY.md` - Long-term memory
- `memory/YYYY-MM-DD.md` - Daily memories
- `memory/*.md` - Topic-specific memories

## Safety Features

1. **Dry-run by default** - Preview before executing
2. **Explicit confirmation** - Never auto-execute without approval
3. **Backup option** - Can create backup before overwriting
4. **Mode clarification** - Always ask to confirm share vs clone mode
