## Description:

Higgsfield AI (higgsfield.ai). Use this skill for ANY Higgsfield AI request — reading, creating, updating, and deleting data. Whenever a task involves Higgsfield AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to submit image or video generation requests, check their status, or cancel queued requests in Higgsfield AI through a connected OOMOL account. The agent reads the live action schema first and obtains confirmation before generation or cancellation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup and automatic synchronization can make persistent changes to other agent skills without clearly explaining them.

Mitigation: Review the CLI release and synchronization behavior before setup; set OO_SKILLS_SYNC_DISABLED=1 for oo invocations if those changes are unwanted.

Risk: Generation requests may consume credit, and the remote installers and hosted service implementation are unverified.

Mitigation: Prefer a reviewed CLI release, check account credit before submitting generation requests, and review the connection and service behavior before enabling the integration.

Risk: Image and video generation change state, and cancellation affects a queued request.

Mitigation: Inspect the live action schema and confirm the exact payload and effect before submitting generation requests or cancelling a request.

## Reference(s):

- [Higgsfield AI](https://higgsfield.ai/)
- [Higgsfield API documentation](https://docs.higgsfield.ai/docs/how-to/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request payloads and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation and cancellation actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
