---
name: prd-writer
description: "Multi-turn PRD (Product Requirements Document) creation assistant. Asks clarifying questions one at a time to gather requirements, then generates a complete, professional PRD. Use when starting a new feature, product, or project. Triggers on 'write PRD', 'create PRD', 'new feature', 'product requirements', or '/prd'."
homepage: https://canlah.ai
metadata: {"openclaw": {"emoji": "📋", "os": ["darwin", "linux"]}}
---

# PRD Writer - Multi-Turn Requirements Gathering

## Overview

Guide users through creating a professional PRD by asking focused questions one at a time. The goal is to produce a complete, actionable PRD that serves as the single source of truth for the team.

## The Process

### Phase 1: Problem Discovery (2-3 questions)

Start by understanding the core problem:

1. **Problem Statement**: "What specific problem are you trying to solve? Describe the user pain point."
2. **Why Now**: "Why is this important to solve now? What happens if we don't solve it?"
3. **Existing Solutions**: "How are users currently solving this problem (workarounds, competitors)?"

### Phase 2: User & Market (2-3 questions)

4. **Target Users**: Ask who the primary users are. Offer common persona types:
   - End consumers (B2C)
   - Business users (B2B)
   - Internal team members
   - Developers/Technical users
   - Other (specify)

5. **User Context**: "In what context will users encounter this? (e.g., mobile on-the-go, desktop at work, specific workflow)"

6. **Market Size/Impact**: "How many users will this affect? Is this a core feature or nice-to-have?"

### Phase 3: Success Metrics (1-2 questions)

7. **Definition of Success**: Ask what success looks like. Offer metric types:
   - User engagement (DAU, retention, time spent)
   - Business metrics (revenue, conversion, cost reduction)
   - Technical metrics (performance, reliability, error rates)
   - User satisfaction (NPS, CSAT, support tickets)

8. **Specific Targets**: "What specific numbers would indicate success? (e.g., 'reduce load time to <2s', 'increase conversion by 15%')"

### Phase 4: Scope Definition (2-3 questions)

9. **Core Features**: "What are the MUST-have features for v1? List the absolute minimum for launch."

10. **Out of Scope**: "What should we explicitly NOT build in this phase? (This prevents scope creep)"

11. **Future Considerations**: "What features might come in v2/v3? (Park these for later)"

### Phase 5: Constraints & Dependencies (1-2 questions)

12. **Technical Constraints**: Ask about limitations:
    - Existing tech stack requirements
    - Integration dependencies
    - Performance requirements
    - Security/compliance needs
    - Budget/resource constraints

13. **Timeline**: "What's the target launch date or deadline? Any external dependencies?"

### Phase 6: Prioritization (1 question)

14. **MoSCoW Ranking**: Present the collected features and ask user to categorize:
    - **Must**: Essential for launch
    - **Should**: Important but can defer if needed
    - **Could**: Nice-to-have
    - **Won't**: Explicitly excluded

## Questioning Guidelines

- **One question at a time** - Never overwhelm with multiple questions
- **Use AskUserQuestion tool** with multiple choice options when categories are clear
- **Offer "Other" option** for open-ended responses
- **Summarize understanding** after each phase before moving on
- **Allow backtracking** - If user wants to revise earlier answers, accommodate
- **Skip if already answered** - If user provided info upfront, don't re-ask

## Example Question Flow

```
Q1: "What problem are you solving?"
→ User describes pain point

Q2: "Why is solving this urgent now?"
→ User explains timing

[Summary]: "So we're solving [X] because [Y]. Correct?"
→ User confirms or corrects

Q3: "Who are the primary users?"
→ [Multiple choice with AskUserQuestion]

... continue through phases ...
```

## Output: PRD Document

After gathering all information, generate a complete PRD with this structure:

```markdown
# PRD: [Product/Feature Name]

## Metadata
| Field | Value |
|-------|-------|
| Author | [User name] |
| Status | Draft |
| Created | [Date] |
| Last Updated | [Date] |

## 1. Problem Statement
[Clear description of the problem and why it matters]

### Why Now?
[Urgency and timing rationale]

## 2. Goals & Success Metrics
### Objectives
- [SMART goal 1]
- [SMART goal 2]

### Success Metrics (KPIs)
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| [Metric 1] | [Baseline] | [Goal] | [When] |

## 3. User & Market
### Target Users
[Primary persona description]

### User Stories
- As a [user type], I want [action] so that [benefit]

### Competitive Landscape
[How users solve this today]

## 4. Scope
### In Scope (v1)
- [Must-have feature 1]
- [Must-have feature 2]

### Out of Scope
- [Explicitly excluded 1]
- [Explicitly excluded 2]

### Future Considerations (v2+)
- [Deferred feature 1]

## 5. Feature Requirements
### Feature: [Name]
**Priority**: Must/Should/Could
**Description**: [What it does]
**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## 6. Technical Constraints
- [Constraint 1]
- [Constraint 2]

### Dependencies
- [External dependency 1]

## 7. Timeline & Milestones
| Milestone | Target Date |
|-----------|-------------|
| Design Complete | [Date] |
| Development Start | [Date] |
| Beta/Testing | [Date] |
| Launch | [Date] |

## 8. Open Questions
- [Unresolved question 1]
- [Unresolved question 2]

## 9. Appendix
[Any additional context, wireframes references, research links]
```

## After PRD Generation

### Step 1: Save & Share
1. **Save PRD**: Ask where to save (`docs/prd/`, `docs/specs/`, or custom path)
2. **Commit to git**: Create a commit with the PRD document
3. **Share for review**: Suggest sending to stakeholders for feedback

### Step 2: Design (if UI/UX involved)
Ask: "Does this feature need UI design?"
- **Yes** → Suggest using `/brainstorming` skill to explore design approaches
- **Yes + need mockups** → Suggest `/frontend-design` for wireframes/prototypes
- **No** → Skip to implementation planning

### Step 3: Technical Architecture
Ask: "Is this feature complex enough to need a technical architecture design?"
- **Complex feature** → Use `architect` subagent for system design
  - Output: component breakdown, data flow, tech selection, interface design
- **Simple feature** → Skip to task breakdown

### Step 4: Break into Tasks
Ask: "Do you want to break the PRD into development tasks?"
- **Yes** → Use `planner` subagent to create implementation plan
  - Break down based on architecture design
  - Generate TaskCreate items with:
    - Clear acceptance criteria from PRD
    - Dependencies marked (blockedBy)
    - Priority from MoSCoW ranking

### Step 5: Implementation
Once tasks are created:
1. `planner` → Detailed implementation plan per task
2. Write code
3. `code-reviewer` → Auto-review before commit
4. `test-creator` → Generate tests
5. `security-reviewer` → If sensitive code

### Step 6: Validation
Before shipping:
1. `e2e-runner` → Automated testing
2. Compare against PRD success metrics
3. Update PRD status to "Shipped"

## Workflow Cheatsheet

```
Phase 0: Requirements
/prd-writer          → Multi-turn Q&A to gather requirements, generate PRD

Phase 1: Planning
architect agent      → Technical architecture design (how to build it)
planner agent        → Break into implementation tasks (what to build)

Phase 2: Implementation
[write code]

Phase 3: Quality Assurance (parallel)
code-reviewer + security-reviewer  → simultaneous review
test-creator                       → add tests

Phase 4: Validation
e2e-runner           → end-to-end validation
doc-updater          → update documentation

PRD status → Shipped
```

## Handoff Prompts

After PRD is complete, offer these next actions:

```
PRD generated! What would you like to do next?

1. UI/UX Design Exploration (/brainstorming) - if there's an interface
2. Technical Architecture Design (architect) - decide how to build it
3. Break into Development Tasks (planner) - decide what to build
4. Save for now, continue later
```

Use AskUserQuestion to let user choose.

## Key Principles

- **Problem before solution** - Never jump to features before understanding the problem
- **Quantify success** - Vague goals lead to vague outcomes
- **Explicit exclusions** - What you DON'T build is as important as what you do
- **Living document** - Remind user to update as requirements evolve
- **YAGNI** - Ruthlessly cut features that aren't essential for v1

---

## Lenny's Podcast Wisdom Integration

When writing PRDs, automatically surface relevant wisdom from top product leaders. Use these to enrich the PRD process:

### Phase 1: Problem Discovery
> **April Dunford**: "Really great positioning feels so clear, so simple - of course that's what it is."
- Ask: What are competitive alternatives (including status quo)?
- Remember: 40% of B2B deals are lost to "no decision" - you're competing with spreadsheets!

> **Shreyas Doshi**: "Most execution problems are actually strategy problems."
- If user describes execution problems, dig deeper into strategy clarity

### Phase 2: Why Now?
> **Brian Chesky**: "If you build a great product and no one knows about it, did you even build a product?"
- Ask: How will you tell the story of this product?
- Think about every release as a chapter of a story

### Phase 3: Scope Definition
> **Brian Chesky**: "Five teams should do one thing rather than one team do five things."
- Ruthlessly cut scope
- Ask: "What would you cut to concentrate on fewer things?"

> **Brian Chesky**: "The best way to slow a project down is add more people to it."
- Small team, focused scope = faster delivery

### Phase 4: Success Metrics
> **Marty Cagan**: "Optimization is easier than innovation; but only innovation wins."
- Don't just optimize metrics - ask what new value is created
- Everything in the backlog is a bet - make better bets

### Phase 5: Risk Assessment
> **Shreyas Doshi**: Pre-mortem framework
After PRD is drafted, suggest running a pre-mortem:
- **Tigers**: Real threats that could kill the project
- **Paper Tigers**: Seeming threats that aren't real
- **Elephants**: Things nobody is talking about

Ask: "What 3 tigers (real threats) could derail this project?"

### Phase 6: Prioritization
> **Shreyas Doshi**: LNO Framework
- **L (Leverage)**: Which features give 10-100x return? Focus here.
- **N (Neutral)**: Standard features, 1x return
- **O (Overhead)**: Features with less return than effort

### Reference: Wisdom Source
All wisdom sourced from Lenny's Podcast. If you have local transcripts, search them for additional context.

## Quick Mode

If user says "quick PRD" or "lean PRD", use abbreviated flow:
1. Problem (1 question)
2. Users (1 question)
3. Success metric (1 question)
4. Must-have features (1 question)
5. Generate One-Pager PRD format

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
