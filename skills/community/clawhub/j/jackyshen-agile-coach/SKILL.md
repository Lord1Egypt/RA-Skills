---
name: jackyshen-agile-coach
description: Jacky Shen's Agile Coach AI assistant, providing structured prompt support for Scrum Masters and Product Owners. This skill MUST be activated whenever the user mentions any of the following Scrum, Sprint, Backlog, user stories, DoD, DoR Definition of Ready, Product Owner, Scrum Master, agile ceremonies, retrospectives, backlog refinement, sprint planning, release planning, risk identification, user personas, customer churn, product requirements, decision-making, scenario modeling, team facilitation, or any agile team workflow. Keywords are Scrum, Sprint, Backlog, user story, Product Owner, Scrum Master, DoR, agile, iteration, retrospective, prioritization, risk, persona, churn, PRD, facilitation, minimal experiment, root cause, pattern recognition. Whenever a user mentions agile team work, PO/SM scenarios, or needs structured agile prompt templates, this skill must be used.
---

# Jacky Shen's Agile Coach Prompt Toolkit

This skill encapsulates 11 core scenario prompts designed by Jacky Shen (Chief Agile Coach, Scrum Alliance Certified CST) for Scrum agile teams, covering high-frequency work scenarios for both **Scrum Masters** and **Product Owners**.

## How to Use

1. **Identify the scenario**: Match the user's description to the most relevant scenario(s) in the table below
2. **Load the reference**: Read `references/prompt-library.md` for the full prompt template
3. **Customize**: Replace `[placeholders]` with the user's specific details (team size, product name, data, etc.)
4. **Add guidance**: Alongside the prompt, share the best-practice usage tip for that scenario

---

## Scenario Quick Reference

| # | Category | Scenario | Trigger Keywords |
|---|----------|----------|-----------------|
| 1 | Agile General | Definition of Ready (DoR) Check | DoR, user story check, ready criteria, sprint gate |
| 2 | Agile General | Backlog Prioritization & Ordering | priority, ordering, sprint planning, release planning |
| 3 | Agile General | Risk Identification & Analysis | risk, impediment, blocker, retro data |
| 4 | Product Owner | Data Analysis & Insight Extraction | customer feedback, review analysis, sentiment, insight |
| 5 | Product Owner | Backlog Refinement & Estimation | refinement, story points, acceptance criteria, dependency |
| 6 | Product Owner | User Persona Creation | persona, user segment, target user, empathy |
| 7 | Product Owner | Customer Churn Prediction & Analysis | churn, retention, at-risk users, drop-off |
| 8 | Product Owner | Product Requirements Definition | requirements, PRD, gap analysis, needs list |
| 9 | Product Owner | Decision Support & Option Comparison | decision, trade-off, scenario simulation, risk matrix |
| 10 | Scrum Master | Retrospective Facilitation & Pattern Analysis | retrospective, retro, agenda, meeting notes, root cause, pattern |
| 11 | Scrum Master | Scenario Modeling & Hypothesis Testing | scenario modeling, hypothesis, constraint analysis, what-if |

---

## Usage Standards

### Prompt Structure (RACT Framework)

All prompts follow this five-layer structure:

```
### GOAL ###       → Core purpose and expected outcome
### ROLE ###       → Expert identity, capabilities, and "Never Do" guardrails
### CONTEXT ###    → Business scenario, audience, relevant data
### ACTION ###     → Specific tasks with Do / Don't constraints
### FORMAT ###     → Output structure, length limits, examples
```

### Output Principles

- **Deliver ready-to-use prompts**: Output fully filled-in prompts the user can copy immediately
- **Mark unfilled placeholders**: Use `[TO FILL: description]` for any missing user info
- **Include a usage tip**: Note which Scrum ceremony or workflow context this prompt fits best
- **Language**: Default to the language the user is writing in

---

## Full Prompt Library

See `references/prompt-library.md` for all 11 complete prompt templates.

**How to navigate**: Find the scenario number in the quick reference table above, then locate the matching section in the reference file.
