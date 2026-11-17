## Description:

Use this skill to read, create, update, and delete data in Memos through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Memos through an OOMOL-connected account can retrieve memos, attachments, and user information, and create, update, or delete memos and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The oo CLI's documented startup synchronization can make lasting changes to other agent skill directories.

Mitigation: Review the CLI setup and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to disable synchronization. Use a reviewed CLI release and approve exact changes or deletions.

Risk: Installer contents and hosted connector behavior remain unverified.

Mitigation: Use a reviewed CLI release and connect only the intended Memos account.

## Reference(s):

- [Memos](https://usememos.com)
- [Memos API documentation](https://usememos.com/docs/api/latest)
- [oo CLI command and environment variable reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON action responses and text or Markdown memo content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs use JSON payloads shaped to each action's live schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
