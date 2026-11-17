## Description:

OAISR helps an agent produce bilingual occupational AI displacement risk assessments for named professions using a four-step exposure-estimation workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silent404](https://clawhub.ai/user/silent404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to ask for a job title or occupation and receive a concise risk analysis that separates theoretical AI exposure from observed practical exposure. The skill is intended for methodology-based estimates, not guaranteed source data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate on simple profession mentions, which may produce an assessment when the user expected a narrower answer.

Mitigation: Confirm the user wants an AI displacement or exposure assessment when the surrounding context is ambiguous.

Risk: Numeric exposure values are methodology-based estimates and may be mistaken for guaranteed source data.

Mitigation: Label each estimate as sourced, analogized, or heuristic, and include the stated confidence level and scope.

## Reference(s):

- [OAISR reference notes](references/README.md)
- [Anthropic: Labor market impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with progress bars, tables, estimates, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include methodology-based numeric estimates and confidence labels; estimates should disclose whether values are sourced, analogized, or heuristic.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
