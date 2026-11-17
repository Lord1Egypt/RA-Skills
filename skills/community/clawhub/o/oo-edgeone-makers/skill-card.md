## Description:

Manage EdgeOne Makers projects, deployments, and environment variables through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project operators use this skill to inspect and manage EdgeOne Makers projects, deployments, and environment variables through the connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation process and remote installer contents have not been verified.

Mitigation: Verify and install a fixed CLI release before use.

Risk: CLI invocations may make undisclosed changes to other agents’ skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 for CLI invocations if automatic skill changes are not wanted, and review any changes before relying on them.

Risk: Project operations may expose credentials or modify or delete project data.

Mitigation: Use limited project credentials and retain the required confirmations for write and destructive actions.

## Reference(s):

- [EdgeOne Pages API documentation](https://pages.edgeone.ai/document/overview)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [EdgeOne Pages](https://edgeone.ai/zh/products/pages)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read project data or request confirmation before writes and destructive changes.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
