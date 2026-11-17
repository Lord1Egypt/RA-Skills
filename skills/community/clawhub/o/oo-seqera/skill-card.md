## Description:

Seqera (seqera.io). Use this skill for ANY Seqera request — reading, creating, and updating data. Whenever a task involves Seqera, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Seqera users and developers can retrieve profiles, workspaces, pipelines, and workflow runs, and launch workflows through their connected Seqera account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI installer code whose contents and exact release are unverified.

Mitigation: Use a reviewed, version-pinned oo CLI installation.

Risk: Startup skill synchronization can install skills into other agent apps.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if cross-agent skill changes are not wanted.

Risk: Seqera requests and credentials are routed through OOMOL.

Mitigation: Confirm that routing Seqera requests and credentials through OOMOL is acceptable before connecting the account.

## Reference(s):

- [Seqera Platform API documentation](https://docs.seqera.io/platform-api)
- [Seqera](https://seqera.io)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured Seqera data and concise text based on connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas; workflow launches are state-changing actions that require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
