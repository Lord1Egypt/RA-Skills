## Description:

Integrates the optional ocms library into PyTorch training scripts to report training metrics to Huawei Octopus for visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Octopus metric reporting to custom PyTorch loops or common training frameworks, then verify the resulting metric files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training metrics written to the platform's METRICS location may be collected by the platform.

Mitigation: Confirm the metric directory and avoid logging sensitive values; the supplied guidance discloses platform collection of metrics written to METRICS.

Risk: Reusing an output directory can overwrite previous run metadata.

Mitigation: Use a separate output directory for each training run.

Risk: The optional proprietary ocms wheel is external to the supplied files.

Mitigation: Obtain the wheel only from a verified provider source and do not grant cloud credentials for this integration.

## Reference(s):

- [IAM Policies](references/iam-policies.md)
- [Integration Patterns](references/integration_patterns.md)
- [OCMS API](references/ocms_api.md)
- [OCMS Recorder](scripts/ocms_recorder.py)
- [OCMS Verification Script](scripts/verify_ocms.py)
- [Official Octopus Courses README](https://gitee.com/huawei-octopus/octopus-courses/blob/master/ch2-Training/2.5-whls/1-octopus-metrics-summary/README.md)
- [ClawHub Skill Listing](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-train-metrics)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Framework-specific integration guidance and optional verification steps]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
