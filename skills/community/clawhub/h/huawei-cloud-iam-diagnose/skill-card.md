## Description:

Analyzes Huawei Cloud IAM policies and permission chains to estimate whether a user can perform an action on a resource, with a confidence grade and trace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to investigate Huawei Cloud IAM access questions by tracing direct, group, and agency permissions. Its verdict is a reference estimate, not an authoritative access decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive IAM metadata using locally configured cloud credentials.

Mitigation: Use a least-privilege read-only IAM credential, and do not share credentials or permission traces unnecessarily.

Risk: Automatic quality telemetry may report skill activity.

Mitigation: Review the telemetry path before use; disable reporting with SKILL_QUALITY_REPORT=0 if inappropriate.

Risk: The telemetry CLI installer can download software onto the local machine.

Mitigation: Avoid running the installer unless you trust its remote endpoints and have reviewed the installation steps.

Risk: A static policy verdict can be misleading when permissions are incomplete or conditional.

Mitigation: Treat results as reference-only and verify critical access decisions through the IAM console, an actual API call, or audit logs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-iam-diagnose)
- [IAM policies and least-privilege access](artifact/references/iam-policies.md)
- [Verdict verification method](artifact/references/verification-method.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/cli/index.html)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, JSON]

**Output Format:** [Text verdict and permission-chain trace; optional JSON trace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-only likely-has/likely-has-not/uncertain verdict with confidence grade; incomplete checks and policy conditions limit certainty.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
