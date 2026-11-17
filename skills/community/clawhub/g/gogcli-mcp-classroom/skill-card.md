## Description:

Use this skill to manage Google Classroom courses, rosters, coursework, submissions, announcements, topics, invitations, profiles, and authentication through gogcli-backed MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and administrators use this skill to let an agent help manage Google Classroom courses, participants, assignments, submissions, grading, announcements, topics, and invitations through an MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make high-impact Google Classroom account and course changes through an unpinned npm-run MCP server.

Mitigation: Trust and review the npm package and publisher, pin or review the package version where possible, use least-privileged Google accounts and scopes, and require explicit confirmation before destructive or administrative actions.

Risk: The escape-hatch command can reach Classroom functionality beyond the dedicated tool list.

Mitigation: Require explicit review and confirmation before using the escape hatch, especially for guardian, material, and assignee-management operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/gogcli-mcp-classroom)
- [gogcli](https://github.com/openclaw/gogcli)
- [gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and MCP tool actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or later, an installed and authenticated gogcli setup, and a configured Google account.]

## Skill Version(s):

2.8.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
