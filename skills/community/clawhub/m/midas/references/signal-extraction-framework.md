# Signal Extraction Framework

The complete methodology for extracting wealth signals from daily-life noise using 6 analytical lenses.

---

## Overview

Every piece of daily noise contains embedded signals about economic opportunity. This framework teaches Midas how to systematically extract those signals using six complementary analytical lenses.

**The fundamental assumption:** Repetition indicates demand. If something appears in your life twice, it's not a coincidence — it's a market signal.

---

## Lens 1: Money Signal Detection

### Definition

Money Signal Detection finds where money is moving, stuck, or leaking in the input. It identifies explicit and implicit financial transactions, expenditures, and monetary frustrations.

### Core Questions

1. Is anyone in this input spending money, or complaining about spending money?
2. Is anyone looking for something to spend money on?
3. Is there a product, service, or resource mentioned more than once?
4. Is someone describing a pain point that has a dollar value attached?
5. Is there a price mentioned that seems too high or too low relative to value?
6. Is anyone negotiating, haggling, or seeking better deals?
7. Are there subscription, recurring, or subscription-like costs mentioned?
8. Is anyone expressing frustration with value received for money spent?

### Signal Strength Criteria

| Strength | Criteria |
|----------|----------|
| **Strong** | Explicit dollar amounts mentioned, multiple people confirming same expense |
| **Medium** | Relative price complaints ("too expensive"), single mentions with specificity |
| **Weak** | Vague money mentions without specificity, general cost awareness |

### Input Type Priority

1. **Purchase receipts/orders** — Direct money flow data
2. **Slack/Teams work chats** — Vendor complaints, tool subscriptions, budget discussions
3. **Text/WhatsApp** — Personal spending discussions, deal-seeking
4. **Photos** — Receipts, price tags, storefronts
5. **Browsing history** — Shopping research, comparison behavior

### Common False Positives

- Small talk about money that doesn't indicate actual spending intent
- Nostalgic references to past purchases ("I remember when gas was $1.50")
- Hypothetical spending ("If I won the lottery, I'd buy...")
- Jokes about money ("I'd rather not know what my Netflix bill is")

### Confidence Scoring Rubric

```
Base: 20%
+ Explicit price mentioned: +15%
+ Multiple confirmations of same expense: +20%
+ Expense is recurring (subscription/service): +15%
+ Person is actively seeking alternatives: +20%
+ Expense exceeds perceived value clearly: +10%

Maximum: 80% (Midas doesn't do stock predictions)
```

---

## Lens 2: Demand Gap Identification

### Definition

Demand Gap Identification finds unmet wants and needs — things people are actively seeking but cannot find, or things that exist but don't work well.

### Core Questions

1. Is someone asking for something that doesn't exist yet?
2. Is someone asking for something that exists but doesn't work well?
3. Is a complaint being repeated by multiple people?
4. Is someone doing a manual workaround for something automatable?
5. Is there a "I wish someone would just..." buried in the noise?
6. Is anyone requesting a referral or recommendation they can't get?
7. Is anyone settling for a suboptimal solution due to lack of alternatives?
8. Are people using workarounds that waste significant time or money?

### Signal Strength Criteria

| Strength | Criteria |
|----------|----------|
| **Strong** | Same complaint from 3+ people, manual workaround mentioned multiple times |
| **Medium** | Single person describing unmet need with specificity, clear frustration |
| **Weak** | Vague wishes, hypothetical wants without real urgency |

### Input Type Priority

1. **Text/WhatsApp group chats** — Repeated requests, recommendations sought
2. **Slack/Teams** — "Anyone know a..." requests, internal tool complaints
3. **Complaint dumps** — Direct articulation of frustrations
4. **Social media** — Viral complaints, trending frustrations
5. **Photos** — Workarounds visible (printed forms, manual processes)

### Common False Positives

- One-time frustrations that won't recur
- Problems people complain about but won't pay to solve
- Wants that require massive infrastructure to address
- Niche problems with zero monetization potential

### Confidence Scoring Rubric

```
Base: 25%
+ Multiple people confirming same gap: +15% per additional person (max +30%)
+ Manual workaround mentioned: +15%
+ Clear willingness to pay implied: +15%
+ Gap is in professional/profitable context: +10%
+ Solution is technically feasible with existing tools: +10%

Maximum: 85%
```

---

## Lens 3: Arbitrage Window Detection

### Definition

Arbitrage Window Detection finds price/value mismatches — opportunities where something costs less than it should in one context while being worth more in another.

### Core Questions

1. Is there a visible price/quality/speed mismatch?
2. Is something cheap in one context and expensive in another?
3. Is someone overpaying because they don't know a better option exists?
4. Is there a middleman extracting value that could be cut out?
5. Is there geographic price variation visible?
6. Is there information asymmetry being exploited?
7. Is there time arbitrage opportunity (buy now, sell later)?
8. Is there regulatory or tax arbitrage being missed?

### Types of Arbitrage

- **Geographic:** Price differences by location
- **Informational:** One party has knowledge another lacks
- **Temporal:** Time-based price fluctuations
- **Structural:** Middleman removal opportunities
- **Regulatory:** Legal variations between jurisdictions
- **Tax:** Effective rate differences
- **Skill-based:** Same service at different quality/price points

### Signal Strength Criteria

| Strength | Criteria |
|----------|----------|
| **Strong** | Explicit price comparison, clear winner, low effort to execute |
| **Medium** | Observable mismatch with unclear execution path |
| **Weak** | Potential arbitrage with high execution friction |

### Input Type Priority

1. **Purchase receipts** — Direct price data
2. **Browsing history** — Comparison shopping, price research
3. **Slack/Teams** — Vendor pricing complaints, "we're paying X for Y"
4. **Text/WhatsApp** — "Did you know [brand] is cheaper at [place]?"
5. **Photos** — Price signage, competitor storefronts

### Common False Positives

- Arbitrage opportunities that are already well-exploited
- Price differences that seem large but have hidden costs
- Arbitrage requiring skills/resources the user doesn't have
- Legal/regulatory arbitrage that crosses into gray areas

### Confidence Scoring Rubric

```
Base: 20%
+ Explicit price comparison available: +25%
+ User has existing access to cheaper source: +20%
+ Low execution friction (can act immediately): +15%
+ No significant competition already exploiting it: +15%
+ Sustainable arbitrage (not one-time): +10%

Maximum: 85%
```

---

## Lens 4: Skill-to-Revenue Bridge

### Definition

Skill-to-Revenue Bridge identifies expertise you've accumulated without realizing it — knowledge, abilities, or insights you demonstrate in daily life that others would pay for.

### Core Questions

1. What topics do you talk about with unusual specificity?
2. What do you photograph or document repeatedly?
3. What videos do you watch for extended periods?
4. What advice do you give repeatedly in conversations?
5. What problems do you solve for others that they thank you for?
6. What do you research obsessively without external prompting?
7. What skills do you use at work that aren't in your job description?
8. What do people ask you about specifically?

### Signal Strength Criteria

| Strength | Criteria |
|----------|----------|
| **Strong** | Demonstrated expertise + expressed willingness to pay + external validation |
| **Medium** | Obsessive research pattern + unsolicited advice-giving + positive reception |
| **Weak** | General interest + occasional advice + no clear monetization path |

### Input Type Priority

1. **Browsing/YouTube history** — Research patterns reveal expertise accumulation
2. **Photos** — What subjects do you repeatedly photograph?
3. **Slack/Teams** — Where do people come to you for answers?
4. **Text/WhatsApp** — What advice do you give unprompted?
5. **Complaints** — What do you complain about with insider knowledge?

### Common False Positives

- Expertise that's table stakes in your industry (everyone knows this)
- Skills you have but don't enjoy (burnout risk)
- Knowledge that's freely available everywhere (no premium)
- Skills requiring certifications you don't have

### Confidence Scoring Rubric

```
Base: 15%
+ 3+ months of consistent research/activity: +20%
+ Others explicitly value your input/help: +20%
+ You've been paid (even informally) for this before: +25%
+ Clear monetization models exist for this skill: +15%
+ You enjoy doing it: +10%

Maximum: 85%
```

---

## Lens 5: Network Monetization Path

### Definition

Network Monetization Path finds deal opportunities in your social graph — people who should be connected, introductions that could happen, and intermediation value you could capture.

### Core Questions

1. Who in the user's orbit has a problem that someone else can solve?
2. Are there two people who should be connected but aren't?
3. Is there a deal that could happen with one introduction?
4. Is the user positioned as a hub without exploiting that position?
5. Are people asking for referrals the user could provide?
6. Is anyone selling something to someone who could buy directly?
7. Is there expertise in the network being underutilized?
8. Are there partnership opportunities being missed?

### Signal Strength Criteria

| Strength | Criteria |
|----------|----------|
| **Strong** | Explicit deal context + both parties have budget/authority + warm intro possible |
| **Medium** | Clear problem/solution match + one party ready to act |
| **Weak** | Potential connection with unclear timing or readiness |

### Input Type Priority

1. **Text/WhatsApp** — Direct requests for referrals, recommendations
2. **Slack/Teams** — Cross-team needs, vendor searches, expertise hunts
3. **Email** — Forwarding patterns, introduction requests
4. **Meeting notes** — Strategic partnerships being discussed
5. **Photos** — Business cards, event badges, professional networking

### Common False Positives

- Connections that seem obvious but both parties don't actually need each other
- Introductions that won't lead to real deals
- Network positions that are weaker than they appear
- Potential deals that require more trust-building than time allows

### Confidence Scoring Rubric

```
Base: 20%
+ Both parties have been searching: +20%
+ Budget or buying intent confirmed: +20%
+ User has relationship with both parties: +15%
+ Timing is immediate: +10%
+ Finder's fee or commission is standard in this context: +15%

Maximum: 80%
```

---

## Lens 6: Behavioral Leverage Point

### Definition

Behavioral Leverage Point identifies repeated actions that could be redirected toward revenue — autopilot behaviors that could be formalized, documented, or monetized.

### Core Questions

1. What does the user do repeatedly on autopilot?
2. Which repeated behaviors could be redirected into income?
3. What subscriptions or purchases happen on a regular schedule?
4. What content does the user create or curate consistently?
5. What routine generates data or insights that could be productized?
6. What expertise-adjacent activity does the user do for free?
7. What platform or tool does the user master through repetition?
8. What repeated behavior compounds if formalized?

### Signal Strength Criteria

| Strength | Criteria |
|----------|----------|
| **Strong** | Daily/weekly repetition + clear monetization model + low pivot effort |
| **Medium** | Regular pattern + one clear monetization path + moderate effort |
| **Weak** | Irregular behavior + unclear monetization + high friction to change |

### Input Type Priority

1. **Purchase history** — Subscription patterns, repeat orders
2. **Browsing/YouTube** — Content consumption patterns
3. **Photos** — Routine documentation (gym, food, travel)
4. **Calendar** — Regular commitments and activities
5. **Slack/Teams** — Regular reports, recurring tasks

### Common False Positives

- Habits that are personal but not monetizable
- Behaviors that require too much effort to formalize
- Compounding that requires rare skills to execute
- Activities that lose value when made "official"

### Confidence Scoring Rubric

```
Base: 15%
+ Daily or near-daily repetition: +20%
+ Already generates external value (reviews, recommendations): +25%
+ Clear adjacent monetization model exists: +20%
+ Low effort to pivot: +15%
+ User has platform or audience already: +10%

Maximum: 85%
```

---

## Cross-Referencing Rules

Cross-referencing is how Midas builds conviction. Signals from different lenses or input types that point to the same opportunity are exponentially more valuable.

### Confidence Stacking

| Source Configuration | Confidence Boost |
|---------------------|------------------|
| Same lens, same input type | +5% (minor confirmation) |
| Different lens, same input type | +10% (method convergence) |
| Same lens, different input type | +20% (source diversification) |
| Different lens, different input type | +30% (strongest convergence) |

### Evidence Chain Examples

**Example 1: Contractor Marketplace Opportunity**

- Signal 1 (Lens 2 - Demand Gap): Dave complains about contractor costs in Slack (35%)
- Signal 2 (Lens 1 - Money Signal): AWS-style pricing mentioned: contractors charge premium (20%)
- Signal 3 (Lens 1 - Money Signal): Photo shows active construction in neighborhood (30%)
- Cross-reference: Construction activity + pricing frustration = local demand confirmed
- **Stacked confidence: 65%**

**Example 2: Woodworking Course Opportunity**

- Signal 1 (Lens 4 - Skill Bridge): 6 months of woodworking YouTube videos (40%)
- Signal 2 (Lens 4 - Skill Bridge): User gives detailed woodworking advice in group chats (35%)
- Signal 3 (Lens 6 - Behavioral): User built multiple furniture pieces (documented in photos) (40%)
- Cross-reference: Expertise + teaching behavior + portfolio = course-ready
- **Stacked confidence: 75%**

### Final Confidence Thresholds

| Confidence | Signal Status | Action |
|-----------|---------------|--------|
| 0-15% | Speculation | Note, don't act |
| 15-35% | Weak signal | Investigate further |
| 35-55% | Moderate signal | Design small test |
| 55-70% | Strong signal | Commit resources |
| 70-90% | Very strong signal | ACT NOW |
| 90%+ | Near-certainty | Risk-adjusted action |

---

## Failure Mode Prevention

### Premature Confidence

**Problem:** Assigning high confidence to single-source signals.

**Prevention:** Always ask "What would need to be true for this to be confirmed by a second independent source?"

### Pattern Overfitting

**Problem:** Seeing signals that confirm existing beliefs rather than new patterns.

**Prevention:** Track which signals surprise you. Novel signals are more valuable than confirmations.

### Ignoring Negative Signals

**Problem:** Only noting positive evidence, discarding negative evidence.

**Prevention:** Explicitly log "what would kill this opportunity" and check against it.

### Analysis Paralysis

**Problem:** Perfecting confidence scores instead of acting.

**Prevention:** Set thresholds. When confidence exceeds threshold, move to action regardless of remaining uncertainty.
