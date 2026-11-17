# Text quality diagnostics

This reference defines portable, configurable diagnostics. It never assumes a
genre, author, or language register. Project policies may promote an advisory
diagnostic to a gate; the built-in Core does not do so.

## Advisory checks

- Prefer concrete sensory detail where it improves the scene.
- Remove filler, repetitive explanations, and generic transition phrases.
- Keep exposition proportional to the reader's current need.
- Make dialogue carry intention, relationship, information asymmetry, or cost.
- Preserve each character's declared vocabulary, rhythm, and boundaries.
- Allow direct psychological narration when the scene requires it; showing and
  telling are tools, not mutually exclusive doctrines.

## Project-owned checks

Identity terms, world rules, taboo vocabulary, paragraph limits, and style
detectors belong in the project profile. They are not silently inherited from a
genre pack. A project may mark any detector as `warning` or `blocking`.

## Output contract

The checker writes JSON containing `rule_id`, `severity`, `blocking`, and
evidence locations. A warning is reported but never blocks delivery. A blocking
result only blocks when the project explicitly enabled that rule.
