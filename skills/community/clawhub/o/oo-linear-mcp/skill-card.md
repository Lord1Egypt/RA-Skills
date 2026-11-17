## Description:

Use the OOMOL-connected Linear MCP to read, create, and update Linear workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect Linear workspaces and manage issues, comments, projects, teams, labels, and workflow statuses through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs execution of downloaded CLI installation code without a separate approval step.

Mitigation: Review and approve the installer separately, use a reviewed fixed release, and grant only the Linear permissions needed.

Risk: Creating or updating issues and comments changes Linear workspace data.

Mitigation: Confirm the exact payload and its effect before running a write action.

## Reference(s):

- [Linear MCP documentation](https://linear.app/docs/mcp)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API responses, JSON, Text]

**Output Format:** [Structured JSON results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include reads and workspace changes; write actions require confirmation.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
