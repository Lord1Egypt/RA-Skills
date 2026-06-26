# Error Recovery

> **Graceful failure handling and systematic recovery strategies**
> Priority: HIGH | Category: Resilience

## Overview

Autonomous agents will encounter errors. The difference between toy and production is how gracefully they handle failures and how systematically they recover.

## Error Categories

### 1. Transient Errors

```yaml
category: "Temporary issues that resolve with retry"
examples:
  - "Network timeout"
  - "API rate limit exceeded"
  - "Service temporarily unavailable"
  - "Resource contention"

handling_strategy: "Retry with exponential backoff"
max_retries: 3
backoff_schedule:
  - "Wait 5 seconds"
  - "Wait 15 seconds"
  - "Wait 30 seconds"
  - "Escalate after 3rd failure"
```

### 2. Configuration Errors

```yaml
category: "Incorrect settings or missing credentials"
examples:
  - "Invalid API key"
  - "Missing environment variable"
  - "Incorrect endpoint URL"
  - "Wrong permission"

handling_strategy: "Stop and escalate"
recovery: "User intervention required"
prevention: "Validate config at session start"
```

### 3. Dependency Errors

```yaml
category: "Missing or incompatible dependencies"
examples:
  - "Package not installed"
  - "Version conflict"
  - "Missing system dependency"

handling_strategy: "Attempt auto-fix, escalate if fails"
recovery_steps:
  1: "Identify missing dependency"
  2: "Attempt installation (if permission allows)"
  3: "Verify installation"
  4: "Retry operation"
  5: "Escalate if installation fails"
```

### 4. Logic Errors

```yaml
category: "Code bugs or incorrect assumptions"
examples:
  - "Null reference"
  - "Type mismatch"
  - "Incorrect algorithm"
  - "Edge case not handled"

handling_strategy: "Log, analyze, attempt fix, re-test"
recovery_steps:
  1: "Capture full error context"
  2: "Analyze root cause"
  3: "Propose fix"
  4: "Implement fix"
  5: "Test fix"
  6: "If fails, escalate"
```

### 5. Scope Errors

```yaml
category: "Attempting operations beyond permissions"
examples:
  - "Access denied"
  - "File permission error"
  - "Operation not allowed"

handling_strategy: "Stop, log, escalate"
recovery: "User approval required for expanded scope"
prevention: "Check permissions before operation"
```

## Error Handling Protocol

### Phase 1: Error Capture

```yaml
when_error_occurs:
  immediate_actions:
    1: "STOP current operation"
    2: "Capture full error message"
    3: "Capture stack trace (if applicable)"
    4: "Capture system state"
    5: "Capture context (what was being attempted)"

  required_information:
    - "Error type and code"
    - "Full error message"
    - "Stack trace or location"
    - "Operation being performed"
    - "Input data that caused error"
    - "System state at error time"
    - "Recent operations that may have contributed"
```

### Error Documentation Template

```markdown
# Error Log: [Descriptive Title]

**Timestamp**: [ISO 8601]
**Error Type**: [Category]
**Severity**: [Critical | High | Medium | Low]
**Task**: [Task ID and name]

## Error Details

**Message**: [Full error message]
**Code**: [Error code if applicable]
**Location**: [File, line, function]

**Stack Trace**:
```
[Full stack trace]
```

## Context

**What I Was Doing**:
[Task description]

**Operation Being Performed**:
[Specific operation]

**Input Data**:
```json
[Input that caused error]
```

**System State**:
- [State item 1]
- [State item 2]

## Root Cause Analysis

**Initial Assessment**: [What caused this]

**Contributing Factors**:
- [Factor 1]
- [Factor 2]

**Confirmation**: [How to verify root cause]

## Impact Assessment

**What Broke**: [What stopped working]
**What Still Works**: [What's still functional]
**Dependencies Affected**: [What else is impacted]

## Recovery Attempt

**Strategy**: [Recovery approach]
**Steps Taken**:
1. [Step 1]
2. [Step 2]

**Result**: [Success | Failed | Partial]

## Next Actions

- [ ] [Action 1]
- [ ] [Action 2]

**Escalation Required**: [Yes | No]
**If Yes**: [What's needed from user]
```

### Phase 2: Error Classification

```python
def classify_error(error):
    """
    Determine error category and appropriate handling
    """
    if is_transient(error):
        return {
            'category': 'TRANSIENT',
            'action': 'RETRY',
            'max_attempts': 3,
            'backoff': [5, 15, 30]
        }

    elif is_configuration_error(error):
        return {
            'category': 'CONFIGURATION',
            'action': 'ESCALATE',
            'reason': 'User intervention required'
        }

    elif is_dependency_error(error):
        return {
            'category': 'DEPENDENCY',
            'action': 'ATTEMPT_FIX',
            'max_attempts': 1,
            'then': 'ESCALATE'
        }

    elif is_logic_error(error):
        return {
            'category': 'LOGIC',
            'action': 'ANALYZE_AND_FIX',
            'max_iterations': 2
        }

    elif is_scope_error(error):
        return {
            'category': 'SCOPE',
            'action': 'STOP_AND_ESCALATE',
            'reason': 'Permission expansion required'
        }

    else:
        return {
            'category': 'UNKNOWN',
            'action': 'ESCALATE',
            'reason': 'Requires investigation'
        }
```

### Phase 3: Recovery Strategy

```yaml
recovery_strategies:
  retry_with_backoff:
    when: "Transient errors"
    process:
      1: "Wait specified backoff time"
      2: "Retry operation"
      3: "If fails again, increase backoff"
      4: "After max retries, escalate"

    log_each: "Yes"
    track_attempts: "Yes"

  attempt_fix:
    when: "Dependency errors, some logic errors"
    process:
      1: "Analyze error"
      2: "Identify potential fix"
      3: "Implement fix"
      4: "Test fix"
      5: "If works, document in LESSONS.md"
      6: "If fails, escalate"

    safety: "Conservative changes only"
    rollback: "Always have rollback plan"

  escalate:
    when: "Configuration errors, scope errors, unknown errors"
    process:
      1: "Document full error context"
      2: "Document attempted fixes (if any)"
      3: "Identify what's needed from user"
      4: "Propose options if possible"
      5: "Create escalation ticket in Todo.md"

    format: "Structured escalation with all context"
    priority: "Based on error severity"
```

### Phase 4: Post-Recovery

```yaml
after_recovery:
  on_success:
    - "Document fix in LESSONS.md"
    - "Update relevant documentation"
    - "Add prevention check if applicable"
    - "Resume work with new knowledge"

  on_failure:
    - "Document all attempts"
    - "Identify why recovery failed"
    - "Escalate with full context"
    - "Mark task as blocked"
    - "Move to next task if possible"
```

## Escalation Protocol

### When to Escalate

```yaml
escalation_triggers:
  immediate:
    - "Security issue detected"
    - "Data loss risk"
    - "Production system impact"
    - "Scope violation detected"

  after_attempts:
    - "3 retries on transient error"
    - "1 failed fix attempt on logic error"
    - "Any configuration error"
    - "Any scope error"

  after_time:
    - "Blocked for >30 minutes on same error"
    - "Task not progressing for >1 hour"
```

### Escalation Message Template

```markdown
# ESCALATION REQUIRED: [Brief Description]

**Severity**: [Critical | High | Medium | Low]
**Timestamp**: [ISO 8601]
**Task**: [Task ID and name]
**Agent**: [Agent name]

## What I Was Doing

[Clear description of the task being performed]

## What Happened

**Error**: [Error message]
**Type**: [Error category]
**Impact**: [What's affected]

### Error Details
```
[Full error details, stack trace, etc.]
```

## What I Tried

### Attempt 1: [Strategy]
- **Action**: [What was done]
- **Result**: [What happened]
- **Duration**: [How long it took]

### Attempt 2: [Strategy]
- **Action**: [What was done]
- **Result**: [What happened]
- **Duration**: [How long it took]

## What I Need

**Specific Requirement**: [Exactly what's needed]

**Options I Can See**:
1. [Option A] - [Pros/cons]
2. [Option B] - [Pros/cons]

**Recommended Action**: [What I think should happen]

## Context

**Relevant Files**: [What's involved]
**Recent Changes**: [What might have contributed]
**System State**: [Current state]

**Blocker For**:
- [Task 1] - [Why]
- [Task 2] - [Why]

## Attachments

- [progress-log.md excerpt]
- [Error logs]
- [Relevant code snippets]

---

**Waiting for user input to proceed**
```

## Prevention Strategies

### Error Prevention Checklist

```yaml
before_operation:
  validation:
    - [ ] "Preconditions verified"
    - [ ] "Dependencies available"
    - [ ] "Permissions sufficient"
    - [ ] "Configuration valid"
    - [ ] "Resources available"

  contingency:
    - [ ] "Rollback plan defined"
    - [ ] "Error handling in place"
    - [ ] "Monitoring configured"
    - [ ] "Escalation path clear"
```

### Learning from Errors

```yaml
post_error_learning:
  lesson_capture:
    filename: "LESSONS.md"
    format: "Error pattern documentation"

    content:
      - "Error pattern"
      - "Root cause"
      - "Prevention measures"
      - "Quick fix for next time"

  prevention_updates:
    - "Update checks in relevant skills"
    - "Add validation to prevent recurrence"
    - "Update documentation with known issues"

  process_improvement:
    - "Identify if protocol needs update"
    - "Check if other skills affected"
    - "Share learning across skills"
```

## Error Recovery Examples

### Example 1: Transient Error - Success

```yaml
scenario: "API timeout while fetching user data"

attempt_1:
  action: "Direct API call"
  result: "Timeout after 30s"
  decision: "Transient error, retry"

attempt_2:
  action: "Retry with 5s backoff"
  result: "Timeout after 30s"
  decision: "Retry with longer backoff"

attempt_3:
  action: "Retry with 15s backoff"
  result: "Success, data received"
  decision: "Document and continue"

lesson_learned:
  pattern: "External API can be slow"
  prevention: "Use longer timeout initially"
  location: "LESSONS.md - API Patterns"
```

### Example 2: Logic Error - Recovery

```yaml
scenario: "Null reference error in user processing"

error_capture:
  error: "TypeError: Cannot read property 'id' of null"
  location: "UserProcessor.js:45"
  context: "Processing user from API"

analysis:
  root_cause: "API returned null for missing user"
  assumption: "User always exists"
  reality: "User can be null"

recovery:
  attempt_1:
    action: "Add null check before accessing user.id"
    test: "Test with null user"
    result: "Success, handled gracefully"

  documentation:
    lesson: "Always validate API responses"
    update: "Add input validation to all API handlers"
    location: "LESSONS.md - API Handling Patterns"
```

### Example 3: Scope Error - Escalation

```yaml
scenario: "Permission denied writing to config file"

error_capture:
  error: "EACCES: permission denied, open '/etc/app/config.json'"
  attempted: "Writing configuration update"

analysis:
  root_cause: "Agent doesn't have write permissions to /etc/"
  category: "Scope error"
  requires: "Elevated permissions or alternative approach"

escalation:
  message: "Need to update system config but lack permissions"

  options:
    1: "Provide sudo access (security risk)"
    2: "Use user-local config instead"
    3: "User performs manual update"

  recommendation: "Option 2 - Use user-local config"

  waiting_for: "User decision on approach"
```

## Key Takeaway

**Errors are inevitable. Catastrophes are optional.** Systematic error recovery turns failures into learning opportunities.

---

**Related Skills**: `execution-discipline.md`, `scope-control.md`, `security-hardening.md`
