<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Usability Test Plan

## Objectives

1. Validate that primary personas can complete their key tasks efficiently
2. Identify friction points in critical flows
3. Measure task completion rates and time-on-task
4. Validate IA labeling and navigation effectiveness
5. {Project-specific objective}

---

## Participants

| Segment | Matches Persona | Count | Recruiting Criteria |
|---------|----------------|:-----:|-------------------|
| {segment} | {persona name} | {5-8} | {behavioral criteria} |
| {segment} | {persona name} | {3-5} | {criteria} |
| Inclusion | {assistive tech user} | {1-2} | {screen reader / keyboard-only / etc.} |

**Total:** {N} participants
**Recruiting method:** {panel / intercept / internal / agency}

---

## Tasks

| # | Task Scenario (user perspective) | Success Criteria | Max Time | Flow Ref | Priority |
|---|----------------------------------|-----------------|:--------:|----------|:--------:|
| 1 | "{Natural language task from user's POV}" | {measurable outcome} | {min} | Flow_{NN} | Critical |
| 2 | "{task}" | {outcome} | {min} | Flow_{NN} | Critical |
| 3 | "{task}" | {outcome} | {min} | Flow_{NN} | Important |
| 4 | "{task}" | {outcome} | {min} | Flow_{NN} | Important |
| 5 | "{task — include an error recovery scenario}" | {outcome} | {min} | Flow_{NN} | Important |

---

## Metrics

| Metric | Type | Target | How Measured |
|--------|------|--------|-------------|
| Task completion rate | Effectiveness | ≥80% | Pass/fail per task |
| Time on task | Efficiency | ≤{N}x expert time | Stopwatch per task |
| Error rate | Effectiveness | ≤{N} errors/task | Count per task |
| SUS score | Satisfaction | ≥68 (above average) | Post-session questionnaire |
| Task difficulty (1-5) | Satisfaction | ≤3.0 average | Post-task rating |
| First-click accuracy | Efficiency | ≥60% correct | First interaction per task |

---

## Method

| Aspect | Decision |
|--------|----------|
| **Setting** | {Remote unmoderated / Remote moderated / In-person} |
| **Platform/tool** | {testing tool name} |
| **Session duration** | {N} minutes |
| **Facilitator** | {moderated: who facilitates / unmoderated: self-guided} |
| **Recording** | {Screen + audio / Screen + video + audio / Think-aloud} |
| **Think-aloud** | {Concurrent / Retrospective} |
| **Compensation** | {amount / gift card / none} |

---

## Session Structure

| Time | Activity |
|:----:|----------|
| 0-5 min | Introduction, consent, warm-up questions |
| 5-{N} min | Task scenarios (in order above) |
| {N}-{N+5} min | Post-task questions, SUS questionnaire |
| Last 5 min | Open debrief: "Anything else? What stood out?" |

---

## Heuristic Evaluation Checklist

Pre-implementation validation against Nielsen's 10 heuristics:

| # | Heuristic | Status | Issues Found | Severity |
|---|-----------|:------:|:------------:|:--------:|
| 1 | Visibility of system status | ✅/⚠️/❌ | {N} | {max severity} |
| 2 | Match between system and real world | ✅/⚠️/❌ | {N} | {max} |
| 3 | User control and freedom | ✅/⚠️/❌ | {N} | {max} |
| 4 | Consistency and standards | ✅/⚠️/❌ | {N} | {max} |
| 5 | Error prevention | ✅/⚠️/❌ | {N} | {max} |
| 6 | Recognition rather than recall | ✅/⚠️/❌ | {N} | {max} |
| 7 | Flexibility and efficiency of use | ✅/⚠️/❌ | {N} | {max} |
| 8 | Aesthetic and minimalist design | ✅/⚠️/❌ | {N} | {max} |
| 9 | Help users recognize and recover from errors | ✅/⚠️/❌ | {N} | {max} |
| 10 | Help and documentation | ✅/⚠️/❌ | {N} | {max} |

---

## Reporting Format

### Executive Summary (1 page)
- Key findings (top 3-5)
- Overall scores (SUS, completion rate)
- Critical issues requiring immediate attention
- Recommendations summary

### Detailed Results
- Per-task results (completion, time, errors, difficulty)
- Issue log (all issues, severity-ranked)
- Issue-to-recommendation mapping
- Participant quotes/observations

### Recommendations
| # | Issue | Severity | Recommendation | Effort | Impact |
|---|-------|:--------:|----------------|:------:|:------:|
| 1 | {issue} | Critical | {specific fix} | {S/M/L} | High |
| 2 | {issue} | Major | {fix} | {effort} | {impact} |

---

## Feedback Intake (Post-Implementation)

| Signal Source | What It Tells Us | Action |
|--------------|-----------------|--------|
| AI-DLC v1 usability signals | Task completion in real use | Compare to test predictions |
| AI-TGE accessibility violations | Components failing WCAG | Update component specs |
| Product analytics | Navigation paths, drop-offs | Validate IA decisions |
| Support tickets | Pain points in production | Feed back to personas/journeys |

---

## Schedule

| Phase | When | Duration |
|-------|------|----------|
| Plan finalization | {date} | 1-2 days |
| Participant recruiting | {date} | 3-5 days |
| Sessions | {date range} | {N} days |
| Analysis | {after sessions} | 2-3 days |
| Report delivery | {date} | 1 day |
