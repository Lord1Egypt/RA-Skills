# Product × Engineering × Operations Alignment SOP

> This SOP synthesizes real product strategy meetings, user feedback intake templates, and beta user interview frameworks into a universal **Product, Engineering, and Operations tri-party alignment** workflow.
>
> **Core Principle:** Everything serves commercialization. Everything serves revenue.
>
> **Usage:** This is a universal template. Replace all `[Product Name]` / `[Project Code]` / `[System Name]` placeholders with your actual information to use directly.

---

## 1. Core Problem Diagnosis: Why Do Product/Engineering/Operations Always Fail to Align?

### 1.1 Three Contradictions Every Growth-Stage Product Encounters

| Contradiction | Symptom | Root Cause |
|---------------|---------|------------|
| **New features vs. User feedback** | Dev team keeps chasing new features while user-reported bugs sit indefinitely | No unified priority decision mechanism |
| **What engineering wants to build vs. What operations needs** | Engineering thinks operations doesn't understand tech; operations thinks engineering ignores users | Lack of shared goals |
| **Fast vs. Stable** | Pushing for growth before the product form is stable; tech debt piles up | No clear product stage assessment |

### 1.2 Solution Framework

> **Insight from real meetings:** Companies that nail commercialization (e.g., Manus, DeepSeek) have their COO or operations lead directly serving monetization, with tight tri-party alignment across product, engineering, and operations.

**Four Core Mechanisms:**

| # | Mechanism | Description |
|---|-----------|-------------|
| 1 | **Unified Kanban** | User feedback and product requirements go into the same pool with a single tagging system |
| 2 | **Shared Goals** | Each iteration has explicit commercial metrics (e.g., "registration→paid conversion from 4.5% → 7%") |
| 3 | **Operations Veto Power** | Issues that directly harm user experience or paid conversion — operations can propose delaying the release |
| 4 | **Tri-party Alignment Before Every Iteration** | Product, engineering, and operations leads jointly decide what to build, what goes first, what gets deferred |

---

## 2. Unified Collaboration Layer: Kanban System Design

### 2.1 Two-Layer Kanban Structure

> **From real experience:** Don't just have per-iteration boards — you must have a master backlog. All raw issues go into the master pool first, then flow into downstream iterations.

| Layer | Name | Content | Owner |
|-------|------|---------|-------|
| **Layer 1: Master Backlog** | `[Product Name] Master Backlog` | All raw issues from every source (user feedback / competitive analysis / strategic needs) | Product Lead |
| **Layer 2: Iteration Board** | `[Version] - [Goal Description]` | Confirmed work for this iteration + must-fix bugs | Iteration Owner |

**Flow Logic:**

```
Master Backlog (all source issues)
    ↓ After review — deemed ready for a solution
Solution-ready requirements
    ↓ After sprint planning decision
Enters a specific iteration
    ↓ In-iteration development
Ship / Roll back to backlog / Defer to next iteration
```

### 2.2 Issue Intake Template (Universal Format)

> **Key principle:** Every issue from operations must include reproducibility information — otherwise engineering can't fix it.

| Field | Description | Example |
|-------|-------------|---------|
| **Issue Title** | Concise problem description | "iOS chart results inconsistent with Android" |
| **Source Channel** | User feedback / Competitive / Strategic | User feedback |
| **Report Count** | How many times the same issue has been reported | 3+ times → tag as severe |
| **System/Platform** | Web / iOS / Android / Self-host | iOS |
| **Version** | Specific version | v2.3.1 |
| **Repro Steps** | Must be reproducible to be fixable | 1. Open synastry 2. Select XX 3. View results |
| **Expected Behavior** | What the user expects | Results should match across both platforms |
| **Actual Behavior** | What actually happens | iOS display order is reversed from Android |
| **Screenshots/Recording** | Attach evidence | [Attachment] |
| **Impact Assessment** | Effect on experience/payments | Caused 1 user to request a refund |
| **Tags** | Bug / Feature Request / UX Improvement | Bug |
| **Priority Suggestion** | Operations-side judgment (High/Medium/Low) | High |

> **Operations Special Rule:** If the same issue is reported **3+ times**, it automatically gets the `severe` tag and must be resolved within the current iteration.

### 2.3 Bug vs. Feature Request Triage

| Type | Definition | Handling |
|------|-----------|----------|
| **Bug** | Existing functionality behaves differently than expected | Goes directly to Bug board; engineering estimates effort and fixes |
| **Feature Request** | User wants new functionality | Goes to master backlog; product writes spec before entering iteration |
| **UX Improvement** | Doesn't break core functionality but hurts experience | Same priority level as Bug; operations can push priority |

---

## 3. Iteration Cadence Design

### 3.1 Choosing Iteration Length

| Product Stage | Recommended Cycle | Rationale |
|---------------|-------------------|-----------|
| **Early PMF Validation** | 1–2 weeks | Fast-paced, rapid experimentation |
| **Growth Stage** | 3–4 weeks | Balance speed and stability |
| **Mature Stage** | 6–8 weeks | Stability first, room for major releases |

> ⚠️ **Note:** In modern web development, compress to **10 days – 2 weeks**. Iterations longer than that kill urgency.

### 3.2 Standard 10-Day Iteration Process

| Day | Engineering Action | Operations Action | Output |
|-----|-------------------|-------------------|--------|
| **Day 1** | Begin development | — | — |
| **Day 6** | Submit **testable build** | Receive build, **complete testing within half a day** | Test report (bug list + priorities) |
| **Day 7** | Fix P0/P1 based on priority | Ops × Eng **alignment call** (20–30 min) | Iteration scope confirmed |
| **Day 8** | Continue fixes + ship 2nd test build | Second round testing (if needed) | — |
| **Day 9** | Final fixes | Prepare **release materials** (screenshots/website/social) | Materials ready |
| **Day 10** | **Ship to production** | Publish content across all channels | Release complete |

### 3.3 Release Cadence Red Lines

> **From real lessons learned:** Never, ever release on a Friday or weekend.

---

## 4. Tri-Party Alignment Meeting Framework

### 4.1 Daily Standup (Daily, 15 minutes)

**Attendees:** All members — product, engineering, operations

- Stand up. Hard limit: 15 minutes.
- Each person covers three things only: ① What I did yesterday ② What I'm working on today ③ Any blockers
- **Operations must report:** Yesterday's user complaint hotspots, newly discovered high-frequency bugs
- **Any meeting over 1 hour means someone is slacking**

### 4.2 Iteration Planning Meeting (Start of each iteration, 30–60 minutes)

**Attendees:** Product, Engineering, and Operations leads

```
Topic 1: Retrospective of Last Iteration (20 min)
  - Core metric completion vs. target
  - What didn't get done? Why?
  - Where is user feedback concentrated?

Topic 2: This Iteration's Goal Setting (20 min)
  - Operations: What must be solved this iteration (tied to commercial goals)
  - Product: Main features/optimizations to push
  - Engineering: Tech debt/refactoring needs
  - Joint decision: Top 3 goals for this iteration

Topic 3: Resource & Schedule Confirmation (20 min)
  - How many person-days from each party?
  - Which features are confirmed? Which are on hold?
  - Are there modules that need refactoring?
```

### 4.3 Iteration Review Meeting (End of each iteration, 30 minutes)

**Core Questions:**
1. Did we hit our **target metrics** this iteration?
2. Are there P0 bugs still unfixed? Do they block the release?
3. Which features are being **deferred to next iteration**?
4. What's the operations focus for the next iteration?

### 4.4 Meeting Frequency Overview

| Meeting | Frequency | Duration | Purpose |
|---------|-----------|----------|---------|
| **Daily Standup** | Daily | 15 min | Sync progress, surface blockers |
| **Iteration Planning** | Start of iteration | 30–60 min | Decide what this iteration builds |
| **Iteration Review** | End of iteration | 30 min | Retrospective + prep for next iteration |
| **Monthly Review** | Monthly | 60–90 min | Core metrics review + direction adjustment |

---

## 5. Operations Role in Alignment

### 5.1 Operations as the "Translator" Between Users and Engineering

| Responsibility | Specific Actions | Frequency |
|----------------|-----------------|-----------|
| **User voice collection** | Aggregate user feedback, extract high-frequency issues, classify Bug / Feature | Daily |
| **Bug pre-screening** | Confirm each issue is reproducible, add repro steps | Daily |
| **Priority recommendations** | Prioritize from UX and commercialization perspective | Per iteration |
| **Version acceptance testing** | Starting Day 6, **complete testing within half a day** with written report | Per iteration |
| **Release materials prep** | App Store updates, website updates, social media content | Per iteration |

### 5.2 Operations Veto Power on Releases

> **Trigger condition:** If a P0 bug that **impacts user experience or paid conversion** is discovered pre-release and remains unfixed, operations can propose **delaying the release**.

**P0 Bug Criteria (Operations-side judgment):**

| Bug Type | Example | P0? |
|----------|---------|-----|
| Payment-related | Payment failure, duplicate charge | ✅ P0 |
| Core functionality unavailable | Can't register, can't generate results | ✅ P0 |
| Data errors | Chart results differ from other platforms | ✅ P0 |
| UI broken but functional | Button position offset | ⚠️ P1 |
| Copy/translation errors | English typo | ❌ P2 |

---

## 6. User Feedback Driving Product Iteration

### 6.1 Feedback → Optimization Closed Loop

```
User uses product → Problem/suggestion arises
        ↓
Operations collects (organizes/classifies/pre-screens)
        ↓
Issue logged to master board (with repro steps)
        ↓
Same issue reported 3+ times → Tag as severe
        ↓
Discussed as priority in iteration planning
        ↓
Enters iteration development
        ↓
Post-launch: operations verifies the fix
        ↓
Notify user that issue is resolved (reinforces feeling valued)
```

### 6.2 Beta User Interview Framework

| Phase | Timing | Action | Owner |
|-------|--------|--------|-------|
| **User screening** | 1 week before beta | Select 10–15 from active users | Operations |
| **Test account distribution** | 3 days before beta | Issue test accounts + credits | Operations |
| **User self-testing** | During beta | Use product based on real needs | User |
| **Deep interviews** | During beta | 30–40 min per session | Operations |
| **Daily summary** | End of each day | Compile high-frequency bugs + core needs | Operations |
| **Weekly review** | Weekly | Decide if ready to release | Product + Eng + Ops |

**Interview Structure (30–40 minutes):**

| Time | Module | Core Questions |
|------|--------|---------------|
| 5 min | User background | What do you do? What tools do you use? Biggest pain point? |
| 20 min | Product test debrief | Which step was smoothest? Where did you get stuck? Any bugs? |
| 10 min | Improvement suggestions | What should we fix first? |
| 5 min | Closing | Willing to keep participating? Would you recommend us? |

> **Core principle:** Don't discuss abstract feelings — only discuss real usage experiences.

---

## 7. Core Metrics Framework

### 7.1 Per-Iteration Target Metrics Template

```
This iteration's goal: [Specific description]
- Baseline: XX%
- Target: XX%
- Validation method: [Data source / query method]
- Owner: Product / Operations / Engineering
```

### 7.2 Commercialization Funnel Metrics

| Stage | Metric | Description |
|-------|--------|-------------|
| **Acquisition** | New registered users | Split by channel (organic / social / paid / KOL) |
| **Activation** | Onboarding completion rate | By module: info input / feature experience / got results |
| **Retention** | Day-1 / Day-7 / Day-30 retention | Split by user source |
| **Monetization** | Registration → paid conversion rate | Split by channel / user attribute |
| **Referral** | K-factor (NPS / referral willingness) | Invite mechanism participation rate |

### 7.3 Iteration Health Self-Check

| Check Item | Healthy | Warning Signal |
|------------|---------|----------------|
| Avg P0 bug fix time | ≤ 2 days | > 3 days |
| On-time feature delivery rate | ≥ 80% | < 60% |
| Avg user feedback response time | ≤ 24 hours | > 48 hours |
| Same bug re-reported count | ≤ 2 times | ≥ 3 times |
| Test report submitted on time | 100% by Day 6.5 | Delayed > half a day |

---

## 8. Technical Debt & Product Refactoring Management

### 8.1 Signals That Trigger Refactoring

| Signal | Explanation |
|--------|-------------|
| Same module has recurring bugs (≥5 related issues) | Fundamental design problem in that module |
| New feature dev cost keeps rising | Underlying architecture limits extensibility |
| Cross-platform data inconsistency | Entity abstractions aren't unified |
| Tech stack is outdated | Needs stack upgrade |

### 8.2 Resource Allocation Guidelines

| Type | Recommended % | Notes |
|------|--------------|-------|
| **New feature development** | 50–60% | Directly serves commercialization goals |
| **Bug fixes** | 20–30% | Ensures baseline experience |
| **Tech debt / Refactoring** | 20–30% | Ensures long-term sustainability |

### 8.3 Handling Refactoring Work

- Refactoring gets its **own project** with a 1–3 month timeline
- Refactoring **must not block normal iteration releases** (two tracks run in parallel)
- Post-refactoring requires **full regression testing** (recommend 3–5 core users participate)

---

## 9. Stage-Specific Priorities

| Stage | Focus | Notes |
|-------|-------|-------|
| **Cold Start (pre-PMF)** | Get the collaboration process running | 2–3 iterations to operationalize the flow; deep-interview 20–30 users |
| **Early Growth** | Lock in core metrics | Onboarding completion rate / conversion rate / retention curve |
| **Rapid Growth** | Boost engineering efficiency | Compress iterations to 10 days; build an in-house growth team |

---

## 10. Recommended Tools

| Purpose | Tool | Notes |
|---------|------|-------|
| Project management | **Linear** / Jira / Lark Base | Single entry point for all issues |
| Analytics | **PostHog** / Amplitude / Mixpanel | Core funnel instrumentation + analysis |
| User feedback collection | GitHub Issues / Linear / Lark Base | Users can submit directly |
| Meeting notes | Lark Smart Minutes | Auto-structured interview recordings |
| Internal communication | Lark / Slack | Channel per project |
| Knowledge management | Notion / Lark Docs | SOPs, templates, wiki |

---

## Appendix A: Bug Report Template

```markdown
## Issue Title
[Concise problem description]

## Basic Info
- **Source Channel**: [User feedback / Support / Social media / Beta]
- **Report Count**: [N] times (mark severe if ≥3)
- **System/Platform**: [Web / iOS / Android / Self-host]
- **Version**: [e.g. v2.3.1]

## Repro Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What the user expects]

## Actual Behavior
[What actually happens]

## Evidence
[Screenshot / screen recording link]

## Impact Assessment
[Effect on UX / paid conversion / retention]

## Tags
[Bug / Feature Request / UX Improvement]

## Priority Suggestion (Operations-side)
[P0 (fix immediately) / P1 (fix this iteration) / P2 (fix next iteration)]
```

---

## Appendix B: Iteration Planning Meeting Template

```markdown
# [Iteration Name] Planning Meeting Notes
**Date:**
**Attendees:**

## 1. Last Iteration Retrospective
| Target Metric | Baseline | Actual | Status |
|--------------|----------|--------|--------|
| | | | |

**Incomplete Items:**
1.
2.

## 2. This Iteration Goals
| # | Goal | Commercial Value | Owner |
|---|------|-----------------|-------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 3. Operations-side Requirements
| Requirement | Context / User Feedback Source | Suggested Priority |
|-------------|-------------------------------|-------------------|
| | | |

## 4. Engineering Assessment
| Requirement | Technical Approach | Effort Estimate | Completable This Iteration? |
|-------------|-------------------|-----------------|----------------------------|
| | | | |

## 5. Final Scope Confirmation
**Entering iteration:**
**Deferred to next:**
**Tech debt allocation:**
```

---

## Appendix C: Product/Engineering/Operations Responsibility Matrix

| Matter | Decision Maker | Advisor | Executor |
|--------|---------------|---------|----------|
| Whether to build a feature | Product + Operations | Operations (demand), Engineering (feasibility) | Engineering |
| Whether to fix a bug | Product + Operations | Operations (report frequency) | Engineering |
| Release timing | All three parties jointly | — | — |
| Priorities from user interviews | Operations | — | Product + Engineering |
| Growth strategy | Operations + Product | Engineering (data support) | Operations |
| Technical architecture/refactoring | Engineering + Product | Operations (UX impact) | Engineering |

---

*This SOP is synthesized from real product strategy meeting minutes, user feedback intake templates, and beta user interview frameworks. It's applicable to any product team that needs to establish an alignment mechanism across product, engineering, and operations.*
