## Description:

Searches and reads Leiga issues, projects, and schemas through a connected Leiga account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Leiga users and teams can retrieve issue details, project information, and project-specific issue schemas using natural-language requests. The skill provides oo CLI commands for these read operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI installation and the delivered CLI release were not verified; startup may also change other agent skill files.

Mitigation: Review and verify the CLI installation before allowing automatic setup. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI to prevent startup writes to agent skill directories.

Risk: The connected Leiga account is accessed through OOMOL.

Mitigation: Confirm the connected account and access are appropriate before running the skill.

## Reference(s):

- [Leiga](https://www.leiga.com/)
- [Leiga API documentation](https://share.apidog.com/apidoc/shared-5a741107-c211-410f-880c-048d1917c984)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only issue, project, and schema retrieval; results depend on the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
