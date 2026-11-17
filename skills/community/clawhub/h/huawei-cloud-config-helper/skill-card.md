## Description:

Queries Huawei Cloud Config to inventory resources, inspect schemas, run resource SQL queries, and review built-in compliance rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud administrators use the skill to review Huawei Cloud resource inventories, configurations, schemas, SQL query results, and built-in compliance rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query results may contain sensitive cloud resource and configuration data, and the skill documents local caching without defining approval, storage protections, or cleanup.

Mitigation: Get user approval before saving results, use a private restricted location, and agree on a deletion period.

Risk: Cloud credentials and third-party SDK dependencies are needed for live queries.

Mitigation: Use dedicated read-only credentials, prefer temporary credentials, keep TLS verification enabled, and lock dependency versions before installation.

## Reference(s):

- [Huawei Cloud Config Helper on ClawHub](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-config-helper)
- [Knowledge Base](artifact/references/knowledge.md)
- [SQL Examples](artifact/references/sql-example.json)
- [Config Concepts](artifact/references/service/config.md)
- [Least-Privilege IAM Policies](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON query results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only resource and compliance data; results may contain sensitive cloud configuration details.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
