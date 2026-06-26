---
name: proposal
description: >
  Design, structure, and improve proposals for sales, services, partnerships, projects,
  and strategic opportunities. Use when someone needs to turn interest into a clear
  offer with scope, value, terms, and a persuasive path to decision.
---

# Proposal

A proposal is not just a document.

A proposal is a decision tool.

Most weak proposals fail for the same reason: they explain what will be done,
but not why it matters, why this approach fits, what outcome is being bought,
what risks are reduced, or what decision should happen next.

A good proposal reduces hesitation by making the value, structure, and choice clearer.

This skill helps turn vague offers into persuasive, usable proposals.

## Trigger Conditions

Use this skill when the user needs to:
- create a proposal for a client, customer, partner, or stakeholder
- structure an offer after discovery or intake
- present scope, pricing, terms, and timeline clearly
- improve proposal win rate
- turn a service idea into a decision-ready document
- compare proposal options or packaging
- rewrite a weak or confusing proposal
- align a proposal with the buyer's goals and constraints

Also trigger when the user says things like:
- "Help me write a proposal"
- "I need to send an offer"
- "How should I structure this proposal"
- "Turn this into a client proposal"
- "Why is my proposal not converting"
- "I need pricing and scope explained clearly"

## Core Principle

A proposal should make the buyer feel:

- understood
- confident
- clear on what happens next

The proposal is not mainly about your service.
It is about the buyer's problem, the promised outcome, the logic of the solution,
the boundaries of the work, and the terms under which a decision feels safe.

## What This Skill Does

This skill helps:
- translate discovery into a structured offer
- define the problem, outcome, and proposed approach
- clarify scope, timeline, pricing, assumptions, and boundaries
- improve proposal logic and persuasiveness
- reduce ambiguity that creates delay or mistrust
- structure options when helpful
- move the reader toward a decision rather than passive review

## Default Outputs

Depending on the request, produce one or more of the following:

1. Proposal Draft  
A full proposal with sections, flow, and buyer-facing language.

2. Proposal Structure  
An outline showing what sections should exist and why.

3. Offer Framing  
A clearer articulation of problem, value, outcome, and fit.

4. Scope and Pricing Model  
A structured explanation of deliverables, assumptions, options, and fees.

5. Proposal Audit  
A diagnosis of why an existing proposal feels weak, unclear, or low-converting.

6. Decision Version  
A simplified proposal optimized for quick stakeholder review and approval.

## Response Rules

When responding:
- start from the buyer's goals, not the seller's features
- define the problem before presenting the solution
- connect deliverables to outcomes
- make scope and exclusions explicit
- reduce ambiguity around timeline, pricing, and responsibility
- use options only when they clarify rather than confuse
- distinguish confidence from hype
- end with a clear decision path

## Proposal Architecture
~~~python
PROPOSAL_ARCHITECTURE = {
  "core_elements": {
    "context": "What the buyer is dealing with and why this matters now",
    "goal": "What outcome the buyer wants",
    "approach": "How the proposed work addresses the goal",
    "scope": "What is included and what is not",
    "timeline": "When major steps and outcomes happen",
    "pricing": "How the work is priced and why",
    "terms": "What assumptions, responsibilities, and conditions apply",
    "decision_path": "What the buyer should do next"
  },
  "guiding_questions": [
    "What problem is the buyer trying to solve",
    "Why now",
    "What does success look like",
    "Why this approach over alternatives",
    "What uncertainty could block approval",
    "What part of the proposal is most likely to create hesitation"
  ]
}
~~~

## Proposal Workflow
~~~python
PROPOSAL_WORKFLOW = {
  "step_1_extract_buying_context": {
    "purpose": "Clarify what decision the proposal is supporting",
    "outputs": [
      "buyer goal",
      "pain point",
      "urgency",
      "stakeholders",
      "constraints"
    ]
  },
  "step_2_define_offer": {
    "purpose": "Translate need into a concrete solution shape",
    "outputs": [
      "recommended approach",
      "deliverables",
      "work phases",
      "client responsibilities",
      "assumptions"
    ]
  },
  "step_3_define_boundaries": {
    "purpose": "Prevent later ambiguity",
    "outputs": [
      "included items",
      "excluded items",
      "change logic",
      "approval points",
      "dependency risks"
    ]
  },
  "step_4_price_and_package": {
    "purpose": "Present the commercial logic clearly",
    "outputs": [
      "fee structure",
      "payment terms",
      "option tiers if useful",
      "rationale for pricing"
    ]
  },
  "step_5_reduce_friction": {
    "purpose": "Address what may slow or block a yes",
    "methods": [
      "clarify process",
      "remove jargon",
      "answer obvious objections",
      "make next steps simple",
      "show credibility without overloading"
    ]
  },
  "step_6_close_cleanly": {
    "purpose": "Make the decision path explicit",
    "outputs": [
      "decision options",
      "acceptance step",
      "timeline to start",
      "what happens after approval"
    ]
  }
}
~~~

## Common Proposal Types
~~~python
PROPOSAL_TYPES = {
  "service_proposal": {
    "use_when": "Selling a defined service engagement",
    "focus": ["problem", "scope", "timeline", "pricing", "deliverables", "working model"]
  },
  "project_proposal": {
    "use_when": "Proposing a project with phases and milestones",
    "focus": ["objectives", "phases", "dependencies", "ownership", "success criteria"]
  },
  "partnership_proposal": {
    "use_when": "Exploring a strategic or commercial collaboration",
    "focus": ["shared value", "roles", "economics", "coordination model", "risk"]
  },
  "internal_proposal": {
    "use_when": "Seeking approval from internal stakeholders",
    "focus": ["business case", "cost", "impact", "tradeoffs", "decision ask"]
  },
  "retainer_proposal": {
    "use_when": "Structuring ongoing work over time",
    "focus": ["scope rhythm", "capacity", "reporting", "responsiveness", "renewal logic"]
  }
}
~~~

## Proposal Logic
~~~python
PROPOSAL_LOGIC = {
  "principles": [
    "The buyer cares more about outcome than activity",
    "Specificity builds confidence",
    "Unclear scope creates slow decisions",
    "Every proposal implies a risk allocation",
    "The document should match the buyer's attention span and decision style",
    "More pages do not equal more persuasion"
  ],
  "common_failures": [
    "Too much about the seller",
    "No clear problem framing",
    "Deliverables disconnected from business value",
    "Scope hidden in vague language",
    "Pricing presented without logic",
    "No clear call to decision",
    "Trying to impress instead of clarify"
  ],
  "corrections": [
    "Lead with the buyer's objective",
    "Show why the approach fits",
    "Tie work to outcomes and constraints",
    "Define scope and exclusions clearly",
    "Make decision steps obvious",
    "Reduce unnecessary complexity"
  ]
}
~~~

## Proposal Output Format

### Proposal Summary
- Buyer or Stakeholder:
- Goal:
- Problem or Opportunity:
- Recommended Approach:
- Scope:
- Timeline:
- Pricing or Commercial Structure:
- Key Assumptions:
- Risks or Open Questions:
- Recommended Next Step:

## Boundaries

This skill helps structure and improve proposals, offers, and decision documents.

It does not replace legal, tax, financial, procurement, or contract advice.
For regulated, high-value, or high-risk deals, outputs should be reviewed against the
user's jurisdiction, internal policies, and formal agreements.

## Quality Check Before Delivering

- [ ] The buyer's goal is clearly stated
- [ ] The proposal explains why this approach fits
- [ ] Scope and exclusions are explicit
- [ ] Timeline and pricing are understandable
- [ ] Assumptions and responsibilities are visible
- [ ] The proposal supports a decision, not just a read-through
- [ ] The next step is concrete
