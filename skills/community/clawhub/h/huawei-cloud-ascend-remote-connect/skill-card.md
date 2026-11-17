## Description:

Provides temporary SSH access to Huawei Cloud Ascend servers for NPU monitoring, system administration, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use the skill to connect to Huawei Cloud Ascend servers, inspect NPU health, manage system resources, and troubleshoot remote services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command safeguards can be bypassed, and credential handling can expose privileged access.

Mitigation: Defer production use until command approval, argument quoting, SSH server-key verification, and session identity isolation are corrected. Use a restricted account, avoid unrestricted sudo and password-bearing command lines or test files, and rotate credentials exposed in examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ascend-remote-connect)
- [IAM Permission Policy](references/iam-policies.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Structured text with remote command results, status, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected remote host and command.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
