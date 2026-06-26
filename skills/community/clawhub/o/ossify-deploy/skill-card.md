## Description: <br>
Guides an agent through deploying a static website to Alibaba Cloud OSS, including credential setup, optional browser-guided configuration, and deployment parameter collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangjfblue](https://clawhub.ai/user/liangjfblue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to configure Alibaba Cloud credentials and deploy static website build output to OSS with domain, ICP filing, and HTTPS choices confirmed before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to create broad, long-lived Alibaba Cloud credentials and provide them in the agent conversation. <br>
Mitigation: Use a dedicated least-privilege RAM user scoped only to the required bucket and domain, avoid sharing secrets beyond the local agent session, and rotate or delete the AccessKey after deployment. <br>
Risk: Browser automation and domain registration steps may affect cloud account settings or create paid resources. <br>
Mitigation: Supervise browser automation, review each form before submission, and explicitly confirm any paid domain or cloud service action. <br>
Risk: Local credential storage can expose Alibaba Cloud access if file permissions or workstation controls are weak. <br>
Mitigation: Store credentials only in the documented local path with user-only permissions and remove the credential file when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangjfblue/ossify-deploy) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [First-use configuration guide](artifact/guide/index.html) <br>
- [Alibaba Cloud](https://www.aliyun.com/) <br>
- [Alibaba Cloud RAM users console](https://ram.console.aliyun.com/users) <br>
- [Alibaba Cloud OSS console](https://oss.console.aliyun.com/) <br>
- [Alibaba Cloud domain registration](https://wanwang.aliyun.com/domain/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown/plain text guidance with inline bash and Node.js command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local credential file and last-deployment metadata when the agent executes the suggested commands with user-provided credentials.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
