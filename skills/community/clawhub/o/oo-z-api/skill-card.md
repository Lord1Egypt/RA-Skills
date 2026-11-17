## Description:

Use Z-API to check status and send text, images, or locations through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to check a connected Z-API instance and send WhatsApp text, images, or locations through the OOMOL connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup and skill synchronization can execute unverified installation code and make broader changes to an agent environment.

Mitigation: Review the CLI installation separately, decide whether to allow setup and synchronization, and consult the oo CLI command reference for available controls.

Risk: Z-API requests pass through OOMOL, and messaging actions can send content to WhatsApp contacts or groups.

Mitigation: Confirm the intended recipient and exact message, image, or location payload before running a write action, and account for OOMOL handling the request.

## Reference(s):

- [Z-API API Reference](https://developer.z-api.io/en/api-reference/introduction)
- [Z-API website](https://www.z-api.io)
- [oo CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON connector requests and responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions send messages or locations and require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
