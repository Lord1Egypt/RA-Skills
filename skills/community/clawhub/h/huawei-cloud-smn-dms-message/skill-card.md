## Description:

Manage Huawei Cloud SMN topics, subscriptions, message templates, and publishing, plus DMS Kafka, RabbitMQ, and RocketMQ instances through KooCLI-backed actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect, create, diagnose, publish to, and delete Huawei Cloud SMN and DMS messaging resources. It supports read-only queries as well as resource-changing actions that can create cost, send notifications, or delete cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage real Huawei Cloud messaging resources, including actions that create cost, send notifications, or delete resources.

Mitigation: Use least-privilege Huawei Cloud credentials and do not allow R2 or R1 actions unless the exact command has been previewed and explicitly approved.

Risk: The skill installs reporting tooling under the user account and sends execution-quality metadata.

Mitigation: Verify KooCLI and skill-quality-cli provenance before use; set SKILL_QUALITY_DISABLE=1 if reporting is not acceptable.

Risk: Cloud authentication material may be exposed if users paste AK/SK credentials into chat or commands.

Mitigation: Use a configured KooCLI profile or out-of-band environment variables, and never print, echo, or hardcode AK/SK values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-smn-dms-message)
- [KooCLI Installation & Authentication Guide](references/cli-installation-guide.md)
- [Engine & Operation Reference](references/engine-operation-reference.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [Security Audit Guide](references/security-audit-guide.md)
- [Huawei Cloud KooCLI install package](https://cn-north-4-hcli.obs.cn-north-4.myhuaweicloud.com/hcli_install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise execution summaries; Huawei Cloud command results may be JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Huawei Cloud KooCLI actions; resource-changing actions should be previewed and explicitly approved before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
