---
name: job
description: >
  Complete job search intelligence system for anyone looking for work, changing careers,
  or trying to advance professionally. Trigger whenever someone needs help finding a job,
  writing a resume, preparing for interviews, negotiating offers, navigating a career
  transition, or understanding what is holding their job search back. Also triggers on
  phrases like "help me find a job", "rewrite my resume", "I have an interview tomorrow",
  "should I take this offer", "I got laid off", "I want to change careers", or any scenario
  where someone's professional livelihood is at stake.
---

# Job — Complete Job Search Intelligence System

## What This Skill Does

A job search is a sales process where you are both the salesperson and the product. The
candidate who understands this — who approaches their search with the same rigor, strategy,
and persistence they would apply to any important professional project — finds better jobs
faster and negotiates better outcomes than the candidate who submits applications and waits.

Most job searches fail not because the candidate is unqualified. They fail because the
resume is not optimized for how it will be read, the applications are going to the wrong
places, the interview preparation is generic rather than specific, and the negotiation
is either skipped entirely or handled poorly.

This skill fixes all of that.

---

## Core Principle

The job search has three phases that require completely different strategies: getting
seen, getting selected, and getting the offer you deserve. Failing in any one phase
produces the same outcome — no job — but requires a completely different fix. The skill
diagnoses which phase is failing and applies the right intervention.

---

## Workflow

### Step 1: Assess the Job Search Situation
```
JOB_SEARCH_PHASES = {
  "getting_seen": {
    "symptom":   "Applying to many jobs, getting few or no responses",
    "causes":    ["Resume not passing ATS", "Wrong keywords", "Applying to wrong roles",
                  "Too broad or too narrow targeting"],
    "fix":       "Resume optimization, targeting strategy, network activation"
  },
  "getting_selected": {
    "symptom":   "Getting interviews but not advancing to next rounds",
    "causes":    ["Weak interview performance", "Poor story structure",
                  "Not researching company specifically", "Failing technical screens"],
    "fix":       "Interview preparation, story development, company research framework"
  },
  "getting_the_offer": {
    "symptom":   "Getting to final round but not receiving offers, or receiving low offers",
    "causes":    ["Reference issues", "Salary expectation mismatch", "Weak close",
                  "Poor negotiation"],
    "fix":       "Reference preparation, salary research, negotiation scripts"
  }
}
```

### Step 2: Resume Architecture
```
RESUME_FRAMEWORK = {
  "ATS_optimization": {
    "how_ATS_works": """
      def ats_score(resume, job_description):
          resume_keywords = extract_keywords(resume)
          jd_keywords = extract_keywords(job_description)
          match_score = len(resume_keywords & jd_keywords) / len(jd_keywords)
          # Resumes scoring below 0.6-0.7 are filtered before human review
          return match_score
    """,
    "rules": [
      "Mirror exact language from job description — not synonyms",
      "Standard section headers: Experience, Education, Skills — not creative alternatives",
      "No tables, columns, headers/footers, or text boxes — ATS cannot parse them",
      "Submit as .docx or .pdf depending on instructions",
      "Spell out acronyms once: Search Engine Optimization (SEO)"
    ]
  },

  "structure": {
    "contact":      "Name, email, phone, LinkedIn, city/state — no full address needed",
    "summary":      "3 sentences: who you are professionally, your strongest value, what you want next",
    "experience":   "Reverse chronological. Each role: company, title, dates, 3-5 bullets.",
    "skills":       "Technical skills, tools, certifications — keywords for ATS",
    "education":    "After experience for anyone with 3+ years of work history"
  },

  "bullet_formula": {
    "structure":  "Action verb + what you did + measurable result",
    "examples": {
      "weak":   "Responsible for managing social media accounts",
      "strong": "Grew Instagram following from 8K to 47K in 14 months through
                 daily content strategy, increasing inbound leads by 34%"
    },
    "action_verbs": ["Led", "Built", "Drove", "Reduced", "Increased", "Launched",
                     "Negotiated", "Designed", "Implemented", "Managed", "Created"],
    "quantify_everything": "Numbers, percentages, dollar amounts, team sizes, timeframes"
  },

  "tailoring_per_application": """
    def tailor_resume(base_resume, job_description):
        jd_keywords = extract_top_keywords(job_description, n=15)
        required_skills = extract_requirements(job_description)

        for keyword in jd_keywords:
            if keyword not in base_resume:
                find_experience_that_demonstrates(keyword)
                rewrite_bullet_to_include(keyword)

        reorder_bullets_by_relevance_to(job_description)
        return tailored_resume
    # Time: 15-20 minutes per application. Worth it for roles you want.
  """
}
```

### Step 3: Job Search Strategy
```
SEARCH_STRATEGY = {
  "targeting": {
    "define_clearly": {
      "role_titles":    "List 5-10 titles for the role you want — they vary by company",
      "company_types":  "Size, industry, stage, culture — be specific",
      "geography":      "In-office, hybrid, remote — know your constraints",
      "level":          "IC vs management, junior vs senior — match to your experience"
    },
    "target_company_list": {
      "size":     "50-100 target companies is manageable",
      "sources":  ["LinkedIn company search", "Industry lists", "Portfolio companies of VCs you know",
                   "Competitors of companies you know well"],
      "tracking": "Spreadsheet: Company | Role | Connection | Status | Next Action | Date"
    }
  },

  "channel_allocation": {
    "network":         "60-70% of jobs are filled through relationships — prioritize this",
    "direct_apply":    "Company career pages directly — better than aggregators",
    "recruiters":      "Valuable for senior roles — build relationships before you need them",
    "job_boards":      "LinkedIn, Indeed — high volume but low conversion, use as supplement",
    "principle":       "A warm introduction converts at 10x the rate of a cold application"
  },

  "networking_approach": {
    "informational_interview": {
      "purpose":   "Learn about a role or company, build relationship, get referred",
      "ask":       "20-minute call to learn about their experience at [company]",
      "never_ask": "Do you know of any openings — too transactional too early",
      "follow_up": "Thank you note within 24 hours. Stay in touch. Ask for one introduction."
    },

    "outreach_script": {
      "cold":    "Hi [name], I came across your work on [specific thing] and am exploring
                  roles in [area]. I would love 20 minutes to hear about your experience
                  at [company] — happy to work around your schedule.",
      "warm":    "Hi [name], [mutual connection] suggested I reach out. I am exploring
                  roles in [area] and would value 20 minutes of your perspective on [company/role]."
    }
  }
}
```

### Step 4: Interview Excellence
```
INTERVIEW_FRAMEWORK = {
  "preparation_system": {
    "company_research": {
      "required": ["Business model and revenue sources",
                   "Recent news — last 3 months",
                   "Products and key competitors",
                   "Culture and values — Glassdoor, LinkedIn posts",
                   "Your interviewer's background — LinkedIn"],
      "use_in_interview": "Ask about something specific you researched — signals genuine interest"
    }
  },

  "story_bank": {
    "STAR_method": {
      "Situation": "Context — brief, specific, relevant",
      "Task":      "What you were responsible for",
      "Action":    "What YOU specifically did — not the team, not the process",
      "Result":    "Measurable outcome — numbers, percentages, business impact"
    },
    "stories_to_prepare": [
      "Greatest professional achievement",
      "Difficult challenge and how you overcame it",
      "Conflict with colleague and resolution",
      "Failed project and what you learned",
      "Time you led without authority",
      "Time you had to change someone's mind with data",
      "Time you had to make a decision with incomplete information"
    ]
  },

  "question_handling": {
    "tell_me_about_yourself": {
      "formula":  "Present → Past → Future",
      "structure": "I am currently [role] at [company] where I [key responsibility].
                    Before that [most relevant background]. I am looking for [specific next step]
                    because [genuine reason that connects to this role].",
      "length":   "90 seconds maximum"
    },
    "weakness_question": {
      "formula":  "Real weakness + what you have done about it + current state",
      "avoid":    "I work too hard. I am a perfectionist. — Interviewers have heard these 1000 times"
    },
    "salary_question": {
      "if_asked_early": "I am flexible — I would want to understand the full scope of the role
                          before discussing compensation. What is the budgeted range?",
      "if_pressed":     "Based on my research and experience, I am targeting [range].
                          Is that aligned with the budget for this role?"
    }
  },

  "questions_to_ask": {
    "about_role":    "What does success look like in the first 90 days",
    "about_team":    "How would you describe the team culture and how decisions get made",
    "about_company": "What is the biggest challenge the team is working through right now",
    "about_interviewer": "What has kept you at [company] — what do you find most energizing",
    "never_ask":     "What does the company do. How much vacation do I get. When will I be promoted."
  }
}
```

### Step 5: Offer Evaluation and Negotiation
```
OFFER_FRAMEWORK = {
  "total_compensation_calculation": """
    def calculate_total_comp(offer):
        base = offer.base_salary
        bonus = base * offer.target_bonus_percent
        equity_annual = estimate_equity_value(offer.equity) / offer.vesting_years
        benefits_value = estimate_benefits(offer.health, offer.retirement_match, offer.pto)

        total = base + bonus + equity_annual + benefits_value
        return {
            "cash_comp":   base + bonus,
            "equity_comp": equity_annual,
            "benefits":    benefits_value,
            "total":       total
        }
    # Never compare offers on base salary alone
  """,

  "negotiation_framework": {
    "always_negotiate": "60% of employers expect negotiation. Not negotiating leaves money on table.",
    "opening_script":   "Thank you for the offer — I am genuinely excited about this opportunity.
                          I was hoping we could get to [target number]. Is there flexibility there?",
    "after_counter":    "Stay silent. Do not justify or elaborate. The discomfort is working for you.",
    "if_base_is_fixed": "If base is truly fixed, negotiate: signing bonus, extra PTO, remote days,
                          accelerated review date, equity refresh, professional development budget",
    "get_it_in_writing": "Verbal offers mean nothing. Do not resign current job until written offer signed."
  },

  "offer_decision_framework": {
    "evaluate_on": ["Compensation vs market rate",
                    "Role scope and growth trajectory",
                    "Manager quality — people leave managers not companies",
                    "Team and culture",
                    "Company trajectory — growing or shrinking",
                    "Mission alignment"],
    "red_flags":   ["Pressure to decide immediately",
                    "Vague role description that no one can clarify",
                    "High turnover in the team",
                    "Rescinded offers or changed terms at last minute"]
  }
}
```

---

## Career Transition Support
```
CAREER_CHANGE_FRAMEWORK = {
  "transferable_skills_audit": {
    "principle": "Every skill has a transferable equivalent. The job is to translate it.",
    "example":   "Teaching → Training and Development, Curriculum Design, Public Speaking",
    "process":   "List everything you have done. Find the business language for each."
  },

  "bridge_building": {
    "education":   "Certifications and courses signal commitment to the new field",
    "projects":    "Build something in the new domain — portfolio beats credentials",
    "network":     "Join communities in the target field before you need a job in it",
    "adjacent_role": "Sometimes the fastest path is an adjacent role at current company"
  }
}
```

---

## Quality Check Before Delivering

- [ ] Job search phase correctly diagnosed — getting seen vs selected vs offer
- [ ] Resume optimized for ATS with job-specific keywords
- [ ] Bullet points follow action-result formula with quantification
- [ ] Interview stories prepared in STAR format for key scenarios
- [ ] Salary research completed before any negotiation guidance
- [ ] Total compensation calculated including equity and benefits
- [ ] Negotiation script specific to offer and situation
- [ ] Red flags in offer or process flagged proactively
