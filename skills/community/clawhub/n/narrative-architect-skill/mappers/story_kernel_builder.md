# Story Kernel Builder

## Purpose

Extract the irreducible story kernel from raw material before any rendering or audience adaptation.

The Story Kernel is not a summary. It is the identification of the conflict structure that gives the material narrative force. Without a kernel, writing becomes explanation. With a kernel, writing becomes movement.

## Source

Based on Robert McKee's *Story*: the gap between expectation and result is the substance of story. The Story Kernel formalizes this for non-fiction and technical material.

## Required Output

```yaml
story_kernel:
  protagonist:
    label:          # who is acting (person, organization, system, idea)
    conscious_desire:  # what they say they want
    unconscious_desire: # what they actually need (may be same)
  forces_of_antagonism:
    - label:
      nature:       # internal / external-personal / external-impersonal
      power_gradient: # positive / negative / neutral (relative to protagonist)
  inciting_incident:
    event:          # what throws the protagonist's life out of balance
    time_zero:      # when the story clock starts
  progressive_complications:
    - label:
    - label:
  gap:
    expectation:   # what the protagonist expected to happen
    result:        # what actually happened
    gap_type:      # information gap / value gap / action gap / structural gap
  crisis_choice:
    irreconcilable_goods:  # two things the protagonist wants but cannot have both
    choice_made:
  climax:
    action:         # the irreversible action that resolves the crisis
    value_change:   # from what → to what
  controlling_idea_seed: # the emerging theme (value + cause)
```

## Extraction Rules

```text
Rule 1: Protagonist identification
Do not confuse the speaker with the protagonist.
The protagonist is whoever faces the irreducible choice.

Rule 2: Antagonistic forces
Every story has antagonistic forces.
If none are visible, the gap between expectation and result IS the antagonist.
Do not fabricate villains. Describe structural tensions.

Rule 3: Gap is mandatory
No gap, no story.
The gap between expectation and result is the minimum viable kernel.
If the material has no gap, flag it: "No narrative tension detected."

Rule 4: Crisis choice must be binary
The crisis is not "what should we do?"
The crisis is "two things we must have but cannot have both."
Irreconcilable goods, not a buffet of options.

Rule 5: Controlling idea emerges, not imposed
Do not write a moral before the story exists.
The controlling idea is discovered through the gap, not pasted on top.

Rule 6: This is internal
Do not expose the Story Kernel in output unless user asks for analysis.
```

## Failure Modes

Bad: treating a feature list as a story.
Fix: where is the gap? What was expected vs. what happened?

Bad: forcing a protagonist where there is none.
Fix: if no entity faces a binary choice, flag the material as "expository."

Bad: writing a controlling idea that is a slogan.
Fix: controlling idea = value charge + cause. "Justice prevails because the protagonist is smarter" not "good wins over evil."
