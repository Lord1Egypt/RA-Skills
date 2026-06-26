---
name: grant
description: >
  Complete grant intelligence system for individuals, nonprofits, startups, researchers, and
  small businesses. Trigger whenever someone needs to find grants, write grant applications,
  understand eligibility criteria, respond to reviewer feedback, or manage grant compliance.
  Also triggers on phrases like "find funding for", "apply for a grant", "write a grant
  proposal", "we need government funding", "what grants are available for", or any scenario
  where someone is seeking non-dilutive funding from government, foundation, or institutional
  sources.
---

# Grant — Complete Grant Intelligence System

## What This Skill Does

Grants are the most underutilized source of funding available to small businesses, nonprofits,
researchers, and individuals. Billions of dollars go unclaimed every year — not because eligible
applicants do not exist, but because the application process is opaque, time-consuming, and
written in language designed for bureaucrats rather than the people the funding is meant to help.

This skill navigates that landscape. It finds the funding, builds the case, and writes the
application.

## Core Principle

Grant applications are not requests. They are arguments. The reviewer is not deciding whether
to give you money — they are deciding whether your project best fulfills the grant objectives.
Every word in a successful application is written from the reviewer perspective, not the
applicant perspective.

## Workflow

### Step 1: Profile the Applicant
```
APPLICANT_TYPES = {
  "nonprofit":      { sources: ["government","foundation","corporate"], strengths: ["impact","track_record","partnerships"] },
  "startup":        { sources: ["innovation","R&D","export","accelerator"], strengths: ["innovation","market","team","scale"] },
  "researcher":     { sources: ["research_councils","university","industry"], strengths: ["methodology","significance","collaboration"] },
  "small_business": { sources: ["business_development","export","energy","hiring"], strengths: ["jobs","economic_contribution","innovation"] },
  "individual":     { sources: ["arts","education","community","professional"], strengths: ["story","impact","viability"] }
}
```

### Step 2: Grant Identification
```
ELIGIBILITY_CHECKLIST = [
  "Organization type matches funder requirements",
  "Geographic location within funded area",
  "Project dates align with grant period",
  "Budget within grant range",
  "Activity type explicitly included in guidelines",
  "No conflict of interest with funder",
  "Organization in good standing"
]

GRANT_SCORING = {
  "eligibility_fit":   "0-3",
  "strategic_fit":     "0-3",
  "competition_level": "0-3",
  "effort_required":   "0-3",
  "funder_relationship": "0-3"
}
# Pursue grants scoring 10+. Below 8, ROI is poor.
```

### Step 3: Application Architecture

#### Executive Summary
Written last, placed first. Maximum 200 words. If the reviewer reads only this, they should
understand and want to fund it.

#### Problem Statement
```
PROBLEM_STRUCTURE = [
  "Scale: how many people or how much is affected",
  "Severity: what happens if this is not addressed",
  "Gap: why existing solutions are insufficient",
  "Urgency: why now"
]
# Use data, research citations, community consultation findings.
# Never frame the problem in terms of your organization needs.
```

#### Proposed Solution
What specifically will be done. How it addresses root cause not symptoms. Why this approach
over alternatives. Your unique capability to deliver it.

#### Methodology
```
WORKPLAN_ELEMENTS = [
  "Phase-by-phase milestones with dates",
  "Team roles and relevant experience",
  "Partners and their specific contributions",
  "Risk identification and mitigation",
  "Timeline fits within grant period"
]
```

#### Outcomes and Evaluation
```
OUTCOMES_FRAMEWORK = {
  "outputs":   "Direct products — number trained, events delivered, reports produced",
  "outcomes":  "Changes that result — skills improved, behavior changed, access increased",
  "impact":    "Long-term change in community or sector"
}
# Every outcome needs a measurable indicator with baseline and target.
```

#### Budget
```
BUDGET_RULES = [
  "Every line item justified in narrative",
  "Administration under 15% unless justified",
  "Show co-contribution if required",
  "Costs verified against market rates",
  "No ineligible expenses included"
]
```

### Step 4: Writing for Reviewers
```
REVIEWER_RULES = {
  "answer_the_question_asked":  "Read each question three times before writing",
  "lead_with_the_answer":       "First sentence answers. Elaboration follows.",
  "use_their_language":         "Mirror exact terminology from grant guidelines",
  "specificity_wins":           "'45 women trained in rural Victoria' beats 'help disadvantaged communities'",
  "evidence_everything":        "Every significant claim needs a source or statistic",
  "no_jargon":                  "Write for intelligent reviewer who is not a specialist"
}

SCORING_OPTIMIZATION = {
  "principle": "Allocate word count proportional to marks available per section",
  "checklist": "Every scoring criterion explicitly addressed before submitting"
}
```

### Step 5: Post-Submission
```
IF_FUNDED = [
  "Review signed agreement before signing",
  "Enter reporting schedule in calendar",
  "Establish budget tracking system",
  "Document everything during delivery"
]

IF_UNSUCCESSFUL = [
  "Request reviewer feedback",
  "Distinguish fit issues from quality issues",
  "Revise and reapply if quality was the issue",
  "Thank funder and express interest in future rounds"
]
```

## Grant Calendar
```
WORKBACK_SCHEDULE = {
  "8_weeks_out": "Eligibility confirmed, decision to apply made",
  "6_weeks_out": "Research complete, outline drafted",
  "4_weeks_out": "First draft complete, internal review done",
  "2_weeks_out": "Revised draft, budget finalized, attachments gathered",
  "1_week_out":  "Final review, proofread, technical submission test",
  "day_of":      "Submit by noon — never on deadline day evening"
}
```

## Quality Check

- [ ] Every section directly answers the question asked
- [ ] Problem framed from beneficiary perspective not applicant perspective
- [ ] All outcomes specific and measurable
- [ ] Budget justified line by line
- [ ] All eligibility criteria explicitly demonstrated
- [ ] All reviewer scoring criteria addressed
- [ ] Word limits respected
- [ ] Attachments checklist complete
