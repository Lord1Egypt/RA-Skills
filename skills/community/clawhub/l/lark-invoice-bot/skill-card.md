## Description:

飞书发票识别与费用报销机器人管理技能，用于启动、停止、监控基于 Feishu CLI and Python OCR 的本地发票报销 Agent，并辅助测试 OCR、调整配置和查看审批模板。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaorui](https://clawhub.ai/user/wuhaorui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage a local Feishu invoice reimbursement bot, check its runtime status and logs, test OCR on invoice images or PDFs, and inspect the approval-template mapping before submitting reimbursements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict flags review-worthy command execution and host modification risks.

Mitigation: Review the skill before installing, restrict use to a trusted local environment, and avoid running start or configuration commands with elevated privileges.

Risk: The skill depends on Feishu application secrets and approval configuration values.

Mitigation: Keep FEISHU_APP_SECRET and related credentials out of chat and logs, store them only in the intended local environment file, and rotate exposed credentials.

Risk: BOT_DIR controls where scripts read logs, modify configuration, and start the bot process.

Mitigation: Set BOT_DIR only to a known safe invoice-bot directory and review dependency and command construction before running management actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaorui/skills/lark-invoice-bot)
- [Lark CLI](https://github.com/larksuite/cli)
- [Feishu Open Platform app setup](https://open.feishu.cn/app)
- [Approval template mapping](references/approval_template.md)
- [Environment variable guide](references/env_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON OCR results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local bot logs, update BOT_DIR/.env configuration, and run local management or OCR test scripts when directed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
