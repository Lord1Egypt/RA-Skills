## Description:

This skill lets agents read and manage Qingflow records, forms, members, and workflows through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and authorized Qingflow workspace users use this skill to inspect apps, records, members, and workflows, and to create or update records or take workflow actions through a connected account. Write and destructive actions require confirmation before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback installation may execute unverified code and introduce broader agent changes.

Mitigation: Review and install a verified oo CLI release yourself, and check its automatic skill synchronization settings before use.

Risk: Connecting Qingflow allows OOMOL to process authorized business data.

Mitigation: Connect only an account authorized for the intended data and keep confirmation requirements for record and workflow changes.

## Reference(s):

- [Qingflow](https://qingflow.com/)
- [Qingflow API documentation](https://exiao.yuque.com/ixwxsb/bgzs0e)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands, JSON payloads, and action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the selected Qingflow action schema.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
