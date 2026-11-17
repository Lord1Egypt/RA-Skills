## Description:

Huawei Cloud GaussDB instance management skill for querying, diagnosing, provisioning, backing up, scaling, permission management, and deletion workflows across GaussDB for MySQL and GaussDB for openGauss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and database administrators use this skill to inspect Huawei Cloud GaussDB inventory, analyze deployment and security posture, and prepare controlled management actions. It supports read-only query and diagnosis flows plus preview-and-confirm workflows for creation, backup, scaling, permission changes, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect sensitive Huawei Cloud GaussDB inventory and security posture using local cloud credentials.

Mitigation: Install it only when the agent is expected to administer GaussDB, and use the narrowest IAM policy needed for the intended read or manage tier.

Risk: R1 and R2 workflows can change database permissions, create resources, scale nodes, create backups, or delete instances.

Mitigation: Require explicit user direction and confirmation before mutating operations, and separate read-only roles from management roles.

Risk: Broad cloud permissions could expose more resources than the requested GaussDB workflow requires.

Mitigation: Avoid routine FullAccess grants; prefer least-privilege GaussDB and VPC read policies and elevate only for the specific operation.

## Reference(s):

- [KooCLI Installation and Authentication Guide](references/cli-installation-guide.md)
- [IAM Policies - GaussDB Least Privilege](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-gaussdb-instance-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Huawei Cloud KooCLI output and requires explicit confirmation before mutating operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
