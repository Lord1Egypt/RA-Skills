## Description:

Guided elicitation skill that activates only when the user explicitly types /interrogate, asks 4-15 adaptive questions in batches of 2, and clarifies vague or complex requests before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inxan3](https://clawhub.ai/user/inxan3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to turn vague or complex requests into clear requirements before the agent begins work. It is useful when the user wants structured clarification, trade-off discussion, and a confirmation summary before action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The clarification flow can add delay before the agent starts work.

Mitigation: Use the skill only when explicitly invoked with /interrogate and rely on its confirmation step before proceeding.

Risk: Multiple-choice options can narrow the user's framing if the available choices do not fit.

Mitigation: The skill explicitly permits free-text answers and instructs the agent to adapt naturally when the user ignores the lettered options.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown questions, option lists, summaries, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces adaptive clarification batches and a final confirmation summary before proceeding.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
