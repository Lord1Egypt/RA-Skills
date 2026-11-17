## Description:

Raygun (raygun.com). Use this skill for ANY Raygun request — reading, creating, updating, and deleting data. Whenever a task involves Raygun, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Raygun applications, deployments, and error groups, and to create, update, or delete deployments through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to execute a downloaded oo CLI installer; the downloaded installer and installed CLI were not verified in this review.

Mitigation: Review and approve a verified oo CLI installation separately before using the skill.

Risk: Creating, updating, or deleting a deployment can change or remove Raygun data.

Mitigation: Confirm the exact payload and effect before write actions, and confirm the target with explicit approval before destructive actions.

## Reference(s):

- [Raygun](https://raygun.com)
- [Raygun API documentation](https://raygun.com/documentation/product-guides/raygun-api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Structured Raygun data and operational guidance returned as JSON through oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by action and connected account permissions.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
