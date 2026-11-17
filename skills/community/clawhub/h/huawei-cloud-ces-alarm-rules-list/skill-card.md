## Description:

Lists Huawei Cloud Cloud Eye (CES) alarm rules and optional rule details in text, table, or JSON form, with filtering and read-only status enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inventory CES alarm definitions by region and review their thresholds, associated resources, current states, and notification settings.

### Deployment Geography for Use:

Huawei Cloud CES regions selected by the user (defaults to cn-north-4)

## Known Risks and Mitigations:

Risk: The optional quality-reporting tool's handling of cloud output and credentials is unclear.

Mitigation: Set SKILL_QUALITY_REPORT=0 and skip installing the reporting tool until its data collection and destination have been reviewed.

Risk: SDK dependency installation can expose the environment to unsafe downloads.

Mitigation: Install dependencies from a certificate-verified source in an isolated environment.

Risk: Cloud inventory access can be over-privileged if configured credentials allow changes.

Mitigation: Use credentials limited to CES read access and the documented minimum IAM permissions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-ces-alarm-rules-list)
- [API verification notes](artifact/references/api-verification.md)
- [Minimum IAM permissions](artifact/references/iam-policies.md)
- [CLI installation and credentials](artifact/references/cli-installation-guide.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Rule-name list, Markdown table, or JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region, rule ID, name, level, state, and resource-type filters; read-only inventory and details]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
