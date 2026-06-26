# Questioning Techniques Reference

Use these methods throughout all interview phases. Do not default to surface-level yes/no questions.

## Socratic Clarification

- "What do you mean by [term]?"
- "Could you give me a concrete example of that?"
- "How would you explain this to someone with no context?"

## Perspective Shifting

- "What would [a skeptical stakeholder] say about this?"
- "If a competitor copied this tomorrow, what would they get wrong?"
- "If this fails, what will the post-mortem say was the reason?"

## Evidence Probing

Shift the conversation from belief to proof:

- "What data or experience supports that?"
- "What is the unit of measurement for this success?"
- "Have you seen this approach work elsewhere? What was different?"

## Laddering (Attribute-Consequence-Value)

Use when you need to connect a concrete feature to the business value it serves. Ask "Why is this important?" repeatedly to climb the chain:

1. **Attribute:** The concrete feature or characteristic. ("We need automated data validation.")
2. **Consequence:** The functional outcome it produces. ("It reduces manual error-correction time.")
3. **Value:** The core business or human goal it serves. ("It gives us confidence in strategic decision-making.")

If the user states an attribute, ladder up to the value. If the user states a value, ladder down to the required attributes.

## Case Comparison

When the user struggles to articulate requirements directly, ask them to compare cases:

- "How is this different from [existing system / competitor / previous attempt]?"
- "What would make this better than that?"

Use the distinctions to extract concrete requirements the user could not state abstractly.

## Inversion (Munger)

Approach problems from the opposite direction. Instead of asking "How do we succeed?", ask "What would guarantee failure?" and systematically avoid those conditions.

**Pre-Mortem technique:**
1. Ask the team to imagine a future where the project has already failed spectacularly.
2. Each person independently lists reasons for the failure.
3. Work backward from each failure scenario to identify root causes: silent degradation, dependency failures, single points of failure, untested assumptions.
4. Convert each failure cause into a concrete mitigation or monitoring plan.

**Interdisciplinary Blind-Spot Check:**
Screen decisions against common failure patterns across disciplines:
- **Psychology:** Sunk cost fallacy, anchoring bias, groupthink, confirmation bias, overconfidence
- **Economics:** Perverse incentives, hidden costs, principal-agent problems, externalities
- **Organizations:** Diffusion of responsibility, information silos, Conway's Law, zombie stakeholders

Key question: "What predictable human error or bias could sabotage this plan, and what structural safeguard prevents it?"

## Steelmanning (Rapoport's Rules)

Before critiquing any position, construct the strongest possible version of it. Follow these steps in strict order:

1. **Paraphrase with clarity:** Re-express the other person's position so clearly that they say, "Thanks, I wish I'd thought of putting it that way."
2. **Identify agreement:** Explicitly list any points on which you agree.
3. **Mention learnings:** State anything you have genuinely learned from the conversation.
4. **Critique the strongest version:** Only after completing steps 1-3 are you permitted to offer a critique or alternative.

**Principle of Charity:** Always find the most reasonable interpretation of the user's words. Attribute to them the most coherent and defensible version of their view. This transforms confrontational probing into collaborative discovery where both parties refine their views to reach a more robust outcome.

## Five Whys

For every major requirement, ask "why" iteratively until you reach the root cause:

1. Why do you need this? (surface request)
2. Why is that a problem? (chain of events)
3. Why did that occur? (process inefficiency)
4. Why does the process allow it? (systemic bottleneck)
5. Why hasn't it been fixed? (root cause)

## Assumption Probing

Challenge each stated assumption:

- "What could we assume instead?"
- "How would you verify that assumption before building?"
- "What happens if this assumption turns out to be wrong?"

## Implication Mapping

For each decision:

- "What are the consequences of this choice?"
- "What doors does this close?"
- "What second-order effects should we anticipate?"

## Think in Models

While interviewing, mentally map responses to structured output. This helps you identify gaps in real time:

- **User Story:** "Who is this for?" and "Why is it valuable?" -- if either is missing, ask.
- **Process Flow:** "Is this step always true 100% of the time?" -- surfaces edge cases and parallel paths.
- **Context Map:** "Where does this data come from and where does it go?" -- reveals integration boundaries.
- **Acceptance Criteria:** "What happens when this is NOT true?" -- defines negative scenarios and error handling.

If you notice a gap in the model forming in your head, that gap is your next question.
