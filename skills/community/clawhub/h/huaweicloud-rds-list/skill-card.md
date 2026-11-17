## Description:

查询华为云账号下指定 Region 的 RDS 实例列表，并输出实例名称、ID、状态、引擎类型和规格的精简清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inventory Huawei Cloud RDS instances in a selected Region before maintenance, troubleshooting, or automation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Huawei Cloud AK/SK credentials must be placed in a local config.json file.

Mitigation: Use a dedicated read-only IAM identity, keep config.json out of shared folders, restrict file permissions, and rotate keys if exposure is suspected.

Risk: If project_id is omitted, the skill also calls IAM project listing to resolve the Region project.

Mitigation: Provide project_id directly when possible, or grant only iam:projects:listProjects in addition to rds:instances:list.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/huaweicloud-rds-list)
- [IAM permission statement](artifact/iam-policies.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text inventory with setup and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs print one row per RDS instance with name, id, status, engine, and spec; empty Regions print a no-instances message.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
