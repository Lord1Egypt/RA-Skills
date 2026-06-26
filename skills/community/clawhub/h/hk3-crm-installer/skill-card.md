## Description: <br>
一键安装 HK3 CRM 客户管理系统（Bursa Malaysia 保健品公司专用）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangyisheng9-bot](https://clawhub.ai/user/jiangyisheng9-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators use this skill to install and start the HK3 CRM customer-management web app locally for a Bursa Malaysia health-products company workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads and runs unpinned remote code. <br>
Mitigation: Review the GitHub repository and requirements before installing, and pin or verify a specific commit when possible. <br>
Risk: The installer leaves a local CRM process running in the background. <br>
Mitigation: Run it in a contained environment and confirm how to stop the service after testing or use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiangyisheng9-bot/hk3-crm-installer) <br>
- [HK3 CRM GitHub Repository](https://github.com/jiangyisheng9-bot/hk3-crm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, setup status, and a local service URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill starts a local CRM service on port 5001 and writes runtime logs under /tmp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
