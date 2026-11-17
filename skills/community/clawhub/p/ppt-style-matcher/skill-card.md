## Description:

PPT Style Matcher helps agents analyze an existing PowerPoint deck's colors, fonts, layout, and rhythm, then generate or revise slides that match that style with python-pptx validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation-focused agents use this skill to inspect a source PPTX, lock style parameters, create matching replacement or new slides, rebuild slide order, and run P0-P3 layout validation before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented global residual-keyword replacement can silently alter unrelated slide content across a whole deck.

Mitigation: Review the exact replacement map before running it, scope replacements to intended slides when possible, and inspect the output deck after validation.

Risk: The skill assumes Chinese presentation font and language conventions that may not fit non-Chinese decks.

Mitigation: Adjust font, East Asian font handling, and language assumptions before applying the workflow to non-Chinese presentations.

## Reference(s):

- [Design Patterns Reference](references/design-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/skills/ppt-style-matcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks; generated or modified PPTX files when applied]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses extracted deck style parameters and readback validation; may apply presentation-wide text replacement only when explicitly reviewed.]

## Skill Version(s):

4.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
