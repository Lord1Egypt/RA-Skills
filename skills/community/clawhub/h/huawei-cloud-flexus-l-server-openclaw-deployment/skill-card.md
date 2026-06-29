## Description: <br>
Creates a Huawei Cloud Flexus L Instance, deploys the OpenClaw application platform, and helps configure models and messaging channels for the deployed instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to deploy OpenClaw on Huawei Cloud Flexus L Instances, then configure LLM model settings and WeCom, Feishu, DingTalk, or QQ channel integrations. <br>

### Deployment Geography for Use: <br>
China Huawei Cloud regions documented by the skill: cn-north-4, cn-east-3, cn-south-1, and cn-southwest-2. <br>

## Known Risks and Mitigations: <br>
Risk: Huawei Cloud credentials can create billable resources and execute scripts on instances. <br>
Mitigation: Use temporary least-privilege credentials, confirm costs and renewal settings before deployment, and remove credentials after use. <br>
Risk: Sensitive tokens, API keys, or authorization data may appear in command arguments or logs. <br>
Mitigation: Prefer environment variables or secret handling, avoid command-line secrets where possible, and review logs for exposed credentials. <br>
Risk: Model and channel setup relies on remote scripts executed on the target instance. <br>
Mitigation: Inspect the remote scripts before execution and run only on trusted instances with the minimum required permissions. <br>
Risk: OpenClaw Web UI access can expose the instance if opened broadly. <br>
Mitigation: Restrict Web UI network access to trusted IP ranges and open only required ports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-flexus-l-server-openclaw-deployment) <br>
- [Huawei Cloud Flexus L create instance API reference](https://support.huaweicloud.com/api-flexusl/create_instance_0001.html) <br>
- [Huawei Cloud Python package index](https://repo.huaweicloud.com/repository/pypi/simple) <br>
- [IAM Permission Policy Reference](artifact/references/iam-policies.md) <br>
- [Skill Verification Method](artifact/references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and status text from deployment actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create billable Huawei Cloud resources and execute Cloud Operations Center scripts on target instances.] <br>

## Skill Version(s): <br>
0.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
