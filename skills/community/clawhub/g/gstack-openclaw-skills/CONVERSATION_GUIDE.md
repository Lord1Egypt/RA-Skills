# gstack-skills Conversation Guide

Complete guide for using gstack-skills through natural conversation with OpenClaw/WorkBuddy.

---

## 🎯 Table of Contents

- [Getting Started](#getting-started)
- [Basic Commands](#basic-commands)
- [Complete Workflow Examples](#complete-workflow-examples)
- [Common Conversations](#common-conversations)
- [Tips and Best Practices](#tips-and-best-practices)
- [Troubleshooting Conversations](#troubleshooting-conversations)

---

## Getting Started

### First Time After Installation

After installing gstack-skills, start by asking:

```
User: /gstack
```

**Response:**
```
AI: Here are the available gstack commands:

Product Ideation:
• /office-hours - Product idea validation and design thinking
• /plan-ceo-review - CEO perspective on feature planning
• /plan-eng-review - Engineering architecture review
• /plan-design-review - Design review

Development:
• /review - Pre-merge code review with automatic fixes
• /investigate - Root cause analysis and debugging
• /design-consultation - Design system consultation

Testing & Release:
• /qa - Test application and fix bugs
• /qa-only - Bug reporting only
• /ship - Automated release workflow

Documentation & Review:
• /document-release - Update documentation
• /retro - Team retrospective

Power Tools:
• /codex - OpenAI Codex independent review
• /careful - Dangerous operation warnings
• /freeze - Lock file editing scope
• /guard - Full safety mode

Try any command to get started!
```

---

## Basic Commands

### 1. Code Review

**Simple:**
```
User: /review

AI: Reviewing your current branch...

Files changed: 3
Lines added: +127, Lines removed: -45

Critical Issues Found:
❌ 1. SQL Injection Risk in src/db/queries.py:42
   ```python
   # Vulnerable
   query = f"SELECT * FROM users WHERE id = {user_id}"
   
   # Fix
   query = "SELECT * FROM users WHERE id = %s"
   cursor.execute(query, (user_id,))
   ```

Informational Issues Found:
💡 1. Magic Number in src/config.py:15
💡 2. Missing Tests

Auto-fixes Applied:
✅ Fixed SQL injection
✅ Added constant for magic number

Status: ⚠️ DONE_WITH_CONCERNS
Remaining: Add tests

NEXT: Run /qa for testing
```

**With Context:**
```
User: /review I just added user authentication

AI: Reviewing user authentication implementation...

[Review focused on auth-specific security checks]
```

### 2. Testing

**Simple:**
```
User: /qa

AI: Running systematic QA tests...

Test Results:
• Unit Tests: 42/42 passed ✅
• Integration Tests: 15/15 passed ✅
• Manual Tests: 8/8 passed ✅

Health Score: 95/100
├─ Functionality: 100/100 ✅
├─ Security: 90/100 ✅
├─ Performance: 95/100 ✅
└─ UX: 95/100 ✅

Bugs Found: 0
Bugs Fixed: 0

Status: ✅ READY TO SHIP

NEXT: /ship to deploy
```

**With Context:**
```
User: /qa the shopping cart feature

AI: Testing shopping cart functionality...

[Tests focused on cart-specific features]
```

### 3. Deployment

**Simple:**
```
User: /ship

AI: Preparing automated release...

1. Merging base branch... ✅
2. Running tests... ✅ (57/57 passed)
3. Checking coverage... ✅ (94%)
4. Updating version... ✅ (v2.2.0)
5. Generating changelog... ✅
6. Creating commit... ✅
7. Pushing to remote... ✅
8. Creating PR... ✅ (#247)

Deployment Summary:
┌─────────────────────────────────────┐
│ Version: v2.2.0                    │
│ Status: ✅ SHIPPED                  │
│ Tests: 57/57 passed                │
│ Coverage: 94%                      │
│ PR: #247                           │
│ Deployment: Ready                  │
└─────────────────────────────────────┘

Status: ✅ DEPLOYED
NEXT: Review and merge PR #247
```

**With Context:**
```
User: /ship the payment integration feature

AI: Shipping payment integration...

[Deployment focused on payment feature]
```

### 4. Product Ideation

```
User: /office-hours I have an idea for an AI code reviewer

AI: Let me validate your startup idea using YC's framework.

Question 1: What is the user's biggest pain point?

User: Code reviews take too long, 2-3 days on average. Developers are frustrated.

AI: How much evidence do you have this is a real problem?

User: I was at Google for 5 years. Code reviews there averaged 2.5 days. 
I've interviewed 20+ developers at startups who say the same thing.

AI: STRONG EVIDENCE ✅
Personal experience at scale + 20+ interviews + industry data.

Question 2: How does your solution solve this?

User: AI that reviews code in seconds and provides instant feedback.

AI: Will developers say "Yes, this is exactly what I need" or "That's interesting"?

User: "Yes, exactly what I need". They're desperate for instant feedback.

AI: PERFECT MATCH ✅

[Completes all 6 questions]

AI: VALIDATION COMPLETE ✅

Summary:
┌─────────────────────────────────────┐
│ Problem: STRONGLY VALIDATED ✅      │
│ Evidence: Strong (industry data)    │
│ Solution: PERFECT FIT ✅            │
│ Market: 30M developers              │
│ Business Model: 40x ROI ✅          │
│ Growth: LTV/CAC: 21,000x ✅        │
└─────────────────────────────────────┘

Recommendation: PROCEED 🚀

NEXT: /plan-eng-review for architecture
```

### 5. Debugging

```
User: /investigate users are reporting 500 errors on login

AI: Starting systematic root cause analysis...

STEP 1: Problem Definition
├─ Error: HTTP 500 during login
├─ Frequency: Intermittent (≈5% of attempts)
├─ Affected: Random users
└─ Impact: Critical

STEP 2: Information Gathering
Checking logs...
┌─────────────────────────────────────┐
│ auth.log (last 24 hours)            │
├─────────────────────────────────────┤
│ ✅ 1,250 successful logins          │
│ ❌ 67 failed logins (500 errors)    │
│ ⚠️ 0 database errors              │
│ ⚠️ 0 network errors               │
└─────────────────────────────────────┘

Checking connection pool...
⚠️ Pool at 96% capacity (50/50 connections)

STEP 3: Hypothesis Formation
Hypothesis 1: Connection pool exhaustion (HIGH likelihood)
Hypothesis 2: Slow queries (LOW likelihood)

STEP 4: Testing Hypothesis 1
Increasing pool to 100 connections...

┌─────────────────────────────────────┐
│ After (100 connections)            │
│ ─────────────────────────────────   │
│ Failures: 0/500 (0%)              ✅
│ Pool usage: 45%                    │
└─────────────────────────────────────┘

ROOT CAUSE: Connection pool exhaustion

FIX:
```python
# config.py
DB_POOL_SIZE = 100  # was 50
```

Applying fix...
✅ Fix applied

Testing under load...
✅ All 10,000 requests successful

Status: ✅ FIXED

NEXT: /ship the fix
```

---

## Complete Workflow Examples

### Example 1: New Feature Development

**Session 1: Idea & Planning**

```
User: /office-hours I want to add user comments to my blog

AI: Validating user comments feature...

[Completes 6-question validation]

AI: VALIDATION COMPLETE ✅
Recommendation: PROCEED

User: /plan-eng-review comments architecture

AI: Reviewing technical architecture...

Database Design:
┌─────────────────────────────────────┐
│ Comments Table                      │
│ id, post_id, parent_id, user_id   │
│ content, created_at, votes_count  │
└─────────────────────────────────────┘

API Endpoints:
• POST /api/posts/:id/comments
• GET /api/posts/:id/comments
• PUT /api/comments/:id
• DELETE /api/comments/:id
• POST /api/comments/:id/vote

Security:
• Input sanitization
• Rate limiting
• Content moderation
• Authentication required

Recommendation: Ready to implement ✅
```

**Session 2: Implementation & Review**

```
[Developer implements comments feature]
```

```
User: /review comments implementation

AI: Reviewing comments feature...

Files changed: 8
Lines: +547, -23

Critical Issues: 2
❌ 1. SQL Injection in src/api/comments.py:89
❌ 2. XSS Vulnerability in content rendering

Auto-fixes Applied:
✅ Fixed SQL injection
✅ Added input sanitization
✅ Added rate limiting

Status: ⚠️ DONE_WITH_CONCERNS
Remaining: Write tests

User: /qa comments feature

AI: Testing comments feature...

Test Results:
• Unit Tests: 42/42 passed ✅
• Integration Tests: 15/15 passed ✅
• Manual Tests: 8/8 passed ✅
• Edge Cases: 5/5 passed ✅

Health Score: 95/100

Bugs Found: 0
Bugs Fixed: 0

Status: ✅ READY TO SHIP
```

**Session 3: Deployment**

```
User: /ship comments feature

AI: Shipping comments feature...

1. Merging base branch... ✅
2. Running tests... ✅ (47/47 passed)
3. Checking coverage... ✅ (92%)
4. Updating version... ✅ (v2.1.0)
5. Generating changelog... ✅
6. Creating PR... ✅ (#234)

Status: ✅ DEPLOYED

Total time: ~15 minutes (vs 2+ hours manually)
```

---

### Example 2: Bug Fix Lifecycle

```
User: /investigate users report intermittent login failures

AI: Investigating login failures...

[Completes root cause analysis]

AI: ROOT CAUSE: Connection pool exhaustion
FIX: Increase pool from 50 to 100

User: Apply the fix

AI: Applying fix...
✅ DB_POOL_SIZE updated to 100
✅ Restarting application...

User: /review the login fix

AI: Reviewing login fix...

Status: ✅ DONE
No issues found

User: /qa the login fix

AI: Testing login under load...

Load Test Results:
┌─────────────────────────────────────┐
│ Requests: 10,000                    │
│ Success: 10,000 (100%)             ✅
│ Avg Response: 120ms                │
│ Pool Usage: 42%                    │
└─────────────────────────────────────┘

Status: ✅ FIXED

User: /ship the login fix

AI: Shipping login fix...

Status: ✅ DEPLOYED (v2.0.4)
```

---

## Common Conversations

### Conversation 1: First Time User

```
User: I just installed gstack-skills. What should I try first?

AI: Welcome to gstack-skills! Here's what I recommend:

Start with these basics:

1. Review your current code
   → Say: /review

2. Test your application
   → Say: /qa

3. See all commands
   → Say: /gstack

Want me to show you an example? Try:
   "/review"

I'll review your current branch automatically!
```

```
User: /review

AI: Reviewing your current branch...

[Shows review results]

This is a quick code review. It found some issues and 
fixed them automatically.

Try /qa next to test your code, or /ship to deploy!
```

### Conversation 2: Daily Workflow

```
User: I'm done coding for the day. What should I do?

AI: Great! Here's the recommended workflow:

1. Review your changes
   → /review

2. Test everything
   → /qa

3. Deploy if ready
   → /ship

Or just say:
   "/review and /qa then /ship if ready"

I'll do it all for you!
```

```
User: /review and /qa then /ship if ready

AI: I'll do all three in sequence...

1. /review
   [Reviewing code...]
   ✅ Review complete, minor issues fixed

2. /qa
   [Running tests...]
   ✅ All tests passed

3. /ship
   [Preparing deployment...]
   ✅ Deployed successfully (v2.1.0)

Everything is done! 🎉
```

### Conversation 3: Getting Help

```
User: How do I use /office-hours?

AI: /office-hours is for validating product ideas and design thinking.

When to use it:
• "I have an idea for..."
• "Help me think through..."
• "Validate my product idea"

How it works:
1. I'll ask you 6 questions from YC's framework
2. You answer each question
3. I provide validation and recommendations

Example:
   → "/office-hours I want to build an AI code reviewer"

Want to try it now?
```

### Conversation 4: Understanding Results

```
User: /review

AI: [Shows review with issues]

User: What does "DONE_WITH_CONCERNS" mean?

AI: "DONE_WITH_CONCERNS" means:

✅ Review is complete
✅ I've fixed what I could automatically
⚠️ Some issues need your attention

In this case:
• I fixed SQL injection ✅
• I added rate limiting ✅
• You need to write tests ⚠️

Next steps:
1. Write the tests I mentioned
2. Run /qa to verify
3. Then /ship to deploy

Does that help clarify?
```

### Conversation 5: Custom Workflow

```
User: Can I review and test in one go?

AI: Yes! You can combine commands in different ways:

Option 1: Sequential
   → "/review then /qa"

Option 2: Conditional
   → "/review and if OK then /qa"

Option 3: Complete workflow
   → "/review → /qa → /ship"

Option 4: Describe what you want
   → "Review my code, test it, and ship if ready"

All of these will work! Which would you prefer?
```

---

## Tips and Best Practices

### Tip 1: Provide Context

**Vague:**
```
User: /review
```

**Better:**
```
User: /review I added user authentication to checkout
```

**Best:**
```
User: /review I added JWT authentication to checkout flow.
Users can now save payment methods. Files in src/auth/ and src/checkout/
```

### Tip 2: Ask for Help

```
User: Help me with /ship

AI: /ship automates the deployment workflow. It will:
1. Merge base branch
2. Run all tests
3. Check code coverage
4. Update version number
5. Generate changelog
6. Create commit
7. Push to remote
8. Create PR

Try it:
   → /ship

Or ask for specific help:
   → "How does /ship handle versioning?"
   → "What does /ship check before shipping?"
```

### Tip 3: Use Natural Language

You don't need exact commands. Natural language works too:

```
User: review my code

AI: Reviewing your current branch...

[Works the same as /review]
```

```
User: deploy this to production

AI: Preparing automated release...

[Works the same as /ship]
```

### Tip 4: Iterate and Refine

```
User: /review

AI: [Shows review with issues]

User: Fix the critical issues

AI: Applying fixes...

[Fixes critical issues]

User: /review again

AI: Re-reviewing...

[Shows updated review with remaining issues]
```

### Tip 5: Ask "Why" to Understand

```
User: /ship

AI: [Deployment complete]

User: Why did you bump to v2.1.0?

AI: I bumped to v2.1.0 because:

Version Rules:
• Major (X.0.0): Breaking changes
• Minor (X.Y.0): New features
• Patch (X.Y.Z): Bug fixes

Your change:
• Added new feature: user comments
• Type: New feature
• Version: 2.0.3 → 2.1.0 (Minor bump)

Want me to use a different version?
```

---

## Troubleshooting Conversations

### Issue: Command Not Recognized

```
User: /review

AI: I don't recognize the command "/review".

Let me help:

1. Check installation:
   Run: ls ~/.openclaw/skills/gstack-skills/SKILL.md

2. Restart OpenClaw/WorkBuddy

3. Try again with /gstack

User: /gstack

AI: Here are the available gstack commands...
[Shows all commands]

Now /review should work. Try again!
```

### Issue: Git Errors

```
User: /ship

AI: Error: Working directory not clean

Current Status:
├─ Modified: src/auth/login.py
├─ New file: src/auth/middleware.py
└─ Deleted: src/auth/legacy.py

You need to commit these changes first:

Option 1: Commit changes
   → git add .
   → git commit -m "feature: auth middleware"

Option 2: Stash changes
   → git stash

Option 3: Abort and fix manually
   → "abort"

Which would you like?

User: commit them

AI: Committing...
✅ git add .
✅ git commit -m "feature: auth middleware"
✅ Committed successfully

Continuing with /ship...
[Proceeds with deployment]
```

### Issue: Test Failures

```
User: /qa

AI: Running tests...

Test Results:
✅ 45 tests passed
❌ 2 tests failed

Failed Tests:
1. test_user_creation (src/tests/test_user.py:87)
   Error: Assertion failed
   
2. test_login_rate_limit (src/tests/test_auth.py:156)
   Error: Timeout

Would you like me to:
A. Fix the failing tests automatically
B. Show you the error details
C. Skip tests and continue (not recommended)

User: A

AI: Analyzing and fixing...

1. test_user_creation
   Issue: Mock not properly set up
   Fix: Added proper mock configuration
   Result: ✅ Fixed

2. test_login_rate_limit
   Issue: Test timeout too short
   Fix: Increased timeout from 1s to 5s
   Result: ✅ Fixed

Re-running tests...
✅ 47/47 tests passed

Status: ✅ ALL TESTS PASSING

NEXT: /ship to deploy
```

---

## Advanced Conversations

### Conversation: Custom Workflow

```
User: I want to create a custom workflow for my team

AI: I can help you create a custom gstack workflow!

Current workflow:
/office-hours → /plan-eng-review → /review → /qa → /ship

Your workflow could be:
1. Describe your typical process
2. I'll create a custom command sequence
3. I can even create a custom skill!

What's your typical process?

User: We do:
   1. Team discussion
   2. Code review
   3. Security review
   4. Testing
   5. Code review again
   6. Deploy

AI: Perfect! Here's your custom workflow:

/custom-workflow:
1. /office-hours (team discussion)
2. /review (first code review)
3. /investigate (security review)
4. /qa (testing)
5. /review (second code review)
6. /ship (deploy)

Try it:
   → "/custom-workflow for the payment feature"

I'll run all steps automatically!

Want me to save this as a custom skill?
```

---

## Summary

### Key Points

1. **Start Simple**: Begin with `/gstack` to see all commands
2. **Natural Language**: You can use natural language, not just commands
3. **Provide Context**: Give details for better results
4. **Ask Questions**: Always ask if you don't understand
5. **Iterate**: You can refine and iterate on results

### Common Patterns

```
Quick review:     /review
Quick test:       /qa
Quick deploy:     /ship
New feature:      /office-hours → /plan-eng-review → code → /review → /qa → /ship
Bug fix:          /investigate → fix → /review → /qa → /ship
Daily workflow:   /review → /qa → /ship (if ready)
```

### Getting Help

- **Command overview**: `/gstack`
- **Command help**: "Help me with [command]"
- **General help**: "How do I use gstack-skills?"

---

**Ready to code faster with gstack-skills! 🚀**

For more examples, see [EXAMPLES.md](EXAMPLES.md)  
For installation, see [INSTALL.md](INSTALL.md)
