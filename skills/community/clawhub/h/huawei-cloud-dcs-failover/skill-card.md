## Description:

Prepares, executes, and reports Huawei Cloud DCS Redis master-slave failover drills with readiness checks, risk assessment, completion polling, and data consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operators use this skill to run controlled DCS failover drills and review high availability behavior, failover completion, and data consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A drill performs a real master-slave failover and may interrupt service; checks and generated scores can give misleading reassurance.

Mitigation: Use a test instance and narrowly scoped credentials. Enforce target confirmation and cross-zone checks, independently verify backups, data integrity, and application health, and do not treat scores as proof of safety.

Risk: The documented one-step CLI installer executes a remote script directly.

Mitigation: Prefer a verified CLI download over executing the remote installer directly.

## Reference(s):

- [IAM policy requirements](artifact/references/iam-policies.md)
- [Risk model](artifact/references/risk-model.md)
- [CLI installation and authentication guide](artifact/references/cli-installation-guide.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, HTML report]

**Output Format:** [Markdown guidance, shell commands, JSON configuration and results, and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces experiment and execution result files plus a failover report.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
