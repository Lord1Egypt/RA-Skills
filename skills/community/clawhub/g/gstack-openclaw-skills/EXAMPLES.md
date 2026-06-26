# gstack-skills Examples

Real-world examples of using gstack-skills in OpenClaw/WorkBuddy.

## Table of Contents

- [Example 1: New Feature Development](#example-1-new-feature-development)
- [Example 2: Bug Investigation](#example-2-bug-investigation)
- [Example 3: Daily Code Review](#example-3-daily-code-review)
- [Example 4: Startup Idea Validation](#example-4-startup-idea-validation)
- [Example 5: Refactoring Project](#example-5-refactoring-project)
- [Example 6: Complete Startup Launch](#example-6-complete-startup-launch)

---

## Example 1: New Feature Development

**Scenario**: Adding user comments to a blog platform.

### Step 1: Idea Validation

```
User: /office-hours I want to add user comments to my blog platform

AI: Let me validate this feature idea using YC's framework.

Question 1: What is the user's biggest pain point?

User: Readers can't engage with blog posts. They want to discuss the content.

AI: How do you know this is a real problem? Have you talked to readers?
Do you have data? Specificity is the only currency here.

User: I've received 50+ emails from readers asking for comments.
I also see 3 Reddit threads discussing my posts.

AI: Good! That's strong evidence. Email requests = clear pain point.
Reddit discussions = existing demand.

Question 2: How does your solution solve this?

User: Add comment section under each post with nested replies and voting.

AI: Will readers say "Yes, this is exactly what I need" or "That's interesting"?

User: They'll say "Yes, exactly what I need".

AI: Perfect match then. Let's continue...

[Completes all 6 questions]

AI: VALIDATION COMPLETE ✅
- Problem: Validated (50+ emails, Reddit threads)
- Solution Fit: Strong (readers explicitly requested)
- Differentiation: Standard feature, need unique angle
- User Acquisition: Existing readers, easy to reach
- Business Model: Increases engagement → retention → revenue
- Growth Model: Existing audience + viral potential

RECOMMENDATION: Proceed with development
NEXT: Use /plan-eng-review for architecture
```

### Step 2: Architecture Planning

```
User: /plan-eng-review user comments feature

AI: Reviewing technical architecture...

DATABASE DESIGN:
┌─────────────────────────────────────┐
│ Comments Table                      │
├─────────────────────────────────────┤
│ id (PK)                            │
│ post_id (FK)                       │
│ parent_id (FK, nullable)           │
│ user_id (FK, nullable)             │
│ content (TEXT)                     │
│ created_at (TIMESTAMP)             │
│ updated_at (TIMESTAMP)             │
│ votes_count (INT, default: 0)       │
│ is_deleted (BOOLEAN, default: F)   │
└─────────────────────────────────────┘

API ENDPOINTS:
POST   /api/posts/:id/comments       # Create comment
GET    /api/posts/:id/comments       # List comments
PUT    /api/comments/:id             # Update comment
DELETE /api/comments/:id             # Delete comment
POST   /api/comments/:id/vote       # Vote on comment

TECHNOLOGY STACK:
- Database: PostgreSQL (already using)
- API: REST (existing infrastructure)
- Caching: Redis for comment threads
- Search: Elasticsearch for comment search

SECURITY:
- Input sanitization (XSS prevention)
- Rate limiting (comment spam)
- Content moderation (profanity filter)
- Authentication required (anonymous comments?)

SCALABILITY:
- Pagination (load 50 comments, scroll load more)
- Nested thread depth limit (max 5 levels)
- CDN for static assets (user avatars)

RISK ASSESSMENT:
⚠️ Medium: Comment spam (need CAPTCHA)
⚠️ Low: Moderation overhead (community flags)
⚠️ Low: Performance (caching solves)

RECOMMENDATION: Ready to implement
NEXT: Proceed to development
```

### Step 3: Implementation

```
[Developer implements the feature over 2-3 days]
```

### Step 4: Code Review

```
User: /review my current branch

AI: Reviewing feature/comments-implementation...

FILES CHANGED: 8 files
LINES ADDED: +547
LINES REMOVED: -23

CRITICAL ISSUES FOUND: 3

❌ 1. SQL Injection Risk
   File: src/api/comments.py:89
   Severity: Critical
   
   ```python
   # Vulnerable
   query = f"SELECT * FROM comments WHERE post_id = {post_id}"
   
   # Fix
   query = "SELECT * FROM comments WHERE post_id = %s"
   cursor.execute(query, (post_id,))
   ```
   
❌ 2. XSS Vulnerability
   File: src/utils/sanitizers.py:45
   Severity: Critical
   
   Comment content is not sanitized before rendering.
   
   Fix: Add bleach library for HTML sanitization.

❌ 3. Missing Authorization
   File: src/api/comments.py:67
   Severity: Critical
   
   Anyone can delete any comment.
   
   Fix: Add user ownership check.

INFORMATIONAL ISSUES FOUND: 5

💡 1. Missing Tests
   - No unit tests for comment nesting logic
   - No integration tests for API endpoints
   
💡 2. No Rate Limiting
   - Comment endpoint vulnerable to spam
   
💡 3. Magic Numbers
   - Hardcoded "50 comments per page" limit
   
💡 4. Missing Error Handling
   - Database errors not caught
   
💡 5. No Logging
   - Comment creation not logged

AUTO-FIXES APPLIED:
✅ 1. Fixed SQL injection (3 instances)
✅ 2. Added input sanitization
✅ 3. Added authorization check
✅ 4. Added rate limiting middleware
✅ 5. Added error handling
✅ 6. Added logging

STATUS: ⚠️ DONE_WITH_CONCERNS

Remaining Tasks:
1. Write unit tests (estimated: 2 hours)
2. Write integration tests (estimated: 1 hour)
3. Manual testing in staging (estimated: 30 min)

NEXT: Run /qa for testing
```

### Step 5: QA Testing

```
User: /qa the comments feature

AI: Running systematic QA tests...

TEST FRAMEWORK DETECTED: pytest
DATABASE: PostgreSQL (staging)

TESTING SUITE:
┌─────────────────────────────────────┐
│ 1. Unit Tests                       │
│    ✅ Comment creation               │
│    ✅ Comment deletion               │
│    ✅ Comment nesting (5 levels)    │
│    ✅ Comment voting                │
│    ✅ Content sanitization           │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ 2. Integration Tests                │
│    ✅ API endpoint responses        │
│    ✅ Database transactions          │
│    ✅ Rate limiting                 │
│    ✅ Authentication flow            │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ 3. Manual Testing                   │
│    ✅ Create comment as user        │
│    ✅ Create nested reply            │
│    ✅ Vote on comment               │
│    ✅ Delete own comment            │
│    ✅ Try to delete others' comment  │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ 4. Edge Cases                       │
│    ✅ Empty comment                 │
│    ✅ Very long comment (10k chars)  │
│    ✅ HTML injection attempt        │
│    ✅ SQL injection attempt          │
│    ✅ Rapid comment creation        │
└─────────────────────────────────────┘

BUGS FOUND: 0
BUGS FIXED: 0

HEALTH SCORE: 95/100
├─ Functionality: 100/100 ✅
├─ Security: 95/100 ✅
├─ Performance: 90/100 ✅
└─ UX: 95/100 ✅

TEST COVERAGE: 92%
├─ Lines: 94%
├─ Branches: 90%
├─ Functions: 93%

STATUS: ✅ READY TO SHIP

Minor Issues:
⚠️ Loading indicator could be smoother
⚠️ Mobile responsiveness needs small tweak

These are optional improvements for future PR.

NEXT: Run /ship to deploy
```

### Step 6: Deployment

```
User: /ship the comments feature

AI: Preparing automated release...

1. CHECKING WORKING DIRECTORY... ✅ Clean

2. MERGING BASE BRANCH...
   Merging main into feature/comments... ✅

3. RUNNING TESTS...
   pytest tests/... 
   47 tests passed ✅

4. CHECKING COVERAGE...
   Coverage: 92% ✅ (target: 90%)

5. PRE-RELEASE REVIEW...
   ✅ No critical issues
   ✅ Security checks passed
   ✅ Code quality: A+

6. VERSION MANAGEMENT...
   Current: v2.0.3
   New: v2.1.0 (Minor: new feature)

7. GENERATING CHANGELOG...
   Added user comments feature
   - Nested comment threads
   - Voting system
   - Content moderation
   - Rate limiting
   Security improvements:
   - Input sanitization
   - XSS prevention
   - Authorization checks

8. UPDATING DOCUMENTATION...
   ✅ README.md updated
   ✅ API docs generated
   ✅ Migration guide added

9. CREATING COMMIT...
   [main abc1234] v2.1.0: Add user comments feature

10. PUSHING TO REMOTE...
    git push origin main ✅

11. CREATING PULL REQUEST...
    PR #234 created: "v2.1.0: Add user comments feature"
    Link: https://github.com/your/repo/pull/234

DEPLOYMENT SUMMARY:
┌─────────────────────────────────────┐
│ Version: v2.1.0                    │
│ Status: ✅ SHIPPED                  │
│ Tests: 47/47 passed                │
│ Coverage: 92%                      │
│ PR: #234                           │
│ Deployment: Ready                  │
└─────────────────────────────────────┘

NEXT:
- Review and merge PR #234
- Deploy to production
- Monitor for issues
- Gather user feedback

🎉 Feature successfully shipped!
```

---

## Example 2: Bug Investigation

**Scenario**: Users report intermittent login failures.

```
User: /investigate the login bug - users are getting 500 errors

AI: Starting systematic root cause analysis...

STEP 1: PROBLEM DEFINITION
├─ Error: HTTP 500 during login
├─ Frequency: Intermittent (≈5% of attempts)
├─ Affected Users: Random (no pattern)
├─ Impact: Critical (users can't login)
└─ Timeline: Started 2 days ago

STEP 2: INFORMATION GATHERING

Checking logs...
┌─────────────────────────────────────┐
│ auth.log (last 24 hours)           │
├─────────────────────────────────────┤
│ ✅ 1,250 successful logins          │
│ ❌ 67 failed logins (500 errors)    │
│ ⚠️ 0 database errors              │
│ ⚠️ 0 network errors               │
└─────────────────────────────────────┘

Analyzing error patterns:
┌─────────────────────────────────────┐
│ Error Distribution                 │
├─────────────────────────────────────┤
│ Time: Random (no pattern)          │
│ User: Random (no pattern)         │
│ IP: Random (no pattern)           │
│ Browser: Random (no pattern)       │
└─────────────────────────────────────┘

Checking database connections:
┌─────────────────────────────────────┐
│ Connection Pool Status             │
├─────────────────────────────────────┤
│ Total Connections: 50/50           │
│ Active: 48                         │
│ Idle: 2                            │
│ Waiting: 0                         │
└─────────────────────────────────────┘

⚠️ Connection pool at 96% capacity!

STEP 3: HYPOTHESIS FORMATION

Hypothesis 1: Connection pool exhaustion
- Evidence: Pool at 96%
- Likelihood: HIGH
- Test: Increase pool size

Hypothesis 2: Slow queries causing timeouts
- Evidence: No slow query logs
- Likelihood: LOW

Hypothesis 3: Race condition in auth logic
- Evidence: Random failures
- Likelihood: MEDIUM
- Test: Add debug logging

STEP 4: TESTING HYPOTHESES

Testing Hypothesis 1 (Connection Pool):
┌─────────────────────────────────────┐
│ Before (50 connections)            │
│ ─────────────────────────────────   │
│ Failures: 67/1,317 (5.1%)         │
│ Pool usage: 96%                    │
└─────────────────────────────────────┘

Increasing to 100 connections...

┌─────────────────────────────────────┐
│ After (100 connections)            │
│ ─────────────────────────────────   │
│ Failures: 0/500 (0%)              ✅
│ Pool usage: 45%                    │
└─────────────────────────────────────┘

Hypothesis 1 CONFIRMED ✅

STEP 5: ROOT CAUSE IDENTIFIED

ROOT CAUSE: Connection pool exhaustion during login bursts

Explanation:
- Connection pool limited to 50 connections
- Login bursts exhaust the pool
- New login requests timeout → 500 errors
- Connections not released quickly enough

Contributing Factors:
1. Insufficient connection pool size
2. No connection pooling in auth layer
3. Lack of rate limiting on login endpoint

STEP 6: FIX IMPLEMENTATION

Recommended Fixes:

1. Increase connection pool (immediate)
   ```python
   # config.py
   DB_POOL_SIZE = 100  # was 50
   ```

2. Add connection pooling to auth layer (short-term)
   ```python
   # Use connection per request, not per function
   @contextmanager
   def get_db_connection():
       conn = pool.getconn()
       try:
           yield conn
       finally:
           pool.putconn(conn)
   ```

3. Add rate limiting (medium-term)
   ```python
   # Limit login attempts: 10 per minute per IP
   @rate_limit(max_requests=10, window=60)
   def login(username, password):
       ...
   ```

4. Add monitoring (long-term)
   ```python
   # Alert if pool usage > 80%
   monitor_connection_pool(threshold=0.8)
   ```

STEP 7: VERIFICATION

Applying fixes...

```bash
# Fix 1: Increase pool size
✅ Applied

# Fix 2: Add connection pooling
✅ Applied

# Fix 3: Add rate limiting
✅ Applied

# Fix 4: Add monitoring
✅ Applied
```

Testing under load...

┌─────────────────────────────────────┐
│ Load Test Results                  │
├─────────────────────────────────────┤
│ Requests: 10,000                    │
│ Success: 10,000 (100%)             ✅
│ Failures: 0 (0%)                   ✅
│ Avg Response: 120ms                │
│ Pool Usage: 42%                    │
└─────────────────────────────────────┘

All tests passed! ✅

STEP 8: DEPLOYMENT

```
User: /ship the login bug fixes

AI: Shipping the login bug fixes...

[Automated deployment process]

Status: ✅ DEPLOYED

Next steps:
- Monitor for 24 hours
- Check production logs
- Alert on any failures
```

ROOT CAUSE ANALYSIS COMPLETE ✅
Fix: Connection pool exhaustion
Deployment: v2.0.4
Monitoring: Active

---

## Example 3: Daily Code Review

**Scenario**: Quick review before merging PR.

```
User: /review

AI: Reviewing current branch...

BRANCH: feature/payment-integration
BASE: main
FILES CHANGED: 3 files
LINES: +243, -89

QUICK SCAN:
┌─────────────────────────────────────┐
│ File Analysis                      │
├─────────────────────────────────────┤
│ src/payments/stripe.py            │
│   Lines: +187, -12                │
│   Security: ⚠️ External API        │
│ ─────────────────────────────────   │
│ tests/payments/test_stripe.py     │
│   Lines: +52, -77                 │
│   Coverage: 100% ✅                │
│ ─────────────────────────────────   │
│ docs/api/payments.md              │
│   Lines: +4, 0                    │
│   Documentation: ✅ Updated        │
└─────────────────────────────────────┘

SECURITY REVIEW:
✅ API keys in environment variables
✅ Input validation on amount
✅ HTTPS only
⚠️ Webhook signature verification (add?)

CODE QUALITY:
✅ Follows PEP 8
✅ Error handling comprehensive
✅ Logging added
✅ Tests added (100% coverage)

PERFORMANCE:
✅ Async I/O used
⚠️ Consider caching rate limit status (optional)

COMPLETENESS:
✅ Error codes documented
✅ Success/failure handling
✅ Webhook handling
⚠️ Missing refund logic (future PR?)

OVERALL ASSESSMENT:
Status: ✅ DONE

Minor Suggestions:
1. Add webhook signature verification
2. Add refund logic in future PR
3. Consider caching rate limits

READY TO MERGE: Yes ✅

NEXT: /qa for final testing OR merge directly
```

---

## Example 4: Startup Idea Validation

**Scenario**: Validating a new startup idea.

```
User: /office-hours I want to build an AI-powered code reviewer

AI: Let me validate this startup idea using YC's framework.

QUESTION 1: What is the user's biggest pain point?

User: Code reviews take too long. Developers wait hours/days for feedback.

AI: How much evidence do you have this is real?

User: I was at Google for 5 years. Code reviews there take 2-3 days average.
I've talked to 20+ devs at startups who say same issue.
GitHub data: Average PR time to review is 4.2 days.

AI: STRONG EVIDENCE ✅
- Personal experience at scale (Google)
- 20+ developer interviews
- Industry data backs it up

QUESTION 2: How does your solution solve this?

User: AI that reviews code in seconds, providing instant feedback.
It checks for bugs, security issues, style violations, and suggests fixes.

AI: Will developers say "Yes, exactly what I need" or "That's interesting"?

User: "Yes, exactly what I need". They're desperate for instant feedback.

AI: PERFECT MATCH ✅

QUESTION 3: Why aren't existing solutions good enough?

User: Static analysis tools (SonarQube, ESLint) only check syntax.
They don't understand context or suggest fixes.
CodeRabbit is AI-based but expensive and GitHub-only.

AI: COMPETITIVE ADVANTAGE:
✅ Static analysis is limited (true)
✅ Context-aware AI (differentiator)
✅ Affordable pricing (opportunity)
⚠️ CodeRabbit exists (but expensive)

QUESTION 4: How many people have this problem?

User: 30M developers worldwide (Stack Overflow survey).
Enterprise: 1000+ dev companies have biggest pain.
I know 50+ dev leads who would pay.

AI: MARKET SIZE:
✅ Total market: 30M developers
✅ Sweet spot: 10K+ employee companies
✅ Direct access: 50+ warm leads
✅ B2B2C model (sell to CTOs)

QUESTION 5: Will people pay? How much?

User: Yes. Code review is mission-critical.
Pricing: $50/dev/month (enterprise), $10/dev/month (startup).
Compared to SonarQube: $100/dev/month.
Compared to CodeRabbit: $30/dev/month.

AI: BUSINESS MODEL:
✅ Mission-critical tool (high willingness to pay)
✅ Competitive pricing
✅ Enterprise pricing ($50/mo/dev)
✅ Startup pricing ($10/mo/dev)
⚠️ Need to prove ROI

ROI Calculation:
- Dev spends 2 hours/day on reviews × $100/hr = $200/day
- AI saves 50% = $100/day saved
- Monthly value: $2,000/dev
- Your cost: $50/dev/month
- ROI: 40x ✅

QUESTION 6: How will users discover your product?

User:
1. GitHub marketplace (free plugin, 50% reduction)
2. Content marketing (dev blogs, case studies)
3. Developer communities (Hacker News, Reddit)
4. Word of mouth (viral potential)

AI: GROWTH MODEL:
✅ GitHub Marketplace (natural discovery)
✅ Content marketing (proven in dev tools)
✅ Viral loops (developers talk to developers)
⚠️ Need early adopters for social proof

CAC (Customer Acquisition Cost):
- GitHub organic: ~$50/lead
- Content: ~$100/lead
- Referrals: ~$20/lead
- Average CAC: ~$57/lead

LTV (Lifetime Value):
- Average company size: 100 devs
- Churn rate: 5%/year
- ARPU: $50/dev/month = $600/dev/year
- LTV: $600 × 100 × (1/0.05) = $1,200,000

LTV/CAC: 21,000x ✅

VALIDATION SUMMARY:
┌─────────────────────────────────────┐
│ YC Office Hours Results            │
├─────────────────────────────────────┤
│ Problem: STRONGLY VALIDATED ✅      │
│ Evidence: Strong (industry data)    │
│ ─────────────────────────────────   │
│ Solution: PERFECT FIT ✅            │
│ "Yes, exactly what I need"        │
│ ─────────────────────────────────   │
│ Differentiation: GOOD ✅            │
│ Context-aware AI vs static tools    │
│ ─────────────────────────────────   │
│ User Access: EXCELLENT ✅          │
│ 30M devs, 50+ warm leads           │
│ ─────────────────────────────────   │
│ Business Model: STRONG ✅          │
│ 40x ROI, competitive pricing       │
│ ─────────────────────────────────   │
│ Growth Model: GOOD ✅              │
│ LTV/CAC: 21,000x, viral loops     │
└─────────────────────────────────────┘

RISKS:
⚠️ Medium: AI quality must be excellent
⚠️ Low: CodeRabbit competition
⚠️ Low: Technical feasibility

RECOMMENDATION: PROCEED ✅

NEXT STEPS:
1. Build MVP (2-3 weeks)
2. Get 10 beta testers (you know 50+ leads)
3. Collect metrics (review time, satisfaction)
4. Launch on GitHub Marketplace
5. Content marketing campaign

EXPECTED TIMELINE:
- Week 1-2: Build MVP
- Week 3: Beta testing
- Week 4: Launch
- Month 2-3: 100 paying customers
- Month 6: 1,000 paying customers

This is a GO. Build it! 🚀
```

---

## More Examples Coming Soon

- [Example 5: Refactoring Project](#example-5-refactoring-project)
- [Example 6: Complete Startup Launch](#example-6-complete-startup-launch)

---

**Want to contribute an example?** See [CONTRIBUTING.md](CONTRIBUTING.md).

---

**Version**: 2.0.0  
**Updated**: 2026-03-21
