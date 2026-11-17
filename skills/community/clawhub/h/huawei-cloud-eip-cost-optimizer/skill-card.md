## Description:

Huawei Cloud EIP Cost Optimizer helps agents list Huawei Cloud Elastic IPs, identify idle or unbound EIPs, generate cost reports, configure alerts, and maintain audit logs through hcloud CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operations teams, and FinOps practitioners use this skill to audit Huawei Cloud EIPs, find idle public IPs, estimate avoidable costs, and prepare monitoring or reporting commands without releasing or modifying EIPs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes setup flows that may install local dependencies, write audit logs, and optionally add a cron job.

Mitigation: Review any --fix or --setup-cron command before running it, and execute setup only in an environment where local package installation, audit-log creation, and scheduled jobs are allowed.

Risk: Security evidence notes write-capable IAM/API guidance that exceeds the skill's read-only framing.

Mitigation: Grant only the minimum read-only IAM policy for EIP listing and detail lookup; do not grant full-management EIP permissions for this skill.

Risk: Documentation includes installer paths that can download and run the Huawei Cloud CLI installer.

Mitigation: Avoid curl-to-bash usage unless the installer source is independently verified; prefer a reviewed local installer or package-manager path where available.

Risk: When environment-variable credentials are used, helper code may pass credentials to hcloud CLI parameters on the local host.

Mitigation: Prefer hcloud configure or temporary credentials on shared systems, use least-privilege AK/SK values, and rotate credentials regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-eip-cost-optimizer)
- [EIP API Reference Guide](references/eip-api-guide.md)
- [IAM Permission Policies](references/iam-policies.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [KooCLI Official Documentation](https://support.huaweicloud.com/cli/index.html)
- [KooCLI Download Page](https://support.huaweicloud.com/cli/reference.html)
- [IAM AK/SK Management](https://support.huaweicloud.com/usermanual-iam/iam_02_0003.html)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON, Code]

**Output Format:** [Markdown guidance with shell command snippets and generated text, HTML, or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only EIP analysis output; cost estimates use a bandwidth billing model because charge_mode is unavailable from the API.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
