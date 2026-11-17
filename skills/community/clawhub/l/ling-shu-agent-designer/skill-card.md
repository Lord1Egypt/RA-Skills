## Description:

Ling Shu Agent Designer helps users turn business requirements into OpenClaw agent plans, workspace skeletons, configuration, and dedicated skill packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business teams use this skill to design industry-specific agents through requirement clarification, scenario outlines, basic agent skeleton creation, and iterative skill-package updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent plans and skeletons may encode incorrect business requirements, approval boundaries, or data-flow assumptions.

Mitigation: Review the seven planning documents, security guardrails, and human approval rules before creating or deploying an agent.

Risk: Generated API or database configuration may affect real business systems if approved without checking scopes and data access.

Mitigation: Validate integrations, permissions, credentials, and data-handling rules with the system owner before connecting production services.

Risk: Generated skill packages or publishing steps may include sensitive business context.

Mitigation: Review and scan generated packages before publication, especially when they describe internal workflows or customer data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce planning documents, OpenClaw configuration, workspace skeleton files, and dedicated skill package content.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
