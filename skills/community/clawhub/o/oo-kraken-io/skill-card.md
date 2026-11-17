## Description:

Kraken.io (kraken.io). Use this skill for ANY Kraken.io request — reading, creating, and updating data. Whenever a task involves Kraken.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can check a Kraken.io account's plan status and optimize an image through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup may install additional agent skills without clearly seeking approval.

Mitigation: Review and approve CLI installation separately, inspect which skills it adds, and disable unwanted startup synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Images submitted for optimization are processed by OOMOL and Kraken.io.

Mitigation: Confirm that the image can be shared with both providers before uploading it.

Risk: The exact remote installer and hosted connector behavior were not verified in the security review.

Mitigation: Review the installer and connector before allowing automatic setup or sending image data.

## Reference(s):

- [Kraken.io API documentation](https://kraken.io/docs/getting-started)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Kraken.io](https://kraken.io)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-kraken-io)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results with concise text guidance and oo CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One connector action per request; image optimization results may be stored in connector transit.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
