## Description:

Guides agents in querying and analyzing Huawei Cloud Elastic Load Balance metrics through Cloud Eye Service for connection, traffic, and supported HTTP performance monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to inspect Huawei Cloud ELB connection, traffic, and available HTTP metrics, troubleshoot load balancers, and assess capacity using CES data.

### Deployment Geography for Use:

Global, subject to Huawei Cloud regional service and metric availability

## Known Risks and Mitigations:

Risk: Documented wildcard cloud permissions grant more access than monitoring requires.

Mitigation: Use a narrowly scoped Huawei Cloud identity with read-only ELB and CES permissions; avoid elb:* and ces:* policies.

Risk: One-line script downloads or non-interactive installers may execute unverified code.

Mitigation: Independently verify installer source and integrity before execution.

Risk: Connectivity checks and debug logs may expose unnecessary account information or credentials.

Mitigation: Do not list IAM users to test connectivity; review and redact debug output before sharing it with support.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ces-elb-monitoring)
- [CES metrics reference](references/ces-metrics-reference.md)
- [KooCLI installation guide](references/cli-installation-guide.md)
- [IAM permissions](references/iam-policies.md)
- [Monitoring report format](references/output-format.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown monitoring report with metric tables, recommendations, and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTTP and backend-group metrics depend on Dedicated ELB availability.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
