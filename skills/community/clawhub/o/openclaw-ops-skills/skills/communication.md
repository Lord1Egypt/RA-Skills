# Communication Standards

> **Clear, structured, and actionable updates for human-agent collaboration**
> Priority: MEDIUM | Category: Collaboration

## Overview

Effective communication prevents ambiguity, reduces back-and-forth, and ensures both human and agent are aligned on goals and progress.

## Communication Principles

```yaml
core_principles:
  clarity_over_brevity:
    "Better to be clear than concise"
    "Avoid jargon unless explained"

  structured_over_freeform:
    "Use templates for common updates"
    "Consistent format for easy scanning"

  evidence_over_assertion:
    "Show logs, don't just claim"
    "Provide proof of completion"

  actionable_over_informational:
    "Every update should inform next action"
    "Highlight what needs attention"
```

## Update Templates

### 1. Task Start Update

```markdown
# Task Started: [Task Title]

**Task ID**: [T-XXX]
**Started**: [HH:MM]
**Agent**: [Agent Name]
**Model**: [Model]

## Understanding
**What I'm doing**: [Clear task description]
**Success criteria**:
- [ ] [Criteria 1]
- [ ] [Criteria 2]

## Approach
**Plan**: [High-level approach]
**First steps**: [Immediate actions]

## Estimated Completion
**Time estimate**: [X minutes/hours]
**Confidence**: [High | Medium | Low]

## Questions/Concerns
- [None OR list clarifications needed]

---
**Status**: 🟡 IN_PROGRESS
```

### 2. Progress Update

```markdown
# Progress Update: [Task Title]

**Task ID**: [T-XXX]
**Time Elapsed**: [X minutes]
**Status**: [IN_PROGRESS | BLOCKED | etc]

## Completed This Cycle
✅ [What was accomplished]
✅ [What was accomplished]

## Working On
🔄 [Current step]

## Next Steps
1. [Next action]
2. [Following action]

## Blockers
🚫 [None OR what's blocking]

## Evidence
[Log excerpt or screenshot]

---
**Status**: 🟡 IN_PROGRESS | 🟢 COMPLETE | 🔴 BLOCKED
```

### 3. Task Completion Update

```markdown
# Task Complete: [Task Title]

**Task ID**: [T-XXX]
**Completed**: [HH:MM]
**Duration**: [X minutes]
**Agent**: [Agent Name]

## What Was Done
[Summary of work completed]

## Changes Made
**Files Modified**:
- [File 1] - [Change summary]
- [File 2] - [Change summary]

**Files Created**:
- [File 1] - [Purpose]

## Tests
**Status**: ✅ ALL PASS | ⚠️ SOME FAILURES
**Coverage**: [X]%

```
[Test results summary]
```

## Definition of Done
- [x] [Criteria 1] - [Status]
- [x] [Criteria 2] - [Status]
- [x] [Criteria 3] - [Status]

## Artifacts
- [Link to relevant files/logs]

## Lessons Learned
[What was discovered]

## Follow-Up Needed
- [None OR what needs attention]

---
**Status**: 🟢 COMPLETE
```

### 4. Escalation Update

```markdown
# ESCALATION REQUIRED

**Severity**: [CRITICAL | HIGH | MEDIUM | LOW]
**Task**: [T-XXX] [Task name]
**Time**: [HH:MM]

## What Happened
[Clear description of issue]

## Context
**What I was doing**: [Task context]
**What went wrong**: [Error description]

## What I Tried
1. [Attempt 1] - [Result]
2. [Attempt 2] - [Result]

## What I Need
[Specific requirement from user]

## Options
1. **[Option A]**: [Description]
   - Pros: [Advantages]
   - Cons: [Disadvantages]

2. **[Option B]**: [Description]
   - Pros: [Advantages]
   - Cons: [Disadvantages]

## Recommendation
**[Option X]** - [Why]

## Impact
**What's affected**: [Systems, tasks, etc.]
**Blocking**: [What's waiting on this]

## Evidence
```
[Logs, error messages, screenshots]
```

---
**Status**: 🔴 WAITING FOR INPUT
```

### 5. Morning Briefing Update

```markdown
# Morning Briefing: [Date]

**Overnight Period**: [Start] - [End]
**Active Time**: [X hours]

## Overview
[One paragraph summary of overnight work]

## What's Working ✅
1. **[Completed Task 1]** - [Brief result]
2. **[Completed Task 2]** - [Brief result]
3. **[Completed Task 3]** - [Brief result]

## What Needs Attention ⚠️
1. **[Issue 1]** - [Suggested action]
2. **[Issue 2]** - [Suggested action]

## What's Blocked 🚫
1. **[Task 1]** - Blocked on [what's needed]
2. **[Task 2]** - Blocked on [what's needed]

## Ready for Review 📋
1. **[Work Item 1]** - [Review notes]
2. **[Work Item 2]** - [Review notes]

## Metrics
- **Tasks Completed**: [N]
- **Tasks Failed**: [N]
- **Success Rate**: [X]%
- **Token Usage**: [N] ($X.XX)
- **Cost Efficiency**: [X tasks per $1]

## Discovered Issues
- **[Issue 1]**: [Description, impact]
- **[Issue 2]**: [Description, impact]

## Next Steps
1. **[Immediate action if needed]**
2. **[Today's priority tasks]**

## Files to Review
- [File 1] - [Why review needed]
- [File 2] - [Why review needed]

---
**Generated**: [HH:MM]
```

## Communication Styles

### For Different Scenarios

```yaml
quick_status:
  use_when: "Routine updates, low complexity"
  format: "Brief, bullet points"
  length: "< 10 lines"

detailed_update:
  use_when: "Complex work, important changes"
  format: "Structured with evidence"
  length: "As needed for clarity"

escalation:
  use_when: "Blocked, critical decisions needed"
  format: "Full context with options"
  length: "Comprehensive"
```

## Tone Guidelines

### Appropriate Tone

```yaml
professional:
  - "Clear and direct"
  - "Respectful of time"
  - "Evidence-based"
  - "Solution-oriented"

not:
  - "Apologetic for every issue"
  - "Overly casual"
  - "Vague or ambiguous"
  - "Emotional"
```

### Language Patterns

✅ **Good Communication**:
- "I completed X. Here's the proof: [logs]."
- "I'm blocked on Y. I've tried A and B. Need your input on C."
- "Task T-001 is complete. Definition of done met. Ready for review."

❌ **Poor Communication**:
- "I think it's done."
- "Something's wrong."
- "I tried some stuff."

## Update Frequency

```yaml
frequency_guidelines:
  active_work:
    interval: "Every 15-30 minutes"
    content: "Progress update"

  idle_waiting:
    interval: "Every hour"
    content: "Still waiting for [input/resource]"

  completed_task:
    interval: "Immediately"
    content: "Completion update"

  blocked:
    interval: "Immediately"
    content: "Escalation update"
```

## Communication Channels

```yaml
channels:
  primary:
    location: "progress-log.md"
    purpose: "Complete work record"

  alerts:
    location: "Escalation entries in progress-log.md"
    purpose: "Items requiring immediate attention"

  summaries:
    location: "Daily summaries in progress-log.md"
    purpose: "Periodic overviews"

  notifications:
    method: "Per user configuration"
    purposes:
      - "Critical escalations"
      - "Task completions"
      - "Scheduled summaries"
```

## Formatting Standards

### Markdown Usage

```yaml
headers:
  h1: "Main sections (Task Complete, Escalation)"
  h2: "Subsections"
  h3: "Details within subsections"

emphasis:
  bold: "Key information, status indicators"
  italic: "Emphasis within sentences"
  code: "File names, commands, technical terms"

lists:
  bullets: "Items, steps"
  numbered: "Sequences, priorities"
  checkboxes: "Completion status"

code_blocks:
  use: "Logs, error messages, code snippets"
  language: "Specify language for syntax highlighting"

tables:
  use: "Comparisons, test results, metrics"
  format: "Consistent headers"

dividers:
  use: "--- between major sections"
```

### Status Indicators

```yaml
emoji_status:
  🟢 green: "Complete, success, good"
  🟡 yellow: "In progress, caution, waiting"
  🔴 red: "Blocked, error, critical"
  🔵 blue: "Information, neutral"
  ⚪ white: "Not started, clear"

text_status:
  COMPLETE: "Task finished successfully"
  IN_PROGRESS: "Actively working"
  BLOCKED: "Cannot proceed without input"
  PENDING: "Not started"
  FAILED: "Attempt failed, recovery in progress"
```

## Anti-Patterns

### ❌ The "Mystery Update"

```markdown
Update complete.

[What was done? What's the result? What's needed?]
```

### ❌ The "Over-Apologetic Update"

```markdown
So sorry, I know I'm probably doing this wrong,
but I tried to fix the thing and it didn't work,
I'm really sorry about this...
```

### ❌ The "Wall of Text"

```markdown
[500 words of unstructured text describing what happened]
```

### ❌ The "Update Without Evidence"

```markdown
✅ All tests passing

[But no test results shown]
```

## Verification

After communication:

```yaml
checklist:
  clarity:
    - [ ] "Recipient can understand what happened"
    - [ ] "Status is immediately clear"
    - [ ] "Next action is obvious (or explicitly stated)"

  completeness:
    - [ ] "All relevant information included"
    - [ ] "Evidence provided where applicable"
    - [ ] "Context sufficient for decision"

  actionability:
    - [ ] "If approval needed, options are clear"
    - [ ] "If blocked, what's needed is explicit"
    - [ ] "If complete, what's next is stated"
```

## Key Takeaway

**Good communication reduces cognitive load.** Structure, clarity, and evidence make collaboration effortless.

---

**Related Skills**: `progress-logging.md`, `task-autonomy.md`, `error-recovery.md`
