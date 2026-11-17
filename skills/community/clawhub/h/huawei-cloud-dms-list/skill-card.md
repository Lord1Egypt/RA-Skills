## Description:

Lists Huawei Cloud DMS Kafka and RabbitMQ instances in a selected region, with filters, pagination, and names, table, or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect Kafka and RabbitMQ instance inventories in Huawei Cloud, apply server-side filters, and retrieve instance IDs for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs a telemetry component, and the available security evidence does not establish what it sends or where.

Mitigation: Review the telemetry component before installation. Prefer a release that makes installation and execution optional, documents its data flow, and authenticates a pinned release independently; use an isolated environment, credentials limited to dms:instance:list, and trusted executable configuration.

## Reference(s):

- [Verification Method](artifact/references/verification-method.md)
- [KooCLI Installation & Credential Guide](artifact/references/cli-installation-guide.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Instance names or a full-field table as text, or the raw instance array as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Kafka and RabbitMQ, region and project selection, server-side filters, and pagination.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
