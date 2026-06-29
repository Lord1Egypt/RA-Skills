---
name: "product-adoption"
description: "Diagnostic sub-skill for analyzing user adoption patterns, feature usage rates, habit formation signs, and activation barriers. Uses Human Behavior OS modules to diagnose WHY users adopt or abandon products. Outputs behavioral diagnosis ONLY — never provides adoption playbooks, habit engineering tactics, or growth hacking strategies."
---

# Product Adoption Behavior Diagnosis

## 0. Relationship to Parent

This reference inherits all 7 diagnostic modules from the parent Human Behavior OS skill. It adds product-specific lenses for **understanding** user adoption and disengagement patterns.

**Scope**: Diagnose WHY users behave as they do with a product. Do NOT provide adoption optimization tactics or habit engineering instructions.

---

## Diagnostic Framework

### The Adoption Lifecycle (Analytical Lens)

```
Awareness → Trial → First Value → Repeat Use → Habit → Advocacy (or Churn)
```

Use this to locate WHERE in the lifecycle behavior changes occur.

| Stage | User State | Diagnostic Focus | Key Behavioral Signal |
|-------|-----------|-----------------|----------------------|
| Awareness | "I've heard of it" | Discovery channel effectiveness | Source attribution, reach |
| Trial | "I'll try it" | Trial trigger & barrier | Signup rate, install rate |
| First Value | "It works!" | Activation speed & clarity | Time-to-value, activation events |
| Repeat Use | "I use it again" | Return motivation | D1/D7 return rate |
| Habit | "I use it regularly" | Usage pattern stability | DAU/MAU ratio, session frequency |
| Advocacy/Churn | "I tell everyone" OR "I quit" | Loyalty or exit drivers | Referral rate, churn rate, NPS |

---

## Module-Specific Diagnostic Applications

### Need Fit Diagnosis (Module 1)

**Product-User Need Alignment Framework:**

| Fit Signal | Strong Fit (Healthy Adoption) | Weak Fit (Adoption Struggle) |
|-----------|------------------------------|----------------------------|
| Acquisition source | Organic, word-of-mouth | Paid, incentivized |
| Activation path | Self-guided, fast | Requires heavy support/onboarding |
| Retention pattern | Natural return behavior | Requires reminders/push notifications |
| Feature usage depth | Core features actively used | Surface-level browsing only |
| Churn signal | Low voluntary churn | High churn despite onboarding efforts |

#### Need Fit Diagnosis Output

```markdown
## Product-User Need Fit Diagnosis
- **Problem Frequency**: How often does the solved problem occur? (1-10)
- **Problem Intensity**: How painful is it? (1-10)
- **Current Alternative Adequacy**: How inadequate are existing solutions? (1-10)
- **Need Fit Score**: X/10 (average of above)
- **Fit Classification**: [Strong / Moderate / Weak]
- **Diagnostic Hypothesis**: [Adoption pattern indicates the product does/does not serve a real user need because...]
```

### Activation Barrier Diagnosis (Module 4)

**Activation Friction Taxonomy:**

| Friction Type | User Experience | Behavioral Signal |
|--------------|-----------------|-------------------|
| Cognitive friction | "I don't get it" | Quick exit during onboarding, low feature exploration |
| Time friction | "This takes too long" | Abandonment during setup, incomplete onboarding |
| Effort friction | "Too much work" | Partial setup, minimal data input |
| Social friction | "My team won't use it" | Individual signup but no team adoption |
| Risk friction | "What if it goes wrong?" | No critical data entered, sandbox-only use |
| Value friction | "I don't see the point" | Signed up but never reached core feature |

#### Activation Diagnosis

```markdown
## Activation Barrier Diagnosis
- **Current Activation Rate**: X%
- **Time to First Value**: X minutes (or never achieved)
- **Primary Drop-off Step**: [Where users quit during activation]
- **Friction Classification**: [From taxonomy above]
- **Root Cause Hypothesis**: [Users fail to activate because...]
```

### Usage Pattern Diagnosis (Modules 5, 7)

**Usage Behavior Classification:**

| Pattern | Behavioral Signals | Diagnostic Meaning |
|---------|-------------------|-------------------|
| Power user | Daily use, deep feature exploration, high session count | Strong need fit, high value delivery |
| Regular user | Consistent but shallow use, same few features | Moderate fit, core value delivered |
| Declining user | Decreasing login frequency, fewer features used | Value decay or competing alternative |
| Dormant user | No login in 14+ days, no close actions | Churn imminent or already occurred |
| New user | < 7 days since signup, still exploring | Too early to classify; monitor trajectory |

#### Usage Trajectory Diagnosis

```markdown
## Usage Pattern Diagnosis
- **Current User Segment Distribution**: [Power / Regular / Declining / Dormant % split]
- **Trajectory Trend**: [Improving / Stable / Declining] (over last 30 days)
- **Key Transition Point**: [Where users typically shift between segments]
- **Predicted 30-Day State**: [Based on current trajectory]
- **Diagnostic Hypothesis**: [Usage pattern indicates...]
```

### Trust-in-Product Diagnosis (Module 3)

**Product Trust Lifecycle Stages:**

| Stage | Trust Focus | Trust Failure Signal |
|-------|------------|--------------------|
| Pre-use | Brand/product credibility | Low signup conversion despite awareness |
| First use | Competence (does it work?) | Bugs, errors, confusion during onboarding |
| Early use | Reliability (consistent?) | Intermittent issues, inconsistency reports |
| Extended use | Value delivery (worth it?) | Usage decline despite no major issues |
| Long-term | Partnership (invested?) | Churn to competitor despite satisfaction |

#### Trust Diagnosis

```markdown
## Product Trust Diagnosis
- **Trust Stage of User Base**: [Where most users are in trust lifecycle]
- **Trust Failure Point**: [If applicable — where trust erodes]
- **Failure Classification**: [Competence / Reliability / Value / Partnership]
- **Diagnostic Hypothesis**: [User trust dynamic indicates...]
```

### Churn Signal Diagnosis (Module 7)

**Pre-Churn Behavioral Indicators:**

| Signal | Lead Time | Diagnostic Confidence |
|--------|-----------|---------------------|
| Login frequency drop >50% | 2-4 weeks | High |
| Core feature usage stops | 1-3 weeks | High |
| Session length declining | 1-3 weeks | Medium-High |
| Support ticket spike (complaints) | 1-2 weeks | High |
| No key action in 7 days | 1-2 weeks | Medium |
| Competitor search (if detectable) | Days | Very High |

#### Churn Risk Diagnosis

```markdown
## Churn Risk Diagnosis
- **At-Risk User Segment**: [Which users show pre-churn signals]
- **Dominant Churn Signal**: [Most prevalent indicator]
- **Churn Driver Hypothesis**: [Why are these users likely to churn?]
- **Predicted Churn Rate**: X% (over next 30 days, with confidence level)
```

---

## Complete Output: Product Adoption Diagnosis Report

```markdown
# Product Adoption Diagnosis Report

## Summary
[One-paragraph diagnosis of the core adoption/engagement issue]

## Findings by Module
1. **Need Fit**: [Does the product serve a real user need?]
2. **Activation Barriers**: [What prevents users from reaching value?]
3. **Usage Patterns**: [How do engaged vs. disengaged users behave differently?]
4. **Trust Dynamics**: [Where does product trust exist or break down?]
5. **Churn Risk**: [Who is likely to leave and why?]

## Primary Root Cause Hypothesis
[Single most likely explanation for the observed adoption pattern]

## Suggested Investigation Paths
- Path A: [User interview question or data point to validate]
- Path B: [Cohort analysis or experiment to run]

## Key Metrics to Observe
[Metrics that will confirm or refute this diagnosis over time]
```
