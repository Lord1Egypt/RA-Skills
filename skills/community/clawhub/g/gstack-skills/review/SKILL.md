---
name: review
description: >
  Pre-merge code review tool. Analyzes SQL security, LLM trust boundaries, race conditions, 
  and structural issues. Automatically reviews git diff, identifies bugs, and provides fixes.
  Use when user says "review this PR", "code review", "pre-landing review", "check my diff", 
  or code is about to be merged.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [code, review, security, quality, git, pre-merge]
---

# Review - Pre-Merge Code Review Tool

Pre-merge PR review tool that analyzes code diffs and provides actionable feedback.

## When to Use This Skill

Use this skill when the user says:

- "review this PR"
- "code review"
- "pre-landing review"
- "check my diff"
- "review the current branch"
- "review my changes"
- Code is about to be merged

## How This Skill Works

This skill performs a systematic code review with automatic execution.

## Execution Workflow

### Step 0: Detect Base Branch

First, determine the base branch to compare against:

1. Check for existing PRs and get the target branch
2. If no PR exists, use the repository's default branch (usually `main` or `master`)
3. Verify the base branch exists locally or fetch it if needed

### Step 1: Branch Validation

Ensure conditions are met for a proper review:

1. **Verify not on base branch**: Current branch should be a feature branch, not main/master
2. **Check for changes**: Confirm there are actual differences to review
3. **Check git status**: Ensure working directory is clean or document uncommitted changes

If conditions aren't met:

```bash
# Check current branch
git branch --show-current

# Check for uncommitted changes
git status

# Show diff if exists
git diff HEAD
```

### Step 2: Scope Drift Detection

Compare the original task/intent with actual code changes:

1. Review the task description or commit message
2. Analyze the actual files changed
3. Identify:
   - **Scope creep**: Changes beyond the original task
   - **Missing requirements**: Intended changes not implemented
   - **Unexpected additions**: Changes that weren't planned

Report any scope drift issues before proceeding.

### Step 3: Load Review Checklist

Load the review checklist if it exists:

```
# Check for review checklist
REVIEW_CHECKLIST.md
.code-review-checklist.md
docs/review-checklist.md
```

Use the checklist to ensure all review points are covered.

### Step 4: Get the Diff

Generate a comprehensive git diff:

```bash
# Get full diff against base branch
git diff origin/main...HEAD

# Or with commit range
git diff <base-branch>...HEAD
```

Parse the diff to understand:
- Files changed (added, modified, deleted)
- Lines added/removed
- Types of changes (logic, tests, docs, config)

### Step 5: Two-Phase Review

Perform review in two phases:

#### Phase 1: Critical Issues (Must Fix)

Review for critical issues that must be addressed:

1. **SQL Security**
   - Check for SQL injection vulnerabilities
   - Verify parameterized queries
   - Ensure proper escaping of user input
   - Review database access patterns

2. **Race Conditions**
   - Identify concurrent access issues
   - Check for missing locks/transactions
   - Verify atomic operations
   - Review state mutations

3. **LLM Trust Boundaries**
   - Check for prompt injection risks
   - Verify input validation
   - Ensure output sanitization
   - Review data flow to/from LLMs

4. **Enum Completeness**
   - Check switch/case statements cover all cases
   - Verify enum values are handled
   - Look for default case handling

5. **Authentication/Authorization**
   - Check permission checks
   - Verify session management
   - Review API security
   - Ensure proper authentication

#### Phase 2: Informational Issues (Should Fix)

Review for quality improvements:

1. **Conditional Side Effects**
   - Check for side effects in conditions
   - Identify hidden mutations
   - Review function purity

2. **Magic Numbers**
   - Identify hardcoded values
   - Suggest named constants
   - Document special values

3. **Dead Code**
   - Find unused variables/functions
   - Identify commented-out code
   - Remove unreachable code

4. **Test Coverage**
   - Check for missing tests
   - Verify test quality
   - Suggest edge cases

5. **Performance Issues**
   - Identify N+1 queries
   - Check for unnecessary loops
   - Review algorithm complexity
   - Suggest optimizations

### Step 6: Design Review (Conditional)

If frontend/UI files were changed, perform design review:

1. Compare against design documents if available
2. Check for:
   - Design system adherence
   - Accessibility compliance
   - Responsive design
   - User experience issues
   - Visual consistency

### Step 7: Provide Fixes

For issues found, categorize and provide fixes:

#### AUTO-FIX Level

Automatically fix mechanical issues:

- Code formatting
- Simple logic errors
- Unused imports/variables
- Basic security fixes

#### ASK Level

Require user confirmation for complex changes:

- Design decisions
- Refactoring suggestions
- Breaking changes
- Architectural concerns

**Example feedback format:**

```markdown
## Critical Issues

### 1. SQL Injection Risk
**File**: `src/db/queries.py:42`
**Severity**: 🔴 Critical
**Status**: ❌ Must Fix

```python
# Current (Vulnerable)
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# Suggested Fix
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))
```

**Reason**: Direct string interpolation allows SQL injection attacks.

---

### 2. Missing Authentication Check
**File**: `src/api/routes.py:87`
**Severity**: 🔴 Critical
**Status**: ❌ Must Fix

The `/admin/delete` endpoint lacks authentication.

**Suggested Fix**:
```python
@app.delete("/admin/delete")
@require_auth  # Add this decorator
def delete_item():
```

---

## Informational Issues

### 1. Magic Number
**File**: `src/config.py:15`
**Severity**: 🟡 Medium
**Status**: 💡 Should Fix

```python
# Current
MAX_RETRIES = 3

# Suggested
MAX_RETRIES = 3  # Retry 3 times before giving up
```

---

## Auto-Fixes Applied

1. ✅ Fixed 2 unused imports in `src/utils/helpers.py`
2. ✅ Formatted `src/models/user.py` with black
3. ✅ Added missing semicolons in `src/styles/main.css`
```

### Step 8: Generate Review Status

Assign a final status to the review:

- **DONE**: Review complete, code can merge
- **DONE_WITH_CONCERNS**: Review complete, but has concerns to monitor
- **BLOCKED**: Cannot proceed, blocking issues exist
- **NEEDS_CONTEXT**: Need more information to complete review

### Step 9: Output Review Report

Generate a comprehensive review report:

```markdown
# Code Review Report

## Review Summary
- **Branch**: `feature/user-authentication`
- **Base**: `main`
- **Files Changed**: 12 files
- **Lines Added**: +342
- **Lines Removed**: -89
- **Status**: ✅ DONE

## Critical Issues: 2
1. SQL Injection Risk - ❌ Must Fix
2. Missing Authentication - ❌ Must Fix

## Informational Issues: 5
1. Magic Number - 💡 Should Fix
2. Dead Code - 💡 Should Fix
3. Missing Tests - 💡 Should Fix
4. Performance Issue - 💡 Should Fix
5. Documentation - 💡 Should Fix

## Auto-Fixes Applied: 3
1. ✅ Fixed unused imports
2. ✅ Formatted code
3. ✅ Fixed typos

## Design Review
✅ No design issues found

## Recommendations
1. Address critical SQL injection vulnerability
2. Add authentication to admin endpoint
3. Increase test coverage to 80%+
4. Remove unused code in `src/utils/legacy.py`

## Next Steps
1. Fix critical issues
2. Re-run review
3. Proceed to /qa for testing
```

## Safety Checks

Before making any automatic fixes:

1. **Create backup**: Document current state
2. **Review changes**: Show what will be changed
3. **Get confirmation**: Ask user before applying fixes
4. **Preserve logic**: Ensure fixes don't break functionality

## Integration with Other Skills

This skill integrates with:

- **office-hours**: Earlier in workflow, for planning
- **qa**: Next in workflow, for testing fixes
- **ship**: Final step, for merging and deploying

## Boil the Lake Principle

> "Don't be half-invested, boil the whole lake"

- **Don't just report bugs, fix them**: When issues are found, actually fix them
- **Complete the task**: A review isn't done until issues are addressed
- **No "good enough"**: Pursue 100% quality with AI assistance

## Review Checklist Template

Use this checklist to ensure thorough reviews:

```markdown
## Code Review Checklist

### Security
- [ ] SQL injection checks
- [ ] XSS prevention
- [ ] Authentication/authorization
- [ ] Input validation
- [ ] Output sanitization

### Functionality
- [ ] Logic correctness
- [ ] Edge cases handled
- [ ] Error handling
- [ ] Data validation

### Code Quality
- [ ] Naming conventions
- [ ] Code organization
- [ ] Comments where needed
- [ ] DRY principle followed

### Performance
- [ ] No N+1 queries
- [ ] Efficient algorithms
- [ ] Proper caching
- [ ] Resource cleanup

### Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Edge cases covered
- [ ] Test quality

### Documentation
- [ ] README updated
- [ ] API docs updated
- [ ] Changes documented
- [ ] Deprecation noted
```

## Error Handling

If review fails:

1. **Check git status**: Ensure repo is in valid state
2. **Verify branch**: Confirm branch tracking is correct
3. **Check permissions**: Ensure file access is available
4. **Provide clear error messages**: Explain what went wrong and how to fix

## Example Usage

**User**: `/review my current branch`

**AI**: I'll review your current branch changes.

[Executes review workflow]

**Output**: Comprehensive review report with identified issues and fixes

**User**: Fix the critical issues

**AI**: Applying fixes...

[Applies auto-fixes]

**Output**: Updated review report with fixes applied, suggests next step: `/qa`

---

**Original**: gstack/review by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version with automated execution  
**Version**: 2.0.0
