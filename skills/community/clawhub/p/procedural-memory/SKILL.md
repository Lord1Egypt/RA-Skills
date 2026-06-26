---
name: procedural-memory
description: "Inspired by Hermes Agent's procedural memory system. When a workflow works, save it as a reusable skill. Triggered when: (1) user says 'remember this workflow', (2) complex task succeeds, (3) same pattern succeeds 2+ times, (4) end-of-day review. Creates SKILL.md files for agent self-evolution."
---

# Procedural Memory — Automatic Workflow Memory

> _"When a workflow works, save it as a reusable skill."_

Inspired by Hermes Agent's core feature: **an agent that learns from experience by saving successful workflows as reusable skills.**

---

## Directory Prerequisites

```bash
mkdir -p ~/self-improving
mkdir -p ~/.openclaw/workspace/skills
```

The log file `~/self-improving/procedural-memory-log.md` will be created automatically if missing.

---

## Trigger Conditions (Priority Order)

### 🔴 High Priority — Explicit User Request
- "记住这个workflow" / "remember this workflow"
- "以后遇到类似就这样做" / "do this next time"
- "这个方法很好，以后也这样用" / "this works, use it again"
- "这个技巧值得记住" / "this is worth remembering"

### 🟡 Medium Priority — Proactive Review
- End of day (or user says "review")
- After a complex task completes successfully

### 🟢 Low Priority — Pattern Recognition
- Same workflow applied successfully 2+ times
- Recurring solutions discovered

---

## Workflow

### Step 1 — Evaluate Worthiness

**Must meet ALL:**
- ✅ Takes 3+ steps to complete
- ✅ Likely applicable to future conversations
- ✅ Not one-time / context-specific
- ✅ User would benefit

**Auto-trigger:** If the same workflow succeeds 3+ times, auto-create skill WITHOUT asking (记录到日志即可)。

Otherwise: ask user "我可以把这个 workflow 存为 skill 吗？"

If user confirms → continue. Otherwise → silent skip.

### Step 2 — Check for Conflicts

```bash
ls ~/.openclaw/workspace/skills/ | grep <keyword>
```

- Same name exists → log "already exists, skip"
- Similar function exists → consider merge or append

### Step 3 — Extract Pattern

Record:
```
**Skill Name**: [verb]-[problem] (kebab-case)
**Trigger**: [when this would be used]
**Problem Solved**: [what issue this solves]
**Steps**: [numbered list]
**Key Insight**: [why this works]
**Limitations**: [when NOT to use]
```

### Step 4 — Create Skill File

Create `~/.openclaw/workspace/skills/[skill-name]/SKILL.md`:

```markdown
---
name: [skill-name]
description: "[one-line description of when to use]
---
# [Skill Name]

## What This Solves
[trigger conditions and problem]

## When to Use
- [specific scenario 1]
- [specific scenario 2]

## How To Execute
[Step 1]
[Step 2]
[Step 3...]

## Key Insight
[why this is effective]

## Limitations
[when this won't work]
```

### Step 5 — Validate

```bash
ls ~/.openclaw/workspace/skills/[skill-name]/SKILL.md
head -20 ~/.openclaw/workspace/skills/[skill-name]/SKILL.md
```

Recreate if corrupted.

### Step 6 — Log

Append to `~/self-improving/procedural-memory-log.md`:

```markdown
## YYYY-MM-DD

### [skill-name]
- **Trigger**: [what triggered this]
- **Problem solved**: [what was solved]
- **Key insight**: [the key learning]
- **Skill file**: `~/.openclaw/workspace/skills/[skill-name]/SKILL.md`
```

### Step 7 — Notify User

Tell user the skill was created and ask if they want to enable auto-execution:

> "已记住这个 workflow，存为 skill/[skill-name]。是否需要我下次遇到类似情况时自动执行？"

**Default behavior:** Do NOT auto-execute without user confirmation.

---

## Skill Loading

When new conversation context matches a saved skill's trigger:
1. Load the skill's SKILL.md
2. Ask user: "我之前学过这个，要我用这个方法吗？"
3. Only execute AFTER user confirms
4. Never auto-execute without explicit user approval

## Privacy Consideration

- This skill scans conversation history to identify worth-saving workflows
- Derived content is persisted to disk (`~/.openclaw/workspace/skills/` and `~/self-improving/`)
- **Sensitive conversation data may be captured** — user is responsible for what they share in conversations
- Log files contain pattern summaries, not raw conversation, but could still contain sensitive references
- Users should be aware of what they discuss with the agent

---

## End-of-Day Review Prompt

When user says "复盘" or at end of day:

> "今天有什么 workflow 值得我记住吗？"

Scan today's conversation for:
- Complex but successful tasks
- Repeatedly used techniques
- Reusable solutions

---

## References

- Skill Creator Guide: `../skill-creator/SKILL.md`
- Self-Improving Memory: `~/self-improving/memory.md`
- Procedural Memory Log: `~/self-improving/procedural-memory-log.md`
