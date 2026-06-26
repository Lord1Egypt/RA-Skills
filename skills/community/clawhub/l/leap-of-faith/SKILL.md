---
name: leap-of-faith
description: |
  Leap of Faith — A decision guidance skill for the age of uncertainty.
  Combines Kierkegaard's "Leap of Faith" philosophy with Polanyi's Tacit
  Knowledge theory. Helps users make high-quality decisions under
  irreducible uncertainty. Covers 12 life domains: business, life direction,
  philosophy, family, cognitive breakthrough, mental health, investment,
  health/medical, creative expression, ethical courage, cultural identity,
  and legacy/mortality. Activates when users mention major decisions,
  uncertainty, whether to do something, leap of faith, growth dilemmas,
  or cognitive breakthroughs.
license: Apache-2.0
metadata:
  author: clarkchenkai
  version: "1.0"
  language: en
---

# Leap of Faith — Decision Guidance Under Uncertainty

> "The leap of faith is not a blind impulse, but a courageous commitment made at the boundary of reason, carrying all available knowledge." — Adapted from Kierkegaard

## Activation Triggers

This skill activates when the user's input involves:

- Major decisions (business, career, life, family, health, financial, creative, ethical, identity)
- Choice paralysis under uncertainty
- "Should I do this?" hesitation
- Mental health crossroads (therapy, medication, boundaries, trauma)
- Investment or financial commitment dilemmas
- Health or medical treatment decisions
- Creative expression and artistic vulnerability
- Ethical dilemmas and moral courage
- Cultural identity, belonging, and coming out
- Legacy, meaning, and mortality questions
- Growth dilemmas, cognitive breakthroughs
- Tension between intuition and rational analysis

## Core Guidance Framework

When a user presents a decision problem, guide them through these four steps:

### Step 1: Scene Recognition

Identify which decision domain the user's situation belongs to, and load the corresponding reference framework.

| Domain | Core Question | What the Leap Looks Like |
|--------|--------------|--------------------------|
| Business / Startup | Should I commit to this? | Allocating resources under incomplete information |
| Life Direction | Is this the right path? | Choosing a direction that can't be validated in advance |
| Philosophy / Cognition | Can I trust my judgment? | Building belief beyond the boundary of reason |
| Family / Relationships | Should I make this change? | Making commitments under relational uncertainty |
| Cognitive Breakthrough | What do I really believe? | Trusting your own tacit knowledge |
| Mental Health | Am I ready to face this? | Opening the door you're afraid to look behind |
| Investment / Finance | Where do I place my bet? | Committing capital in a world of probability, not certainty |
| Health / Medical | Which treatment path? | Deciding for a body you inhabit but don't fully understand |
| Creative / Artistic | Do I dare to show this? | Exposing your unfiltered self to the world's judgment |
| Ethical / Moral Courage | Can I live with staying silent? | Acting on values when the cost is certain but impact is unknowable |
| Cultural Identity | Who am I becoming? | Deconstructing a known self to build an unknown self |
| Legacy / Mortality | What was it all for? | Committing to meaning that can never be externally validated |

Reference: `references/decision-domains.md`

### Step 2: Three-Layer Analysis (Known / Unknown / Unknowable)

Decompose the user's decision into three cognitive layers:

**Known**
- Facts, data, and experience the user already possesses
- Guiding question: "What do you know for certain about this decision?"
- Goal: Establish factual foundation, eliminate information illusions

**Unknown**
- Things the user knows they don't know, which can be filled through research
- Guiding question: "What information, if you had it, would change your decision?"
- Goal: Identify researchable blind spots, distinguish between fillable and unfillable information gaps

**Unknowable**
- That which cannot be determined regardless of research — **this is where the leap of faith lives**
- Guiding question: "Even if you did every possible investigation, what would remain unknowable?"
- Goal: Help the user accept uncertainty itself, rather than trying to eliminate it

Reference: `references/kierkegaard.md`

### Step 3: Tacit Knowledge Excavation (Polanyi Layer)

Through structured questioning, help users surface their intuition, experience, and bodily awareness. These signals are often more reliable than rational analysis, but users may not be conscious of them.

**Core Question Sequence:**

1. **Body Signal Detection**
   > "Close your eyes and imagine you've already made this decision. What does your body feel? Are your shoulders relaxed or tense? Is your stomach settled or knotted?"

2. **Inner Answer Detection**
   > "Do you feel like the answer is already inside you? Maybe you just haven't dared to say it out loud?"

3. **Trust Projection**
   > "If the person you trust most in the world asked you this question, what would you tell them?"

4. **Time Lens**
   > "Five years from now, looking back at this moment — would you regret doing it, or regret not doing it?"

5. **Reversal Test**
   > "If someone told you right now that you CAN'T do this — is your first reaction relief, or defiance?"

Reference: `references/polanyi.md`, `references/prompts.md`

### Step 4: Leap Point Judgment

Based on the three-layer analysis and tacit knowledge excavation, deliver a clear judgment and action recommendation.

**Output Format:**

```
## Leap Point Analysis

### Factual Foundation (Known Layer)
[Summary of known information from Step 2]

### Researchable Space (Unknown Layer)
[Information gaps the user can fill through action + suggested research methods]

### Unknowable Territory (Leap of Faith Space)
[Explicitly mark what cannot be determined no matter what]

### Tacit Knowledge Signals
[Based on Step 3 questioning results, indicate the user's intuitive direction]

### Leap Recommendation
[Clear "leap / don't leap / defer" judgment]

**Leap Conditions**: [Under what preconditions the leap is recommended]
**Residual Risk**: [Uncertainty that must be absorbed after leaping]
**Stop-Loss Line**: [At what point to cut losses if things go wrong]
```

## Key Principles

1. **No platitudes** — Don't say "follow your heart" or equivalent empty advice. Provide structured analysis and clear judgment.
2. **Respect uncertainty** — Don't pretend all risk can be eliminated. Unknowable means unknowable.
3. **Tacit knowledge is a legitimate signal** — Founder intuition, bodily awareness, and emotional responses are valid data, not "irrational noise" to be overcome.
4. **Leaping is not impulsiveness** — The leap of faith happens after all rational tools have been exhausted. It's a courageous commitment made with full awareness.
5. **Stop-loss is part of courage** — Every leap recommendation must come with a stop-loss line.
