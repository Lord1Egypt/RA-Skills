# Progress Logging

> **Comprehensive, searchable logs for complete visibility into autonomous work**
> Priority: CRITICAL | Category: Observability

## Overview

When your agent works while you sleep, you need to wake up to a clear picture of what happened. This skill ensures comprehensive logging that replaces the need to scroll through chat history.

## The Problem

```yaml
scenario: "Agent works overnight"
user_expects: "Wake up, know what happened"
reality:
  - "Chat history compressed, context lost"
  - "Decisions made but not visible"
  - "Failures happened but unclear why"
  - "Progress made but not measurable"
```

## The Solution: Structured Progress Logs

### Progress Log Structure

`progress-log.md` should be a chronological, searchable record of all work:

```markdown
# Progress Log

## Statistics
- **Session Start**: [Date/Time]
- **Last Update**: [Date/Time]
- **Total Cycles**: [N]
- **Tasks Completed**: [N]
- **Tasks Failed**: [N]
- **Current Task**: [Task Name]

---

## [YYYY-MM-DD]

### [HH:MM] - Cycle #[N]: [Brief Title]
**Status**: completed | failed | in_progress | blocked
**Task**: [T-XXX] [Task Name]
**Agent**: [Agent Name]
**Model**: [Model Used]

#### Phase: RECONNAISSANCE
**Documentation Reviewed**:
- [Doc 1] - [Key finding]
- [Doc 2] - [Key finding]

**Existing Solutions Found**:
- [Solution 1] - [Relevance]

#### Phase: BUILD
**Changes Made**:
- [File 1]: [Brief description of change]
- [File 2]: [Brief description of change]

**Files Modified**:
```diff
[Optional diff summary]
```

#### Phase: TEST
**Tests Run**:

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| [Test name] | [Expected] | [Actual] | [Pass/Fail] |

**Test Evidence**:
```
[Log output or key results]
```

#### Phase: DECISION
**Outcome**: ITERATE | ESCALATE | CLOSE | RE-PLAN
**Reasoning**: [Why this decision]
**Evidence**: [What supports this decision]

#### Results
**Pass**: [N] tests
**Fail**: [N] tests
**Coverage**: [N]%

#### Next Action
- [ ] [Specific next step]

#### Artifacts Created
- [File/Artifact]: [Purpose]

---

### [HH:MM] - Task Completed: [Task Name]
**Task ID**: [T-XXX]
**Started**: [HH:MM]
**Completed**: [HH:MM]
**Duration**: [X minutes]
**Cycles**: [N]

**Summary**:
[What was accomplished]

**Definition of Done - Status**:
- [x] [Criteria 1] - Met
- [x] [Criteria 2] - Met
- [x] [Criteria 3] - Met

**Files Changed**:
- [File 1] (5 lines added, 2 removed)
- [File 2] (new file, 45 lines)

**Tests Status**:
- Passing: [N]
- Failing: [N]

**Lessons Learned**:
[What was discovered during this task]

---

### [HH:MM] - Escalation: [Brief Description]
**Task**: [T-XXX] [Task Name]
**Escalated At**: [HH:MM]

**What I Was Doing**:
[Task context]

**What Happened**:
[Issue description]

**What I Need**:
[Specific requirement from user]

**Context**:
```
[Relevant logs, error messages, state]
```

**Suggested Options**:
1. [Option 1]
2. [Option 2]

---

## Daily Summaries

### [YYYY-MM-DD] - Overnight Work Summary
**Work Period**: 22:00 - 06:00 (8 hours)
**Active Time**: [X hours]
**Tasks Completed**: [N]
**Tasks Failed**: [N]
**Cycles Executed**: [N]

#### Completed Tasks
1. **[T-XXX] [Task Name]** ([HH:MM]-[HH:MM], [X] min)
   [Brief description of what was done]

2. **[T-XXX] [Task Name]** ([HH:MM]-[HH:MM], [X] min)
   [Brief description of what was done]

#### Failed/Blocked Tasks
1. **[T-XXX] [Task Name]** - Blocked since [HH:MM]
   **Reason**: [Why blocked]

#### Issues Discovered
- [Issue 1] - [Impact]
- [Issue 2] - [Impact]

#### Metrics
- **Total Tokens Used**: [N]
- **Cost**: [$X.XX]
- **Average Task Duration**: [X] min
- **Success Rate**: [X]%

#### Ready for Review
- [ ] [Review item 1]
- [ ] [Review item 2]

---

## Morning Briefing Template

### Morning Briefing: [YYYY-MM-DD]

#### Overview
[One paragraph summary of overnight work]

#### What's Working ✅
- [Working item 1]
- [Working item 2]

#### What Needs Attention ⚠️
- [Issue 1] - [Suggested action]
- [Issue 2] - [Suggested action]

#### What's Blocked 🚫
- [Blocked task 1] - [What's needed]
- [Blocked task 2] - [What's needed]

#### Tasks Ready for Review 📋
1. [Task 1] - [Review notes]
2. [Task 2] - [Review notes]

#### Next Steps
1. [Immediate action needed]
2. [Today's priority]

#### Metrics
- Work completed: [N] tasks
- Success rate: [X]%
- Token usage: [N] ($X.XX)

---

## Patterns & Trends

### Success Patterns 🎯
[List patterns that led to success]

### Failure Patterns ❌
[List patterns that caused failures]

### Optimization Opportunities 💡
[List areas for improvement]

---

## Error Log

### [YYYY-MM-DD HH:MM] - [Error Type]
**Task**: [Task context]
**Error**: [Error message]
**Root Cause**: [What caused it]
**Resolution**: [How it was fixed]
**Prevention**: [How to prevent recurrence]

```

## Logging Rules

### WHEN to Log

```yaml
mandatory_logging:
  - "Every BUILD phase completion"
  - "Every TEST phase result"
  - "Every DECISION made"
  - "Every TASK completion"
  - "Every ESCALATION"
  - "Every ERROR encountered"

optional_logging:
  - "Intermediate progress notes"
  - "Thought process for complex decisions"
  - "Alternative approaches considered"
```

### WHAT to Log

```yaml
required_fields:
  timestamp: "Always ISO 8601 format"
  task_id: "T-XXX format"
  agent_name: "Which agent"
  model_used: "Which model"
  phase: "RECON | BUILD | TEST | DECISION"
  status: "completed | failed | blocked | escalated"

context_fields:
  duration: "How long it took"
  files_changed: "What was touched"
  tests_run: "What was tested"
  decision_reasoning: "Why this decision"
  evidence: "Supporting data"
```

### HOW to Log

```yaml
formatting:
  structure: "Consistent markdown hierarchy"
  timestamps: "Always at top of entry"
  separators: "Use --- between entries"
  tables: "For test results and comparisons"
  code_blocks: "For logs and errors"

accessibility:
  searchable: "Use consistent section headers"
  scannable: "Use tables and bullets"
  linkable: "Anchor IDs for sections"
  filterable: "Status tags in headers"
```

## Quick Reference Commands

```bash
# View today's progress
openclaw progress today

# View specific task
openclaw progress task T-XXX

# View failures only
openclaw progress --filter=failed

# View overnight summary
openclaw progress overnight

# Generate morning briefing
openclaw briefing

# Search logs
openclaw progress search "keyword"

# Export logs
openclaw progress export --format=json --from=2026-03-01
```

## Integration with Cron

### Overnight Progress Template

```bash
# Add to cron jobs for progress updates
openclaw cron add --name "log-progress-2am" \
  --cron "0 2 * * *" \
  --message "Update progress-log.md with current status"

openclaw cron add --name "log-progress-4am" \
  --cron "0 4 * * *" \
  --message "Update progress-log.md with current status"

openclaw cron add --name "morning-briefing" \
  --cron "0 7 * * *" \
  --message "Generate morning briefing in progress-log.md"
```

## Log Quality Standards

### Minimum Content Per Entry

```yaml
cycle_entry:
  required:
    - "Timestamp"
    - "Task reference"
    - "Phase completed"
    - "Decision/outcome"

  recommended:
    - "Duration"
    - "Files changed"
    - "Tests run"
    - "Reasoning"

completion_entry:
  required:
    - "Task ID"
    - "Start time"
    - "End time"
    - "Summary"
    - "Definition of done status"

  recommended:
    - "Files changed list"
    - "Test results"
    - "Lessons learned"
```

## Anti-Patterns

### ❌ The "Black Box" Log
```yaml
pattern: "Only logs 'task done' with no details"
problem: "No visibility into what happened"
fix: "Always include: what, how, why, result"
```

### ❌ The "Memory Dump"
```yaml
pattern: "Raw chat logs pasted without structure"
problem: "Unsearchable, unscannable"
fix: "Structure into phases and sections"
```

### ❌ The "Rose-Colored" Log
```yaml
pattern: "Only logging successes, hiding failures"
problem: "False sense of progress"
fix: "Always log failures with root cause analysis"
```

### ❌ The "Orphan" Log
```yaml
pattern: "Logging without linking to tasks"
problem: "Lost context"
fix: "Always reference task ID"
```

## Verification

After implementing this skill:

```bash
# Check log completeness
openclaw audit logs --completeness

# Verify log quality
openclaw audit logs --quality

# Test morning briefing
openclaw briefing --preview
```

## Key Takeaway

**Your morning coffee should be accompanied by a clear picture of overnight work.** Progress logs are your window into autonomous operations.

---

**Related Skills**: `task-autonomy.md`, `execution-discipline.md`, `cron-orchestration.md`
