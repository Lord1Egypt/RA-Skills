---
name: lease
description: >
  Complete lease intelligence system for tenants, landlords, and property managers. Trigger
  whenever someone needs to understand, negotiate, draft, or dispute anything related to a
  lease agreement. Also triggers on phrases like "review my lease", "what does this clause mean",
  "my landlord is doing this", "I want to break my lease", "draft a rental agreement", or any
  property rental scenario.
---

# Lease — Complete Lease Intelligence System

## What This Skill Does

A lease is one of the most consequential contracts most people sign — and one they almost never
read carefully before signing. The clauses that seem like boilerplate are the ones that determine
whether you get your deposit back, whether your landlord can enter without notice, and what it
costs you if life changes and you need to leave early.

This skill reads the fine print so you do not have to discover it the hard way.

---

## Core Principle

Every lease is a negotiation that most tenants do not realize has already started. Landlords
draft leases to protect themselves. That is rational. What is irrational is signing without
understanding what you agreed to. This skill corrects that asymmetry.

---

## Workflow

### Step 1: Identify the User and Scenario
```
USER_TYPES = {
  "tenant":           "Reviewing before signing, mid-tenancy dispute, move-out preparation",
  "landlord":         "Drafting agreements, managing disputes, understanding obligations",
  "property_manager": "Portfolio compliance, clause standardization, dispute resolution"
}

LEASE_SCENARIOS = {
  "pre_signing":      "Review and negotiate before committing",
  "mid_tenancy":      "Understand rights, handle disputes, request repairs",
  "break_lease":      "Calculate costs, understand options, minimize penalties",
  "move_out":         "Deposit recovery, condition documentation, final inspection",
  "dispute":          "Landlord non-compliance, illegal entry, retaliation, habitability",
  "drafting":         "Create legally sound rental agreements for landlords"
}
```

### Step 2: Clause Analysis Framework

When reviewing a lease, apply systematic clause analysis:
```
CRITICAL_CLAUSES = {
  "rent_escalation": {
    "what_to_find":  "How much can rent increase and when",
    "red_flags":     ["unlimited discretion", "no cap", "CPI + percentage above 3%"],
    "ideal":         "Fixed percentage cap or CPI-linked with maximum"
  },
  "entry_rights": {
    "what_to_find":  "When landlord can enter and how much notice",
    "red_flags":     ["entry without notice", "notice less than 24 hours for non-emergency"],
    "ideal":         "48 hours written notice except genuine emergency"
  },
  "deposit": {
    "what_to_find":  "Amount, permitted deductions, return timeline",
    "red_flags":     ["vague deduction language", "no return timeline", "non-refundable fees"],
    "ideal":         "Specific deduction list, 14-21 day return window, itemized statement required"
  },
  "break_clause": {
    "what_to_find":  "Early termination rights, penalty structure, notice required",
    "red_flags":     ["no break clause", "penalty equals remaining rent", "no subletting option"],
    "ideal":         "Clear penalty formula, subletting permitted with approval"
  },
  "repairs": {
    "what_to_find":  "Who is responsible for what, response timeframes",
    "red_flags":     ["tenant responsible for all repairs", "no emergency repair provision"],
    "ideal":         "Landlord responsible for structural and essential services, defined timeframes"
  },
  "pets": {
    "what_to_find":  "Permission, conditions, additional deposit",
    "red_flags":     ["blanket prohibition with no process", "non-refundable pet fee"],
    "ideal":         "Permission not unreasonably withheld, refundable pet bond"
  },
  "alterations": {
    "what_to_find":  "What modifications are permitted and what must be restored",
    "red_flags":     ["no alterations whatsoever", "restoration required for all changes"],
    "ideal":         "Minor alterations permitted, major require written consent"
  }
}
```

### Step 3: Negotiation Playbook

Most tenants do not negotiate leases. Most landlords expect some negotiation on certain points.
Knowing what is negotiable and how to ask is the entire skill.
```
NEGOTIATION_FRAMEWORK = {
  "always_try_to_negotiate": [
    "Rent increase cap — add a fixed percentage maximum",
    "Break clause — if absent, request one after month 6",
    "Entry notice — push from 24 to 48 hours",
    "Pet clause — request approval process rather than blanket ban"
  ],

  "negotiation_scripts": {
    "rent_cap": "I am very interested in the property. I would like to add a clause capping
                 annual rent increases at [X]% to give both of us predictability. This is
                 standard in many agreements — would you be open to including it?",

    "break_clause": "I intend to stay the full term, but circumstances can change for anyone.
                     Could we add a break clause after month 6 with 8 weeks notice and
                     [one month's rent] as a fee? It protects both of us.",

    "deposit_terms": "I would like the deposit return clause to specify that itemized deductions
                      will be provided within 14 days of move-out. Happy to put that in writing."
  },

  "negotiation_rules": [
    "Ask in writing — creates a record and gives the landlord time to consider",
    "Ask for everything at once — multiple small requests feel less demanding than sequential ones",
    "Offer something in return — longer lease term, faster payment, direct debit",
    "Accept partial wins — getting one clause changed is better than getting nothing"
  ]
}
```

### Step 4: Move-Out Deposit Protection

The deposit dispute is the most common and most preventable lease conflict.
```
DEPOSIT_PROTECTION_SYSTEM = {
  "move_in": {
    "documentation": [
      "Photograph every room from 4 corners",
      "Photograph every wall, floor, fixture, and appliance",
      "Note every existing mark, stain, or damage in writing",
      "Send condition report to landlord via email on day 1",
      "Keep sent email as timestamped proof"
    ],
    "principle": "If it is not documented on move-in, it will be claimed on move-out"
  },

  "move_out": {
    "preparation": [
      "Reference move-in photos for every room",
      "Clean to the standard documented at move-in — not higher",
      "Repair only damage you caused — not pre-existing wear",
      "Conduct your own inspection before the landlord's",
      "Be present at the final inspection"
    ],
    "if_disputed": {
      "step_1": "Request itemized deduction list in writing",
      "step_2": "Compare each item against move-in documentation",
      "step_3": "Dispute specific items with evidence, not general disagreement",
      "step_4": "Reference local tenancy tribunal process if unresolved"
    }
  },

  "normal_wear_vs_damage": {
    "normal_wear": ["Faded paint", "Minor scuffs on walls", "Worn carpet in traffic areas",
                    "Small nail holes from pictures", "Loose door handles"],
    "tenant_damage": ["Holes in walls", "Stained carpet from spills", "Broken fixtures",
                      "Unauthorized paint colors", "Pet damage"]
  }
}
```

### Step 5: Breaking a Lease Early
```
BREAK_LEASE_OPTIONS = {
  "negotiated_exit": {
    "approach":  "Talk to landlord directly. Many prefer a clean exit to a difficult tenancy.",
    "offer":     "Finding a replacement tenant is the strongest negotiating position you have.",
    "document":  "Any agreement to exit early must be in writing with signatures."
  },

  "subletting": {
    "check_first": "Review lease for subletting clause before proceeding",
    "process":     "Written request to landlord, proposed subtenant details, await written approval",
    "risk":        "You remain liable for rent and damage unless novation agreement signed"
  },

  "hardship_grounds": {
    "domestic_violence": "Most jurisdictions allow immediate termination — document and apply",
    "job_loss":          "Some jurisdictions recognize financial hardship — check local law",
    "uninhabitability":  "Landlord failure to maintain habitable conditions may void lease"
  },

  "cost_calculation": {
    "formula": "Weeks remaining × weekly rent × break_fee_multiplier",
    "typical_range": "4-8 weeks rent as penalty for fixed-term break",
    "offset": "Penalty reduces as landlord finds replacement tenant"
  }
}
```

---

## Quality Check Before Delivering

- [ ] Jurisdiction flagged — lease law varies significantly by location
- [ ] User type identified — tenant and landlord advice differs substantially
- [ ] Critical clauses all reviewed if full lease analysis requested
- [ ] Negotiation language is specific and ready to use
- [ ] Any habitability or safety issue flagged for urgent attention
- [ ] Professional legal advice recommended for complex disputes
