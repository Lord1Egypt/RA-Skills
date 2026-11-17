## Description:

Use when user input is vague, underspecified, lacks boundaries or acceptance criteria, or would benefit from being reframed into a more executable prompt before work begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lq434239](https://clawhub.ai/user/lq434239)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn vague or underspecified requests into clear, actionable, verifiable prompts before execution. It is useful when a task needs explicit goals, boundaries, output format, or acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-applying a rewritten prompt could proceed with wording the user did not intend.

Mitigation: Use explicit instructions such as 'show me the refined prompt first' or 'do not refine this' when the confirmation flow matters.

## Reference(s):

- [Prompt Refinement Patterns](references/prompt-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/lq434239/skills/prompt-refiner)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text prompt refinement with optional confirmation choice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user to choose between the refined and original prompt before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
