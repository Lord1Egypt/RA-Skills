# Memory System v2.0 - Detailed Design

> **⚠️ Legacy Reference** — This document describes the v2.0 design. The current version is v2.2 with Memory-Knowledge layering + Scientific memory loop (Encode→Consolidate→Retrieve) + Metacognitive training. See [SKILL.md](../SKILL.md) for the current design.

Based on Atkinson-Shiffrin three-stage memory model (1968) + Community Optimizations (2026)

## Theory Background

### Atkinson-Shiffrin Model

```
Sensory Memory → Short-Term Memory → Long-Term Memory
   (0.25-2s)        (5-20s)            (Permanent)
     ↓                   ↓                   ↓
  Attention         Rehearsal          Consolidation
```

### Community Optimization (2026)

Based on practical testing, the three-stage model has been optimized:

| Metric | Before | After |
|--------|--------|-------|
| Task completion rate | 67% | 88% |
| Response speed | 1x | 2x |
| Retrieval accuracy | - | >70% |

### Key Mechanisms

1. **Information Filtering**: Selective attention filters sensory → short-term
2. **Storage Maintenance**: Rehearsal maintains short-term and transfers to long-term
3. **Capacity Limitations**: Each stage has capacity bottlenecks
4. **Smart Caching**: Instant cache for 10 turns with priority-based retrieval

## Implementation for AI

### Stage 0: Instant Cache (v2.0 NEW)

**Location**: Memory buffer / session context  
**Capacity**: Last 10 conversation turns  
**Duration**: Instant (cleared after 10 turns or new session)

```
User Input → Check Cache → Cache Hit? → Use cached response
                    ↓
              Cache Miss? → Continue to sensory
```

**Characteristics**:
- ⚡ Fastest response (priority 1)
- Low memory footprint
- Auto-cleared after 10 turns
- Stores key context only

---

### Stage 1: Sensory Memory (Instant)

**Location**: Tool call context / current input buffer  
**Capacity**: Last 3-5 exchanges  
**Duration**: Current turn only

```
User Input → Parse → Understand Intent → Check Context → Respond
                         ↑
                    Recent history (3-5 turns)
```

**Characteristics**:
- No persistence
- Only maintains conversational flow
- Auto-cleared after each response

---

### Stage 2: Short-Term Memory (Session + 7 Days)

**Location**: session context + memory/YYYY-MM-DD.md  
**Capacity**: Last 7 days of conversation  
**Duration**: 7 days (then auto-cleanup)

**v2.0 Optimization**:
- 7-day retention period (tested with >70% accuracy)
- Auto-cleanup after 7 days
- Priority-based retrieval (check recent days first)

**Location**: session context + memory/YYYY-MM-DD.md  
**Capacity**: Today's full conversation  
**Duration**: Current session + rest of day

**When to Write**:
- Every significant exchange
- New tasks or requests
- User preferences revealed
- Decisions made

**Writing Template**:
```markdown
## [Time] - Topic

**User said**: [brief summary]
**I did**: [action taken]
**Remember**: [key point for future]
```

---

### Stage 3: Long-Term Memory (Permanent)

**Location**: MEMORY.md + knowledge/*.md  
**Capacity**: Unlimited  
**Duration**: Permanent

**What Gets Consolidated** (rehearsal triggered):
- User confirms important information
- User corrects a mistake
- Promise or commitment made
- Personal details (name, role, preferences)
- Project milestones

**Consolidation Process**:
1. Identify important info during conversation
2. Immediately write to today's memory
3. Before next session, review and move key points to MEMORY.md
4. Delete routine info from daily log after 7 days

---

## Memory File Specifications

### MEMORY.md - Core Long-Term

**Contents**:
- User identity and profile
- Key relationships and context
- Important commitments
- Major project statuses
- Learned preferences

**Update Triggers**:
- New user session
- User provides personal info
- Promise made
- Significant decision

**Format**:
```markdown
### [Category]

**Date**: YYYY-MM-DD
**Content**: [What to remember]
**Context**: [Why it matters]
```

---

### memory/YYYY-MM-DD.md - Daily Log

**Contents**:
- Detailed conversation logs
- Tasks handled
- Questions asked
- Responses given

**Auto-cleanup**:
- Keep last 7 days
- Archive to memory/archive/ after 30 days

---

### USER.md - User Profile

**Contents**:
- Name, how to address
- Role/position
- Communication preferences
- Timezone
- Known preferences

**Keep Updated**:
- New personal info revealed
- Preference changed

---

### todos.md - Active Tasks

**Contents**:
- Pending actions
- Follow-ups needed
- Promises to user

**Review**:
- Every session start
- After completing task, mark done

---

## Memory Search Protocol (v2.0)

Before answering questions that might reference past:

```
Query Received
├── Check Instant Cache (10 turns) → ⚡ Fastest
├── Check Short-Term (7 days) → 🔄 Common
├── Check Long-Term MEMORY.md → 📚 Core Facts
└── Check knowledge/ → 📖 Structured Info
```

**Priority Order** (v2.0):
1. Instant cache - most recent 10 turns
2. Short-term memory - last 7 days
3. Long-term memory - permanent facts
4. Knowledge base - structured information

**Search queries**:
- "What did user say about X?"
- "Did we discuss Y before?"
- "User mentioned Z previously"

---

## Quality Assurance

### Good Memory Practice

✅ Remember:
- User's name and role
- Past discussions on same topic
- Unfulfilled promises
- User's preferences

❌ Forget:
- Exact wording of past messages
- Timestamps (unless important)
- Routine exchanges
- Sensitive info (unless authorized)

### Failure Recovery

**If I forget**:
1. User says "I told you before" → Apologize, ask them to remind you
2. User corrects me → Immediately update memory, thank them
3. I notice gap → "Just to confirm, is it still X?"

---

## Continuous Improvement

Track memory failures:
- What did I forget that I should have remembered?
- What did user correct me on?
- What context was missing?

→ Use these to improve memory writing habits

---

*Design: Atkinson & Shiffrin (1968)*
*Community Optimization: 2026*
*Implementation: OpenClaw*
*Version: 2.0*
