# Action-Reaction-Gap

## Purpose

This file defines the dramatic engine used by the skill.

A story does not move because information is presented.
A story moves because someone acts, the world responds, and the response is not what was expected.

This gap between expectation and reality is the engine of narrative.

## Core Chain

the skill should use the following chain:

```text
Desire
→ Action
→ Expected Reaction
→ Actual Reaction
→ Gap
→ New Information
→ Value Shift
→ Next Action
```

## Field Definitions

### Desire

What the protagonist wants.

Examples:

```text
make a reliable decision
enter a new market
explain a hard concept
use AI safely
convince a skeptical audience
avoid costly mistakes
```

### Action

What the protagonist does to get the desired value.

Examples:

```text
uses AI directly
writes a pitch
runs a test
talks to customers
launches a product
trusts a report
asks for a summary
```

### Expected Reaction

What the protagonist expects the world to do.

Examples:

```text
the answer will be correct
the customer will understand
the market will respond
the audience will be convinced
the tool will save time
```

### Actual Reaction

What the world actually does.

Examples:

```text
the answer sounds fluent but contains hidden errors
the audience understands the words but not the point
the customer asks a different question
the market blocks adoption through hidden constraints
the tool creates new review burden
```

### Gap

The gap is the difference between expected and actual reaction.
This is where meaning appears.

Examples:

```text
The team expected speed, but got unreviewable output.
The founder expected interest, but got confusion.
The reader expected explanation, but got jargon.
The buyer expected value, but found risk.
```

### New Information

The gap should reveal something.

Examples:

```text
The real problem was not writing quality, but trust.
The real audience barrier was not intelligence, but entry point.
The real market risk was not demand, but adoption friction.
```

### Value Shift

The gap should change the value state.

Examples:

```text
confidence → caution
confusion → clarity
speed → control
surface quality → real reliability
```

## Gap Rule

No gap, no story.

If the output has no expectation-reality gap, it is probably only an explanation, list, or claim.

the skill should not force drama where no gap exists, but it should actively check whether a meaningful gap is present.

## Common Gap Types

```text
knowledge gap
trust gap
adoption gap
execution gap
evidence gap
audience gap
market gap
technical gap
ethical gap
```

## Runtime Fields

the skill should internally produce:

```yaml
action_reaction_gap:
 desire:
 protagonist_action:
 expected_reaction:
 actual_reaction:
 gap:
 new_information:
 value_shift:
 next_action:
```

## Failure Modes

Fail if:

1. The protagonist does nothing.
2. The world does not react.
3. The reaction is exactly as expected.
4. The gap reveals no new information.
5. The value state does not change.
6. The text becomes a linear explanation with no tension.
7. The gap is exaggerated beyond the source material.

## Rewrite Rule

If no gap is visible, rewrite by asking:

```text
What did the protagonist assume?
What did reality reveal instead?
What changed after that discovery?
```

Then rebuild the output around that discovery.

## Final Rule

the skill should not merely describe what something is.
It should explain what changed when someone tried to use it in the real world.
