## Description:

Processes Huawei Cloud OBS images with mosaic, blur, or region redaction rules, and can optionally automate processing for new uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to redact images stored in Huawei Cloud OBS, either in batches or through an optional upload-triggered workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic processing may overwrite original images or repeatedly trigger cloud charges.

Mitigation: Avoid automatic mode until originals are preserved and repeated triggering is prevented. Keep backups, restrict access to dedicated image locations, and test redaction on sample images before handling sensitive data.

Risk: The required telemetry tool's reporting behavior remains unverified, even though an off switch is documented.

Mitigation: Review and verify the telemetry CLI before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-image-desens)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Natural-language guidance and JSON processing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-image processing results and configuration guidance.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
