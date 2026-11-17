## Description:

Diagnoses Huawei Cloud CDN origin configuration and reachability issues using read-only configuration queries and origin connectivity probes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CDN operators and engineers use this skill to investigate origin connection failures, inspect CDN origin settings, and receive a diagnosis report with suggested next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Origin probes can reach private or internal addresses from CDN configuration in the agent's network.

Mitigation: Use trusted CDN configurations and account collaborators; from sensitive networks, block or require explicit confirmation for private, loopback, link-local, reserved, and privately resolving origin hosts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cdn-origin-diagnosis)
- [Origin connectivity probe](references/task-origin-probe.md)
- [Diagnosis report format](references/task-report-generation.md)
- [Huawei Cloud CLI documentation](https://support.huaweicloud.com/hcloudcli/index.html)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Structured text diagnosis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes origin settings, probe results, and remediation suggestions; excludes credentials.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
