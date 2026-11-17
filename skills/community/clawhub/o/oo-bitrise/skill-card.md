## Description:

Bitrise (bitrise.io). Use this skill for ANY Bitrise request — reading, creating, and updating data. Whenever a task involves Bitrise, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Bitrise apps and builds and retrieve build details through an OOMOL-connected account. They can also trigger builds when the user confirms the action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run remote installer code whose behavior has not been verified.

Mitigation: Review setup, install a verified oo CLI version yourself, and review or disable automatic skill synchronization.

Risk: Connecting Bitrise authorizes OOMOL to mediate account operations, and triggered builds may consume resources.

Mitigation: Review the connection and build details, and keep the requirement to confirm the exact build action with the user.

## Reference(s):

- [Bitrise](https://bitrise.io)
- [Bitrise API documentation](https://docs.bitrise.io/en/bitrise-ci/api/api-overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured Bitrise action results with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read actions and user-confirmed build triggering.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
