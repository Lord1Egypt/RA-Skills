## Description:

Searches and reads Chuhaijiang data through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search Chuhaijiang and retrieve TikTok Shop product, creator, live stream, review, and video data through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup path runs downloaded installer code without verifying its contents or clearly requiring approval.

Mitigation: Install a verified oo CLI release yourself and require approval before running installers. Disable automatic skill synchronization if you want agent configuration changes under your control.

## Reference(s):

- [Chuhaijiang homepage](https://www.chuhaijiang.com/)
- [Chuhaijiang API documentation](https://openapi-doc.chuhaijiang.com/introduction)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Retrieved data, Guidance]

**Output Format:** [CLI commands with JSON input and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are built from the connector action schema; responses include retrieved Chuhaijiang data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
