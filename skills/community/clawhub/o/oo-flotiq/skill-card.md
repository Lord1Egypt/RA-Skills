## Description:

Flotiq (flotiq.com). Use this skill for ANY Flotiq request — reading, creating, updating, and deleting data. Whenever a task involves Flotiq, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage Flotiq content and content type data through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified downloaded installers, and the hosted connector implementation has not been verified.

Mitigation: Review and explicitly approve CLI installation; prefer a verified fixed release and review or disable automatic skill synchronization.

Risk: The connected account can be used to change or delete Flotiq data.

Mitigation: Preserve the skill's confirmation requirements for write and destructive actions.

## Reference(s):

- [Flotiq](https://flotiq.com/)
- [Flotiq API documentation](https://flotiq.com/docs/API/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Flotiq ClawHub release](https://clawhub.ai/oomol/skills/oo-flotiq)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON payloads and API responses, with oo CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use live Flotiq schemas; write and delete actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
