## Description:

Connects to Huawei switches and routers over SSH to run health, alarm, security, and resource checks and produce inspection reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[v585](https://clawhub.ai/user/v585)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators and engineers use this skill for routine health checks, troubleshooting, and security audits of Huawei switches and routers. It is intended for authorized inspection of managed infrastructure devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes plaintext SSH credentials for infrastructure devices.

Mitigation: Treat the credentials as exposed, rotate them if they correspond to real devices, and replace embedded credentials with a secret manager or user-supplied credentials.

Risk: The SSH example disables host key verification.

Mitigation: Enable verified SSH host keys before use to reduce impersonation and man-in-the-middle risk.

Risk: The skill performs administrative inspection against network devices.

Mitigation: Run inspections only against devices the operator is authorized to administer and review commands before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated inspection reports are Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and pexpect; optional sshpass is mentioned for simple commands. Output depends on Huawei CLI responses and the supplied device access details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
