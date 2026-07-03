# Vendor Evaluation & Selection

## Objectives

Based on RFP responses, through written evaluation → vendor demos → PoC → reference checks → final decision, select the optimal vendor and produce a selection decision report.

---

## Prerequisites
- RFP has been issued, proposals have been collected
- Evaluation team has been formed (business + IT + procurement + security + legal)
- Scoring criteria and weights have been published in the RFP

## Inputs
- Vendor proposals (3-5)
- Vendor standardized pricing tables (cross-comparable)
- Evaluation scorecard template (from templates/Vendor Scorecard Template.md)

---

## Operation Steps

### Step 1: Written Proposal Evaluation

#### 1.1 Form the Evaluation Committee

| Role | Responsibility | Voting Weight |
|------|------|---------|
| Business Owner (Lead Evaluator) | Business requirements fit | 30% |
| IT Lead | Technical fit + architecture | 25% |
| CIO / IT Director (Decision Maker) | Strategic fit + final decision | 20% |
| Procurement | Commercial terms + risk | 10% |
| Security Lead | Security & compliance | 10% |
| Legal | Contract risk | 5% |

#### 1.2 Independent Scoring (score individually first, then aggregate and discuss)

**Discipline:**
- Each evaluator reads proposals and scores independently first (no cross-discussion, to avoid "herd mentality")
- After scoring is complete, aggregate all scores
- Only discuss items where score variance exceeds 2 points (on a 10-point scale)
- Scores may be adjusted after discussion, but the reason for adjustment must be recorded

#### 1.3 Score Aggregation

| Evaluation Dimension | Weight | Vendor A | Vendor B | Vendor C |
|---------|------|--------|--------|--------|
| Functional Coverage | 25% | 8.5 | 9.0 | 7.0 |
| Technical Architecture | 15% | 8.0 | 8.5 | 6.0 |
| Implementation Capability | 15% | 7.0 | 8.0 | 8.5 |
| Industry Experience | 10% | 9.0 | 7.0 | 6.0 |
| Company Stability | 5% | 9.0 | 8.0 | 7.0 |
| Support Services | 10% | 7.0 | 8.5 | 8.0 |
| Total Cost (TCO 5-Year) | 15% | 6.0 (expensive) | 8.0 (mid) | 9.0 (affordable) |
| Innovation / Future-readiness | 5% | 8.0 | 9.0 | 5.0 |
| **Weighted Total** | **100%** | **7.65** | **8.30** | **7.23** |

Cost score conversion: (budget median / vendor price) × 10, capped at 10

#### 1.4 Narrow to 2-3 Vendors for Demo Stage

Principles:
- Top 3 by total score (if the gap between 3rd and 4th is within 0.5 points, both advance to demo)
- Any vendor failing a "must-have" requirement is eliminated immediately (regardless of total score)
- Watch for extreme single-dimension scores: e.g., perfect technical score but 3 for implementation capability → red flag

---

### Step 2: Vendor Demo Evaluation

#### 2.1 Demo Day Preparation

**Standardized Agenda (3 hours per vendor):**
```
0:00-0:30  Vendor company introduction + project understanding (30min)
0:30-1:30  Product/solution demo (60min) — CORE!
1:30-2:00  Implementation methodology + team introduction (30min)
2:00-2:30  Customer case sharing (30min)
2:30-3:00  Q&A (30min)
```

**Mandatory Requirements:**
- Demo must use the real product, not just slides (unless you're buying slides)
- Prepare 3-5 real business scenario scripts; have vendors demonstrate how they meet each one live
- All vendors demo the same scenarios for easy comparison
- The vendor demo team = the team that will do your implementation (don't let sales do the demo and then have a completely different implementation team)

#### 2.2 Demo Evaluation Dimensions

| Dimension | Score (1-10) | Observation Points |
|------|----------|---------|
| Product Functionality | [1-10] | Fit + usability + response speed |
| Demo Preparedness | [1-10] | Well-prepared? Scenarios address pain points? |
| Team Capability | [1-10] | Professional answers? Honest enough to say "I don't know"? |
| Communication & Understanding | [1-10] | Understands our business? Or just generic slides? |
| Flexibility | [1-10] | Willing to customize? Or "our product is what it is"? |
| Cultural Fit | [1-10] | Imagine working with this group for 18 months — how does it feel? |

#### 2.3 Post-Demo Summary

Each evaluator completes:
```
Vendor: [Name]
Most appreciated: [up to 3 points]
Most concerned about: [up to 3 points]
If we choose this vendor, what is the biggest risk?
If we choose this vendor, would you be willing to be the project's business sponsor? (Yes/No)
Other thoughts:
```

---

### Step 3: PoC (Proof of Concept) / Trial

#### 3.1 When Is a PoC Needed?

PoC is needed when:
- The product's capability in key scenarios is uncertain
- Technical integration complexity is high
- Vendor is small but product is innovative (need to verify it can actually deliver)
- This is a "platform" product that many future systems will depend on

PoC is NOT needed when:
- Mature product / industry standard (e.g., Office 365, Salesforce)
- Proven success cases at the same scale in the same industry
- Evaluation team is highly confident in product capabilities
- Time / budget does not permit

#### 3.2 PoC Design

**5 Elements of a Successful PoC:**

1. **Scoped**: 1-3 most critical scenarios, not "set up the entire system and try it out"
2. **Time-boxed**: 2-4 weeks, no longer (otherwise it becomes a mini-project)
3. **Clear success criteria**: Not a vague "let's try it out," but:
   ```
   PoC Success Criteria:
   □ Scenario 1: Import 1 million user records, time <2 hours, data accuracy >99.9%
   □ Scenario 2: Core API response time <200ms (P99), 500 concurrent QPS without degradation
   □ Scenario 3: Bidirectional data sync with existing CRM, latency <5 seconds
   All 3 met = PoC passed
   1 not met = discuss whether acceptable (depending on deviation)
   2 not met = not passed
   ```
4. **Client-provided data**: Use the client's own (anonymized) data, not fake data for PoC
5. **PoC is also a team test**: Observe the vendor PoC team's professionalism / communication / responsiveness → this is what project implementation will look like

#### 3.3 Post-PoC Decision

```
PoC Result:
├── All passed → Enter final negotiation
├── Partially passed → Analyze whether gaps are acceptable
│   ├── Acceptable → Require vendor to commit in contract to resolve before go-live
│   └── Not acceptable → Eliminate or request second PoC
└── Not passed → Eliminate
```

---

### Step 4: Reference Customer Investigation

#### 4.1 Find Real Reference Customers

Don't just ask the vendor for their "friendly customers." Instead:
- Randomly pick from vendor's case list
- Use LinkedIn / industry networks to find peers using the vendor's product
- Ask the vendor: "Do you have any clients in XX industry / XX scale / gone live within the last year?"

#### 4.2 Reference Check Question List

**5 Must-Ask Questions:**

1. "If you could do it over, would you still choose this vendor? Why / why not?"

2. "What was the actual total cost compared to your initial budget? (The answer is usually 1.5-2x — find out what drove the increase)"

3. "What was the biggest problem during implementation? Was there anything the vendor promised but didn't deliver?"

4. "After go-live, how stable is the system? How often do issues occur? How quickly do they resolve them?"

5. "Is their team, especially key personnel, stable? Did anyone change during the project?"

**Additional Questions:**
- "How is their support / customer service quality? How long does it typically take to resolve an issue?"
- "Did the implementation go over time? By how much? What caused it?"
- "Were there any hidden costs not written into the contract?"
- "If you could do it again, what clause would you write into the contract?"

**Interview Tips:**
- Phone call > email questionnaire (people are more honest on the phone)
- Build trust first: "We're peers — help me avoid the pitfalls you encountered"
- If they are vague or overly formal, be cautious (they may have signed an NDA preventing honest feedback, or they may simply be dissatisfied)

---

### Step 5: Final Evaluation & Decision

#### 5.1 Update Composite Score

Incorporate demo and PoC results into scoring:

| Stage | Weight | Vendor A | Vendor B |
|------|------|--------|--------|
| Written Proposal | 40% | 7.65 | 8.30 |
| Demo Evaluation | 25% | 7.0 | 8.5 |
| PoC Result | 20% | 8.0 (PoC passed) | — (not done) |
| Reference Check | 15% | 8.0 | 7.0 |
| **Final Composite Score** | **100%** | **7.63** | **8.03** |

#### 5.2 Decision Matrix (Beyond Just Scores)

The final decision is not just about the highest score — also answer:

```
Strategic Level:
□ Will this vendor still exist and thrive in 3-5 years?
□ Is this vendor's product roadmap aligned with our IT strategy direction?
□ If we choose this vendor, will we be locked in (Vendor Lock-in)?

Execution Level:
□ Do we have enough internal capacity to manage this vendor?
□ How much leverage do we have in contract negotiation? (sole source vs. multiple options)
□ If implementation fails, how high is the exit cost?

Political Level:
□ Can all key stakeholders accept this choice?
□ Is there anyone with strong objections that need to be addressed in advance?
```

#### 5.3 Selection Decision Report

```
Selection Decision Report: [Project Name]

1. Evaluation Overview
   - Project background and scope
   - Participating vendors: A / B / C (D eliminated due to late submission)
   - Evaluation process: Written (Week 1-2) → Demo (Week 3) → PoC (Week 4-6) → Reference Check (Week 5)

2. Composite Evaluation Results
   | Vendor | Written (40%) | Demo (25%) | PoC (20%) | Reference (15%) | Total |
   |--------|----------|----------|---------|----------|------|
   | A      | ...      | ...      | ...     | ...      | ...  |
   | B      | ...      | ...      | ...     | ...      | ...  |

3. Key Differentiators
   - Vendor A's core strengths: ...
   - Vendor A's main risks: ...
   - Vendor B's core strengths: ...
   - Vendor B's main risks: ...

4. Recommendation
   - Recommended choice: Vendor [__]
   - Rationale: [1-2 paragraphs]
   - Key negotiation points: ...
   - Key implementation risks and mitigations: ...

5. Decision Record
   - Evaluation committee member signatures
   - Final decision-maker signature
   - Date
```

---

## Outputs
1. **Written evaluation score summary table**
2. **Demo evaluation summary** (one per vendor)
3. **PoC report** (including success criteria + results)
4. **Reference check report**
5. **Final selection decision report**

---

## Quality Checklist
- [ ] Each evaluator scored independently, with written records
- [ ] Cost calculation considers 5-year TCO, not just Year 1
- [ ] At least 2 reference customers contacted via real conversation (not email questionnaire)
- [ ] PoC had clear pass/fail criteria defined before execution
- [ ] Final decision has complete written record (including why other vendors were not selected)
- [ ] Legal has reviewed key aspects of the vendor contract

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|------|---------|---------|
| Sales demo = product capability | Demo environment is carefully prepared, data is clean, network is dedicated | Require PoC with your own (anonymized) data, running in a real environment |
| Focus on features, ignore the team | Bought the best product, but implementation team is outsourced interns | Lock key team members in the contract; no arbitrary replacement during implementation |
| Not calling for reference checks | Vendor's "friendly list" will only say good things | Find real customers, call them (not send surveys); ask "if you could do it over" |
| Attracted by low pricing | Year 1 quote is very low, Years 3-5 renewal doubles | Look at 5-year TCO, renewal terms, hidden costs (customization / integration / training) |
| Over-reliance on Gartner | Gartner quadrants are pay-to-participate, not objective evaluations | Combine peer feedback + PoC + reference checks to form independent judgment |
| Decision procrastination | "Let's evaluate one more" → "Let's look again" → project window closes | Set a clear decision date and decide before it |