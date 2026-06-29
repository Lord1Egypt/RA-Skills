---
name: "persuasive-copywriting"
description: "Diagnostic sub-skill for analyzing why specific copy and communication performed well or poorly. Uses Human Behavior OS modules to diagnose message reception, attention capture, trust signals, and emotional response in existing content. Outputs analysis ONLY — never generates persuasive copy, headlines, CTAs, or marketing content."
---

# Copy & Communication Effect Diagnosis

## 0. Relationship to Parent

This reference inherits all 7 diagnostic modules, the Master Formula (as analytical lens), and quality standards from the parent Human Behavior OS skill. It adds copy-specific frameworks for **analyzing** why text-based communication succeeded or failed.

**Scope**: Diagnose existing copy performance. Do NOT generate new copy.

---

## Diagnostic Framework

### The Communication Reception Sequence

```
Attention Capture → Message Processing → Emotional Response → Trust Assessment → Action Decision
```

Use this sequence to **analyze** where a given piece of copy succeeded or failed at each stage.

| Stage | Diagnostic Question | Failure Mode |
|-------|---------------------|--------------|
| Attention | Did the headline/hook stop the reader? | Ignored, scrolled past |
| Interest | Did the lead address a real need? | Irrelevant, disconnected |
| Desire | Did benefits resonate emotionally? | No emotional engagement |
| Trust | Was the claim believable? | Skepticism, disbelief |
| Action | Did the reader take the intended action? | Inaction, abandonment |

---

## Module-Specific Diagnostic Applications

### Analyzing Attention Performance (Module 2)

**Headline/Hook Classification Table:**

Use this to **classify** what mechanism an existing headline uses — not to create new ones.

| Trigger Type | Diagnostic Marker | Example Pattern |
|-------------|-------------------|-----------------|
| Curiosity gap | Creates information void | "The X things about Y..." |
| Benefit promise | Clear gain stated | "How to [result]..." |
| Danger/risk | Threat or warning signal | "X mistakes that..." |
| Social proof | Others' validation | "Join X+ people..." |
| Story | Narrative opening | "How [person]..." |
| Contrast | Unexpected juxtaposition | "Why [common belief] is wrong" |
| Novelty | Newness claim | "The first/only..." |
| Authority | Expert/source citation | "[Expert] says..." |

#### Attention Diagnosis Output

```markdown
## Attention Analysis
- **Trigger(s) Used**: [Classified from actual copy]
- **Trigger-Scenario Fit**: [Does this trigger match the target audience's need layer?]
- **Attention Capture Score**: X/10 — [Based on available engagement data]
- **Diagnosis**: [Why this hook did/didn't work for this audience]
```

### Analyzing Need Alignment (Module 1)

**Copy-Need Mapping:**

| Need Layer | What to Look For in Copy | Misalignment Signal |
|-----------|-------------------------|-------------------|
| L1 Survival | Safety, security, essential claims | Over-promising on non-essentials |
| L2 Efficiency | Time/money saving claims | Vague benefit statements |
| L3 Emotion | Feeling, belonging language | Cold, purely functional tone |
| L4 Identity | Status, expertise signals | Tone mismatch with audience self-image |
| L5 Growth | Potential, mastery framing | Insufficient aspirational resonance |

#### Need Alignment Diagnosis

```markdown
## Need Alignment Analysis
- **Target Audience Need Layer**: [Inferred from product/context]
- **Copy's Addressed Layer**: [What need the copy actually speaks to]
- **Alignment Gap**: [Mismatch between audience need and copy focus]
- **Diagnosis**: [The copy resonated/failed because...]
```

### Analyzing Emotional Response (Module 5)

> ⚠️ **Guardrail**: This section diagnoses what emotions existing copy evokes. It does NOT prescribe emotional manipulation techniques.

**Emotion Detection in Copy:**

| Emotion | Language Markers | Behavioral Indicator |
|---------|-----------------|---------------------|
| Fear | Risk, loss, danger words | Urgent clicks, anxiety-driven action |
| Anticipation | Upcoming, soon, limited | Waitlist signups, pre-registration |
| Surprise | Unexpected, never, first | High share rates, comments |
| Aspiration | Imagine, become, unlock | Long read times, saves/bookmarks |
| Relief | Finally, solved, easy | Low bounce rate, completion |
| Curiosity | Why, how, discover | Click-through, exploration |
| Achievement | Results, transformed, won | Testimonials, reviews |

#### Emotion Response Diagnosis

```markdown
## Emotion Response Analysis
- **Dominant Emotion Evoked**: [Classified from copy language + response data]
- **Emotion-Audience Match**: [Is this emotion appropriate for the context?]
- **Proportionality Check**: [Is emotional intensity proportional to product value?]
- **Diagnosis**: [The copy's emotional impact was effective/problematic because...]
```

### Analyzing Trust Signals in Copy (Module 3)

**Trust Element Audit Checklist:**

Use this to **audit** what trust elements exist in a piece of copy:

| Trust Element | Present? | Credibility Assessor |
|---------------|----------|---------------------|
| Specific numbers/data | ☐ Yes / ☐ No | Are sources cited? Verifiable? |
| Testimonials/reviews | ☐ Yes / ☐ No | Authentic? Specific? Recent? |
| Expert authority | ☐ Yes / ☐ No | Relevant credentials? |
| Case studies | ☐ Yes / ☐ No | Attributed? Measurable results? |
| Guarantee/risk reversal | ☐ Yes / ☐ No | Terms clear? Genuinely risk-free? |
| Transparency | ☐ Yes / ☐ No | Pricing clear? Limitations disclosed? |

#### Trust Diagnosis

```markdown
## Trust Signal Audit
- **Elements Present**: [List]
- **Missing Elements**: [List — potential trust gaps]
- **Credibility Assessment**: [Are present signals authentic or generic?]
- **Diagnosis**: [Trust was/was not established because...]
```

### Analyzing Decision Friction in Copy (Module 4)

**Friction Point Detection:**

| Friction Type | What to Look For in Copy | Diagnostic Question |
|--------------|--------------------------|---------------------|
| Unclear value proposition | Vague benefits, jargon | Does reader know WHAT they get? |
| Unclear next step | Weak/missing CTA | Does reader know WHAT to do? |
| Perceived risk unaddressed | No guarantees, no reassurance | Does reader feel SAFE acting? |
| Overwhelming options | Too many choices/paths | Is there ONE clear action? |
| Cost justification missing | Price without value anchor | Does reader understand WHY it's worth it? |

#### Decision Friction Diagnosis

```markdown
## Decision Friction Analysis
- **Identified Frictions**: [List from audit]
- **#1 Barrier**: [Primary friction point with evidence]
- **Friction Impact**: [How this friction likely affected conversion]
- **Diagnosis**: [Readers stopped/because of...]
```

### Analyzing Spread/Shareability (Module 6)

**Shareability Assessment for Existing Content:**

| Sharing Motive | Does Content Serve This Motive? | Evidence |
|---------------|-------------------------------|----------|
| Self-expression | ☐ Yes / ☐ No | Opinion/identity content? |
| Helping others | ☐ Yes / ☐ No | Utility/tips content? |
| Identity signaling | ☐ Yes / ☐ No | Expertise/signal content? |
| Emotional release | ☐ Yes / ☐ No | Strong emotion content? |
| Social currency | ☐ Yes / ☐ No | Exclusive/insider content? |

#### Shareability Diagnosis

```markdown
## Shareability Analysis
- **Sharing Motive(s) Served**: [Classified]
- **Shareability Score**: X/10 — [Based on motive coverage × identity relevance]
- **Spread Blocker(s)**: [What prevented sharing, if applicable]
- **Diagnosis**: [Content spread/failed to spread because...]
```

---

## Complete Output: Copy Effect Diagnosis Report

```markdown
# Copy Effect Diagnosis Report

## Summary
[One-paragraph verdict: why this copy performed as it did]

## Stage-by-Stage Analysis
1. **Attention Stage**: [Did it stop the reader? Why/why not?]
2. **Need Alignment**: [Does it address the right user need?]
3. **Emotional Response**: [What emotion did it evoke? Appropriate?]
4. **Trust Assessment**: [Were trust signals credible?]
5. **Decision Friction**: [What blocked the final action?]
6. **Shareability**: [Would readers share this? Why/why not?]

## Primary Finding
[Single most important success/failure factor]

## Suggested Investigation Paths
(For further testing — NOT copy recommendations)
- Path A: [A/B test variable to investigate hypothesis]
- Path B: [Data point to gather to validate diagnosis]
```
