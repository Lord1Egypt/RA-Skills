---
name: "community-engagement"
description: "Diagnostic sub-skill for analyzing community participation patterns, group dynamics, member motivation, and community health indicators. Uses Human Behavior OS modules to diagnose WHY community members behave as they do. Outputs behavioral diagnosis ONLY — never provides engagement playbooks, growth hacking tactics, moderation strategies, or community design blueprints."
---

# Community Participation Behavior Diagnosis

## 0. Relationship to Parent

This reference inherits all 7 diagnostic modules from the parent Human Behavior OS skill. It adds community-specific lenses for **understanding** group behavior and participation patterns.

**Scope**: Diagnose WHY community members behave as they do. Do NOT provide community building tactics, engagement manipulation, or growth recipes.

---

## Diagnostic Framework

### The Community Participation Lifecycle (Analytical Lens)

```
Discover → Join → Participate → Contribute → Lead → Advocate (or Leave)
```

| Stage | Member State | Diagnostic Focus | Key Signal |
|-------|-------------|-----------------|------------|
| Discover | "I found this place" | Discovery channel effectiveness | Traffic source, impressions |
| Join | "I'll create an account" | Join decision drivers | Signup conversion rate |
| Participate | "I'm engaging" | Participation motivation | Posts, comments, reactions per user |
| Contribute | "I'm creating value" | Contribution drivers | Content creation rate, quality |
| Lead | "I'm shaping things" | Leadership emergence | Organizer, moderator, mentor behavior |
| Advocate | "I bring others" | Referral motivation | Invite rate, external sharing |
| Leave | "I'm done here" | Departure reasons | Churn, inactivity, exit feedback |

---

## Module-Specific Diagnostic Applications

### Member Need Diagnosis (Module 1)

**Community Need Layer Reference:**

| Need Layer | Community Expression | Member Type | Behavioral Signal |
|-----------|---------------------|-------------|-------------------|
| L1 Survival | Safety, mutual aid, crisis support | Vulnerable member | Seeks help, support posts |
| L2 Efficiency | Knowledge sharing, tool tips | Practitioner | Q&A, resource sharing |
| L3 Emotion | Belonging, companionship | Social seeker | Casual chat, off-topic posts |
| L4 Identity | Reputation, expertise display | Expert | Thought leadership, long-form answers |
| L5 Growth | Learning, mentorship, advancement | Ambitious member | Mentorship, organized learning |

#### Member Need Diagnosis Output

```markdown
## Community Member Need Diagnosis
- **Predominant Need Layer(s)**: [From member behavior observation]
- **Need-Community Fit**: [Does the community serve these needs?]
- **Unmet Need Signals**: [Behaviors indicating unsatisfied needs]
- **Diagnostic Hypothesis**: [Members join/participate/leave because...]
```

### Participation Friction Diagnosis (Module 4)

**Participation Barrier Taxonomy:**

| Barrier Type | Member Experience | Behavioral Signal |
|--------------|------------------|-------------------|
| Lurker friction | "I have nothing valuable to say" | Views but no reactions/comments |
| Social risk | "What if I look foolish?" | Anonymous views only, no identity |
| Effort friction | "Too much work to contribute" | Reactions only, no text contributions |
| Relevance friction | "This isn't for me" | Selective engagement, partial-topic only |
| Expertise friction | "Everyone knows more than me" | Reads but never asks/questions |
| Culture friction | "I don't fit in here" | Short membership, early exit |

#### Participation Diagnosis

```markdown
## Participation Friction Diagnosis
- **Active Member Ratio**: X% (members who posted/commented in last 30 days)
- **Lurker Ratio**: X% (viewed but never engaged)
- **Primary Barrier**: [From taxonomy above]
- **Barrier Distribution**: [% per barrier type from available signals]
- **Hypothesis**: [Non-participation occurs because...]
```

### Trust Dynamics Diagnosis (Module 3)

**Community Trust Level Reference:**

| Trust Level | What It Means | Breakdown Signal |
|-------------|--------------|-----------------|
| L1 Platform | "This site is safe to use" | Security concerns, privacy complaints |
| L2 Social | "These are real people" | Bot/spam concerns, authenticity doubts |
| L3 Content | "Information here is reliable" | Misinformation spread, fact disputes |
| L4 Relational | "I can be vulnerable here" | Toxicity reports, harassment incidents |
| L5 Identity | "This is my tribe" | Low belonging indicators, weak identity signals |

#### Trust Diagnosis

```markdown
## Community Trust Diagnosis
- **Current Trust Level**: [L1-L5 for the community overall]
- **Trust-Breakdown Event(s)**: [If applicable — what damaged trust]
- **Recovery Status**: [Recovering / Stable / Ongoing erosion]
- **Hypothesis**: [Community trust dynamics indicate...]
```

### Group Emotion Diagnosis (Module 5)

**Community Emotional Climate Classification:**

| Climate | Behavioral Signals | Diagnostic Meaning |
|---------|-------------------|-------------------|
| Positive/Thriving | Celebrations, mutual support, warm interactions | Healthy emotional foundation |
| Neutral/Functional | Task-focused, polite but distant | Functional but low belonging |
| Tense/Polarized | Debates, factions, us-vs-them dynamics | Conflict risk, potential toxicity |
| Toxic/Deteriorating | Harassment, pile-ons, exodus | Culture failure, urgent intervention needed |
| Apathetic/Stale | Minimal interaction, ghost town | Relevance or energy crisis |

#### Emotion Climate Diagnosis

```markdown
## Community Emotional Climate Diagnosis
- **Current Climate**: [From classification above]
- **Sentiment Trend**: [Improving / Stable / Declining over 30 days]
- **Key Emotion Drivers**: [What events/content shaped current climate]
- **Hypothesis**: [Community emotional state reflects...]
```

### Community Health Forecast (Module 7)

**Health Indicator Dashboard:**

| Indicator | Healthy Range | Warning Signal | Critical Signal |
|-----------|--------------|---------------|----------------|
| Active member ratio | > 20% of total | 10-20% | < 10% |
| New member retention (D30) | > 40% | 20-40% | < 20% |
| Content creation rate | Steady or growing | Declining | Sharp drop |
| Sentiment score | > 7/10 | 5-7 | < 5 |
| Top contributor activity | Stable or growing | Declining | Left or inactive |
| Toxicity report rate | < 1/1000 posts | 1-5/1000 | > 5/1000 |
| Response time | < 24hr avg | 24-72hr | > 72hr |

#### Health Forecast Diagnosis

```markdown
## Community Health Forecast
- **Current Health Score**: X/10 (from indicator dashboard)
- **Trend Direction**: [Improving / Stable / Declining]
- **At-Risk Indicators**: [Which metrics are in warning/critical range]
- **Prediction**: [30-day community state forecast with confidence]
- **Key Assumptions**: [What this forecast depends on]
```

---

## Complete Output: Community Behavior Diagnosis Report

```markdown
# Community Behavior Diagnosis Report

## Summary
[One-paragraph diagnosis of the core community health issue]

## Findings by Module
1. **Member Needs**: [What brings members and keeps them?]
2. **Participation Barriers**: [What prevents deeper engagement?]
3. **Trust Dynamics**: [What is the community's trust level?]
4. **Emotional Climate**: [What is the group's emotional state?]
5. **Health Forecast**: [What is the predicted community trajectory?]

## Primary Root Cause Hypothesis
[Single most likely explanation for observed community behavior patterns]

## Suggested Investigation Paths
- Path A: [Survey question or metric to investigate further]
- Path B: [Experiment or cohort analysis to validate]

## Key Metrics to Track
[Metrics that will confirm or refine this diagnosis over time]
```
