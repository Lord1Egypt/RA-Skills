# Example: International pricing PRD review

A complete end-to-end example showing the skill running on a realistic English pricing PRD. Use this as the **calibration reference** for tone, length, and structure in the international version.

---

## Input PRD

```
PRD: Launch "Pro" tier at $19/month

Target user: Power users of our free analytics tool (top 10% by usage volume)

User problem: Free tier hits a 100K events/month cap; power users have to leave 
for competitor X once they outgrow our limits.

Proposal:
- Introduce a "Pro" tier at $19/month
- Pro removes the 100K cap, adds advanced filters, adds 5 team seats
- Free tier remains, capped at 100K events
- Upgrade prompts triggered when user hits 80% of their cap

Success metric: ARR
Scope: Pro tier only this quarter. Enterprise tier deferred to next year.
```

---

## Full output

```
⚠️ About Expert Perspectives

The views attributed to each expert below are interpretive applications
of their publicly documented frameworks, not the individuals' actual
opinions on your specific proposal. "Senior PM Director" and "The Closer"
are fictional archetypes.

Use these perspectives as thinking tools, not authoritative endorsements.


Senior PM Director: Let me scan the PRD first.

[brief pause]

Senior PM Director: You wrote "ARR" as the success metric. What's the target — 6 months out, 12 months out?

PM: $1M ARR in 12 months.

Senior PM Director: Got it. What free → Pro conversion rate is that assuming? 1%? 5%?

PM: skip

Senior PM Director: Fine. We'll assume you haven't modeled it. Cagan will pick that up.

Senior PM Director: $19/month. Why $19? Competitive benchmark?

PM: Competitor X charges $29 for a similar feature set. We're undercutting.

Senior PM Director: Okay. Under what condition would you kill the Pro tier?

PM: < 2% of eligible free users convert in the first 6 months.

Senior PM Director: That's a real kill criterion. Noted. Last one: anything special about your free→paid funnel today, or is this the first paid tier?

PM: First paid tier. We've never charged before.

Senior PM Director: Mmm. That's going to come up later. Okay, enough. Let's go.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎤 Today's review panel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

▸ Marty Cagan
  Author of *Inspired*, founder of SVPG
  Lens: Four Big Risks (value / usability / feasibility / viability)
  Signature: "How do you know users want this?"

▸ Clayton Christensen
  Harvard Business School, JTBD theorist
  Lens: Jobs to be Done — what is the user hiring this for?
  Signature: "What are they using instead today?"

▸ Senior PM Director
  15+ years at top tech, 3+ 0-to-1 products shipped
  Lens: Experiential opposition, historical failure pattern-matching
  Signature: "I saw this at [X] and it didn't end well."

▸ Reid Hoffman
  Co-founder of LinkedIn, *Blitzscaling* author
  Lens: Network effects, growth loops, market timing
  Signature: "Does this product get better at user 1M than at user 100?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRD classification: Business model / Pricing
Panel size: 4 experts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Round 1: Parallel Reviews
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Marty Cagan] Tendency: GO

Walking through the 4 risks:
- Value: clear — power users already leave for paid competitors. Validated.
- Usability: low risk for a pricing change.
- Feasibility: trivial.
- Viability: depends on conversion math, which the PM didn't model. Kill criterion at 2% is reasonable.

The value risk is largely de-risked by the existence of competitor X. The main unknown is conversion economics.

📍 Follow-up: What's your projected free → Pro conversion rate at the 80% cap trigger point? You need a number, not just a kill threshold.

───

[Clayton Christensen] Tendency: CONDITIONAL

The job your free users are hiring you for: "show me what's happening in my product without engineering effort." When they hit the cap, they fire you and hire competitor X. Pro is a way to stay hired.

But: there are two distinct jobs hidden here. The "I'm growing past the cap" job is solved by removing the cap. The "I need advanced filters and team seats" job is a different need. Bundling them at $19 may underprice the second job.

📍 Follow-up: Have you talked to users who already left for competitor X? What did they hire X to do that you couldn't?

───

[Senior PM Director] Tendency: CONDITIONAL

First paid tier at a company that's never charged before. This is the riskiest moment — not because the feature is wrong, but because the org isn't prepared.

I've seen this twice: tooling-first SaaS launches a paid tier, ARR looks fine for 2 quarters, then churn hits 6%/month because no one built renewal infrastructure. Billing, support escalation paths, dunning workflows — none of this is in the PRD.

📍 Follow-up: Who owns renewal? Who handles billing disputes? If you don't have answers, the launch is premature regardless of price.

───

[Reid Hoffman] Tendency: GO

Pricing aggressively below competitor X is the right move at this stage. The job is to convert power users into paying users to validate the pricing surface, not to maximize ARPU.

The "5 team seats" is the smart part — it creates a small network effect within paying accounts. Once a team is on it, switching cost is multi-user, not single-user.

📍 Follow-up: Does the per-team-seat structure scale into an Enterprise tier later? Have you sketched what the next pricing surface looks like?


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[The Closer · Final Verdict]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I count 2 GO, 0 NO-GO, 2 CONDITIONAL.

Cagan called this "largely de-risked by competitor X." Hoffman noted the team-seat structure as "a small network effect" already strategically sound. But the two CONDITIONALs converge on a different concern: org-readiness. Christensen flagged that bundled jobs may underprice. The Senior PM Director was sharper: "Billing, support escalation paths, dunning workflows — none of this is in the PRD."

The product side has consensus. The launch-readiness side has unresolved gaps.

Verdict: CONDITIONAL GO

Conditions (must be met before launch):
  1. Document the renewal owner, billing operations owner, and support 
     escalation path. Deadline: 3 weeks.
  2. Interview 5 users who already left for competitor X. Identify 
     whether $19 captures all the jobs or just one. Deadline: 2 weeks.
  3. Model expected free → Pro conversion at three scenarios (1%, 3%, 5%) 
     and present to leadership. Deadline: 1 week.

Revert to NO-GO if any of these signals appear:
  • Pro subscriber churn ≥ 5% per month within first 90 days
  • < 1% of eligible (≥ 80% cap) free users convert to Pro in first 6 months
  • Customer interviews reveal "team seats" is a niche need and the primary 
    unblocking value is just "remove the cap" — pricing model is wrong

Done.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Dissent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Held by Clayton Christensen and Senior PM Director (both CONDITIONAL):

Strongest argument (Christensen):
  "Bundling two jobs at $19 may underprice the higher-value one. If 
   'advanced filters + team seats' is a more substantial need than 'remove 
   the cap,' you're leaving real money on the table."

Strongest argument (Senior PM Director):
  "First paid tier at a company that's never charged before. ARR will look 
   fine for two quarters, then churn hits if you haven't built renewal 
   infrastructure."

Failure signals to monitor (if any appear, the dissent was right):
  1. Within 6 months, the ratio of "team seats used" to "cap removal" usage 
     exceeds 2:1 — meaning team-seat is the dominant value driver, not the 
     cap. Implication: re-price upward.
  2. Pro subscriber churn ≥ 5% / month within first 90 days.
  3. > 30% of Pro support tickets are billing-related — meaning operations 
     was the binding constraint, not the product.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Immediate actions:
  • Schedule 5 interviews with churned users (Christensen's condition)
  • Document the billing/renewal ownership matrix (Senior PM Director's condition)
  • Model conversion scenarios at 1% / 3% / 5% (Cagan's condition)

Critical evidence still needed:
  • Free → Pro conversion rate projection (skipped during intake)
  • Renewal infrastructure ownership (raised by Senior PM Director)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## What this example demonstrates (for calibration)

| Aspect | Demonstration |
|---|---|
| Length | Full review ~175 lines, within the 100-180 target |
| Intake | 5 turns, 1 skip logged |
| Round 1 | Each expert ≤ 80 words, tendency labels clear, each in own voice |
| Round 2 | Skipped because no GO + NO-GO simultaneously (only CONDITIONAL was the opposition) |
| The Closer | Quoted specific phrases from Round 1; cited skip log; gave 3 conditions with deadlines; gave 3 failure signals |
| Dissent | Two CONDITIONAL voices preserved as full dissent with arguments and observable failure signals |
| Tone | Professional, decisive, honest. No flattery. No personal attacks. |
