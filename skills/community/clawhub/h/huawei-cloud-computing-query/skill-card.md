## Description:

Queries Huawei Cloud ECS, BMS, IMS, Auto Scaling, and CCE resources, returning read-only inventory and details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and engineers use it to inspect Huawei Cloud compute resources, specifications, quotas, images, scaling configuration, and cluster inventories. It is limited to read-only queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports cloud password-retrieval features and IAM user-listing access.

Mitigation: Review those operations before use and limit credentials to the permissions required for the intended queries.

Risk: The security scan reports TLS and package-installation concerns, and notes that setup-script analysis is incomplete.

Mitigation: Verify TLS checks and package-mirror authentication, pin dependencies, and review setup scripts before installing or using the skill with cloud credentials.

## Reference(s):

- [Huawei Cloud skill release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-computing-query)
- [ECS Query Guide](references/ecs/guide.md)
- [BMS Query Guide](references/bms/guide.md)
- [IMS Query Guide](references/ims/guide.md)
- [AS Query Guide](references/as/guide.md)
- [CCE Query Guide](references/cce/guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [CLI Installation Guide and operation boundary](references/cli-installation-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown tables, text summaries, or JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resource details depend on the selected service, query, and fields.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
