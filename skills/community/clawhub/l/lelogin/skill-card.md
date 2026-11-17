## Description:

Guides agents through lelogin CLI setup checks, authorization-sensitive secret management, and exec-based credential injection for MySQL, SSH, application startup, Alibaba Cloud CLI, and mail workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcmilan](https://clawhub.ai/user/zcmilan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent operate the lelogin CLI for credential listing, saving, deletion, and scoped secret injection into command-line workflows. It is intended for tasks where the user explicitly approves each credential path and operation before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SSH example can expose a stored password by disabling server identity checks.

Mitigation: Require strict host-key verification, avoid direct root password login, and prefer key-based or least-privileged SSH access.

Risk: Secret list, save, delete, or exec operations can access or change credentials outside the intended task.

Mitigation: Obtain explicit user approval for the specific secret paths and operation purpose before running lelogin commands.

Risk: Resolved secrets could be exposed in logs, command output, or shell history.

Mitigation: Use env-file based lelogin exec patterns where possible, avoid printing secrets, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zcmilan/skills/lelogin)
- [lelogin CLI download page](https://lelogin.nationauth.cn/lelogin-portal/home_page/download)
- [Alibaba Cloud CLI credential configuration](https://help.aliyun.com/zh/cli/configure-credentials)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and env-file examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes approval gates and secret-handling cautions for credential operations.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
