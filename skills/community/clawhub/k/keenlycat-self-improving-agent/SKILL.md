---
name: self-improving-agent
description: Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects the agent's behavior, (3) Agent completes a complex task successfully, (4) Periodic review of past learnings.
---

# Self-Improving Agent

## Overview

This skill enables OpenClaw to continuously improve by capturing learnings from:
- Failed operations and errors
- User corrections and feedback
- Successful complex task completions
- Periodic review and consolidation

## When to Use

1. **Error Recovery**: When a command or operation fails unexpectedly
2. **User Correction**: When the user corrects the agent's behavior or output
3. **Success Capture**: After completing a complex task successfully
4. **Learning Review**: Periodic review of past learnings to consolidate knowledge

## Core Workflow

### 1. Capture Learning

When something noteworthy happens:

```
Type: error | correction | success | insight
Context: What was being attempted
Issue: What went wrong (for errors)
Correction: What should be done differently
Lesson: Generalizable takeaway
Tags: Relevant topics/skills
```

### 2. Store Learning

Learnings are stored in `memory/learnings.jsonl` with:
- Timestamp
- Type and severity
- Full context and details
- Tags for searchability

### 3. Retrieve Relevant Learnings

Before starting a task, search past learnings:
- Match by task type
- Match by tags
- Match by error patterns

### 4. Apply Learnings

Use retrieved learnings to:
- Avoid past mistakes
- Apply successful patterns
- Adjust approach based on corrections

## Memory Structure

Learnings are stored in JSONL format:

```json
{
  "timestamp": "2026-03-06T10:30:00Z",
  "type": "error",
  "severity": "high",
  "context": "Installing npm package globally",
  "issue": "Permission denied without sudo",
  "correction": "Use sudo for global installs or configure npm prefix",
  "lesson": "Always check if operation requires elevated privileges",
  "tags": ["npm", "permissions", "installation"],
  "taskSlug": "npm-global-install"
}
```

## Learning Types

| Type | When to Use | Example |
|------|-------------|---------|
| **error** | Operation failed | Command returned non-zero exit code |
| **correction** | User corrected behavior | "Don't use rm, use trash instead" |
| **success** | Complex task completed | Successfully deployed to production |
| **insight** | Discovered optimization | "This API is faster than alternatives" |

## Severity Levels

- **critical**: System-breaking errors, data loss risk
- **high**: Task-blocking errors, significant issues
- **medium**: Minor issues, workarounds available
- **low**: Optimization opportunities, nice-to-know

## Commands

### Capture a Learning

```bash
# Manual capture (for user corrections)
openclaw memory add-learning --type correction --context "..." --lesson "..."
```

### Search Learnings

```bash
# Search by keyword
openclaw memory search-learnings "npm permissions"

# Search by tag
openclaw memory search-learnings --tag npm

# Search by type
openclaw memory search-learnings --type error
```

### Review Learnings

```bash
# Review recent learnings
openclaw memory review-learnings --days 7

# Review by category
openclaw memory review-learnings --tag deployment
```

## Best Practices

1. **Capture Immediately**: Record learnings while context is fresh
2. **Be Specific**: Include full error messages and exact commands
3. **Generalize Lessons**: Extract principles that apply beyond this instance
4. **Tag Thoughtfully**: Use consistent tags for easy retrieval
5. **Review Regularly**: Weekly review helps consolidate knowledge
6. **Avoid Duplicates**: Check existing learnings before adding new ones

## Integration Points

- **Error Handlers**: Automatically capture command failures
- **User Feedback**: Listen for correction patterns in conversation
- **Task Completion**: Prompt for learning capture after complex tasks
- **Heartbeat**: Include learning review in periodic checks

## Example Scenarios

### Scenario 1: Command Failure

```
Context: Running `npm install -g package`
Issue: EACCES permission error
Correction: Run with sudo or configure npm prefix
Lesson: Check if global install requires elevated privileges
Tags: npm, permissions, installation
```

### Scenario 2: User Correction

```
Context: Suggested using `rm -rf` for cleanup
Correction: User prefers `trash` for safety
Lesson: Default to safe, reversible operations
Tags: safety, file-operations, user-preference
```

### Scenario 3: Success Pattern

```
Context: Deploying to VPS via SSH
Success: Used rsync with specific flags for reliability
Lesson: rsync -avz --delete is reliable for deployments
Tags: deployment, ssh, rsync, success
```

## Safety Rules

- Never store sensitive data (passwords, API keys, tokens)
- Sanitize error messages that might contain secrets
- Require user approval before storing corrections
- Allow users to delete or edit learnings
- Respect user privacy preferences
