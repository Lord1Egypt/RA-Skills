## Description: <br>
Automates deployment of the JiuwenSwarm/JiuwenClaw multi-agent collaboration platform on Huawei Cloud Flexus L instances, including instance creation, COC-based deployment, model configuration, and Xiaoyi/Feishu/DingTalk channel setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to deploy JiuwenSwarm or JiuwenClaw on Huawei Cloud Flexus L, create or target cloud instances, run COC deployment tasks, and configure model APIs and messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create paid Huawei Cloud resources and modify cloud infrastructure. <br>
Mitigation: Use temporary, least-privilege Huawei credentials, confirm the exact target instance and expected charges before creation, and avoid production hosts unless reviewed. <br>
Risk: The skill can run root remote scripts through Huawei Cloud COC and may leave sensitive values in deployment artifacts. <br>
Mitigation: Review the deployment scope before execution, rotate model and channel secrets after testing, and do not share COC logs or result JSON files. <br>
Risk: The deployed web service may be reachable on port 5173 after security group changes. <br>
Mitigation: Open access only when needed, restrict source IPs where possible, and close the port after use. <br>


## Reference(s): <br>
- [API Specification](references/api_specs.md) <br>
- [Deployment Checklist](references/deployment_checklist.md) <br>
- [IAM Permission Policies](references/iam_policies.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Huawei Cloud IAM FAQ](https://support.huaweicloud.com/iam_faq/iam_01_0620.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and deployment status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Huawei Cloud COC execution UUIDs, instance details, web access URLs, and error guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
