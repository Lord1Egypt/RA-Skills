## Description:

Queries Huawei Cloud RDS instance lists, instance details, and CPU, memory, and disk monitoring metrics through the Huawei Cloud SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud RDS inventory, retrieve instance configuration details, and review basic CPU, memory, and disk metrics for operations and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose infrastructure details such as RDS instance IDs, IP addresses, VPCs, subnets, security groups, and metrics.

Mitigation: Run it only with least-privileged Huawei Cloud IAM credentials and share outputs only with authorized operators.

Risk: The security guidance flags TLS verification, region validation, credential-variable selection, and dependency pinning as issues to fix before use with sensitive accounts.

Mitigation: Review and remediate those items before installing the skill in sensitive or production cloud environments.

Risk: The security verdict is suspicious due to review-worthy credential and cloud API connection handling.

Mitigation: Review the skill before installing and validate behavior in a controlled account before broader use.

## Reference(s):

- [Huawei Cloud RDS API Documentation](https://console.huaweicloud.com/apiexplorer/#/openapi/RDS/doc)
- [Huawei Cloud CES API Documentation](https://console.huaweicloud.com/apiexplorer/#/openapi/CES/doc)
- [Huawei Cloud SDK Center](https://console.huaweicloud.com/apiexplorer/#/sdkcenter)
- [IAM Policies](artifact/iam-policies.md)
- [Verification Method](artifact/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and shell commands; runtime commands return JSON or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill's runtime commands may return RDS instance IDs, IP addresses, VPCs, subnets, security groups, and monitoring metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
