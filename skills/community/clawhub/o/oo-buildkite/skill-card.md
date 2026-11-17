## Description:

Use this skill for Buildkite requests to inspect organizations, pipelines, and builds, or to create, rebuild, or cancel builds through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect Buildkite organizations, pipelines, and builds, and to create, rebuild, or cancel builds through an OOMOL-connected account. It requires checking the action schema first and confirming state-changing actions as described by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified code, and startup synchronization can make lasting changes to other agents’ skills.

Mitigation: Review setup before installing, use a verified CLI release, grant only necessary Buildkite permissions, and set OO_SKILLS_SYNC_DISABLED if cross-agent skill changes should be disabled.

Risk: Creating, rebuilding, or canceling a Buildkite build changes project state.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval before destructive actions.

## Reference(s):

- [Buildkite](https://buildkite.com)
- [Buildkite REST API documentation](https://buildkite.com/docs/apis/rest-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Buildkite read and write action results; state-changing actions require confirmation as described by the skill.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
