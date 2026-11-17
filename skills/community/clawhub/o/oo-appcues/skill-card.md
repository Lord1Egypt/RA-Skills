## Description:

Use this skill to read, create, update, and delete Appcues data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users managing an Appcues account can retrieve flows and tags, and publish or unpublish flows through the OOMOL-connected Appcues service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup leaves remote code execution and persistent changes to installed agent skills insufficiently controlled.

Mitigation: Review the CLI installation separately, use a reviewed release, and check or disable automatic skill synchronization with the publisher's documented control before running it.

Risk: Publishing or unpublishing a flow changes Appcues account state.

Mitigation: Keep the skill's explicit approval step and confirm the target and intended effect before running either action.

## Reference(s):

- [Appcues skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-appcues)
- [Appcues](https://www.appcues.com)
- [Appcues public API documentation](https://docs.appcues.com/en_US/dev-api-data/appcues-public-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that publish or unpublish flows change Appcues state and require explicit user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
