## Description: <br>
One-click deployment tool for Hermes on Huawei Cloud Flexus L instances, including deployment, ModelArts large model configuration, robot channel configuration, and gateway management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to deploy Hermes on Huawei Cloud Flexus L instances and configure ModelArts models, Feishu or WeCom channels, UniAgent checks, and gateway operations. <br>

### Deployment Geography for Use: <br>
Huawei Cloud supported deployment regions listed in the skill: cn-north-4, cn-east-3, cn-south-1, and cn-southwest-2. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable Huawei Cloud resources. <br>
Mitigation: Install only with an account prepared for cloud charges, review the IAM policy before use, and plan cleanup for created instances and COC scripts. <br>
Risk: The skill handles sensitive Huawei Cloud credentials and robot channel secrets. <br>
Mitigation: Prefer temporary, least-privilege credentials, avoid passing secrets on the command line, and keep secrets in controlled environment variables or secret storage. <br>
Risk: The skill can run remote COC scripts with weak scoping. <br>
Mitigation: Review the requested operations before execution, limit granted permissions to the documented actions, and verify targets before running deployment or configuration commands. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/huaweiclouddev/huawei-cloud-flexus-l-server-hermes-deployment) <br>
- [IAM permissions reference](references/iam-policies.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Huawei Cloud PyPI mirror](https://repo.huaweicloud.com/repository/pypi/simple) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command executions may return JSON status objects for deployment, model configuration, channel configuration, gateway operations, and COC execution queries.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
