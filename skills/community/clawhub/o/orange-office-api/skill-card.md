## Description:

橙子通（orange-office.cn）库存管理系统 API 自动化。用于通过 API 创建出库单、查询库存、管理主播仓库等，无需浏览器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao1230123](https://clawhub.ai/user/xiao1230123)

### License/Terms of Use:

MIT-0

## Use Case:

Operations staff and developers use this skill to automate Orange Office inventory workflows, including stock queries, outbound order creation or update, warehouse mapping, and DingTalk inventory table writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes session/signing details and operational configuration values.

Mitigation: Use only in a trusted internal context, rotate or remove exposed values if distributed broadly, and load session cookies, table IDs, and personnel mappings from protected runtime configuration.

Risk: The skill enables business-record changes, including Orange Office stock-out create, update, or delete operations and DingTalk writes.

Mitigation: Require explicit human approval before any stock-out update/delete or DingTalk write, and review proposed records before execution.

## Reference(s):

- [Orange Office](https://orange-office.cn)
- [ClawHub skill page](https://clawhub.ai/xiao1230123/skills/orange-office-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request bodies and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signed HTTP request examples and operational checklists; current session credentials must be supplied at runtime.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/openclaw.skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
