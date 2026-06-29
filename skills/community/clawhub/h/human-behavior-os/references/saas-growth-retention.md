---
name: "saas-growth-retention"
description: "Diagnostic sub-skill for analyzing SaaS user lifecycle behavior, engagement patterns, retention/churn dynamics, and expansion signals. Uses Human Behavior OS modules to diagnose WHY SaaS users behave as they do. Outputs behavioral diagnosis ONLY — never provides growth playbooks, retention tactics, churn prevention campaigns, or revenue optimization strategies."
---

# SaaS User Lifecycle Behavior Diagnosis

## 0. Relationship to Parent

This reference inherits all 7 diagnostic modules from the parent Human Behavior OS skill. It adds SaaS-specific lenses for **understanding** subscription-based user behavior patterns.

**Scope**: Diagnose WHY SaaS users behave as they do. Do NOT provide growth hacks, retention campaigns, or revenue optimization tactics.

---

## Diagnostic Framework

### The SaaS User Lifecycle (Analytical Lens)

```
Signup → Activation → Engagement → Retention Decision → Expansion (or Churn)
```

Use each stage as a diagnostic checkpoint for understanding user behavior.

| Stage | User State | Diagnostic Focus | Key Signal |
|-------|-----------|-----------------|------------|
| Signup | "I'll try this" | What drove trial signup? | Source, signup rate |
| Activation | "It works!" | Did they reach value moment? | Activation rate, time-to-value |
| Engagement | "I use it regularly" | How deeply do they use it? | DAU/MAU, feature breadth |
| Retention Decision | "Stay or go?" | What determines renewal? | Renewal rate, NPS, login trend |
| Expansion | "I want more" | What triggers upgrade? | Seat expansion, plan upgrade |
| Churn | "I'm leaving" | What drove departure? | Churn reason, cancel stage |

---

## Module-Specific Diagnostic Applications

### SaaS User Need Diagnosis (Module 1)

**SaaS Need Layer Reference:**

| Need Layer | SaaS Expression | User Profile | Behavioral Signal |
|-----------|-----------------|--------------|-------------------|
| L1 Survival | Business continuity, security, compliance | Enterprise buyer | Fast decision, contract-driven |
| L2 Efficiency | Automation, time-saving, cost reduction | Team lead / ops | Feature utilization focused |
| L3 Emotion | Team cohesion, reduced stress | Manager | Collaboration features, dashboards |
| L4 Identity | Professional capability, expertise | Individual contributor | Portfolio, export, sharing features |
| L5 Growth | Scale, competitive advantage | Executive / founder | Analytics, integrations, API usage |

#### User Job Story Diagnosis

Format: "When [situation], I want [motivation], so I can [outcome]."

```markdown
## SaaS User Need Diagnosis
- **Primary Job Story**: [The main user task this SaaS serves]
- **Need Layer**: [L1-L5 classification]
- **Need Intensity**: X/10 — [How badly do they need this?]
- **Alternative Solutions Available**: [What else could they use?]
- **Need Fit Assessment**: [Strong / Moderate / Weak match between product capability and user need]
```

### Activation Diagnosis (Module 4)

**Activation Success Factors (Diagnostic Lens):**

| Factor | What to Measure | Healthy Signal | Unhealthy Signal |
|--------|----------------|---------------|-----------------|
| Time to value | Minutes from signup to first "aha!" | < 5 min | > 30 min or never |
| Steps to value | Number of actions required | ≤ 3 steps | > 7 steps |
| First-session depth | Features explored in first visit | Core feature used | Only settings/profile viewed |
| Return within 48h | Second session occurrence | > 60% return | < 20% return |

#### Activation Diagnosis Output

```markdown
## Activation Diagnosis
- **Activation Rate**: X% (signup → first value moment)
- **Time to Value**: X minutes
- **Steps to Value**: X steps
- **#1 Activation Barrier**: [Specific blocker with evidence]
- **Barrier Classification**: [Cognitive / Time / Effort / Value / Technical]
- **Hypothesis**: [Users fail to activate because...]
```

### Engagement Depth Diagnosis (Module 5)

**Engagement Quality Classification:**

| Engaged Type | Behavioral Pattern | Diagnostic Meaning |
|-------------|-------------------|-------------------|
| Core-feature engaged | Uses primary feature daily/weekly | Product serves primary need well |
| Surface engaged | Logs in but doesn't use key features | Onboarding incomplete or need unclear |
| Declining engagement | Logins decreasing, sessions shortening | Value decay or competing alternative |
| Sporadic | Occasional logins, no pattern | Low priority, "nice to have" not "must have" |
| Disengaged | No meaningful activity in 14+ days | Effective churn (not yet cancelled) |

#### Engagement Diagnosis

```markdown
## Engagement Depth Diagnosis
- **Engagement Distribution**: [% per type above]
- **30-Day Trend**: [Improving / Stable / Declining]
- **Core Feature Adoption Rate**: X% of active users
- **Feature Discovery Depth**: Avg X features used per user
- **Hypothesis**: [Engagement pattern indicates...]
```

### Retention/Churn Diagnosis (Modules 3, 7)

**Churn Type Classification:**

| Churn Type | Behavioral Signal | Diagnostic Question |
|-----------|------------------|---------------------|
| Value churn | Never activated or stopped early | Did product ever deliver on its promise? |
| Trust churn | Left after bugs/support issues | Did reliability problems erode confidence? |
| Cost churn | Cited price as reason | Did perceived value justify the cost? |
| Friction churn | Found product hard to use | Was UX/complexity the blocker? |
| Attention churn | Simply stopped using (no explicit reason) | Did they forget or lose interest? |
| Competition churn | Switched to competitor | Did another solution better serve the need? |

**Pre-Churn Signal Timeline:**

| Signal | Typical Lead Time | Confidence |
|--------|-------------------|-----------|
| Login frequency drop >50% | 2-4 weeks | High |
| Feature usage narrowing | 1-3 weeks | Medium-High |
| Support tickets (complaints) | 1-2 weeks | High |
| No key action in 7 days | 1-2 weeks | Medium |
| Negative feedback/NPS | 1-4 weeks | High |
| Competitor detection (if possible) | Days | Very High |

#### Retention/Churn Diagnosis

```markdown
## Retention & Churn Diagnosis
- **Current Retention Rate**: X% (D30 / D90 / D180)
- **Primary Churn Type**: [From classification above]
- **At-Risk Cohort Size**: X users showing pre-churn signals
- **Churn Driver Hypothesis**: [Users churn because...]
- **Confidence Level**: [Based on available signal data]
```

### Expansion Signal Diagnosis (Module 4)

**Expansion Readiness Indicators:**

| Signal | Behavioral Indicator | Diagnostic Meaning |
|--------|---------------------|-------------------|
| Seat pressure | Team collaboration features heavily used | Natural seat expansion opportunity |
| Feature ceiling | User hitting plan limits frequently | Plan upgrade opportunity |
| Advanced need | User exploring power-user features | Premium tier opportunity |
| ROI achievement | User reporting/achieving major wins | Upsell based on proven value |
| Time investment | Heavy usage, workflows built-in | High switching cost = renewal likelihood |

#### Expansion Diagnosis

```markdown
## Expansion Signal Diagnosis
- **Expansion-Ready Segment**: [Users showing readiness signals]
- **Primary Expansion Driver**: [Seat / Feature / Tier / Use-case]
- **Expansion Probability Estimate**: [Per segment, with confidence]
- **Non-Expansion Barrier**: [For users who should expand but don't — why not?]
```

---

## Complete Output: SaaS Behavior Diagnosis Report

```markdown
# SaaS User Behavior Diagnosis Report

## Summary
[One-paragraph diagnosis of the core SaaS user behavior issue]

## Findings by Lifecycle Stage
1. **Signup & Activation**: [Do users reach value? What blocks them?]
2. **Engagement Depth**: [How deeply do they use the product?]
3. **Retention Dynamics**: [Who stays, who leaves, and why?]
4. **Expansion Signals**: [Who is ready to grow their usage?]
5. **Churn Risk**: [Who is likely to leave and when?]

## Primary Root Cause Hypothesis
[Single most likely explanation for the observed behavior pattern]

## Suggested Investigation Paths
- Path A: [Cohort analysis or survey question to validate]
- Path B: [Experiment or data point to gather]

## Key Metrics to Observe
[Metrics that will confirm or refute this diagnosis over time]
```
