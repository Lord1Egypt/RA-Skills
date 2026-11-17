<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 12: Usability Validation Plan

## Purpose

Define how the design will be validated for usability — both pre-implementation (heuristic evaluation against the design) and post-implementation (usability testing with real users). Also defines the feedback intake channel from AI-DLC v1.

---

## Depth Adaptation

| Depth | Validation Output |
|-------|-------------------|
| **Minimal** | Heuristic evaluation checklist + 3-5 key task scenarios |
| **Standard** | Full heuristic checklist + usability test plan with tasks, metrics, participants |
| **Comprehensive** | Full plan + cognitive walkthrough method + longitudinal feedback plan + analytics requirements |

---

## Steps

### Step 1: Heuristic Evaluation Checklist

Evaluate the design against Nielsen's 10 Usability Heuristics:

```markdown
## Heuristic Evaluation Checklist

| # | Heuristic | Check Questions | Severity if Violated |
|---|-----------|----------------|---------------------|
| 1 | **Visibility of system status** | Does the user always know where they are and what's happening? Loading states? Progress indicators? | High |
| 2 | **Match between system and real world** | Does the terminology match user language (per voice & tone)? Are metaphors intuitive? | Medium |
| 3 | **User control and freedom** | Can users undo? Exit flows? Go back? Cancel operations? | High |
| 4 | **Consistency and standards** | Do same patterns behave the same way? Are platform conventions followed? | Medium |
| 5 | **Error prevention** | Are destructive actions confirmed? Are constraints visible before errors occur? | High |
| 6 | **Recognition over recall** | Are options visible? Do labels explain themselves? Is context provided? | Medium |
| 7 | **Flexibility and efficiency** | Are there shortcuts for expert users? Can frequent tasks be streamlined? | Low |
| 8 | **Aesthetic and minimalist design** | Is every element needed? Is there information that competes with the primary task? | Low |
| 9 | **Help users recover from errors** | Do error messages explain what happened + how to fix? Is recovery clear? | High |
| 10 | **Help and documentation** | Is contextual help available? Are complex features explained? | Low |
```

For each heuristic, evaluate against the wireframes and flows:

```markdown
### Heuristic 1: Visibility of System Status

| Screen/Flow | Issue Found | Severity (0-4) | Recommendation |
|-------------|------------|-----------------|----------------|
| {screen} | {issue} | {0=none, 1=cosmetic, 2=minor, 3=major, 4=catastrophic} | {fix} |
```

### Step 2: Define Usability Test Plan

```markdown
## Usability Test Plan

### Objectives
1. Validate that primary personas can complete their key tasks
2. Identify friction points in the most critical flows
3. Measure task completion rates and time-on-task
4. Validate that the IA labeling makes sense to real users

### Participants
| Segment | Count | Recruiting Criteria |
|---------|-------|-------------------|
| {persona match} | 5-8 | {behavioral criteria, not demographics} |
| {inclusion participant} | 1-2 | {assistive technology user} |

### Tasks (mapped to flows)
| # | Task Scenario | Success Criteria | Max Time | Flow Reference |
|---|---------------|-----------------|----------|---------------|
| 1 | "{scenario from user's perspective}" | {what counts as success} | {minutes} | Flow_{NN} |
| 2 | ... | ... | ... | ... |

### Metrics
| Metric | Type | Target |
|--------|------|--------|
| Task completion rate | Effectiveness | ≥80% |
| Time on task | Efficiency | Within {N}x of expert time |
| Error rate | Effectiveness | ≤{N} errors per task |
| SUS score | Satisfaction | ≥68 (above average) |
| Task difficulty rating (1-5) | Satisfaction | ≤3 per task |

### Method
| Setting | Remote unmoderated / Remote moderated / In-person |
| Tool | {recording/testing platform} |
| Duration | {minutes per session} |
| Facilitator script | {included in appendix or separate document} |

### Reporting Format
| Section | Content |
|---------|---------|
| Executive summary | Key findings + recommendations (1 page) |
| Task results | Per-task completion, time, errors |
| Issue log | All issues found, severity-ranked |
| Recommendations | Design changes mapped to issues |
| Raw data | Session recordings, notes (appendix) |
```

### Step 3: Cognitive Walkthrough (Comprehensive Only)

At Comprehensive depth, include a cognitive walkthrough for critical flows:

```markdown
## Cognitive Walkthrough: {Flow Name}

For each step, answer:
1. Will the user try to achieve the right effect?
2. Will the user notice that the correct action is available?
3. Will the user associate the correct action with the desired effect?
4. If the correct action is performed, will the user see progress?

| Step | Q1 | Q2 | Q3 | Q4 | Issue | Severity |
|------|----|----|----|----|-------|----------|
| {step} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {if ❌} | {1-4} |
```

### Step 4: Define Feedback Intake Channel

Define how post-implementation signals from AI-DLC v1 feed back:

```markdown
## Feedback Intake: AI-DLC v1 → AI-UXD

### Signal Types
| Signal | Source | What It Tells Us | UXP Impact |
|--------|--------|-----------------|-----------|
| Accessibility violations | Automated testing / AI-TGE | Components failing WCAG | Update component spec |
| Usability metrics | Analytics / user testing | Task completion, drop-off | Revise flow / IA |
| Behavioral patterns | Product analytics | Feature usage, navigation paths | Validate or revise IA |
| User feedback | Support tickets, reviews | Pain points, feature requests | Feed back to personas/journeys |

### Feedback Loop Process
1. Signal arrives (from AI-DLC v1 / AI-TGE / analytics)
2. Categorize: Accessibility / Usability / Behavioral / Request
3. Assess severity: Does it require immediate UXP revision or next-cycle?
4. If revision needed: update affected artifact + log as UXD-C-NNN in Change Log
5. Signal AI-POLC if the change affects user stories / priorities
```

### Step 5: Present for Approval

Present:
- Heuristic evaluation results (issues found, if any, from wireframe review)
- Usability test plan (tasks, participants, metrics)
- Feedback intake process
- Cognitive walkthrough (Comprehensive only)

---

## Gate

**Approval required before proceeding to Stage 13.**

User must confirm:
- Heuristic evaluation is thorough
- Test plan tasks cover critical flows
- Metrics and targets are realistic
- Feedback intake process is clear
- (Comprehensive) Cognitive walkthrough covers critical paths

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 12 with date and artifact (`11_Usability_Test_Plan.md`)
- Current Stage: 13

---

## Transition

After gate approval:
```
Stage 12 complete. Usability validation plan defined.

Moving to Stage 13: Design QA Framework. I'll now define how to
detect and govern design-to-code drift once implementation begins.
```

Load `validate/design-qa-framework.md`.
