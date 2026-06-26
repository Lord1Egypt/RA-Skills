# Logistics Exception Management — LLM Grading Rubric

## Purpose

This rubric guides an LLM grader in scoring agent responses to logistics exception management evaluation scenarios. Each scenario contains 3–5 evaluation criteria with pass/fail rubric descriptions. The grader assigns a score to each criterion, and the weighted sum produces the scenario score.

---

## Grading Scale

| Rating | Score | Definition |
|---|---|---|
| **Pass** | 1.0 | Response demonstrates domain expertise. The recommended actions are what an experienced freight exceptions analyst would do. Correct legal/regulatory frameworks are cited. Severity classification, escalation triggers, and financial thresholds are applied accurately. The response reflects operational judgment — not just textbook knowledge but awareness of how things actually play out with carriers, customers, and internal teams. |
| **Partial** | 0.5 | Response is directionally correct but incomplete or imprecise. The agent identifies the general category of problem and suggests reasonable actions, but misses critical operational details, applies thresholds incorrectly, omits a key stakeholder, or provides advice that would work in theory but cause problems in practice (e.g., filing a claim before all partial deliveries are reconciled, or threatening a carrier during peak season when alternatives are scarce). |
| **Fail** | 0.0 | Response is incorrect, dangerously incomplete, or generic. The agent either misidentifies the exception type, applies the wrong legal framework (e.g., Carmack for international air), recommends actions that would harm financial recovery or carrier relationships, or provides advice so generic it could apply to any industry ("contact the vendor and request a resolution"). A response that sounds plausible to a layperson but would make a logistics professional wince. |

### Grading Decision Guide

When choosing between adjacent ratings, use these tiebreakers:

**Pass vs. Partial:**
- Did the response identify the *single most critical action* for this scenario? If yes and the rest is reasonable, lean Pass.
- Would an operations manager reading this response need to add significant corrections before acting on it? If yes, Partial.

**Partial vs. Fail:**
- Does the response demonstrate awareness that this is a logistics/freight context (not generic supply chain)? If not, Fail.
- Would following the response's advice cause active harm (financial loss, regulatory violation, relationship damage, patient/safety risk)? If yes, Fail.
- Is the response merely incomplete but pointed in the right direction? Partial.

---

## Domain Expertise vs. Generic Response

The core distinction this rubric enforces is between responses grounded in freight operations expertise and responses that apply generic business logic to a logistics-shaped problem.

### What Constitutes Domain Expertise

An expert-level response demonstrates knowledge that can only come from working in freight exception management. Specifically:

**1. Carrier-Specific Operational Knowledge**
- Knows that LTL freight touches 2–4 terminals and each touch is a damage/loss risk point
- Understands that calling a specific terminal is different from calling the carrier's 800 number, and far more effective
- Recognizes that carrier claims departments have settlement authority thresholds (e.g., terminal managers up to ~$2,500)
- Knows that a carrier's set-point temperature recorder and an in-cargo data logger (Sensitech/TempTale) measure different things and can legitimately disagree
- Understands the difference between a broker and an asset carrier, and why double-brokering creates insurance gaps

**2. Legal and Regulatory Framework Application**
- Applies Carmack Amendment correctly to domestic surface transportation and knows its exceptions (act of God, public enemy, shipper, public authority, inherent vice)
- Applies Montreal Convention to international air freight with correct liability limits (22 SDR/kg) and filing deadlines (14 days for damage)
- Applies COGSA to ocean freight with correct per-package limits ($500)
- Knows the 9-month claims filing deadline under 49 USC § 14706
- Distinguishes between the 5-day concealed damage notification (industry practice) and the 9-month statutory filing deadline
- Understands that force majeure limits delay liability but does not eliminate the carrier's duty of care for the cargo

**3. Financial Threshold Judgment**
- Correctly maps claim values to the eat-the-cost/fight-the-claim framework:
  - < $500: absorb if relationship is good
  - $500–$2,500: standard process, accept partial settlements above 70%
  - $2,500–$10,000: full process, escalate at 30 days, reject below 80%
  - \> $10,000: VP awareness, dedicated handler, reject below 90%
- Calculates total exposure including consequential costs, not just product value
- Considers the ROI of claims processing ($150–$250 internal cost per claim)

**4. Operational Sequencing and Timing**
- Knows when to act immediately vs. when to wait (e.g., allow trace time for LTL shortages before filing loss claims)
- Understands hours-of-service (HOS) constraints on driver rerouting decisions
- Calculates reefer fuel burn rates for stationary trucks
- Knows that filing a shortage claim before all partial deliveries are reconciled gives the carrier ammunition to reject

**5. Stakeholder and Relationship Awareness**
- Never names the carrier to the customer in negative communications
- Matches communication tone to severity and relationship quality
- Knows that threatening to pull volume during peak season is an empty threat when alternatives are scarce
- Engages carrier account managers (not just claims reps) for significant issues
- Involves procurement for carrier performance reviews because they own the rate relationship

### Common Indicators of Generic Responses

These patterns indicate the response lacks domain-specific expertise. Any single indicator is not disqualifying, but multiple indicators strongly suggest a Fail or low Partial:

**1. Wrong Abstraction Layer**
- Refers to the carrier as "the vendor" or "the supplier"
- Calls the BOL a "receipt" or "shipping document" without using the correct term
- Describes claims as "complaints" or "disputes" without referencing the formal claims process
- Suggests "contacting customer service" rather than specific departments (OS&D, claims, terminal operations)

**2. Missing Operational Mechanics**
- Does not annotate the POD at delivery — this is the single most important action for visible damage/shortage
- Suggests signing a clean BOL and "filing a claim later" for visible exceptions
- Does not distinguish between FTL and LTL resolution strategies (scan gaps mean different things for each)
- Recommends refusing an entire multi-pallet shipment over 1 damaged pallet
- Does not preserve packaging or physical evidence for carrier inspection

**3. Incorrect Legal Application**
- Cites Carmack Amendment for international air or ocean freight
- Uses the wrong filing deadline (e.g., 60 days or 1 year instead of 9 months for domestic surface)
- Does not know that consequential damages are generally excluded under Carmack
- Treats force majeure as a complete liability shield (it limits delay liability, not cargo care)
- Applies domestic US regulations to cross-border or international shipments

**4. One-Dimensional Analysis**
- Addresses only the carrier claim without considering the customer's timeline
- Focuses on financial recovery without considering regulatory implications (pharma, food, controlled substances)
- Suggests a single course of action without contingency planning
- Does not consider the pattern when evaluating individual exceptions (e.g., 5th exception from same carrier)

**5. Tone-Deaf Communication**
- Recommends aggressive/threatening communication for minor exceptions
- Blames the carrier by name in customer-facing communications
- Sends an email when a phone call is needed (or vice versa)
- Does not calibrate urgency to severity — treats a $3,200 delay the same as a $340,000 pharma temperature excursion

---

## Scoring Individual Criteria

For each criterion within a scenario, the grader should:

1. **Read the scenario context and task** to understand what the agent was asked to do.
2. **Read the criterion's pass and fail rubric descriptions** — these are specific to the scenario, not generic.
3. **Evaluate the agent's response** against both the pass and fail descriptions.
4. **Assign a rating:**
   - **Pass (1.0):** The response matches the pass description substantively. Minor wording differences are fine — the grader is evaluating whether the agent demonstrated the same operational judgment, not whether it used identical phrasing.
   - **Partial (0.5):** The response falls between the pass and fail descriptions. It captures some elements of the pass description but misses others, or gets the direction right but the details wrong.
   - **Fail (0.0):** The response matches the fail description, or is worse than the fail description, or does not address the criterion at all.

### Important Scoring Nuances

**Specificity Matters**
A response that says "contact the carrier about the damage" is not the same as a response that says "annotate the POD with damage details before the driver leaves, photograph from multiple angles, and request a carrier inspection." The first is generic; the second demonstrates process knowledge. Grade accordingly.

**Sequence Matters**
In logistics exceptions, the order of actions often matters as much as the actions themselves. A response that recommends the right actions in the wrong order (e.g., filing a claim before completing a count, or contacting the customer before having a resolution plan) should receive Partial rather than Pass.

**Omission Is Failure**
If a criterion's pass description includes 4 elements and the response covers 2 well but ignores 2, this is Partial — not Pass. The pass description represents the complete expert response.

**Over-Escalation Is as Wrong as Under-Escalation**
A response that triggers VP notification and a fraud investigation for a $900 LTL shortage is as incorrect as one that ignores a $340,000 pharma temperature excursion. Correct severity classification is fundamental to domain expertise.

**Practicality Test**
Would an experienced freight exceptions analyst read this response and say "yes, that's exactly what I'd do"? If yes, Pass. Would they say "that's roughly right but they're missing X"? Partial. Would they say "no, that would make things worse"? Fail.

---

## Grading Edge Cases

### When the Response Is Right for the Wrong Reasons

If the agent recommends the correct action but explains it using incorrect reasoning (e.g., recommends filing within 9 months but cites the wrong statute), assign **Partial**. Correct actions with wrong reasoning suggest the agent may not replicate the correct behavior in novel situations.

### When the Response Adds Correct Information Not in the Rubric

If the agent provides additional relevant and correct information beyond what the pass rubric describes, this does not change the scoring — it's still a Pass. Do not penalize for additional correct content, even if it wasn't asked for, unless it contradicts other parts of the response.

### When the Response Contradicts Itself

If the agent states conflicting recommendations (e.g., "absorb the cost" in one paragraph and "file a full claim" in another), assign **Fail** for that criterion unless one recommendation is clearly framed as contingent on a condition.

### When the Scenario Has Evolved Since the Rubric Was Written

The rubric pass/fail descriptions reflect the expected best practice at the time of writing. If the agent references a legitimate recent change in regulations, carrier practices, or industry standards that alters the expected response, the grader should give the benefit of the doubt and assign **Partial** at minimum, then flag the scenario for rubric review.

### When the Response Addresses a Different Aspect of the Problem

If the criterion asks about "carrier communication" and the agent's response focuses entirely on "customer communication" (a different criterion), assign **Fail** for the carrier communication criterion even if the customer communication content is excellent. Each criterion is graded independently.

---

## Terminology Weighting

Domain-specific terminology usage is a signal, not a score. The grader should use terminology as follows:

**Terminology that signals expertise (positive signal, supports higher scores):**
- Correct use of: BOL, POD, PRO number, OS&D, Carmack, Montreal Convention, COGSA, HTS code, USMCA, SDR, concealed damage window, force majeure, detention, demurrage, lumper, accessorial, declared value, carrier authority, MC number, FMCSA, SAFER
- Correct differentiation between: LTL vs FTL resolution paths, broker vs asset carrier, origin vs destination detention, set-point vs cargo temperature, filing deadline vs notification window

**Terminology that signals generic knowledge (neutral — neither helps nor hurts):**
- Standard business terms used correctly: escalation, stakeholder, SLA, KPI, root cause analysis
- General logistics terms: supply chain, last mile, fulfillment, logistics provider

**Terminology that signals misunderstanding (negative signal, supports lower scores):**
- Misuse of industry terms (e.g., calling a BOL a "bill of landing," using "PRO number" for an air waybill)
- Using generic terms where specific terms exist (e.g., "shipping company" instead of "carrier" or "broker")
- Applying the wrong framework's terminology (e.g., "return authorization" for a freight claim)

**Important:** Terminology alone does not determine the score. An agent that uses all the right words but recommends the wrong actions should still fail. An agent that uses plain language but recommends the correct actions with proper operational judgment should still pass. Terminology is a supporting signal for borderline cases.

---

## Aggregate Interpretation

After scoring all criteria for all scenarios, the following aggregate benchmarks indicate capability levels:

| Aggregate Score | Interpretation |
|---|---|
| **≥ 85%** | Expert-level logistics exception management capability. The agent can handle the full range of exceptions with minimal human oversight. Suitable for production use in exception triage, initial response, and routine claims processing. |
| **70–84%** | Competent with supervision. The agent handles routine exceptions well but needs human review on complex multi-party disputes, regulatory situations, and high-value claims. Suitable for first-draft responses that a human analyst reviews. |
| **50–69%** | Inconsistent. The agent demonstrates some domain knowledge but has significant gaps. May produce harmful advice on hard scenarios. Requires heavy human supervision and should not be used for customer-facing communications without review. |
| **< 50%** | Insufficient domain expertise. The agent's responses are predominantly generic and would not be useful to a logistics professional. Not suitable for any autonomous exception management tasks. |

### Difficulty-Adjusted Expectations

The scenario set is designed with a difficulty distribution:
- **Easy (~30%):** An agent with basic logistics training should pass these. Failure on easy scenarios is a strong negative signal.
- **Medium (~40%):** An agent needs genuine operational knowledge to pass these consistently. Partial scores are common and acceptable.
- **Hard (~30%):** These are designed to trip up agents without deep domain expertise. Even competent agents may score Partial on some hard scenarios. Consistent Pass on hard scenarios indicates true expert-level capability.

A capable agent should score ≥90% on easy, ≥70% on medium, and ≥50% on hard scenarios. An agent scoring below 50% on easy scenarios has fundamental gaps that disqualify it from the domain.
