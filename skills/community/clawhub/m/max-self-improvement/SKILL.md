---
name: max-self-improvement
description: MiniMax Agent self-evolution system with 5-layer memory architecture and continuous learning. Triggers: "remember this preference", "continue from last time", "improve your response", "analyze failure", "do you remember", "self-evolve", "record this lesson", build personal memory system.
---

# Max-Self-Improvement — Self-Evolution & Memory System

## Overview

MiniMax Agent's self-evolution framework integrating 5-layer memory architecture, supporting cross-session persistent context and continuous performance optimization.

---

## Core Components

### 1. Five-Layer Memory Architecture

| Layer | Name | Storage | Function |
|-------|------|---------|----------|
| L1 | Sensory Memory | Context Window | Immediate input/output stream |
| L2 | Working Memory | `/memories/session_notes.md` | Current task state |
| L3 | Long-Term Memory | `/memories/*.md` | User preferences, domain knowledge |
| L4 | Episodic Memory | `/memories/evolution/` | Patterns, lessons, cases |
| L5 | Metacognitive | `/memories/evolution/metrics.md` | Performance tracking |

### 2. Learnings System

Records structured learnings from errors, corrections, and successes.

```
.learnings/
├── LEARNINGS.md         # Learning entries
├── ERRORS.md            # Error logs
└── FEATURE_REQUESTS.md  # Feature requests
```

---

## Entry ID Format

```
TYPE-YYYYMMDD-XXX
├── TYPE: LRN | ERR | FEAT
├── YYYYMMDD: Current date
└── XXX: Sequence number or random 3 chars
```

---

## Trigger Scenarios

### Learning Triggers → LEARNINGS.md

| Situation | Category |
|-----------|----------|
| Command/operation fails | error |
| User corrects you | correction |
| Discovered better approach | best_practice |
| Found outdated knowledge | knowledge_gap |
| User provides unknown info | knowledge_gap |

### Error Triggers → ERRORS.md

| Situation | Action |
|-----------|--------|
| Non-zero exit code | Log to ERRORS.md |
| Exception/stack trace | Log to ERRORS.md |
| Unexpected output | Log to ERRORS.md |
| API/tool failure | Log to ERRORS.md |

### Feature Triggers → FEATURE_REQUESTS.md

| User Says | Action |
|-----------|--------|
| "Can you also..." | Log to FEATURE_REQUESTS.md |
| "I wish you could..." | Log to FEATURE_REQUESTS.md |
| "Is there a way to..." | Log to FEATURE_REQUESTS.md |
| "Why can't you..." | Log to FEATURE_REQUESTS.md |

---

## Correction Detection Patterns

When user says phrases like:
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "That's outdated..."

→ Create LRN entry with category: `correction`

---

## Entry Templates

### Learning Entry (LEARNINGS.md)

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | acknowledged | applied
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback | discovery
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX
- Pattern-Key: simplify.dead_code | harden.input_validation
- Recurrence-Count: 1
- First-Seen: YYYY-MM-DD
- Last-Seen: YYYY-MM-DD
```

### Error Entry (ERRORS.md)

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending | investigated | resolved
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of what failed

### Error
Actual error message or output

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-YYYYMMDD-XXX
```

### Feature Request Entry (FEATURE_REQUESTS.md)

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending | planned | implemented | rejected
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted to do

### User Context
Why they needed it, what problem they're solving

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what it might extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name
```

---

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| critical | Blocks core function, data loss risk, security issue |
| high | Major impact, affects common workflows, recurring issues |
| medium | Moderate impact, workaround exists |
| low | Minor inconvenience, edge case |

---

## Area Labels

| Area | Scope |
|------|-------|
| frontend | UI, components, client code |
| backend | API, services, server-side |
| infra | CI/CD, deployment, Docker, cloud |
| tests | Test files, test tools, coverage |
| docs | Documentation, comments, README |
| config | Config files, environment, settings |

---

## Memory Promotion Targets

| Learning Type | Promote To |
|---------------|-----------|
| Behavioral patterns | `/memories/user_preferences.md` |
| Workflow improvements | `/memories/workflow_library.md` |
| Tool tips | `/memories/domain_knowledge.md` |
| Project facts/conventions | `/memories/project/[slug]/context.md` |

---

## Tool Usage Rules

| Operation | Correct Tool | Wrong Approach |
|-----------|--------------|----------------|
| Update specific line | `str_replace_memory` | `create_memory` overwrites |
| Create new memory | `create_memory` | Reuse unrelated files |
| Read large content | `view_memory` full | Multiple small reads |
| Record new Episode | `create_memory` new file | Append to session_notes |

---

## Conflict Resolution Priority

```
User Explicit Instruction > Recent Implicit Behavior > High-Confidence LT Memory > Low-Confidence Pattern > Default Reasoning
```

---

## Common Mistakes to Avoid

1. **session_notes stack appending** — Update in-place, keep file lean
2. **Not reading memory before work** — Must read session_notes + user_preferences first
3. **Logging everything to memory** — Only write reusable content, avoid noise
4. **No confidence tags on memory** — Knowledge without confidence is blindly adopted
5. **Not saving before restart** — Must write all in-progress state before restart

---

## Quick Reference

| User Says | Agent Action |
|-----------|--------------|
| "Remember this preference" | Update user_preferences.md |
| "Continue from last time" | Read session_notes + project context |
| "Improve your response" | Analyze recent output, update patterns |
| "Analyze failure" | Root cause → lessons.md + proactive pattern |
| "Do you remember" | Search long-term + episodic memory |
| "What did you learn" | Retrieve patterns.md + lessons.md summary |

---

## Related References

- Detailed architecture: `references/architecture.md`
- Memory templates: `references/memory_templates.md`
- Evolution cases: `references/evolution_cases.md`
- Learning templates: `assets/SKILL-TEMPLATE.md`
