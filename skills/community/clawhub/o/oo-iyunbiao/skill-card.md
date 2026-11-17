## Description:

Yunbiao (iyunbiao.com). Use this skill for ANY Yunbiao request — reading, creating, updating, and deleting data. Whenever a task involves Yunbiao, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to read and manage Yunbiao business data through an OOMOL-connected account, including forms, users, roles, attachments, and templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback runs a remote CLI installer without a separate approval step or integrity check.

Mitigation: Review and approve CLI installation separately, preferably using a pinned, verified release, before allowing the fallback to run.

Risk: Yunbiao actions can create, update, or delete business data and account records.

Mitigation: Connect only the Yunbiao account and permissions needed, and retain the required approvals for business-data and account changes.

## Reference(s):

- [Yunbiao OpenAPI documentation](https://docs.iyunbiao.com/openAPI/1)
- [Yunbiao](https://www.iyunbiao.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Connector commands with JSON payloads and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Yunbiao account and available server features.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
