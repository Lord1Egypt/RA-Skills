---
name: nova-self-improver
description: >-
  Complete self-improvement system for AI agents. Implements a four-layer memory architecture with
  continuous learning, experimentation, and autonomous file maintenance. Use when: (1) Building an agent that learns
  from its own performance, (2) Creating self-improving AI systems, (3) Implementing memory layers for
  agent context, (4) Automating agent self-maintenance without human prompts. Inspired by Hermes Agent, AutoAgent,
  and ClawChief architectures.
---

# Nova Self-Improver 🧠

A complete self-improvement system for AI agents. Transforms a static AI into a living, learning entity that improves itself.

## Overview

This skill implements:
- **Four-layer memory system** (inspired by Hermes Agent)
- **Self-improvement loop** (inspired by AutoAgent) 
- **Circuit breaker fallback** (inspired by Mem0)
- **Autonomous file maintenance**
- **User preference learning**

## What This Skill Does

1. **Continuous Learning**: After each task, reflect and log what worked/didn't
2. **Memory Layers**: Maintain context across sessions (4 layers)
3. **Self-Evaluation**: Track successes, failures, and patterns
4. **Autonomous Updates**: Keep own files current without prompting
5. **Experiment Framework**: Try multiple approaches, measure results
6. **User Learning**: Auto-learn preferences from interactions

## When to Use

Trigger phrases:
- "build self-improvement"
- "make me learn from mistakes"
- "implement memory layers"
- "autonomous agent"
- "self-improving system"
- "add learning loop"
- "implement four-layer memory"

## Files Required

Create these files in your workspace:

```
workspace/
├── MEMORY.md              # Curated long-term memory (layer 1)
├── USER.md                # User context + auto-learned preferences  
├── SESSION-STATE.md       # Hot RAM - survives compaction
├── identity.md            # Your identity
├── .learnings/
│   ├── LEARNINGS.md       # Successful patterns (layer 4)
│   ├── ERRORS.md          # Failures to avoid
│   ├── FEATURE_REQUESTS.md # Capabilities you want
│   └── PATTERN_COUNTER.md # Track successful approaches
└── memory/
    └── YYYY-MM-DD.md     # Daily logs (layer 2)
```

## Implementation

### Step 1: Create Four-Layer Memory

**Layer 1: Prompt Memory**
Files to load every session:
- MEMORY.md (~3.5K char max)
- USER.md
- SESSION-STATE.md

**Layer 2: Session Search**  
Use your platform's memory_search:
- Search across MEMORY.md + memory/*.md
- Returns relevant past context

**Layer 3: Skills**
- Store reusable procedures in skills/
- Name + summary loads; full on invocation

**Layer 4: Learnings**
- .learnings/LEARNINGS.md
- .learnings/ERRORS.md
- .learnings/FEATURE_REQUESTS.md

### Step 2: Implement Learning Loop

After any significant task, execute:

```
1. Task Complete → Did it work?
2. Reflect → What worked? What didn't?
3. Pattern ID → Repeat issue or new?
4. Update → Log to appropriate .learnings/ file
5. Suggest → Proactively recommend improvement
```

Reflection triggers (auto-evaluate):
- Tool/command failure
- User correction ("No, that's wrong...")
- Capability gap discovered
- External API failure

### Step 3: Implement Circuit Breaker

When primary systems fail, fallback chain:

```
memory_search (primary)
    ↓ (fails)
grep + read files (backup)
    ↓ (fails)  
return "no results" + log error
```

### Step 4: Auto-Update USER.md

Learn user preferences automatically:

```
After each session:
1. Did user correct me? → Log to USER.md
2. Did something work they liked? → Note it
3. Discover new preference? → Add to USER.md
4. Every 10 sessions: compress the auto-learned section
```

Format:
```markdown
## Auto-Learned Preferences
### Communication Style
- [date]: [preference discovered]

### Task Preferences  
- [date]: [preference discovered]

### Feedback Patterns
- [date] Corrected: [what they fixed]
- [date] Approved: [what worked]
```

### Step 5: Add Autonomous Cron Jobs

Schedule self-maintenance:

| Cron | Schedule | Purpose |
|-----|----------|---------|
| self-improvement-loop | Hourly | Review learnings, errors |
| auto-system-update | Daily midnight | Update all memory files |
| skill-audit | Weekly | Verify all skills work |

Example cron (JSON):
```json
{
  "name": "self-improvement-loop",
  "schedule": {"kind": "cron", "expr": "0 * * * *"},
  "payload": {"kind": "agentTurn", "message": "Review .learnings/, update files"},
  "sessionTarget": "isolated"
}
```

## Key Patterns

### Learning Loop Protocol
```
[TRIGGER] After any task completion or failure:
1. Read .learnings/ERRORS.md - avoid known failures
2. Read .learnings/LEARNINGS.md - replicate successes  
3. Log new pattern to appropriate file
4. If approach succeeded 3x → suggest skill creation
5. Update memory/YYYY-MM-DD.md
```

### Experiment Framework
```
When unsure of best approach:
1. Try multiple approaches (keep it small)
2. Measure outcome (success/fail/faster)
3. Log result to .learnings/EXPERIMENTS.md
4. Keep what works, discard what doesn't
5. Document the winner for future reference
```

### Skill Auto-Creation Protocol
```
When same approach works 3+ times:
1. Note it in PATTERN_COUNTER.md
2. When count reaches 3 → create a skill
3. Skill template includes "Evolved From" field
4. Skills are NOT final - they evolve over time
```

## Configuration

### Required Files

Create SESSION-STATE.md:
```markdown
# SESSION-STATE.md — Active Working Memory

## Current Task
[None]

## Key Context
[Fill in key context]

## Pending Actions
- [ ] None

## Recent Decisions
- [date]: [decision made]
```

### File Size Limits
- MEMORY.md: ~3,500 chars max
- SESSION-STATE.md: Keep under 2KB
- Daily logs: No limit but archive after 30 days

## Metrics to Track

| Metric | How |
|--------|-----|
| Task Success Rate | Completed / Total |
| Turn Efficiency | Avg turns per task |
| Error Recovery | Recovered vs. permanent |
| Learning Velocity | Patterns / week |

## Evolved From

- Hermes Agent (Graeme): Four-layer memory, learning loop
- AutoAgent (Kevin Gu): Self-improvement via meta-agent
- ClawChief (Ryan Carson): Gmail message-level search, canonical task list
- Vox (@Voxyz_ai): Living skills > static skills
- Mem0: Circuit breaker, auto-update preferences

---

*Built by Nova 🧠 — Available on OpenClaw + clawhub*
*License: MIT*