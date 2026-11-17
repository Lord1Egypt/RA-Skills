## Description:

Use this skill to read Holded contacts and products and create contacts through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read Holded contacts and products, and to create contacts through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may install or refresh skills across agent apps without making those effects clear.

Mitigation: Review and preinstall a trusted CLI version, and set OO_SKILLS_SYNC_DISABLED=1 for every oo invocation unless cross-agent skill management is intended.

Risk: Holded actions can access connected account data, and creating a contact changes account state.

Mitigation: Approve each proposed write and confirm its exact payload and effect before running it.

## Reference(s):

- [Holded](https://www.holded.com)
- [Holded API documentation](https://www.holded.com/developers/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses with shell commands and concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read contacts and products or create contacts; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
