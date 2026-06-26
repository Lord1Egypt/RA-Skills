# gstack-skills Usage Guide

Complete guide for using gstack-skills with OpenClaw/WorkBuddy.

## Installation

### Option 1: Copy to OpenClaw/WorkBuddy Skills Directory

```bash
# Clone or download the repository
cd gstack-openclaw-skills

# Copy to OpenClaw skills directory
cp -r gstack-skills ~/.openclaw/skills/

# Or for WorkBuddy
cp -r gstack-skills ~/.workbuddy/skills/
```

### Option 2: Create Symbolic Link

```bash
# Create symbolic link for development
ln -s /path/to/gstack-openclaw-skills/gstack-skills ~/.openclaw/skills/gstack-skills
```

### Option 3: Use as a Project Skill

Copy the entire `gstack-skills` directory to your project root:

```bash
cp -r gstack-skills/ /path/to/your/project/
```

## Quick Start

### 1. Basic Command Usage

Once installed, you can use any gstack command directly:

```python
# Example 1: Product ideation
user: "/office-hours I have an idea for an AI code reviewer"

# Example 2: Code review
user: "/review my current branch"

# Example 3: Deployment
user: "/ship the user authentication feature"
```

### 2. Interactive Help

Get help and see all available commands:

```python
user: "/gstack"

# AI will show:
# Available gstack commands:
# /office-hours - Product ideation and validation
# /plan-ceo-review - CEO perspective planning
# /plan-eng-review - Engineering architecture review
# /review - Pre-merge code review
# /qa - Test application and fix bugs
# /ship - Automated release workflow
# ... (and more)
```

## Common Workflows

### Workflow 1: New Feature Development

Complete lifecycle for developing a new feature:

```python
# Step 1: Validate the idea
user: "/office-hours I want to add user profiles to my app"

# AI will guide through YC's 6 questions:
# 1. What is the user's pain point?
# 2. How does your solution solve it?
# 3. Why aren't existing solutions good enough?
# 4. Can you reach these users?
# 5. Will people pay?
# 6. How will users discover it?

# Step 2: CEO perspective review
user: "/plan-ceo-review the user profiles feature"

# AI will analyze from CEO perspective:
# - Strategic alignment
# - Market opportunity
# - Resource requirements
# - Risk assessment

# Step 3: Engineering architecture review
user: "/plan-eng-review user profiles architecture"

# AI will review technical aspects:
# - Database design
# - API structure
# - Security considerations
# - Scalability

# Step 4: Implement the feature
[Developer writes code]

# Step 5: Code review
user: "/review my current branch"

# AI will:
# - Analyze git diff
# - Check for security issues
# - Identify bugs
# - Provide fixes

# Step 6: QA testing
user: "/qa the user profiles feature"

# AI will:
# - Run tests
# - Check for bugs
# - Fix issues found
# - Generate test report

# Step 7: Deploy
user: "/ship user profiles to production"

# AI will:
# - Merge base branch
# - Run all tests
# - Create PR
# - Update version
# - Deploy
```

### Workflow 2: Bug Investigation

When a bug is reported:

```python
# Step 1: Investigate root cause
user: "/investigate the login bug users are reporting"

# AI will:
# - Analyze error logs
# - Trace code execution
# - Identify root cause
# - Propose fixes

# Step 2: Review fix
user: "/review the login bug fix"

# AI will review the fix:
# - Check for regressions
# - Verify security
# - Test edge cases

# Step 3: Test fix
user: "/qa the login bug fix"

# AI will:
# - Run tests
# - Verify fix works
# - Check for side effects

# Step 4: Deploy fix
user: "/ship the login bug fix"
```

### Workflow 3: Quick Code Review

Fast code review for daily work:

```python
# Simple branch review
user: "/review"

# Review with context
user: "/review I added user authentication"

# Review specific file
user: "/review check the auth middleware"
```

## Advanced Usage

### Workflow State Management

Track state across multiple commands:

```python
# Start a workflow
user: "/gstack start workflow for user profiles"

# AI creates workflow ID: abc12345

# Each skill can reference this workflow
user: "/office-hours (workflow: abc12345)"
user: "/plan-eng-review (workflow: abc12345)"
user: "/review (workflow: abc12345)"
```

### Command Shortcuts

Use keyword detection instead of explicit commands:

```python
# These all trigger /office-hours
user: "brainstorm ideas for user profiles"
user: "I have an idea for a new feature"
user: "help me think through this problem"

# These all trigger /review
user: "review my code"
user: "check my diff"
user: "review the current branch"

# These all trigger /ship
user: "deploy to production"
user: "push to main"
user: "create a PR"
```

### Combining Skills

Use multiple skills together:

```python
# Validate idea + architecture review
user: "/office-hours and /plan-eng-review for payment processing"

# Code review + QA
user: "/review and /qa the shopping cart feature"

# Full workflow
user: "/gstack full workflow: /office-hours → /plan-eng-review → /review → /qa → /ship"
```

## Command Reference

### Product Ideation

| Command | Purpose | Example |
|---------|---------|---------|
| `/office-hours` | Validate product ideas | "/office-hours I want to build a..." |
| `/plan-ceo-review` | CEO perspective | "/plan-ceo-review feature X" |
| `/plan-eng-review` | Architecture review | "/plan-eng-review API design" |
| `/plan-design-review` | Design review | "/plan-design-review UI changes" |

### Development

| Command | Purpose | Example |
|---------|---------|---------|
| `/review` | Code review | "/review my changes" |
| `/investigate` | Debugging | "/investigate the crash bug" |
| `/design-consultation` | Design help | "/design-consultation color scheme" |

### Testing & Deployment

| Command | Purpose | Example |
|---------|---------|---------|
| `/qa` | Test and fix | "/qa the new feature" |
| `/qa-only` | Bug report only | "/qa-only checkout flow" |
| `/ship` | Deploy | "/ship feature to main" |

### Documentation

| Command | Purpose | Example |
|---------|---------|---------|
| `/document-release` | Update docs | "/document-release API changes" |
| `/retro` | Team retrospective | "/retro this week's work" |

### Power Tools

| Command | Purpose | Example |
|---------|---------|---------|
| `/codex` | Second opinion | "/codex review this code" |
| `/careful` | Safety warnings | "/careful before deleting DB" |
| `/freeze` | Lock edits | "/freeze only edit src/auth/" |
| `/guard` | Full safety | "/guard critical deployment" |

## Best Practices

### 1. Follow the Complete Workflow

For major features, use the complete workflow:

```
/office-hours → /plan-ceo-review → /plan-eng-review → 
/plan-design-review → /review → /qa → /ship
```

### 2. Always Review Before Merging

Never skip `/review` before merging code:

```python
# Bad practice
[Write code] → [Ship] ❌

# Good practice
[Write code] → [/review] → [/qa] → [/ship] ✅
```

### 3. Use /careful for Risky Operations

When performing dangerous operations:

```python
user: "/careful I want to delete the production database"

# AI will:
# 1. Show clear warning
# 2. Ask for confirmation
# 3. Explain consequences
# 4. Provide alternative approaches
```

### 4. Leverage State Management

Track work across sessions:

```python
# Session 1
user: "/office-hours (workflow: feature-x)"
[AI saves state]

# Session 2 (next day)
user: "/plan-eng-review (workflow: feature-x)"
[AI loads previous state and continues]
```

### 5. Provide Context

Give the AI context for better results:

```python
# Vague
user: "/review"

# Better
user: "/review I added user authentication to the checkout flow"

# Best
user: "/review I added JWT authentication to checkout. 
       Users can now save payment methods. The code is 
       in src/auth/ and src/checkout/."
```

## Troubleshooting

### Issue: Command Not Recognized

**Problem**: AI doesn't recognize a gstack command.

**Solution**: 
- Use explicit command format: `/command`
- Check the command spelling
- Use `/gstack` to see available commands

### Issue: Skill Not Found

**Problem**: AI says a skill is not available.

**Solution**:
```bash
# Verify installation
ls ~/.openclaw/skills/gstack-skills

# Reinstall if needed
cp -r gstack-skills ~/.openclaw/skills/
```

### Issue: Git Errors

**Problem**: `/ship` fails with git errors.

**Solution**:
```bash
# Check git status
git status

# Ensure clean working directory
git stash

# Resolve merge conflicts
git merge main
```

### Issue: Test Failures

**Problem**: `/qa` finds bugs but tests still fail.

**Solution**:
- Review the test report
- Fix remaining bugs manually
- Re-run `/qa` until all tests pass

## Examples

### Example 1: Startup Idea Validation

```python
user: "/office-hours I want to build an AI-powered code reviewer"

AI: Let me validate your startup idea using YC's framework.

Step 1: What is the user's biggest pain point?

User: Developers spend hours debugging code issues.

AI: How do you know this is a real problem? 
     Have you talked to developers? Do you have data?
     Specificity is the only currency here.

[Continues through all 6 questions]

AI: Here's your validation report:
- Problem: Validated ✅ (5 developers interviewed)
- Solution: Strong fit ✅
- Differentiation: Needs more work ⚠️
- ...
```

### Example 2: Quick Code Review

```python
user: "/review"

AI: Reviewing your current branch...

Files changed: 3
Lines added: +127
Lines removed: -45

Critical Issues Found:
1. SQL Injection Risk in src/db/queries.py:42
2. Missing Authentication in src/api/routes.py:87

Informational Issues Found:
1. Magic Number in src/config.py:15
2. Dead Code in src/utils/legacy.py

Auto-fixes Applied:
1. ✅ Fixed 2 unused imports
2. ✅ Formatted src/models/user.py

Status: ⚠️ DONE_WITH_CONCERNS
Please fix critical issues before merging.
```

### Example 3: Complete Feature Deployment

```python
user: "/gstack full workflow for user comments feature"

AI: I'll guide you through the complete gstack workflow.

Step 1: /office-hours
[Validates the user comments feature]

Step 2: /plan-eng-review
[Reviews technical architecture]

Step 3: Implementation
[You write the code]

Step 4: /review
[Reviews your code]

Step 5: /qa
[Tests the feature]

Step 6: /ship
[Deploys to production]

Feature deployed successfully! ✅
```

## Contributing

Want to improve gstack-skills? See [CONTRIBUTING.md](CONTRIBUTING.md).

## Support

- GitHub Issues: https://github.com/AICreator-Wind/gstack-openclaw-skills/issues
- Original gstack: https://github.com/garrytan/gstack

---

**Version**: 2.0.0  
**Updated**: 2026-03-21
