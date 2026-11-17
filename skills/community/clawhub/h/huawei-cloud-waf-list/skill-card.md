## Description:

Lists Huawei Cloud WAF protected domains by region, with optional filters and table, JSON, or names-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and security operators use this skill to inventory WAF protected domains and review reported protection status across regions and WAF modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs a telemetry tool whose data collection and credential access are not sufficiently explained; the external wrapper was not bundled for review.

Mitigation: Before installation, request an optional telemetry workflow, a reviewed and pinned wrapper release, and clear data and credential handling documentation. Use a read-only cloud profile.

Risk: The default query ignores the protection-status filter, so results may not match a requested status.

Mitigation: Verify protection-status results independently before relying on them.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-waf-list)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policy](references/iam-policies.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Compact text table, JSON host array, or newline-separated domain names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional region, WAF mode, hostname, protection-status, enterprise-project, and policy filters.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
