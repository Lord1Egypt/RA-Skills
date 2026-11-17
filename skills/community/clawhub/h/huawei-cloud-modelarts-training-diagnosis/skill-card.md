## Description:

Huawei Cloud ModelArts training job fault diagnosis skill that uses hcloud CLI to call ModelArts training job log and event APIs, analyze failed, timed out, abnormal, or stuck training jobs, and provide diagnosis conclusions with fix suggestions and confidence levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ML engineers, and cloud operators use this skill to inspect Huawei Cloud ModelArts training jobs, collect read-only status, event, stage, and log evidence, and produce concise root-cause diagnosis with confidence-rated remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects cloud training job metadata and log snippets that may contain sensitive information.

Mitigation: Use the documented read-only ModelArts IAM permissions, avoid printing credentials, mask sensitive fields, and include only key error or traceback lines in reports.

Risk: Installation guidance includes downloading and running hcloud installer scripts.

Mitigation: Verify the download source before running installers, prefer interactive or manual installation when possible, and avoid non-interactive installer execution unless the source is trusted.

Risk: Weakening TLS verification can expose credentials or diagnostic data.

Mitigation: Keep TLS verification enabled unless a controlled environment explicitly requires otherwise, and restore secure verification after troubleshooting.

Risk: Uninstall commands can remove local hcloud configuration.

Mitigation: Review uninstall commands before execution and back up required hcloud profiles or configuration files first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-modelarts-training-diagnosis)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/wtsnew-hcli/index.html)
- [API Catalog](references/api-catalog.md)
- [Diagnosis Flow](references/diagnosis-flow.md)
- [hcloud Command Templates](references/hcloud-command-templates.md)
- [Confidence Rules](references/confidence-rules.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown diagnosis report with tables, confidence labels, fix suggestions, and inline hcloud CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HIGH, MEDIUM, and LOW confidence levels; extracts only key error or traceback lines rather than full logs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
