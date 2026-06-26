---
name: hr
description: >
  Complete human resources intelligence system for founders, managers, and HR professionals.
  Trigger whenever someone needs help with hiring, onboarding, performance management,
  compensation, employee relations, termination, compliance, or building the people systems
  that determine whether a team thrives or fails. Also triggers on phrases like "how do I
  hire", "an employee is underperforming", "what do I need to know about employment law",
  "write a job description", "how do I let someone go", or any scenario involving the
  relationship between an organization and the people who work for it.
---

# HR — Complete Human Resources Intelligence System

## What This Skill Does

The people decisions in an organization compound faster than almost any other decisions.
A great hire in a critical role returns ten times their cost in the first year. A bad hire
in the same role costs twice their salary in direct costs and multiples of that in
organizational drag, team morale, and founder time. Getting people decisions right is not
an HR function — it is a strategy function.

This skill treats it that way.

---

## Core Principle

HR systems exist to help people do their best work and to protect the organization when
they do not. The organizations that build these systems thoughtfully — before they need
them — have an enormous advantage over those that build them reactively in response to
problems they could have prevented.

---

## Workflow

### Step 1: Identify the HR Scenario
```
HR_SCENARIOS = {
  "hiring": {
    "stages":    ["role_definition", "job_description", "sourcing", "screening",
                  "interviewing", "assessment", "offer", "negotiation"],
    "key_risk":  "Hiring for the wrong role definition is the most expensive hiring mistake"
  },
  "onboarding": {
    "stages":    ["pre_start", "day_one", "first_week", "30_60_90_day"],
    "key_risk":  "Poor onboarding doubles time to productivity and increases early attrition"
  },
  "performance": {
    "stages":    ["goal_setting", "regular_feedback", "formal_review", "PIP", "exit"],
    "key_risk":  "Delayed feedback turns fixable problems into terminations"
  },
  "compensation": {
    "components": ["base", "bonus", "equity", "benefits", "non_monetary"],
    "key_risk":   "Below-market compensation is invisible until your best people leave"
  },
  "termination": {
    "types":     ["performance", "redundancy", "misconduct", "mutual_agreement"],
    "key_risk":  "Procedural errors in termination create legal liability regardless of merit"
  },
  "compliance": {
    "areas":     ["employment_contracts", "leave_entitlements", "workplace_safety",
                  "discrimination", "privacy", "wage_and_hour"],
    "key_risk":  "Employment law violations are expensive and reputationally damaging"
  }
}
```

### Step 2: Hiring Intelligence
```
HIRING_FRAMEWORK = {
  "role_definition": {
    "before_writing_JD": [
      "What problem does this role solve that is not currently being solved",
      "What does success look like in 90 days, 6 months, and 2 years",
      "What skills are truly required versus nice to have",
      "What type of person thrives in this team and culture",
      "Is this definitely a hire or could it be a tool, contractor, or process change"
    ]
  },

  "job_description_structure": {
    "title":         "Accurate to market — affects who applies and at what salary expectation",
    "about_company": "2-3 sentences. What you do and why it matters. No fluff.",
    "role_summary":  "What this person will own and what impact they will have",
    "responsibilities": "What they will actually do — specific verbs, not vague categories",
    "requirements":  {
      "must_have":   "Skills without which the person cannot do the job",
      "nice_to_have": "Skills that would accelerate their contribution",
      "rule":        "Every requirement must be genuinely necessary — credential inflation
                       screens out strong candidates and reduces diversity"
    },
    "compensation":  "Include range — job posts with salary ranges get 30% more applicants",
    "tone":          "Write for the candidate you want to attract, not the job spec lawyer"
  },

  "interview_framework": {
    "structured_interviews": {
      "principle": "Same questions in same order for all candidates — reduces bias, improves comparison",
      "question_types": {
        "behavioral": "Tell me about a time when — reveals actual past behavior",
        "situational": "What would you do if — reveals thinking and values",
        "technical":   "Demonstrate or solve — reveals actual skill level",
        "motivational": "Why this role, why now — reveals fit and retention risk"
      }
    },

    "evaluation_framework": """
      def evaluate_candidate(interview_notes):
          score_on = {
              "skill_match":      rate(1-5),  # Can they do the job
              "culture_add":      rate(1-5),  # Will they make the team better
              "motivation":       rate(1-5),  # Do they genuinely want this specifically
              "growth_potential": rate(1-5),  # Can they grow with the role
              "reference_signal": rate(1-5)   # What did references actually say
          }
          return {
              "hire":        all(v >= 3 for v in score_on.values()),
              "strong_hire": all(v >= 4 for v in score_on.values()),
              "no_hire":     any(v <= 2 for v in score_on.values())
          }
    """
  }
}
```

### Step 3: Performance Management
```
PERFORMANCE_FRAMEWORK = {
  "goal_setting": {
    "OKR_structure": {
      "objective":     "Qualitative, inspiring, direction-setting",
      "key_results":   "3-5 measurable outcomes that define objective achievement",
      "principle":     "Key Results must be measurable. If you cannot measure it, it is not a KR."
    },
    "review_cadence": "Weekly 1:1s for real-time feedback. Monthly check-ins for goal tracking.
                       Quarterly formal reviews. Annual compensation review."
  },

  "feedback_delivery": {
    "SBI_framework": {
      "Situation":  "Specific context where the behavior occurred",
      "Behavior":   "Observable action — not interpretation, not character",
      "Impact":     "Concrete effect of the behavior on work, team, or outcomes"
    },
    "rules": ["Specific beats general always",
               "Immediate beats delayed — feedback loses value with time",
               "Private for criticism, public for praise",
               "Balanced feedback includes both what to continue and what to change"],
    "what_not_to_say": ["You always...", "You never...", "Your attitude is...",
                         "Everyone thinks...", "You should be more like..."]
  },

  "performance_improvement": {
    "PIP_principles": [
      "A PIP should be a genuine attempt to help the person succeed — not documentation for termination",
      "Specific, measurable performance standards that are achievable",
      "Regular check-ins during the PIP period",
      "Support and resources to address the gap",
      "Clear consequence if standards are not met"
    ],
    "PIP_structure": {
      "current_performance": "Specific examples of where performance falls short",
      "expected_standard":   "Exactly what good looks like, measured how",
      "support_provided":    "What the company will do to help",
      "timeline":            "Specific dates for review",
      "consequence":         "What happens if standard is not met"
    }
  }
}
```

### Step 4: Compensation Architecture
```
COMPENSATION_FRAMEWORK = {
  "market_benchmarking": {
    "sources":    ["Levels.fyi for tech", "Glassdoor", "LinkedIn Salary",
                   "Industry surveys", "Recruiter conversations"],
    "principle":  "Pay at or above market for roles critical to your success.
                   Below-market compensation is an invisible tax you pay in attrition."
  },

  "pay_bands": {
    "purpose":    "Defined ranges for each role level — enables fair, consistent decisions",
    "structure":  "Minimum (entry for role) — Midpoint (fully proficient) — Maximum (top of range)",
    "rule":       "If someone is above the maximum, they have grown beyond the role — promote or accept flight risk"
  },

  "equity_principles": {
    "early_stage": "Options are the deferred compensation that makes below-market base viable",
    "cliff":       "Standard: 1-year cliff before any vesting begins",
    "vesting":     "Standard: 4-year vest with monthly vesting after cliff",
    "refreshers":  "Top performers need new grants to maintain retention incentive"
  }
}
```

### Step 5: Termination Protocol
```
TERMINATION_FRAMEWORK = {
  "before_termination": {
    "documentation_required": [
      "Performance issues communicated in writing with dates",
      "Feedback given and documented",
      "PIP completed if performance-based termination",
      "HR or legal review completed",
      "Final decision maker aligned"
    ],
    "legal_review":   "Employment law is jurisdiction-specific. Review before any termination."
  },

  "the_conversation": {
    "timing":     "Monday or Tuesday morning — not Friday. Gives person time to take action.",
    "location":   "Private. In person where possible.",
    "duration":   "15-20 minutes maximum. Decision is made and not reversible.",
    "script":     {
      "opening":  "This is a difficult conversation. [Name], we have decided to end your employment.",
      "reason":   "State reason clearly and briefly. No lengthy justification.",
      "logistics": "Cover: last day, pay, benefits continuation, reference policy, equipment return",
      "closing":  "Dignified. Brief. Do not extend."
    },
    "what_not_to_do": ["Apologize repeatedly", "Argue or debate", "Give false hope",
                        "Over-explain", "Be surprised by emotional reaction"]
  },

  "post_termination": {
    "immediate":  ["Access revoked same day", "Equipment returned", "Team notified with appropriate explanation"],
    "severance":  "Consult legal on requirements. Voluntary severance above legal minimum often reduces risk.",
    "reference":  "Establish reference policy before you are asked — typically title, dates, eligibility for rehire only"
  }
}
```

---

## Employment Law Principles
```
LEGAL_PRINCIPLES = {
  "employment_contracts": "Written contracts protect both parties. Verbal agreements are enforceable
                           but expensive to prove.",
  "at_will_vs_notice":    "At-will employment (US) differs significantly from notice period
                           requirements elsewhere — know your jurisdiction.",
  "protected_classes":    "Termination, discipline, and hiring decisions must never be based on
                           protected characteristics — race, gender, age, religion, disability,
                           and others vary by jurisdiction.",
  "wage_and_hour":        "Overtime rules, minimum wage, and classification of employees vs
                           contractors are heavily regulated with significant penalties for violations.",
  "disclaimer":           "Employment law is highly jurisdiction-specific and changes frequently.
                           HR decisions with legal exposure should be reviewed by employment counsel."
}
```

---

## Quality Check Before Delivering

- [ ] Jurisdiction flagged — employment law varies significantly by location
- [ ] Role definition completed before job description drafted
- [ ] Interview questions are structured and behavioral
- [ ] Performance feedback follows SBI or equivalent specific framework
- [ ] PIP includes measurable standards and genuine support
- [ ] Termination documentation is complete before conversation happens
- [ ] Legal review recommended for any termination or discrimination-adjacent scenario
