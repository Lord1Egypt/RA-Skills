## Description:

Makes this agent a Maintainer in an MPAS multi-party approval workflow. It independently reviews high-impact MCP tool calls proposed by other agents, meaning calls for which policy requires additional Approvals, and approves or rejects each one through MPAS signer tools: an independent check before a proposing agent's call executes. Changes agent behavior by design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oma3](https://clawhub.ai/user/oma3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to independently review high-impact Actions proposed by other agents, then approve or reject the exact reviewed Action through a configured MPAS signer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving an Action can trigger immediate execution, including consequential or irreversible operations.

Mitigation: Review the complete exact Action, verify it against user intent and policy, and approve only when its execution is intended.

Risk: An agent assigned the Maintainer role with excessive signer permissions could approve Actions beyond its intended scope.

Mitigation: Assign this role only to an intended approver and restrict signer permissions to appropriate resources.

## Reference(s):

- [MPAS project](https://github.com/oma3dao/mpas)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance]

**Output Format:** [Text decisions and rationale submitted through configured MPAS signer tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decisions apply to the exact reviewed Action; submission acceptance must be confirmed.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
