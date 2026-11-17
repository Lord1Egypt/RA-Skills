## Description:

一键安装 HK3 CRM 客户管理系统（Bursa Malaysia 保健品公司专用）

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangyisheng9-bot](https://clawhub.ai/user/jiangyisheng9-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and start a local HK3 CRM instance by cloning the application, installing Python dependencies, and launching the service on localhost port 5001.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads mutable remote code and installs dependencies before running the CRM service.

Mitigation: Review or pin the repository revision, inspect requirements.txt, and run the installer only under an account and environment where that code is acceptable.

Risk: The installer starts a background service without clear consent gates in the artifact.

Mitigation: Use a virtual environment or container, monitor /tmp/hk3-crm.log, and stop the recorded PID when the CRM process is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangyisheng9-bot/skills/hk3-crm-installer)
- [HK3 CRM GitHub repository](https://github.com/jiangyisheng9-bot/hk3-crm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local service status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a background local CRM process, stores its PID in the cloned repository, and writes logs to /tmp/hk3-crm.log.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
