---
name: intake
description: >
  Design intake forms, discovery interviews, onboarding workflows, and intake summaries
  for service relationships. Use when someone needs to collect the right information
  before starting work with a client, patient, customer, student, tenant, or employee.
---

# Intake

Intake is the system for collecting the right information, in the right order,
with the right level of trust, before real work begins.

## Trigger Conditions

Use this skill when the user needs to:
- onboard a new client, patient, customer, tenant, student, or employee
- design an intake form or discovery questionnaire
- structure an onboarding workflow
- gather requirements before providing a service
- identify what information should be collected at the start of a relationship
- improve an existing intake process that feels incomplete, bureaucratic, or low-conversion

Also trigger when the user says things like:
- "I need an intake form"
- "Help me onboard a new client"
- "What should I ask before starting"
- "I need a discovery process"
- "How do I collect the right information upfront"

## The Information You Wish You Had Asked

Every service relationship has a moment — usually six weeks in — where the provider thinks:
I wish I had known that at the start.

The therapist who discovers the client has tried this approach twice before.
The contractor who finds out the client had a bad experience with the last three contractors.
The accountant who learns about the offshore account in month four.
The coach who realizes the presenting goal is not the real goal.

Intake is not paperwork. It is the intelligence-gathering operation that determines whether
the work that follows will be effective or expensive.

This skill builds intake systems that surface the information that matters — before the
work begins.

## Core Principle

People do not withhold important information because they are secretive. They withhold it
because nobody asked the right question, or because the form felt like bureaucracy rather
than care. The intake process that feels like a thoughtful conversation extracts more
useful information than the intake process that feels like a legal requirement.

Design for the conversation. The information follows.

## Default Outputs

Depending on the request, produce one or more of the following:

1. Intake Form  
A structured form with sections, field names, and question wording.

2. Intake Interview Guide  
A conversation-based script for live intake calls or first sessions.

3. Intake Workflow  
A step-by-step onboarding flow showing what is collected, when, and why.

4. Intake Summary Template  
A reusable template for summarizing what was learned during intake.

5. Intake Audit  
A diagnostic review of an existing intake process, including friction points,
missing questions, over-collection, and compliance considerations.

## Response Rules

When responding:
- first identify the service type
- separate administrative intake from discovery intake
- avoid collecting information that will not be used
- explain why sensitive questions are asked
- prefer clarity and usability over comprehensiveness
- flag privacy or regulatory issues without pretending to give legal, medical, or financial advice

## Intake System Architecture
~~~python
INTAKE_FRAMEWORK = {
  "information_layers": {
    "layer_1_administrative": {
      "purpose":  "Legal, billing, and contact requirements",
      "examples": ["Full legal name", "Date of birth", "Contact information",
                   "Insurance or billing details", "Emergency contact",
                   "Consent and authorization signatures"],
      "format":   "Form — this is genuinely administrative, forms are appropriate here"
    },
    "layer_2_presenting": {
      "purpose":  "Why they are here and what they want",
      "examples": ["Primary reason for seeking service",
                   "What they hope to achieve",
                   "What has already been tried",
                   "Timeline and urgency"],
      "format":   "Questionnaire with open-ended fields — not multiple choice"
    },
    "layer_3_context": {
      "purpose":  "The information that changes how you provide the service",
      "examples": ["Relevant history", "Previous experiences with similar services",
                   "Factors that affect delivery", "Preferences and constraints",
                   "What success looks like to them specifically"],
      "format":   "Intake interview — conversation extracts what forms miss"
    },
    "layer_4_relationship": {
      "purpose":  "How to work with this person effectively",
      "examples": ["Communication preferences", "Decision-making style",
                   "What they need from a provider relationship",
                   "Previous experiences that shaped their expectations"],
      "format":   "Discovery conversation — built into first session or call"
    }
  }
}
~~~

## Intake Form Design
~~~python
FORM_DESIGN = {
  "principles": {
    "minimum_viable_intake":  "Collect only what you will actually use — every field
                                not used creates friction without return",
    "progressive_disclosure": "Administrative fields first, sensitive questions later —
                                trust is built before vulnerability is requested",
    "open_fields_over_checkboxes": "Checkboxes tell you what you gave them to say.
                                     Open fields tell you what they actually think.",
    "explain_why":            "A sentence explaining why you need sensitive information
                                dramatically increases completion rate and accuracy"
  },

  "question_design": {
    "weak":   "Do you have any medical conditions? [ ] Yes [ ] No",
    "strong": "Please describe any physical conditions, injuries, or health factors
               that are relevant to our work together. This helps me tailor my approach
               from our first session.",

    "weak_2":   "What are your goals?",
    "strong_2": "If our work together goes exactly as you hope, what will be different
                 in your life six months from now? Be as specific as you can."
  },

  "completion_rate_factors": [
    "Mobile-optimized — 60%+ of forms are completed on phone",
    "Progress indicator for multi-page forms",
    "Save and resume for longer forms",
    "Plain language — no jargon or clinical terminology",
    "Estimated completion time stated upfront",
    "Confirmation message that feels human not automated"
  ]
}
~~~

## The Intake Interview
~~~python
INTAKE_INTERVIEW = {
  "structure": {
    "opening":    {
      "purpose":  "Establish safety and set expectations",
      "script":   "Before we dive in, I want to explain how I use what you share with me.
                   Everything you tell me today helps me [specific benefit]. There are no
                   wrong answers — the more honest you can be, the better I can help you."
    },
    "presenting": {
      "questions": ["What brings you here now — why today rather than six months ago",
                    "What have you already tried, and what happened",
                    "What would have to change for you to feel this was worth it"],
      "listen_for": "Gap between stated goal and real goal — they are often different"
    },
    "history":    {
      "questions": ["What is the relevant background I should know",
                    "Have you worked with someone on this before — what was that like",
                    "What has gotten in the way in the past"],
      "purpose":   "Previous failed attempts contain more useful information than successes"
    },
    "expectations": {
      "questions": ["What do you expect this process to look like",
                    "What would make you want to stop working together",
                    "What do you need from me that you have not always gotten"],
      "purpose":   "Surface misaligned expectations before they become relationship problems"
    },
    "closing":    {
      "script":   "Is there anything important that I have not asked about — something
                   you came in hoping I would understand that we have not covered yet",
      "purpose":  "This single question surfaces more useful information than
                   most of the rest of the interview combined"
    }
  },

  "active_listening_protocol": """
    INTAKE_LISTENING = {
        "note_what_is_avoided":   "Topics skirted or answered too quickly often matter most",
        "note_energy_shifts":     "Where does engagement increase or decrease",
        "note_contradictions":    "Between stated priorities and described behavior",
        "note_language":          "Their exact words for their problem become your vocabulary",
        "do_not_solve_yet":       "Intake is information gathering — resist the urge to help
                                   before you understand"
    }
  """
}
~~~

## Intake by Service Type
~~~python
SERVICE_SPECIFIC = {
  "healthcare_therapy": {
    "required":     ["Chief complaint", "Medical history", "Medications and allergies",
                     "Previous treatment", "Family history if relevant",
                     "Consent and privacy acknowledgment"],
    "sensitive":    "Trauma history, substance use, mental health history —
                     ask with care, explain purpose, never require before trust is established"
  },
  "legal": {
    "required":     ["Matter description", "Relevant dates and deadlines",
                     "Prior legal representation", "Documents in possession",
                     "Desired outcome", "Budget and timeline expectations"],
    "conflict_check": "Run conflict check before intake interview — before sensitive
                       information is shared"
  },
  "financial_advisory": {
    "required":     ["Current financial situation", "Income and assets",
                     "Liabilities and obligations", "Risk tolerance",
                     "Goals and timeline", "Previous advisory relationships"],
    "sensitive":    "Financial shame is real — create psychological safety before
                     asking for numbers"
  },
  "coaching": {
    "required":     ["Presenting goal", "Current situation", "Previous attempts",
                     "Resources available", "Accountability preferences",
                     "Definition of success"],
    "distinguish":  "Presenting goal vs real goal vs root cause —
                     coaching intake should surface all three"
  },
  "creative_services": {
    "required":     ["Project scope and deliverables", "Timeline and milestones",
                     "Budget", "Decision-making process", "Brand guidelines",
                     "Examples of work they love and hate — both equally important"],
    "critical":     "Examples of work they hate prevent the most expensive revisions"
  }
}
~~~

## Information Management
~~~python
INTAKE_DATA_MANAGEMENT = {
  "storage_principles": [
    "Information collected for one purpose should not be used for another",
    "Sensitive information needs appropriate security — not in email threads",
    "Retention policy defined before collection begins",
    "Destruction process for data when relationship ends"
  ],

  "usability": {
    "principle":   "Intake information only has value if it is used",
    "system":      "Review intake notes before every session — not just the first",
    "update":      "Intake is not a one-time event — update as circumstances change",
    "transfer":    "If client transfers to another provider, intake summary
                    is the most valuable thing you can provide"
  },

  "compliance_flags": {
    "healthcare":   "HIPAA (US) or equivalent — specific requirements for PHI",
    "financial":    "KYC and AML obligations for financial services",
    "general":      "GDPR, CCPA, or applicable privacy regulation — get legal advice
                     for your jurisdiction before collecting sensitive data"
  }
}
~~~

## Boundaries

This skill helps design intake systems, forms, interviews, and information workflows.
It does not replace legal, medical, financial, privacy, or regulatory advice.

For regulated contexts, adapt outputs to the user's jurisdiction and consult a qualified
professional before using the workflow in production.

## Quality Check Before Delivering

- [ ] Information layers separated — administrative, presenting, context, relationship
- [ ] Form questions are open-ended not checkbox-dominated
- [ ] Sensitive questions explained with purpose
- [ ] Intake interview includes closing question — what have I not asked
- [ ] Service type matched to specific intake requirements
- [ ] Data storage and compliance flagged for sensitive service types
- [ ] Review protocol built in — intake used throughout relationship not just at start
