## Description:

Use when managing secrets, credentials, encryption keys, certificates, or other sensitive data on Huawei Cloud with CSMS, KMS, and CTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud DEW secrets and encryption keys, diagnose rotation and usage, and perform approved key or secret rotation changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic quality reporting and session discovery can send sensitive cloud results and local agent-session identifiers beyond the requested task.

Mitigation: Set SKILL_QUALITY_REPORT=0 before invocation; use an isolated installation and request removal of automatic session discovery and unredacted reporting.

Risk: Key deletion and secret rotation can have lasting effects, including loss of access to encrypted data or stale credentials.

Mitigation: Use narrowly scoped IAM permissions and retain explicit approval for rotation and deletion; review deletion timing and consequences before confirming.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dew-key-management)
- [Huawei Cloud DEW documentation](https://support.huaweicloud.com/dew/)
- [Huawei Cloud DEW API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/DEW/doc)
- [KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [IAM policies](references/iam-policies.md)
- [CSMS usage guide](references/csms-usage.md)
- [KMS usage guide](references/kms-usage.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON summaries and readable Markdown reports, with Huawei Cloud CLI commands and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports secret and key metadata without secret values; write actions require explicit confirmation.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
