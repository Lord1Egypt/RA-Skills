## Description:

Provides read-only Huawei Cloud CDN query guidance and command templates for domain settings, traffic statistics, task history, logs, and account information using hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CDN operators and developers use this skill to select and run read-only Huawei Cloud CDN queries, inspect domain configuration and performance, and retrieve logs or reports when a more specific CDN skill does not apply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDN queries use the agent's configured cloud identity and may reveal sensitive account or domain information.

Mitigation: Grant least-privilege IAM access, review commands before execution, and never paste access keys or secrets into chat.

Risk: Downloaded CDN logs and exported reports may contain client IPs, URLs, referers, and user-agent data.

Mitigation: Treat retrieved logs and reports as sensitive and restrict their access and sharing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cdn-universal-query)
- [CDN domain management API reference](artifact/references/api-domain-management.md)
- [CDN statistics API reference](artifact/references/api-statistics.md)
- [CDN logs and exports API reference](artifact/references/api-refresh-log-export.md)
- [CDN templates, rules, tags, and account API reference](artifact/references/api-template-rule-tag-account.md)
- [CDN read-only operation boundaries](artifact/references/prohibited-operations.md)
- [CDN IAM policies](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline hcloud commands and summarized query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports metrics with units, time ranges, and source commands; excludes credentials and other tenants' data.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
