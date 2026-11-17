## Description:

Featurebase (featurebase.app). Use this skill for ANY Featurebase request — reading, creating, updating, and deleting data. Whenever a task involves Featurebase, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read Featurebase boards, posts, and contacts, and to create or update feedback and contact records through an OOMOL-connected account. The skill requires confirmation for writes and explicit approval for destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback CLI setup runs downloaded installer code without a separate approval step.

Mitigation: Review CLI installation separately and use a verified release before running the installer.

Risk: Write actions can change Featurebase records, and destructive actions can delete contacts or posts.

Mitigation: Confirm the exact payload and effect for writes, and require explicit approval for the target of destructive actions.

Risk: The oo CLI may automatically synchronize skills before first use.

Mitigation: Check the CLI command reference and configure OO_SKILLS_SYNC_DISABLED if synchronization should be disabled.

## Reference(s):

- [Featurebase REST API documentation](https://docs.featurebase.app/rest-api.md)
- [Featurebase homepage](https://www.featurebase.app/)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Text responses with oo CLI commands and JSON action payloads or results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results and fields depend on the selected Featurebase action.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
