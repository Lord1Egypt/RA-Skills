---
name: Prospect
description: >
  Filter raw target lists into prioritized prospects worth pursuing.
  Score fit, timing, value, and access. Route each target to pursue, research,
  watch, or drop.
version: 2.0.0
---

# Prospect

> **Turn 100 possible targets into 5 prospects you should actually pursue.**

Prospect is a target filter and priority ranker for sales, partnerships, and business development.

Use this skill when you have a list of names, companies, or accounts and need to decide:
- who is worth pursuing
- who should be prioritized
- who belongs on a watchlist
- who should be dropped

This skill does NOT:
- find targets for you (use search tools or lead sources to gather raw targets first)
- handle active conversations (use Lead skill once someone has engaged)
- write outreach messages (use outreach or messaging tools for that)

---

## Prospect vs Lead

Clarity first. These skills serve different stages.

| | Prospect | Lead |
|---|----------|------|
| **Stage** | Before contact | After engagement |
| **Question** | "Is this target worth reaching out to?" | "Should I keep pursuing this person?" |
| **Input** | Names, profiles, company data, signals | Conversation history, responses, behavior |
| **Output** | Priority tier + route | Qualification score + next action |
| **Score dimensions** | Fit, Timing, Value, Access | Fit, Intent, Urgency, Authority |

**Typical flow:**
1. Prospect skill filters and ranks targets
2. You reach out
3. They respond
4. `/lead` evaluates and advances the engaged opportunity
5. `/pipeline` manages active opportunities across the full deal book

Use Prospect before contact. Use Lead after engagement begins.

---

## What This Skill Does

Prospect helps:
- separate poor-fit targets from viable prospects
- rank prospects by fit, timing, value, and accessibility
- identify what information is missing
- recommend the next best route for each prospect
- reduce wasted outreach effort

It does not replace human judgment about ethics, compliance, privacy, or regulatory requirements.

---

## What to Provide

The better the input, the sharper the judgment.

Useful information includes:
- target name and company
- role or title
- industry or sector
- company size or stage
- any visible signals (hiring, funding, expansion, pain points, tool gaps, complaints)
- source of the target (referral, search, event, inbound)
- any prior context or relationship

Missing information is fine. The skill will identify gaps and recommend whether to research further or proceed anyway.

---

## Standard Output Format

For each prospect, return:

PROSPECT: [Name / Company]  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
PRIORITY: [High / Medium / Watch / Drop]

SCORES:  
Fit: [0-10] — [reason in one line]  
Timing: [0-10] — [reason in one line]  
Value: [0-10] — [reason in one line]  
Access: [0-10] — [reason in one line]

TOTAL: [X/40]

SIGNALS:  
✅ [positive signal or fit indicator]  
✅ [positive signal or fit indicator]  
⚠️ [risk, gap, or unknown]

ROUTE:  
→ [Pursue now / Research further / Add to watchlist / Drop]

REASONING:  
[2-3 sentences explaining why this priority tier and route]

NEXT STEP:  
[specific action if pursue or research]

**Batch mode (10+ prospects):**

Show summary table first:

| Name | Company | Priority | Score | Route |
|------|---------|----------|-------|-------|
| ...  | ...     | ...      | .../40 | ...  |

Then provide detailed breakdown for top 5 only.

---

## Scoring Dimensions

### Fit (0-10)
How well does this target match the ideal prospect profile?
- industry relevance
- company size or stage
- role relevance
- problem-product alignment

### Timing (0-10)
Is now a relevant moment to pursue this target?
- recent funding, hiring, or expansion
- visible pain points or inefficiencies
- role changes or new initiatives
- regulatory or market pressure
- competitive moves or tooling gaps

### Value (0-10)
What is the potential upside if this prospect converts?
- deal size or revenue potential
- strategic importance
- account expansion potential
- referral or case study value
- long-term partnership fit

### Access (0-10)
How reachable or engageable is this target?
- existing relationship or warm intro
- responsiveness indicators
- organizational openness
- decision-making complexity
- competitive saturation

---

## Priority Tiers and Routes

**High Priority (32-40 points):**  
Route → Pursue now  
Strong fit, good timing, high value, accessible. Act within 48 hours.

**Medium Priority (24-31 points):**  
Route → Research further  
Promising but missing key information. Gather more signals before committing effort.

**Watchlist (16-23 points):**  
Route → Add to watchlist  
Decent fit but weak timing or unclear value. Monitor for changes. Revisit in 30-90 days.

**Drop (0-15 points):**  
Route → Drop  
Poor fit, bad timing, low value, or inaccessible. Not worth pursuit. Preserve effort for better targets.

---

## Disqualifiers

Certain conditions should trigger an immediate drop or downgrade, regardless of other scores:

- wrong industry or segment with no realistic path to fit
- no meaningful need or problem relevance
- budget or capacity constraints that make purchase implausible
- structural barriers (compliance, geography, competitive locks)
- ethical, legal, or reputational risks

Disqualifiers prevent wasted effort on targets that will not convert.

---

## When to Use Prospect

Use this skill when:
- you have a list of targets and need to decide who is worth pursuing
- multiple prospects need prioritization
- a target looks interesting but you need structured judgment
- you want to avoid wasting effort on poor-fit outreach
- you are building a prospecting workflow and need qualification logic

Do not use this skill when:
- you need help finding targets (use search tools or lead sources first)
- the target has already engaged and you need to evaluate next steps (use Lead skill)
- you need legal, compliance, or regulatory judgment about targeting or outreach

---

## Response Principles

When analyzing prospects:
- prioritize fit over volume
- separate static traits from timing signals
- make disqualifiers explicit
- identify information gaps clearly
- recommend routes that match effort to opportunity
- preserve honesty about uncertainty

Do not:
- inflate prospect quality without evidence
- ignore visible disqualifiers
- recommend aggressive pursuit without strong signals
- fabricate timing, value, or access where none exists

---

## Execution Protocol (for AI agents)

When user provides target information, follow this sequence:

### Step 1: Parse Input
Extract:
- prospect identity (name, company, role)
- industry and segment
- company size or stage
- any visible signals (funding, hiring, complaints, expansion)
- source or context

### Step 2: Score Each Dimension
Assign 0-10 scores for:
- **Fit:** Does this target match the ideal profile?
- **Timing:** Is now a relevant moment?
- **Value:** What is the upside if they convert?
- **Access:** How reachable are they?

Total score = sum of 4 dimensions (max 40).

### Step 3: Identify Gaps
List critical unknowns:
- Don't know their current solution
- Don't know decision-making structure
- Don't know budget or urgency

### Step 4: Check Disqualifiers
Flag any structural barriers that would prevent conversion regardless of scores.

### Step 5: Assign Priority and Route
Based on total score and context:
- 32-40 → High Priority → Pursue now
- 24-31 → Medium Priority → Research further
- 16-23 → Watchlist → Monitor for changes
- 0-15 → Drop → Not worth effort

### Step 6: Provide Reasoning
Explain in 2-3 sentences:
- why this tier
- what makes this prospect worth or not worth pursuit
- what the next step should be

### Step 7: Format Output
Use the standard output template for each prospect.

For batch requests (10+ prospects), show summary table first, then detailed breakdown for top 5.

---

## Activation Rules (for AI agents)

### When to use this skill
Activate when user asks about:
- evaluating a target or prospect before outreach
- prioritizing a list of targets
- deciding who to pursue
- building a target list or prospecting strategy
- filtering or ranking potential accounts

### When NOT to use this skill
Do not activate when:
- user is asking about active leads or ongoing conversations (use Lead skill)
- user needs help finding or sourcing targets (not a filtering task)
- prospect appears in non-sales contexts
- user is asking about recruiting or hiring prospects unless explicitly framed as business development targeting

### Ambiguous cases
If prospect is mentioned but context is unclear, ask:
"Are you asking about evaluating sales or business targets, or something else?"

Only proceed if user confirms it is about target selection for sales, partnerships, or business development.

---

## Quality Check Before Delivering

- [ ] Priority tier is clear and justified
- [ ] Score breakdown is specific, not generic
- [ ] Information gaps are identified
- [ ] Route recommendation matches the scores
- [ ] Reasoning is honest about uncertainty
- [ ] Next step is concrete (if pursue or research)
- [ ] Disqualifiers are flagged if present
- [ ] Output follows standard format

---

## Boundaries

This skill supports target selection for sales, partnerships, and business development.

It does not replace:
- legal or compliance review of targeting practices
- ethical judgment about outreach appropriateness
- privacy or data handling obligations
- regulatory requirements for marketing or contact

Adapt outputs to your jurisdiction, platform rules, and applicable laws.
