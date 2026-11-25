## Description:

Deploys static websites to Alibaba Cloud OSS by guiding credential setup, deployment parameter collection, and auto-static-web CLI execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangjfblue](https://clawhub.ai/user/liangjfblue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use this skill to configure Alibaba Cloud OSS credentials and deploy static website build output to OSS with domain and HTTPS choices collected step by step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can expose long-lived Alibaba Cloud AccessKey credentials in chat or screenshots.

Mitigation: Use a narrowly scoped temporary RAM credential, avoid sharing secrets in chat or screenshots, and rotate or revoke keys after deployment.

Risk: The requested OSS, DNS, and CDN FullAccess policies grant broad cloud permissions.

Mitigation: Grant only the permissions needed for the deployment and review permissions before running generated deployment commands.

Risk: The workflow stores credentials in a local JSON file.

Mitigation: Prefer a local secure credential prompt or credential manager where possible and restrict local file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangjfblue/skills/ossify-deploy)
- [Bundled first-use guide](guide/index.html)
- [Alibaba Cloud](https://www.aliyun.com/)
- [Alibaba Cloud RAM users console](https://ram.console.aliyun.com/users)
- [Alibaba Cloud OSS console](https://oss.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style agent guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local credential storage, lightweight credential validation, deployment command construction, and post-deployment configuration updates.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
