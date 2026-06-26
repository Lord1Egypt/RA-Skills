## Description: <br>
Guides agents through lelogin CLI credential management, including auth/configuration, listing, saving, deleting, and injecting secrets into MySQL, SSH, app startup, Alibaba Cloud CLI, and mail workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcmilan](https://clawhub.ai/user/zcmilan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to manage lelogin secret paths or run commands with credentials resolved through lelogin without exposing plaintext secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential paths could be listed, modified, deleted, or injected into an untrusted command without enough user intent. <br>
Mitigation: Confirm the exact lelogin secret path, operation, and target command with the user before list, save, delete, or exec actions. <br>
Risk: Resolved credentials could be exposed in logs, chat output, shell history, or generated configuration. <br>
Mitigation: Do not print plaintext secrets; prefer lelogin:// references and exec --env-file patterns that resolve credentials only for the child process. <br>
Risk: A missing lelogin CLI could lead an agent to fetch or run installer scripts automatically. <br>
Mitigation: When lelogin is unavailable, pause and direct the user to install the CLI manually from the official download page. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zcmilan/lelogin) <br>
- [lelogin CLI download page](https://lelogin.nationauth.cn/lelogin-portal/home_page/download) <br>
- [Alibaba Cloud CLI credential configuration](https://help.aliyun.com/zh/cli/configure-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and env examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should avoid plaintext secret values and require explicit user approval before sensitive lelogin operations.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
