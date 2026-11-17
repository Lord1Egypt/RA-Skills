## Description:

Analyze candidate models before adapter implementation by identifying implementation source, structural features, layer-by-layer loading needs, and MoE fused-weight risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and model engineers use this skill to assess whether a local model is suitable for msModelSlim adapter work. It classifies the implementation and model structure, checks loading and MoE considerations, and produces findings and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This local model-analysis skill can unexpectedly use existing cloud credentials to send model metadata and diagnostic details externally.

Mitigation: Review the reporting behavior, or set SKILL_QUALITY_DISABLE=1 before starting Python and exclude cloud credentials from the process. If reporting is enabled, require informed opt-in, a restricted HTTPS destination, and certificate verification.

Risk: Candidate model code may be untrusted if executed during inspection.

Mitigation: Review candidate code first and execute it only with isolation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-msmodelslim-model-analysis)
- [Analysis Checklist](artifact/references/analysis-checklist.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Verification Method](artifact/references/verification-method.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [IAM Policies](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown analysis report with findings, risk assessment, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the model configuration and implementation files available for review.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
