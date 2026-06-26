# Scope Control & Boundaries

> **Define and enforce operational boundaries to prevent catastrophic errors**
> Priority: CRITICAL | Category: Safety

## Overview

A common agent failure mode is "mission creep" - making changes beyond the assigned task, editing files it shouldn't, or making architectural decisions without authority. This skill enforces strict boundaries.

## The Problem

```yaml
examples:
  - "Task: Fix login bug → Result: Rewrote entire auth system"
  - "Task: Add one field → Result: Refactored database schema"
  - "Task: Update config → Result: Changed system architecture"
  - "Task: Small fix → Result: Broke unrelated module"
```

## The Solution: Explicit Boundaries

### Boundary Declaration Template

Before ANY task, agent must declare scope:

```markdown
# Scope Declaration: [Task Name]

## Authorized Scope
**Task**: [Clear, bounded task description]
**Files**: [Explicit list of files that may be touched]
**Changes**: [Explicit list of permitted changes]

## Explicit Boundaries

### File Boundaries
**MAY MODIFY**:
- [path/to/file1] - [Specific changes permitted]
- [path/to/file2] - [Specific changes permitted]

**MAY READ ONLY**:
- [path/to/file3] - [For context only]
- [path/to/file4] - [For reference only]

**MUST NOT TOUCH**:
- [path/to/file5] - [Reason: out of scope]
- [path/to/file6] - [Reason: production config]

### Change Boundaries
**PERMITTED**:
- [Specific change type 1]
- [Specific change type 2]

**PROHIBITED**:
- [Change type 1] - [Reason]
- [Change type 2] - [Reason]

### Architectural Boundaries
**MAY NOT**:
- Change data structures
- Modify API contracts
- Alter system architecture
- Change deployment configuration

**REQUIRES APPROVAL FOR**:
- New dependencies
- Database migrations
- API changes
- Breaking changes

## Definition of Done
1. [Specific criterion 1]
2. [Specific criterion 2]
3. [Specific criterion 3]

## Out of Scope Handling
If task requires going beyond declared scope:
1. STOP immediately
2. Document what's needed
3. Create new task for expanded scope
4. Get approval before proceeding

## Confirmation
✓ I understand these boundaries
✓ I will not exceed them without explicit approval
✓ I will escalate if scope needs expansion
```

## Boundary Categories

### 1. File System Boundaries

```yaml
safe_zones:
  - "workspace/src/feature-xyz/"  # Task-specific code
  - "workspace/tests/test-xyz/"   # Related tests
  - "workspace/docs/feature-xyz/" # Feature docs

restricted_zones:
  - "workspace/config/"           # Requires approval
  - "package.json"                # Requires approval
  - "Dockerfile"                  # Requires approval
  - ".env*"                       # NEVER touch

forbidden_zones:
  - "system/"                     # System files
  - "/etc/"                       # OS configuration
  - "../other-project/"           # Other projects
  - "node_modules/"               # Dependencies
```

### 2. Change Type Boundaries

```yaml
permitted_changes:
  - "Add new functions in target module"
  - "Fix bugs in target module"
  - "Update related tests"
  - "Update feature documentation"

requires_approval:
  - "Add new dependencies"
  - "Change function signatures"
  - "Modify database schema"
  - "Change API endpoints"
  - "Update build configuration"

forbidden_changes:
  - "Refactor unrelated code"
  - "Change project structure"
  - "Modify other features"
  - "Change deployment settings"
```

### 3. Architectural Boundaries

```yaml
within_scope:
  - "Implement feature as specified"
  - "Follow existing patterns"
  - "Use established libraries"

requires_architect_approval:
  - "Introduce new patterns"
  - "Change architectural approach"
  - "Modify system boundaries"
  - "Change technology choices"
```

### 4. Time/Resource Boundaries

```yaml
time_limits:
  max_duration: "2 hours"
  max_iterations: "3"
  escalation_point: "If not progressing after 30 minutes"

resource_limits:
  max_tokens: "100,000"
  max_api_calls: "50"
  max_files_modified: "5"
```

## Scope Creep Detection

### Warning Signs

```yaml
indicators_of_scope_creep:
  - "Editing files not in original scope"
  - "Making 'nice to have' improvements"
  - "Refactoring 'while I'm here'"
  - "Adding features not requested"
  - "Changing architecture"
  - "Introducing new dependencies"
```

### Detection Protocol

Every 15 minutes, agent must check:

```python
def check_scope_compliance():
    """
    Verify current work matches declared scope
    """
    questions = [
        "Am I editing files in the MAY MODIFY list?",
        "Am I making changes in the PERMITTED list?",
        "Am I staying within architectural boundaries?",
        "Have I introduced any side effects?",
        "Am I still working toward the original goal?"
    ]

    for question in questions:
        if answer_is_no(question):
            return SCOPE_VIOLATION_DETECTED

    return SCOPE_COMPLIANT
```

### When Scope Creep Detected

```yaml
immediate_actions:
  1: "STOP all changes"
  2: "Document what was done beyond scope"
  3: "Assess if changes should be reverted"
  4: "Create separate task for expanded scope"
  5: "Escalate for guidance"

decision_tree:
  revert_if:
    - "Changes are broken"
    - "Changes conflict with task"
    - "Changes weren't necessary"

  keep_if:
    - "Changes are necessary for task"
    - "Changes improve implementation"
    - "User approves expanded scope"
```

## Examples

### Example 1: Properly Scoped Task

```markdown
# Scope Declaration: Fix Login Validation

## Authorized Scope
**Task**: Fix email validation in login form to reject invalid formats
**Files**: src/auth/login.js, tests/auth/login.test.js
**Changes**: Add email validation regex, update tests

## Explicit Boundaries

### File Boundaries
**MAY MODIFY**:
- src/auth/login.js - Add validation only
- tests/auth/login.test.js - Add test cases

**MAY READ ONLY**:
- src/auth/validation.js - For reference on existing patterns

**MUST NOT TOUCH**:
- src/auth/auth.js - Authentication logic
- src/auth/session.js - Session management
- package.json - No new dependencies

### Change Boundaries
**PERMITTED**:
- Add email validation function
- Update login to use validation
- Add tests for validation

**PROHIBITED**:
- Change authentication flow
- Modify session handling
- Add new dependencies
- Change API contract

## Definition of Done
1. Email validation rejects invalid formats
2. Valid emails still work
3. Tests pass (new + existing)
4. No other login behavior changed
```

### Example 2: Scope Violation

```yaml
original_task: "Fix login validation"

what_happened:
  - "Fixed validation (✓ in scope)"
  - "Refactored auth module (✗ NOT in scope)"
  - "Added password strength checker (✗ NOT in scope)"
  - "Changed session timeout (✗ NOT in scope)"
  - "Updated to latest auth library (✗ NOT in scope)"

result:
  - "Multiple systems broken"
  - "Unexpected side effects"
  - "Deployment delayed"
  - "Rollback required"
```

## Pre-Task Checklist

Before starting any task:

```yaml
scope_checklist:
  definition:
    - [ ] "Task is clearly defined"
    - [ ] "Success criteria are explicit"
    - [ ] "Boundaries are documented"

  files:
    - [ ] "Files that may be modified listed"
    - [ ] "Files that are read-only identified"
    - [ ] "Files that must not be touched marked"

  changes:
    - [ ] "Permitted changes enumerated"
    - [ ] "Prohibited changes listed"
    - [ ] "Approval requirements clear"

  constraints:
    - [ ] "Time limits set"
    - [ ] "Resource limits defined"
    - [ ] "Escalation points identified"
```

## Mid-Task Checkpoint

Every 30 minutes during task:

```yaml
checkpoint_questions:
  1: "Am I still working on the original task?"
  2: "Are all file changes in scope?"
  3: "Have I introduced any side effects?"
  4: "Am I within time/resource limits?"
  5: "Do I need to update scope declaration?"

trigger_escalation_if:
  - "Answer to any checkpoint is 'no'"
  - "Discovered requirement to expand scope"
  - "Approach needs fundamental change"
  - "Blocker encountered"
```

## Post-Task Validation

After completing task:

```yaml
validation_questions:
  scope_compliance:
    - "Did I only modify permitted files?"
    - "Did I only make permitted changes?"
    - "Did I stay within architectural boundaries?"

  impact_assessment:
    - "What changed?"
    - "What stayed the same?"
    - "Any unexpected side effects?"
    - "Any systems affected beyond scope?"

  cleanup:
    - "Revert any out-of-scope changes"
    - "Document any necessary scope expansions"
    - "Create tasks for discovered but out-of-scope work"
```

## Emergency Scope Violation Recovery

If agent realizes it violated scope:

```yaml
immediate_actions:
  1: "STOP all work"
  2: "Document all changes made"
  3: "Assess impact of out-of-scope changes"
  4: "Create rollback plan"
  5: "Escalate with full context"

escalation_template: |
  SCOPE VIOLATION DETECTED

  Original Task: [Task description]
  Declared Scope: [What was authorized]

  What I Did:
  - [Change 1 - in scope]
  - [Change 2 - OUT of scope]
  - [Change 3 - OUT of scope]

  Impact Assessment:
  - [What broke]
  - [What's affected]
  - [Risk level]

  Proposed Actions:
  1. [Rollback plan]
  2. [Corrective approach]

  Awaiting Guidance.
```

## Verification

```bash
# Check scope compliance
openclaw audit scope --last-task

# Verify no out-of-scope changes
openclaw diff --scope-check

# Test scope enforcement
openclaw test scope-enforcement
```

## Key Takeaway

**Good agents do exactly what's asked. Great agents do exactly what's asked and nothing more.** Scope boundaries are not limitations - they're safety rails.

---

**Related Skills**: `docs-first.md`, `execution-discipline.md`, `security-hardening.md`
