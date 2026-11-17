## Description:

Use the connected Glyphic account to search and read Glyphic data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Glyphic users use the skill to search calls, retrieve call content and media metadata, and read playbooks and tags through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to run remote CLI installers whose contents were not verified in the release evidence.

Mitigation: Review and approve CLI installation separately, and prefer a verified, fixed release before running an installer.

Risk: Connecting Glyphic permits OOMOL-mediated access to call content; the CLI may also synchronize agent skills automatically.

Mitigation: Review the connection and its access, and review or disable automatic agent-skill synchronization.

## Reference(s):

- [Glyphic API documentation](https://docs.glyphic.ai/articles/7806662155-glyphic-api)
- [Glyphic homepage](https://www.goairspeed.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON action results with returned call, transcript, playbook, or tag content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available content depends on the connected Glyphic account and the selected read action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
