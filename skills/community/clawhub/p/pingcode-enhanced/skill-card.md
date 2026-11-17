## Description:

Integrates with PingCode R&D management APIs to query work items, test libraries, project progress, organization data, wiki content, DevOps records, weekly reports, and dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geji](https://clawhub.ai/user/geji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to inspect and update PingCode project-management data, summarize weekly work, and generate operational views from their own PingCode workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles PingCode credentials and may expose token-request details through logs or command output.

Mitigation: Install with narrowly scoped PingCode credentials, prefer read-only permissions, avoid sharing logs that may include token-request URLs, and rotate credentials if exposure is suspected.

Risk: The documented update workflow can modify live work items without strong safeguards.

Mitigation: Avoid the update command unless updates are intentional, the work-item ID is fully verified, and the operator has confirmed the target record and requested changes.

## Reference(s):

- [PingCode Open API reference](references/api_docs.md)
- [PingCode Open API endpoint](https://open.pingcode.com)
- [ClawHub skill page](https://clawhub.ai/geji/skills/pingcode-enhanced)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Console text, JSON output, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PINGCODE_CLIENT_ID and PINGCODE_CLIENT_SECRET environment variables.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
