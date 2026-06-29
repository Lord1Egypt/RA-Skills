---
name: "content-viral-spread"
description: "Diagnostic sub-skill for analyzing why specific content did or didn't spread. Uses Human Behavior OS modules to diagnose sharing patterns, attention capture effectiveness, and engagement drivers in existing content. Outputs behavioral diagnosis ONLY — never creates viral content strategies, share optimization tactics, or growth hacking instructions."
---

# Content Spread Pattern Diagnosis

## 0. Relationship to Parent

This reference inherits all 7 diagnostic modules from the parent Human Behavior OS skill. It adds content-specific lenses for **understanding** why content spreads or fails to spread.

**Scope**: Diagnose WHY content behaved as it did. Do NOT provide viral content recipes or growth tactics.

---

## Diagnostic Framework

### The Spread Equation (Analytical Lens)

```
Spread Potential = (Emotional Intensity × Identity Relevance) ÷ Sharing Friction
```

Use this equation to **explain** an observed spread outcome — not to engineer one.

| Dimension | Diagnostic Question | Data Sources |
|-----------|---------------------|-------------|
| Emotional Intensity | How strongly did content make people feel? | Comments, reactions, sentiment |
| Identity Relevance | Does sharing this say something about the sharer? | Share demographics, profile types |
| Sharing Friction | How easy or hard was it to share? | Share button clicks, platform distribution |

---

## Module-Specific Diagnostic Applications

### Attention Capture Diagnosis (Module 2)

**Hook Mechanism Classifier:**

Use this to identify what attention mechanism existing content used:

| Hook Type | Content Pattern | Diagnostic Question |
|-----------|----------------|---------------------|
| Curiosity | Information gap created | Did curiosity drive initial engagement? |
| Contrast | Unexpected juxtaposition | Did surprise break through noise? |
| Danger/Risk | Warning or threat frame | Did fear/alarm drive attention? |
| Benefit | Clear gain promised | Was the value proposition immediate? |
| Social Proof | Others' validation shown | Did social signals boost credibility? |
| Story | Narrative arc present | Did narrative sustain attention? |
| Novelty | Newness emphasized | Did uniqueness drive initial interest? |
| Conflict | Opposing forces presented | Did controversy drive engagement? |

#### Attention Diagnosis Output

```markdown
## Content Attention Diagnosis
- **Hook Mechanism Used**: [Classified from actual content]
- **Initial Engagement Signal**: [Views, impressions, click-through rate]
- **Hook-Effectiveness Assessment**: [Did this hook work for this audience?]
- **Diagnosis**: [Attention was captured/lost because...]
```

### Emotion-Spread Link Diagnosis (Module 5)

> ⚠️ **Guardrail**: This classifies emotions observed in content and their correlation to sharing behavior. It does NOT recommend emotional engineering or amplification.

**Emotion-Spread Correlation Table:**

| Dominant Emotion in Content | Typical Spread Pattern | Diagnostic Use |
|----------------------------|----------------------|---------------|
| Awe/Wonder | High share, high save | Classify awe-driven virality |
| Anger/Outrage | High share, mixed sentiment | Classify outrage-driven spread |
| Joy/Humor | Medium-high share, positive sentiment | Classify humor-driven spread |
| Fear/Warning | Medium share, "helping others" motive | Classify alert-driven spread |
| Sadness/Empathy | Lower share, high engagement depth | Classify empathy-driven engagement |
| Surprise | High share, curiosity-driven | Classify surprise-driven virality |

#### Emotion-Spread Diagnosis

```markdown
## Emotion-Spread Analysis
- **Dominant Emotion in Content**: [Classified from content + reaction data]
- **Observed Spread Pattern**: [Actual sharing/engagement data]
- **Emotion-Spread Correlation**: [Does the emotion explain the spread pattern?]
- **Proportionality Check**: [Was emotional intensity proportionate to content substance?]
- **Diagnosis**: [Content spread/failed to spread because...]
```

### Sharing Motive Diagnosis (Module 6)

**Sharing Motive Classifier:**

Use this to deduce WHY people shared (or didn't share) a piece of content:

| Motive | Behavioral Signal in Data | When This Motive Is Active |
|--------|--------------------------|--------------------------|
| Self-expression | Shares with commentary/opinion | Opinion pieces, values content |
| Helping others | Saves, "send to friend", bookmarks | Tips, guides, warnings |
| Identity signaling | Shares to professional networks | Expertise, insight content |
| Emotional release | Reactive shares, emotional captions | Strong emotion content |
| Social currency | Early shares, "first" comments | Exclusive, breaking content |
| Social validation | Shares seeking likes/confirmation | Achievement, milestone content |

#### Sharing Diagnosis

```markdown
## Sharing Motive Analysis
- **Active Sharing Motive(s)**: [Deduced from share behavior data]
- **Motive-Content Fit**: [Did content actually serve this motive well?]
- **Non-Sharer Barrier**: [For those who saw but didn't share — why not?]
- **Diagnosis**: [Sharing behavior indicates...]
```

### Audience Need Diagnosis (Module 1)

**Content-Audience Need Alignment:**

| Need Layer | Content That Serves It | Misalignment Signal |
|-----------|----------------------|---------------------|
| L1 Survival | Crisis info, how-to survive, money-saving | Low save rate, quick bounce if mismatched |
| L2 Efficiency | Productivity tips, shortcuts, tools | Low bookmark rate if content is entertainment-only |
| L3 Emotion | Entertainment, stories, community | Low comment depth if content is purely informational |
| L4 Identity | Expertise, taste, professional insight | Low LinkedIn/share-to-network if content lacks depth |
| L5 Growth | Learning, self-improvement, mastery | Low long-term engagement if content is shallow |

#### Need Alignment Diagnosis

```markdown
## Content-Audience Need Alignment
- **Target Audience Need Profile**: [Inferred from audience data]
- **Content's Need Address**: [What need the content serves]
- **Alignment Gap**: [Mismatch between audience needs and content offering]
- **Diagnosis**: [Engagement pattern reflects this need alignment/misalignment because...]
```

### Platform-Behavior Diagnosis (Module 2 + 7)

**Platform Behavior Reference:**

| Platform | Typical Attention Window | Expected Behavior Pattern |
|----------|-------------------------|--------------------------|
| Twitter/X | 1-3 seconds | Quick consume, quick react or move on |
| Instagram | 1-2 seconds | Visual-first decision, save or scroll |
| TikTok | 0.5-1 second | Entertainment filter, instant stay/go |
| LinkedIn | 3-5 seconds | Professional relevance check, engage or skip |
| YouTube | 5-10 seconds | Topic relevance assessment, watch or leave |
| Newsletter | Subject line: 1-2 seconds | Sender/value judgment, open or delete |

#### Platform-Fit Diagnosis

```markdown
## Platform Fit Analysis
- **Platform**: [Where content was published]
- **Platform-Native Behavior**: [Expected behavior on this platform]
- **Content Adaptation Level**: [Well-adapted / partially adapted / misaligned]
- **Performance-vs-Platform Norm**: [Above/below average for this platform?]
- **Diagnosis**: [Content performed as it did on this platform because...]
```

---

## Complete Output: Content Spread Diagnosis Report

```markdown
# Content Spread Diagnosis Report

## Summary
[One-paragraph diagnosis of why content spread or failed to spread]

## Findings
1. **Attention Analysis**: [Hook effectiveness, platform fit]
2. **Emotion Analysis**: [Dominant emotion, spread correlation]
3. **Need Alignment**: [Content-audience need match]
4. **Sharing Motive**: [Why people shared or didn't]
5. **Friction Analysis**: [Barriers to sharing/engagement]

## Primary Root Cause Hypothesis
[Single most likely explanation for the observed spread pattern]

## Suggested Investigation Paths
- Path A: [A/B test or data point to validate]
- Path B: [Alternative angle to investigate]

## Key Metrics to Track
[Metrics that will confirm or refine this diagnosis]
```
