## Description: <br>
实施项目经理 helps IT and software delivery project managers run Feishu-based project setup, milestone tracking, risk and change management, contract receivables, subcontract payments, and Chinese Markdown reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Implementation project managers use this skill to manage IT/software delivery projects in Feishu spreadsheets, calculate milestones and payment status, identify project risks, and generate Chinese Markdown project documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports an exposed Feishu App Secret. <br>
Mitigation: Rotate the secret, remove hardcoded credentials, and require credentials through secure user configuration before installation. <br>
Risk: New project sheets are configured for broad organization-wide edit access by default. <br>
Mitigation: Change sharing defaults to private or project-team-only and require explicit confirmation before widening access. <br>
Risk: The skill can read and update Feishu project spreadsheets containing project, contract, and payment tracking data. <br>
Mitigation: Confirm Feishu app permissions, target sheets, and write operations before use, and keep changes reversible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smallkeyboy/impl-project-manager) <br>
- [需求说明](references/requirements.md) <br>
- [里程碑模板](references/milestone-template.md) <br>
- [风险识别规则](references/risk-rules.md) <br>
- [变更管理模板](references/change-management.md) <br>
- [合同与回款模板](references/contract-payment-template.md) <br>
- [分包类型参考](references/subcontract-types.md) <br>
- [飞书应用配置](references/feishu-config.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown guidance with optional Python command snippets and Feishu spreadsheet updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read from and write to Feishu online spreadsheets after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
