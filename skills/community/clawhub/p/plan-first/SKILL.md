---
name: plan-first
description: Solve complex multi-step tasks by generating a detailed plan before execution. Based on the Plan-and-Solve prompting research, this skill breaks tasks into clear steps, validates the approach, then executes systematically. Use for any task with multiple steps, dependencies, or where jumping straight to the answer might miss important details. Critical for coding, writing, analysis, and problem-solving tasks.
---

# Plan First - Structured Problem Solving

**Plan First** implements the **Plan-and-Solve** research paradigm for tackling complex tasks systematically.

The core insight: **Generative AI performs better when it plans before acting**, especially on multi-step tasks where dependencies exist between steps.

## The Analogy: Architect vs. Builder

| Builder Approach | Architect Approach (Plan First) |
|------------------|----------------------------------|
| Start building immediately | Design blueprints first |
| Discover problems mid-project | Anticipate issues before they arise |
| May need to tear down and rebuild | Build correctly the first time |
| Works for simple structures | Essential for complex projects |

## When to Use Plan First

**Perfect for:**
- 🏗️ **Multi-step coding tasks** (implement feature X that requires Y, Z, W)
- 📝 **Complex writing** (reports, documentation with sections)
- 🔬 **Analysis tasks** (data analysis with multiple phases)
- 🧩 **Problem-solving** (math, logic, puzzles with steps)
- 📋 **Project planning** (breaking down large initiatives)

**Skip for:**
- ⚡ Single-step tasks ("What is 2+2?")
- 🎯 Direct questions ("What is the capital of France?")
- 🔄 Pure exploration (brainstorming without structure)

## The Workflow

### Step 1: Generate the Plan

Before ANY execution, create a detailed plan:

```
TASK: "Build a user authentication system"

PLAN:
1. [SETUP] Initialize database schema for users table
   - Dependencies: None
   - Success criteria: Migration runs without errors

2. [IMPLEMENTATION] Create password hashing utilities
   - Dependencies: Step 1 complete
   - Success criteria: bcrypt integration works

3. [IMPLEMENTATION] Build login endpoint
   - Dependencies: Steps 1, 2
   - Success criteria: Returns JWT on valid credentials

4. [IMPLEMENTATION] Build signup endpoint
   - Dependencies: Steps 1, 2
   - Success criteria: Creates user, returns token

5. [INTEGRATION] Add middleware for protected routes
   - Dependencies: Steps 3, 4
   - Success criteria: Unauthorized requests rejected

6. [TESTING] Write comprehensive tests
   - Dependencies: Steps 3, 4, 5
   - Success criteria: All tests pass
```

### Step 2: Validate the Plan

**Self-check before proceeding:**

- [ ] Are steps in logical order?
- [ ] Are dependencies clearly marked?
- [ ] Is each step specific and actionable?
- [ ] Are success criteria verifiable?
- [ ] Did I miss any prerequisite steps?

**If gaps found:** Revise the plan first.

### Step 3: Execute Step by Step

Execute ONE step at a time, in order:

```
Executing Step 1: Initialize database schema
✓ Run: CREATE TABLE users...
✓ Verify: Table exists with correct columns
✓ Mark complete

Executing Step 2: Create password hashing utilities
✓ Run: Implement hash_password(), verify_password()
✓ Verify: Unit tests pass
✓ Mark complete

... continue until all steps complete
```

### Step 4: Handle Deviations

**If a step fails:**
1. Analyze why it failed
2. Revise plan if needed (add missing steps, reorder)
3. Resume from current step

**If requirements change:**
1. Stop execution
2. Revise remaining plan
3. Continue with updated plan

## Plan Format Template

```markdown
## Task
[Clear statement of what needs to be done]

## Plan

### Step N: [Action Verb] [What to do]
**Dependencies:** [List prerequisite steps]
**Approach:** [How to accomplish this step]
**Verification:** [How to confirm success]
**Files/Tools:** [What to modify or use]

---

### Step 1: [SETUP/IMPLEMENTATION/ANALYSIS/TESTING] Description
**Dependencies:** None
**Approach:** 
- Detail 1
- Detail 2
**Verification:** [Specific test or check]
**Files:** [Files to create/modify]

### Step 2: ...
[Continue for all steps]

## Risk Analysis
**Potential blockers:** [What could go wrong]
**Mitigation:** [How to handle issues]

## Rollback Plan
**If fails at step N:** [How to undo/reset]
```

## Examples

### Example 1: Code Implementation

**Task:** "Add email verification to signup flow"

```markdown
## Plan

### Step 1: [SETUP] Create email_tokens table
**Dependencies:** None
**Approach:** 
- Create migration for email_tokens table
- Fields: id, user_id, token, expires_at, used
**Verification:** Migration runs, table structure correct
**Files:** migrations/003_email_tokens.sql

### Step 2: [IMPLEMENTATION] Add email sending utility
**Dependencies:** Step 1
**Approach:**
- Create utils/email.py with send_verification_email()
- Use SMTP or SendGrid
- Include token in email link
**Verification:** Can send test email successfully
**Files:** utils/email.py

### Step 3: [IMPLEMENTATION] Modify signup endpoint
**Dependencies:** Steps 1, 2
**Approach:**
- After user creation, generate token
- Send verification email
- Return "check your email" response
**Verification:** Signup creates token and sends email
**Files:** routes/auth.py

### Step 4: [IMPLEMENTATION] Create verify endpoint
**Dependencies:** Step 1
**Approach:**
- GET /verify-email?token=xxx
- Check token valid and not expired
- Mark user as verified
**Verification:** Clicking link marks user verified
**Files:** routes/auth.py

### Step 5: [INTEGRATION] Add verified check to login
**Dependencies:** Step 4
**Approach:**
- Modify login to require verified=True
- Return appropriate error if unverified
**Verification:** Unverified users can't login
**Files:** routes/auth.py

### Step 6: [TESTING] Write tests
**Dependencies:** Steps 1-5
**Approach:**
- Test signup creates token
- Test email sent
- Test verification works
- Test unverified can't login
**Verification:** All tests pass
**Files:** tests/test_auth.py
```

### Example 2: Writing Task

**Task:** "Write annual report for engineering team"

```markdown
## Plan

### Step 1: [ANALYSIS] Gather metrics
**Dependencies:** None
**Approach:**
- Pull deployment frequency from CI/CD
- Get incident data from monitoring
- Collect code review stats
**Verification:** Have all data points needed
**Files:** data/raw_metrics.json

### Step 2: [DRAFTING] Write executive summary
**Dependencies:** Step 1
**Approach:**
- Highlight key achievements
- Include year-over-year comparison
- Keep to 1 page
**Verification:** Covers all major points
**Files:** report/executive_summary.md

### Step 3: [DRAFTING] Write detailed sections
**Dependencies:** Step 2 (for tone consistency)
**Approach:**
- Infrastructure improvements
- Team growth and hiring
- Process optimizations
- Major projects delivered
**Verification:** Each section has data + narrative
**Files:** report/sections/*.md

### Step 4: [INTEGRATION] Compile and format
**Dependencies:** Steps 2, 3
**Approach:**
- Combine sections
- Add table of contents
- Apply company template
**Verification:** Document is complete and formatted
**Files:** report/annual_report_2024.md

### Step 5: [REVIEW] Self-review and polish
**Dependencies:** Step 4
**Approach:**
- Check for typos
- Verify all numbers accurate
- Ensure flow between sections
**Verification:** Ready for stakeholder review
**Files:** [same]
```

### Example 3: Data Analysis

**Task:** "Analyze customer churn for Q4"

```markdown
## Plan

### Step 1: [DATA] Extract customer data
**Dependencies:** None
**Approach:**
- Query database for customers active in Q3
- Get their Q4 activity status
- Include subscription tier, signup date
**Verification:** Dataset has expected row count
**Files:** data/customers_q4.csv

### Step 2: [ANALYSIS] Calculate churn rate
**Dependencies:** Step 1
**Approach:**
- Define churn: no activity in Q4
- Calculate overall rate
- Break down by tier, acquisition channel
**Verification:** Numbers match expectations
**Files:** analysis/churn_basic.py

### Step 3: [ANALYSIS] Identify patterns
**Dependencies:** Step 2
**Approach:**
- Time-series analysis of churn
- Correlation with features
- Segment analysis
**Verification:** Charts show clear patterns
**Files:** analysis/churn_patterns.ipynb

### Step 4: [SYNTHESIS] Create recommendations
**Dependencies:** Step 3
**Approach:**
- Based on patterns, propose interventions
- Prioritize by impact/effort
- Include success metrics
**Verification:** Recommendations are actionable
**Files:** report/recommendations.md

### Step 5: [DELIVERY] Create presentation
**Dependencies:** Steps 2, 3, 4
**Approach:**
- Executive summary slide
- Key findings with charts
- Recommendations with impact
**Verification:** Stakeholders can act on it
**Files:** presentation/churn_analysis_q4.pptx
```

## Best Practices

### 1. Make Steps Concrete

❌ **Vague:** "Set up authentication"
✅ **Concrete:** "Create users table with bcrypt password hashing"

### 2. Define Clear Verification

Every step needs a pass/fail check:
- "Tests pass"
- "Database table exists with correct schema"
- "Can send test email successfully"
- "Response time < 200ms"

### 3. Keep Steps Small

Break large steps into smaller ones:

❌ "Build entire API"
✅ 
- "Create database schema"
- "Implement GET endpoint"
- "Implement POST endpoint"
- "Add validation"
- "Write tests"

### 4. Mark Dependencies Explicitly

This prevents trying to build on foundations that don't exist.

### 5. Plan for Failure

Include what to do if a step fails:
- Rollback procedure
- Alternative approaches
- When to stop and reassess

## Comparison: Direct vs Plan-First

**Task:** "Build a REST API for todos"

| Direct Approach | Plan-First Approach |
|----------------|---------------------|
| Start coding endpoints | Plan database schema first |
| Discover need auth later | Include auth in initial plan |
| Maybe forget validation | Explicit validation step |
| Inconsistent error handling | Define error format upfront |
| Tests added at end | Test steps interleaved |

## When Plans Change

**Mid-execution discovery:** "Actually we need OAuth, not simple auth"

1. Stop current execution
2. Reassess remaining plan
3. Add OAuth-specific steps
4. Update dependencies
5. Resume with revised plan

Don't wing it. Update the plan.

## Integration with Other Skills

**Plan First + Team Code:**
1. Generate master plan
2. Delegate parallelizable steps to agents
3. Execute dependency-aware

**Plan First + Self-Critique:**
1. Generate plan
2. Critique the plan ("Am I missing anything?")
3. Revise
4. Execute

## Quick Start Template

```markdown
## Task
[Your task here]

## Plan

### Step 1: [VERB] Description
**Dependencies:** None
**Approach:**
- 
- 
**Verification:** 
**Files:** 

### Step 2: [VERB] Description
**Dependencies:** Step 1
**Approach:**
- 
- 
**Verification:** 
**Files:** 

[Continue...]

## Risk Analysis
**Blockers:** 
**Mitigation:** 

## Rollback
**If fails:** 
```

## References

- Research: "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models" (Wang et al., 2023)
- Related: Chain-of-Thought (CoT), Tree-of-Thought (ToT), ReAct
- See [references/examples.md](references/examples.md) for more detailed examples
