## Description:

Use this skill to manage or diagnose Huawei Cloud security groups, including querying groups and rules, analyzing connectivity and rule conflicts, auditing over-exposure, and creating, updating, or deleting groups and rules with previews and explicit confirmation for managed actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use the skill to inspect Huawei Cloud VPC security groups, diagnose port access, identify conflicting or over-exposed rules, and make approved rule or group changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports installation of an unrelated quality-reporting tool, automatic telemetry guidance, and possible inaccuracies in security-rule analysis; scan coverage was partial.

Mitigation: Review the quality CLI and its telemetry before installing it, and independently verify security-rule audit and diagnosis results, keeping the partial scan coverage in mind.

## Reference(s):

- [Huawei Cloud security group documentation](https://support.huaweicloud.com/usermanual-vpc/vpc_SecurityGroup_0001.html)
- [Huawei Cloud KooCLI installation and usage](https://support.huaweicloud.com/cli/index.html)
- [Huawei Cloud VPC API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/VPC/doc)
- [CLI parameters](artifact/references/cli-parameters.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Security group rule reference](artifact/references/sg-rule-reference.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Structured JSON results with readable summaries and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries and analysis; managed changes require preview and explicit user confirmation.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
