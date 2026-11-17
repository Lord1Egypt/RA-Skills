<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Risk Management

## Stage: 13 of 16
## Phase: 🟢 PLANNING
## Execution: ALWAYS

---

## Purpose

Systematically identify, assess, and plan responses for all significant project risks. Produce a Risk Register that serves as a living document throughout project execution, including scoring methodology, top risks for steering attention, contingency reserves, and review cadence.

---

## Depth Adaptation

| Depth | Risk Count | Analysis Detail | Reserves |
|-------|:----------:|----------------|----------|
| **Minimal** | 5-8 risks | Probability/Impact scoring, brief response. No formal matrix visualization. | Single contingency statement |
| **Standard** | 10-15 risks | Full P×I scoring, response strategies, ownership, Top 5 for steering, contingency reserves defined | Schedule + budget contingency |
| **Comprehensive** | 15-25 risks | Full scoring, detailed response actions, trigger indicators, secondary risks, quantitative analysis where data supports, descoping candidates, Monte Carlo note if applicable | Schedule + budget + scope contingency with triggers |

---

## MANDATORY: Stage Sub-Role — Risk Analyst

During THIS stage, ALSO adopt the mindset of a **Risk Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Scan every risk category systematically (technical, operational, financial, schedule, external, organizational) — not just the obvious ones
- Score probability × impact with supporting evidence; assign an owner and a trigger indicator to each risk
- Convert every active assumption (from the Assumptions register) into a tracked risk
- Derive contingency reserves from the top risks, not a flat percentage guess

### Anti-Patterns for This Stage
- Do NOT list risks without P×I scores — an unscored risk is just a worry
- Do NOT propose "monitor" as the only response for a high-impact risk

### Quality Check
A good output at this stage sounds like:
- "14 risks across 6 categories; Top 5 by P×I escalated to steering; R-07 trigger: vendor negotiation past Week 4 → escalate; schedule contingency +15% from 3 high-prob schedule risks..."

---

## Step-by-Step Execution

### Step 1: Load Context

Gather risk inputs from all prior stages:

| Source | Risk Signals |
|--------|-------------|
| Requirements Analysis (Stage 4) | Unresolved gaps, ambiguities, feasibility signals |
| Clarification (Stage 5) | Deferred questions, assumptions made |
| Feasibility Assessment (Stage 6) | Low-scoring dimensions, conditions for proceeding |
| Business Case (Stage 8) | Cost uncertainties, dependency concerns |
| Project Charter (Stage 9) | Initial risks listed, constraints |
| Stakeholder Register (Stage 10) | Stakeholder risks, availability concerns |
| Scope Statement (Stage 11) | Scope complexity, boundary disputes |
| Resource Plan (Stage 12) | Sourcing risks, budget assumptions |
| Assumptions Register | Every assumption is a potential risk if wrong |
| Decision Log | Any decision made under uncertainty |

---

### Step 2: Identify Risks — Category Scan

Systematically scan each risk category:

| Category | Questions to Ask | Typical Risks |
|----------|-----------------|---------------|
| **Technical** | Is the technology proven? Are there integration challenges? Performance concerns? Architectural unknowns? | Tech complexity, integration failure, performance shortfall, data migration issues |
| **Resource** | Can we get the people? Are key skills available? Key person dependency? | Recruitment delays, skill gaps, key person loss, team turnover |
| **Scope** | Is scope stable? Could stakeholders push changes? Are boundaries clear? | Scope creep, gold-plating, requirements volatility, boundary disputes |
| **Schedule** | Is the timeline realistic? Are there hard deadlines? Sequential dependencies? | Timeline overrun, dependency delays, critical path compression |
| **Financial** | Is budget confirmed? Are estimates reliable? Cost uncertainty? | Budget rejection, cost overrun, rate increases, hidden costs |
| **Operational** | Will users adopt? Is change management sufficient? Process disruption? | Adoption resistance, training gaps, operational disruption, process conflicts |
| **External** | Third-party dependencies? Vendor risk? Market changes? Regulatory shifts? | Vendor failure, regulatory change, market shift, partner delays |
| **Security** | Data risks? Compliance exposure? Vulnerability potential? | Security breach, compliance failure, late vulnerability discovery |
| **Organizational** | Sponsor commitment? Competing priorities? Restructuring? Political? | Sponsor departure, priority shift, organizational change, political resistance |
| **Quality** | Can we meet quality standards? Testing sufficient? Technical debt? | Quality shortfall, test coverage gaps, technical debt accumulation |

**For each category:** Identify 1-3 risks that are relevant to THIS project (not all will apply).

---

### Step 3: Formulate Risk Statements

Each risk must be stated clearly using the cause-event-impact format:

```
Because of [CAUSE/CONDITION], there is a risk that [EVENT/UNCERTAINTY] which would result in [IMPACT/CONSEQUENCE].
```

**Good examples:**
- "Because recruitment of senior developers is competitive in the current market, there is a risk that the team cannot be assembled within 6 weeks, which would result in a 4-8 week schedule delay to Build Phase 1."
- "Because the third-party API has not been validated against production-scale use cases, there is a risk that the integration proves inadequate, which would result in the dependent module being deferred or requiring workarounds."

**Bad examples (avoid):**
- ❌ "Risk of failure" (too vague)
- ❌ "Technology might not work" (no cause, no specific impact)
- ❌ "Budget overrun" (an impact, not a risk statement)

---

### Step 4: Assess Each Risk — Probability × Impact

#### Probability Scale

| Score | Label | Definition |
|:-----:|-------|-----------|
| 1 | Very Low | <10% chance of occurring; highly unlikely |
| 2 | Low | 10-25% chance; unlikely but possible |
| 3 | Medium | 25-50% chance; could go either way |
| 4 | High | 50-75% chance; more likely than not |
| 5 | Very High | >75% chance; almost certain to occur |

#### Impact Scale

| Score | Label | Schedule | Budget | Scope | Quality |
|:-----:|-------|:--------:|:------:|:-----:|:-------:|
| 1 | Very Low | <1 week slip | <5% overrun | Negligible scope change | Minor defect |
| 2 | Low | 1-2 week slip | 5-10% overrun | Minor feature affected | Non-critical quality issue |
| 3 | Medium | 2-4 week slip | 10-20% overrun | Significant feature affected | Noticeable quality reduction |
| 4 | High | 1-2 month slip | 20-35% overrun | Major deliverable affected | Major quality/compliance issue |
| 5 | Very High | >2 month slip | >35% overrun | Project scope fundamentally changed | Critical failure or safety issue |

#### Risk Score Matrix

```markdown
## Risk Assessment Matrix

```
              IMPACT
              Very Low(1) Low(2)   Medium(3)  High(4)  Very High(5)
             ┌──────────┬────────┬──────────┬────────┬────────────┐
Very High(5) │    5     │  10    │    15    │   20   │     25     │
             ├──────────┼────────┼──────────┼────────┼────────────┤
High(4)      │    4     │   8    │    12    │   16   │     20     │
PROBABILITY  ├──────────┼────────┼──────────┼────────┼────────────┤
Medium(3)    │    3     │   6    │     9    │   12   │     15     │
             ├──────────┼────────┼──────────┼────────┼────────────┤
Low(2)       │    2     │   4    │     6    │    8   │     10     │
             ├──────────┼────────┼──────────┼────────┼────────────┤
Very Low(1)  │    1     │   2    │     3    │    4   │      5     │
             └──────────┴────────┴──────────┴────────┴────────────┘

Score Thresholds:
  🔴 Very High (20-25): Immediate action required; Steering Committee escalation
  🟠 High (12-16):      Active mitigation required; PM monitors weekly
  🟡 Medium (6-10):     Mitigation planned; PM monitors bi-weekly
  🟢 Low (1-5):         Accepted; monitor only
```
```

---

### Step 5: Plan Risk Responses

For each risk, select a response strategy:

| Strategy | Definition | When to Use |
|----------|-----------|-------------|
| **Avoid** | Eliminate the risk by removing the cause | When the cause can be eliminated without major trade-off |
| **Mitigate** | Reduce probability and/or impact | Most common strategy; when risk can be partially controlled |
| **Transfer** | Shift impact to a third party | Insurance, contracts, outsourcing the risky component |
| **Accept** | Acknowledge and monitor; no proactive action | When cost of response exceeds impact, or probability is very low |
| **Escalate** | Raise to higher authority for decision | When risk is beyond project team's control |

For each risk, document:
1. Response strategy (one of the above)
2. Specific response actions (2-4 concrete actions)
3. Risk owner (who is responsible for monitoring and responding)
4. Trigger indicator (what signals the risk is materializing) — Comprehensive depth only
5. Secondary risks (risks created by the response) — Comprehensive depth only

---

### Step 6: Compile the Risk Register

```markdown
## Risk Register

| Risk ID | Category | Risk Description | Prob (1-5) | Impact (1-5) | Score | Priority | Response Strategy | Response Actions | Owner | Status | Trend |
|:-------:|:--------:|------------------|:----------:|:------------:|:-----:|:--------:|:-----------------:|-----------------|:-----:|:------:|:-----:|
| R-001 | {cat} | {cause-event-impact statement} | {n} | {n} | {n×n} | {🔴🟠🟡🟢} | {strategy} | 1. {action} 2. {action} | {role} | ☐ Open | → |
```

**Status values:** ☐ Open, ⚡ Active (materializing), ✅ Closed, ⏸️ Dormant
**Trend values:** ↑ Increasing, → Stable, ↓ Decreasing

---

### Step 7: Identify Top 5 Risks

Select the 5 highest-scoring risks for steering committee attention:

```markdown
## Top 5 Risks (for Steering Committee)

| # | Risk ID | Risk | Score | Owner | Key Action | Trend |
|---|:-------:|------|:-----:|:-----:|------------|:-----:|
| 1 | R-{nnn} | {Brief description} | {score} | {role} | {Most important action} | → |
| 2 | R-{nnn} | {Description} | {score} | {role} | {Action} | → |
| 3 | R-{nnn} | {Description} | {score} | {role} | {Action} | → |
| 4 | R-{nnn} | {Description} | {score} | {role} | {Action} | → |
| 5 | R-{nnn} | {Description} | {score} | {role} | {Action} | → |
```

---

### Step 8: Define Contingency Reserves

```markdown
## Contingency Reserves

### Schedule Contingency
| Reserve | Amount | Trigger |
|---------|:------:|---------|
| Buffer after {critical phase} | +{n} weeks | Activated if >{n} high risks materialize simultaneously |

### Budget Contingency
| Reserve | Amount | Trigger |
|---------|:------:|---------|
| Contingency fund | {n}% of total ({$X}) | Activated per approval authority in Charter governance matrix |

### Scope Contingency (Descoping Candidates)
| Priority | Feature/Item | Impact of Deferral |
|:--------:|-------------|-------------------|
| 1 (first to cut) | {Feature name} | {What happens if deferred — minimal user impact} |
| 2 | {Feature} | {Impact} |
| 3 | {Feature} | {Impact} |
```

**Rules:**
- Scope contingency: identify 3-5 in-scope items that could be deferred to a v1.1 if schedule/budget risk materializes
- These must be genuinely deferrable (not core to the project's value proposition)
- Order by "safest to defer" — least user/business impact first

---

### Step 9: Define Risk Review Cadence

```markdown
## Risk Review Schedule

| Review Type | Frequency | Participants | Focus |
|-------------|:---------:|--------------|-------|
| PM risk monitoring | Weekly | PM + Tech Lead | All open risks; trigger review |
| Team risk review | Bi-weekly | Project team | New risks; update existing; close resolved |
| Steering Committee risk report | {Cadence from Charter} | Steering Committee | Top 5; escalated risks; decisions needed |
| Phase gate risk reassessment | At each milestone | Full team + Sponsor | Complete re-scoring; new phase risks |
```

### Escalation Criteria

```markdown
## Risk Escalation Criteria

A risk must be escalated to the Steering Committee when:
- Risk score reaches 20+ (Very High)
- Risk has materialized into an issue with no resolution path within the team
- Two or more High risks (12+) have trend moving upward (↑) simultaneously
- Risk requires budget, scope, or timeline decision beyond PM authority
```

---

### Step 10: Produce Summary by Category

```markdown
## Risk Summary by Category

| Category | Count | Highest Score | Top Risk |
|----------|:-----:|:-------------:|----------|
| {Category} | {n} | {max score} (R-{nnn}) | {Brief description of highest} |
```

---

### Step 11: Assemble and Validate

1. Compile using template `templates/risk-register.md`
2. Validate:
   - [ ] All categories scanned (no blank categories without justification)
   - [ ] Risk statements are cause-event-impact format
   - [ ] Scores are consistent (similar risks have similar scores)
   - [ ] Every risk has an owner
   - [ ] Every 🔴/🟠 risk has specific response actions
   - [ ] Top 5 are genuinely the highest-scored
   - [ ] Contingency reserves are proportional to risk exposure
   - [ ] Cross-reference: assumptions from earlier stages reflected as risks where appropriate

---

### Step 12: Present for Review

```markdown
## Review: Risk Register — {project_name}

I've produced the Risk Register. Key highlights:

- **Total risks identified:** {n}
- **By severity:** 🔴 {n} Very High | 🟠 {n} High | 🟡 {n} Medium | 🟢 {n} Low
- **Top risk:** R-{nnn} — {brief description} (Score: {n})
- **Risk categories covered:** {n} of 10
- **Contingency:** Schedule +{n} weeks; Budget +{n}%; {n} descoping candidates

**Top 3 risks:**
1. {R-nnn}: {description} — Score {n} — Owner: {role}
2. {R-nnn}: {description} — Score {n} — Owner: {role}
3. {R-nnn}: {description} — Score {n} — Owner: {role}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Risk register is comprehensive; proceed
- (b) **Add risks** — I'm aware of additional risks not captured
- (c) **Adjust scores** — Some probabilities or impacts are mis-assessed
- (d) **Revise responses** — Response strategies need different approach
- (e) **Adjust contingency** — Contingency reserves need revision
```

---

### Step 13: Log and Transition

1. **Decision Log:** D-{nnn}: "Risk Register approved. {n} risks identified: {very_high} very high, {high} high, {medium} medium, {low} low. Top risk: R-{nnn}."
2. **State File:** Stage 13 = ✅ Done; Current Stage = 14
3. **Lessons Learned:** LL-{nnn}: Note any pattern (e.g., "Resource risks dominant — reflects tight labor market")

Display:

```
✅ Stage 13: Risk Management — Complete

⚠️ Risks: {n} total | 🔴 {n} | 🟠 {n} | 🟡 {n} | 🟢 {n}
📄 Saved to: {file_path}

Next → Stage 14: Governance & Communication
```

---

## Output File

Save to:
- Numbered: `{output_root}/08_Risk_Management/Risk_Register.md`
- Flat: `{output_root}/pilc-docs/planning/Risk_Register.md`

---

## Risk Identification Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| Complete coverage | All 10 categories considered; gaps justified |
| Specific statements | Cause-event-impact format; no vague one-liners |
| Balanced scoring | Not all risks scored the same; differentiation exists |
| Owned | Every risk has a named owner (role at minimum) |
| Actionable responses | Response actions are concrete, not "monitor the situation" |
| Proportional | Response effort proportional to risk severity |
| No duplicates | Each risk is distinct; related risks may be grouped but not duplicated |
| Connected to assumptions | Key assumptions from register reflected as risks |
