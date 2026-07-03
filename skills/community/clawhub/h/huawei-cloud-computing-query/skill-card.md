## Description: <br>
Queries Huawei Cloud ECS, BMS, IMS, and AS resources through packaged read-only Python scripts and service-specific usage guides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and infrastructure engineers use this skill to inventory Huawei Cloud compute resources, inspect available specifications and images, and retrieve resource identifiers needed for verification or automation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scripts may expose sensitive ECS server passwords or remote console URLs in command output. <br>
Mitigation: Run password and console URL scripts only for authorized administrative tasks, keep outputs out of shared logs, and redact sensitive values before sharing results. <br>
Risk: The package weakens TLS certificate verification while handling Huawei Cloud credentials. <br>
Mitigation: Review and modify the HTTP configuration to enforce certificate verification before production use, especially outside controlled networks. <br>
Risk: Cloud API access relies on Huawei Cloud access keys and may reveal resource inventory or account structure. <br>
Mitigation: Use least-privilege, scoped credentials and temporary security tokens where possible; avoid broad account-level permissions for routine inventory queries. <br>


## Reference(s): <br>
- [Huawei Cloud Auto Scaling (AS) Query Guide](references/as/guide.md) <br>
- [BMS (Bare Metal Server) Query Guide](references/bms/guide.md) <br>
- [Huawei Cloud ECS Query Guide](references/ecs/guide.md) <br>
- [Huawei Cloud IMS Query Guide](references/ims/guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with skill action command invocations and JSON query results from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query outputs may include cloud resource identifiers, status fields, image and flavor details, quotas, console URLs, or passwords depending on the selected script.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
