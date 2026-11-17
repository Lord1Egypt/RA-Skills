## Description:

Track questions Hans failed to answer and flag missing knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atiati82](https://clawhub.ai/user/atiati82)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent maintainers use this skill to log questions Hans cannot answer, summarize recurring knowledge gaps, and support later knowledge-base improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run a shell command using user question text.

Mitigation: Use the skill only when the logger is present and audited, and invoke it without shell interpolation.

Risk: Unanswered user questions may be stored in a persistent knowledge-gap log.

Mitigation: Add consent, redaction, retention limits, and access controls before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atiati82/skills/knowledge-gaps)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the agent to log unanswered questions and later summarize recurring gaps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
