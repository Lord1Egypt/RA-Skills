## Description:

Huawei Cloud RDS Smart Service helps agents answer RDS questions, inspect and operate database instances, optimize SQL, troubleshoot faults, tune parameters, and guide backup or recovery workflows across supported Huawei Cloud RDS database engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DBAs, SREs, and operations teams use this skill to generate Huawei Cloud RDS commands, diagnostics, health checks, SQL tuning guidance, and backup or recovery procedures. It is intended for assisted administration where high-impact operations remain subject to explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or execute high-impact RDS administration actions such as restart, failover, resize, restore, delete, security-group, SQL-limit, and parameter changes.

Mitigation: Start with read-only IAM permissions, review the operations allowed for the deployment, and require explicit human approval before any mutating command is run.

Risk: The security evidence flags incomplete confirmation and installation safeguards.

Mitigation: Fix the confirmation wrapper to fail closed before production use and independently verify installer downloads instead of running curl-to-bash commands blindly.

Risk: Huawei Cloud AK/SK credentials may be exposed through shell history, shared terminals, or logs.

Mitigation: Use environment or secret-management practices that keep credentials out of command history and shared logs, and limit credentials to the least privilege needed.

## Reference(s):

- [Huawei Cloud RDS Smart Service on ClawHub](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-rds-smart-service)
- [Huawei Cloud hcloud CLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Dataflow Diagram](references/dataflow-diagram.md)
- [IAM Policies for RDS Smart Service](references/iam-policies.md)
- [RDS REST API Paths](references/api-paths.md)
- [RDS Troubleshooting Guide](references/rds-troubleshooting-guide.md)
- [SQL Performance Optimization Guide](references/sql-optimization-guide.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, JSON health-check output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Huawei Cloud CLI, SDK, or REST API fallback steps; mutating operations require explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
