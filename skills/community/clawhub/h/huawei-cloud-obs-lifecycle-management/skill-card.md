## Description:

Helps manage Huawei Cloud OBS lifecycle rules, diagnose ineffective policies, preview affected objects, and estimate storage-class costs through the Huawei Cloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and storage administrators use this skill to inspect and troubleshoot OBS lifecycle policies, preview rule effects, and create, update, or delete rules after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lifecycle changes can affect or delete objects, and the built-in approval gates may be insufficient.

Mitigation: Use dedicated bucket-scoped credentials; independently review the preview and require explicit approval before any apply or deletion.

Risk: The helper CLI is installed persistently from a remote download without built-in checksum or signature verification.

Mitigation: Do not run the helper installer unless the download and installation method meet your software verification policy.

Risk: Automatic quality telemetry may expose sensitive bucket names or object prefixes.

Mitigation: Disable reporting with SKILL_QUALITY_REPORT=0 when those details are sensitive.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-lifecycle-management)
- [Huawei Cloud CLI documentation](https://support.huaweicloud.com/cli/index.html)
- [Lifecycle rule format](references/lifecycle-rule-format.md)
- [IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown explanations and command examples; JSON lifecycle configurations and preview results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Affected-object previews and approximate cost estimates may depend on the objects scanned.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
