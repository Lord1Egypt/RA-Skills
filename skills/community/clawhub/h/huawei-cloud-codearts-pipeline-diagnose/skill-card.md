## Description:

Helps diagnose build and pipeline failures and manage CodeArts Pipeline and CodeArts Build resources through Huawei Cloud's hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps operators use this skill to inspect CodeArts pipelines, build tasks and logs, diagnose failures, and create, start or delete resources with confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An additional telemetry CLI can be downloaded and installed persistently without sufficient integrity details.

Mitigation: Review or preinstall the quality CLI from a trusted source before allowing the installer scripts to run.

Risk: The telemetry wrapper runs around every Huawei Cloud command and may expose sensitive activity.

Mitigation: Set SKILL_QUALITY_REPORT=0 in sensitive environments and assess the wrapper's privacy behavior before use.

Risk: Create, start and delete actions can change or remove cloud resources.

Mitigation: Prefer read-only credentials for diagnosis; grant write access only when needed and require the documented preview and confirmation before changes.

## Reference(s):

- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/cli/index.html)
- [CodeArts IAM policies](artifact/references/iam-policies.md)
- [Build error classification](artifact/references/build-error-classification.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands and structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are scoped to the selected Huawei Cloud region and CodeArts project.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
