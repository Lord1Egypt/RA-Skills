## Description:

Shotstack (shotstack.io). Use this skill for ANY Shotstack request — reading, creating, and updating data. Whenever a task involves Shotstack, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill through an OOMOL-connected account to check Shotstack render status and submit video, image, or audio edits for rendering. Review each render payload and its expected charges before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can trigger execution of an unverified remote CLI installer without separate approval.

Mitigation: Review and install the required CLI yourself, and require explicit approval before executing any installer.

Risk: OOMOL mediates the Shotstack connection and submitted render data, and render requests may incur charges.

Mitigation: Verify the account permissions and review each render payload and its expected charges.

## Reference(s):

- [Shotstack API documentation](https://shotstack.io/docs/api/)
- [Shotstack](https://shotstack.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and text render status or output URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Render submissions are asynchronous and return a render ID.]

## Skill Version(s):

1.0.4 (source: frontmatter; release evidence agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
