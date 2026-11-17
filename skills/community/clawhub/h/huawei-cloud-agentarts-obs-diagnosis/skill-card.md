## Description:

Diagnoses missing metrics, logs, and traces in Huawei Cloud AgentArts by checking subscriptions, observability pipelines, query settings, and access permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to investigate absent AgentArts metrics, logs, or traces and produce a root-cause report with recommended fixes.

### Deployment Geography for Use:

Global (select the region matching the deployment; examples use cn-north-4)

## Known Risks and Mitigations:

Risk: Diagnostic instructions include cloud resource creation that may change subscriptions or incur costs.

Mitigation: Require explicit approval from an authorized user and review cost impact before running CreateBusiness, CreatePromInstance, or similar creation steps.

Risk: Diagnosing cloud observability requires access to sensitive telemetry and IAM information.

Mitigation: Grant only the required Huawei Cloud observability and IAM read access, and use the deployment's actual region instead of assuming cn-north-4.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-agentarts-obs-diagnosis)
- [Huawei Cloud KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer)
- [IAM policies](references/iam-policies.md)
- [Diagnostic report template](references/diagnostic-report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown diagnostic report with suggested verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Root-cause analysis and recommended fixes for missing observability data]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
