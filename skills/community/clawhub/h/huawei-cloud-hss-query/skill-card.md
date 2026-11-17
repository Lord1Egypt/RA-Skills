## Description:

Query Huawei Cloud HSS to inspect host assets, vulnerabilities, security baselines, intrusion alerts, login activity, and risk scores, and to update alert and vulnerability status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Security operators use this skill to review Huawei Cloud host health, vulnerabilities, security baselines, intrusion alerts, and login activity, then summarize risks and recommendations. It also supports alert and vulnerability status changes when the user confirms the specific action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes vulnerability repair and lasting alert-suppression changes beyond routine inspection and alert status handling.

Mitigation: Use the query-only IAM policy by default. Enable write permissions only for an explicitly requested change, and explain the exact targets, consequences, and rollback before asking for confirmation.

Risk: The skill requires an authenticated hcloud CLI and provides an installer command.

Mitigation: Configure credentials yourself, use least-privilege access, and review and verify the CLI installer before running it.

## Reference(s):

- [hcloud CLI installation and authentication](references/cli-installation-guide.md)
- [Least-privilege HSS IAM policies](references/iam-policies.md)
- [HSS event class reference](references/hss-event-class-reference.md)
- [Verification method](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Security analysis and guidance]

**Output Format:** [hcloud CLI commands, JSON query results, and Markdown inspection summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries are scoped by Huawei Cloud region and project; status changes require user confirmation.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
