## Description:

Helps agents compare AI models, estimate usage costs, and optionally delegate approved tasks through OceanToken.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceantoken](https://clawhub.ai/user/oceantoken)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can compare model capabilities and prices, estimate costs, and, with user approval, send a defined task to another model for an answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegation sends user content to another model provider.

Mitigation: Get user approval, identify the receiving model and content before sending, and exclude secrets and private files.

Risk: Model usage may incur charges, and cost estimates may be uncertain.

Mitigation: Show estimate confidence and assumptions, check available balance, and monitor actual charges.

Risk: Delegated model answers may contain mistakes.

Mitigation: Review delegated answers before relying on them and disclose the other model's contribution.

## Reference(s):

- [OceanToken homepage](https://oceantoken.ai)
- [OceanToken Models ClawHub listing](https://clawhub.ai/oceantoken/skills/oceantoken-models)
- [OceanToken installation guide](https://github.com/NextFormAI/oceantoken-plugins#install)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with comparison tables, cost estimates, and optional setup commands or delegated answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates include confidence and assumptions; delegated answers may include usage and cost.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
