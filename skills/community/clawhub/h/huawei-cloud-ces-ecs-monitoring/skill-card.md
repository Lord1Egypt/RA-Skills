## Description: <br>
Huawei Cloud ECS monitoring skill using Cloud Eye Service (CES) for querying and analyzing Elastic Cloud Server CPU, memory, disk, network, and system metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Huawei Cloud ECS instance health, query CES metrics, analyze utilization trends, and troubleshoot performance issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Huawei Cloud CLI with cloud credentials. <br>
Mitigation: Use the minimum read-only IAM policy, configure credentials outside the chat session, and do not paste secrets into the conversation. <br>
Risk: Some documentation includes privileged installation steps and broad optional permissions. <br>
Mitigation: Review curl, bash, sudo, and permission-expanding commands before execution, and avoid full-access policies unless explicitly required. <br>


## Reference(s): <br>
- [Huawei Cloud CES Metrics Reference for ECS](references/ces-metrics-reference.md) <br>
- [Huawei Cloud KooCLI Installation Guide](references/cli-installation-guide.md) <br>
- [IAM Policies for Huawei Cloud ECS Monitoring](references/iam-policies.md) <br>
- [Huawei Cloud CLI Command Reference](references/related-commands.md) <br>
- [Huawei Cloud ECS Monitoring Troubleshooting Guide](references/troubleshooting-guide.md) <br>
- [Huawei Cloud ECS Monitoring Best Practices](references/best-practices.md) <br>
- [Huawei Cloud ECS Documentation](https://support.huaweicloud.com/usermanual-ecs/ecs_03_1001.html) <br>
- [Huawei Cloud CLI Documentation](https://support.huaweicloud.com/function-hcli/index.html) <br>
- [Huawei Cloud CES API Reference](https://support.huaweicloud.com/api-ces/ces_03_0041.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/huaweiclouddev/huawei-cloud-ces-ecs-monitoring) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with Huawei Cloud CLI command examples and monitoring report tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include metric summaries, trend analysis, troubleshooting recommendations, and command snippets for CES and ECS queries.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
