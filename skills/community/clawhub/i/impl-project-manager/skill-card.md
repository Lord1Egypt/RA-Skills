## Description:

实施项目经理 is an agent skill for IT and software delivery project managers that reads Feishu sheet data, calculates milestones, payment status, risks, and warnings, and updates sheets after conversational confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers and delivery teams use this skill to manage IT/software delivery workflows across project initiation, milestones, risks, changes, contract receivables, subcontract payments, progress reporting, and closeout reviews. The skill is designed around Feishu online sheets as the source of project data and produces Chinese project-management guidance and Markdown deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an exposed Feishu App Secret and token handling that can leave credentials available to unintended users.

Mitigation: Rotate and remove the exposed secret, require credentials through a protected secret mechanism, and disable token printing and insecure source-tree token caching before use.

Risk: The release evidence reports that newly created project sheets are automatically made editable across the organization.

Mitigation: Make new sheets private by default and require explicit approval before broadening sharing to organization-wide edit access.

Risk: The release evidence recommends reviewing broad Feishu permissions used for reading, writing, creating sheets, and changing drive sharing.

Mitigation: Reduce Feishu scopes to only the operations actually needed for the deployment and review the skill before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/impl-project-manager)
- [需求说明](references/requirements.md)
- [飞书配置](references/feishu-config.md)
- [里程碑模板](references/milestone-template.md)
- [风险识别规则](references/risk-rules.md)
- [变更管理模板](references/change-management.md)
- [合同与回款模板](references/contract-payment-template.md)
- [分包类型参考](references/subcontract-types.md)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown, conversational guidance, shell command examples, and structured tabular updates for Feishu sheets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, create, and update Feishu online sheets when credentials, permissions, and sheet tokens are available; calculates milestone dates, payment amounts, status labels, warnings, and risk records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
