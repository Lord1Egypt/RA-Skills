# How to Evaluate an Idea Before Building

**Purpose:** Practical guide for using AI-ILC to take a raw idea and put it through structured evaluation — determining whether it's worth committing resources to, what its scope and risk profile look like, and whether to approve, defer, or reject before spending initiation effort.

---

## Who This Is For

Product owners, innovation leads, or anyone with an idea that MIGHT become a project. You want a structured answer to: "Should we invest in this? Is it feasible? Is it valuable enough? Does it fit our portfolio?" — before spending weeks on full project initiation.

---

## Before You Start

**You need:**
- AI-ILC installed in your AI workspace (see `ai-ilc/setup/INSTALL.md`)
- An idea in any form:
  - A sentence ("We should build a customer portal")
  - A paragraph from a meeting
  - A feature request from a user
  - A competitive observation ("Competitor X has this — should we?")
  - A technical improvement ("We should migrate to microservices")

**You do NOT need:**
- A business case (that's what evaluation produces)
- Market research (AI-ILC helps you identify what research is needed)
- Stakeholder buy-in (evaluation informs the buy-in conversation)
- Technical feasibility proof (evaluation surfaces feasibility questions)

---

## The Evaluation Process

AI-ILC guides you through structured evaluation across multiple dimensions:

### Stage 1: Idea Capture

**What happens:** AI-ILC takes your raw idea and structures it.

**You provide:**
- The idea (any format, any length)
- Context: where it came from, what triggered it

**AI-ILC produces:**
- Structured problem statement
- Initial hypothesis (what we believe this would achieve)
- Assumption inventory (what must be true for this to work)

### Stage 2: Problem Validation

**What happens:** AI-ILC challenges whether the problem is real and worth solving.

**Questions explored:**
- Who has this problem? (specific personas, not "users")
- How do they solve it today? (current alternatives)
- What's the cost of the problem remaining unsolved?
- Is this a problem we're uniquely positioned to solve?
- What evidence exists that this problem matters?

**Output:** Problem validation score with evidence gaps identified.

### Stage 3: Solution Fit Assessment

**What happens:** AI-ILC evaluates whether your proposed approach fits the problem.

**Questions explored:**
- Does the solution actually address the root problem?
- Are there simpler solutions we're overlooking?
- What's the minimum viable version?
- Does this fit within our existing architecture/platform?
- What's the technical risk level?

**Output:** Solution-fit score with identified risks and alternatives.

### Stage 4: Value & Effort Estimation

**What happens:** AI-ILC produces rough-order-magnitude value and effort estimates.

**Value dimensions:**
- Revenue impact (direct or indirect)
- Cost reduction potential
- User satisfaction / retention impact
- Strategic positioning value
- Risk reduction value

**Effort dimensions:**
- Development complexity (T-shirt sizing)
- Team capability gap
- Integration complexity
- Operational overhead
- Timeline estimate (order of magnitude)

**Output:** Value/Effort ratio with confidence level.

### Stage 5: Portfolio Fit

**What happens:** AI-ILC checks whether this idea fits your current portfolio context.

**Questions explored:**
- Does this compete with existing initiatives for resources?
- Does this depend on other initiatives completing first?
- Does this align with stated strategic goals?
- What's the opportunity cost of doing this vs. something else?
- Is the timing right? (market window, team availability, dependencies)

**Output:** Portfolio fit assessment with dependencies and conflicts.

### Stage 6: Decision Gate

**What happens:** AI-ILC presents the evaluation summary for decision.

**Decision options:**
| Decision | Meaning | Next Step |
|----------|---------|-----------|
| **Approve** | Worth investing in | Proceeds to AI-PILC for full initiation |
| **Defer** | Good idea, bad timing | Logged in register with re-evaluation date |
| **Pivot** | Problem is real, solution needs rethinking | Return to Stage 3 with new approach |
| **Reject** | Not worth pursuing | Documented with rationale (future reference) |

---

## What You Get (The Idea Brief)

```
{your-output-folder}/
├── ilc-state.md                    ← Marker file (chain handoff + session resume)
├── Idea_Brief.md                   ← Structured evaluation summary
│   ├── Problem Statement
│   ├── Proposed Solution
│   ├── Evaluation Scores
│   │   ├── Problem Validation: {score}/5
│   │   ├── Solution Fit: {score}/5
│   │   ├── Value/Effort Ratio: {score}/5
│   │   └── Portfolio Fit: {score}/5
│   ├── Key Assumptions (validated/unvalidated)
│   ├── Risks Identified
│   ├── Recommendation: {Approve/Defer/Pivot/Reject}
│   └── Next Steps
└── Evaluation_Evidence.md          ← Supporting analysis, alternatives considered
```

---

## Depth Levels

| Depth | Best For | Time | What You Get |
|-------|----------|------|-------------|
| **Minimal** | Quick screening, obvious ideas | 20-30 min | Problem + solution + go/no-go (Stages 1, 3, 6 only) |
| **Standard** | Most ideas — recommended | 45-90 min | Full 6-stage evaluation with scores |
| **Comprehensive** | Strategic initiatives, large investments | 2-3 hours | Deep analysis, competitive landscape, detailed assumptions |

---

## When to Use AI-ILC vs. Skip to AI-PILC

| Situation | Recommendation |
|-----------|---------------|
| "I have a vague idea, not sure if it's worth pursuing" | Use AI-ILC first |
| "Leadership approved this — we're doing it" | Skip to AI-PILC |
| "I have 5 ideas, need to pick the best one" | Run AI-ILC on all 5, compare scores |
| "Customer explicitly requested this feature" | Use AI-ILC (validated demand ≠ feasible solution) |
| "We need to do this for compliance/regulatory reasons" | Skip to AI-PILC (decision is made, evaluate inside initiation) |
| "I want to explore before committing team time" | Use AI-ILC (that's exactly its purpose) |

---

## Tips for Better Evaluations

1. **Be honest about assumptions.** Every idea rests on beliefs ("users will want this," "we can build it in 3 months," "the market is ready"). AI-ILC makes these explicit. Don't defend them — test them.

2. **Embrace rejection.** A rejected idea evaluated in 1 hour saves 3 months of building the wrong thing. Rejection is a success of the evaluation process, not a failure of the idea.

3. **Score relatively, not absolutely.** "Is this a 4/5 value?" is less useful than "Is this higher value than the other 3 ideas competing for the same team?"

4. **Don't skip portfolio fit.** The best idea in isolation might be the wrong idea in context. If it blocks a higher-priority initiative or arrives too early for the market, timing beats quality.

5. **Document rejected ideas.** Today's "reject" might be next year's "approve." Context changes. Having the evaluation on file means you don't re-evaluate from scratch.

---

## What Happens Next

| Decision | Where It Goes |
|----------|--------------|
| Approved | AI-PILC for full project initiation (Idea Brief feeds as input) |
| Approved (feature-level) | AI-POLC for backlog entry (Feature Brief format) |
| Deferred | Idea Register with re-evaluation trigger date |
| Multiple approved | AI-PPM for portfolio prioritization across initiatives |

The handoff is via `ilc-state.md` — AI-PILC auto-detects the approved Idea Brief and uses it as input context, skipping questions already answered during evaluation.

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How to Initiate a Project | `knowledge_docs/HOW_TO_INITIATE_A_PROJECT.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| Why Project Initiation Matters | `knowledge_docs/WHY_PROJECT_INITIATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
