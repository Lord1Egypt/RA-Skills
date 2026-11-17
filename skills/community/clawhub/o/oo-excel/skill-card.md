## Description:

Excel (microsoft.com). Use this skill for ANY Excel request — reading, creating, updating, and deleting data. Whenever a task involves Excel, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to read and manage Excel workbooks through their connected OOMOL account. It guides an agent in checking action schemas and submitting connector requests for workbook operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes a remote installer whose contents can change, and the installer and hosted connector implementation were not independently audited.

Mitigation: Review and approve a specific verified CLI release before use, and prevent unattended installer execution.

Risk: Setup may automatically install or synchronize other agent skills.

Mitigation: Check whether that behavior is acceptable before enabling it.

Risk: The connected Excel account can make workbook changes, including destructive operations.

Mitigation: Review connected-account permissions and approve only intended workbook changes.

## Reference(s):

- [Excel skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-excel)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel)
- [Microsoft Graph Excel API documentation](https://learn.microsoft.com/en-us/graph/api/resources/excel?view=graph-rest-1.0)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Guidance]

**Output Format:** [JSON connector requests and responses, workbook data or files, and concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workbook writes and destructive operations require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
