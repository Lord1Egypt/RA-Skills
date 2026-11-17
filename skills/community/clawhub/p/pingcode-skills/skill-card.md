## Description:

PingCode integrates with the PingCode R&D management API to query work items, generate weekly reports, and manage project progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anytao](https://clawhub.ai/user/anytao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to retrieve PingCode tasks and project work items, generate project status reports, and update work-item ownership, dates, status, or priority through PingCode Open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles PingCode client credentials and project data.

Mitigation: Install only in trusted environments, limit PingCode application scopes, keep credentials in environment variables, and avoid proxies or logging systems that may record request URLs.

Risk: The work-item update script can change remote project data without an interactive confirmation step.

Mitigation: Review command arguments and PingCode permissions before running update commands, and prefer tightly scoped credentials for write access.

Risk: Abbreviated work-item IDs may resolve ambiguously.

Mitigation: Use full work-item IDs where possible and verify the resolved item before applying ownership, date, status, or priority changes.

## Reference(s):

- [PingCode API reference](artifact/references/api_docs.md)
- [PingCode Open API documentation](https://open.pingcode.com/)
- [ClawHub PingCode skill page](https://clawhub.ai/anytao/skills/pingcode-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Terminal text, optional JSON output, and Markdown weekly reports from Python CLI scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PINGCODE_CLIENT_ID and PINGCODE_CLIENT_SECRET environment variables; update operations depend on PingCode API permissions.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
