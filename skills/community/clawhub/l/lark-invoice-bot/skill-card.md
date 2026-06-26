## Description: <br>
Manages a local Feishu invoice recognition and reimbursement bot, including start, stop, status, log review, OCR testing, configuration, and approval-template lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaorui](https://clawhub.ai/user/wuhaorui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a Feishu/Lark invoice reimbursement bot that performs local OCR on invoice images or PDFs, checks bot health, edits bot configuration, and prepares Feishu approval submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell command construction depends on BOT_DIR and can be sensitive to unsafe paths. <br>
Mitigation: Set BOT_DIR to a trusted, simple local path without shell metacharacters and review scripts/manage.py before using start or config commands. <br>
Risk: The management script may attempt automatic package installation and starts a long-running bot process. <br>
Mitigation: Run the skill only in a controlled bot environment where package installation and tmux process management are expected. <br>
Risk: Feishu application secrets and bot configuration can be exposed through chat, logs, or configuration output if mishandled. <br>
Mitigation: Avoid sharing raw .env values in chat or logs, restrict access to bot logs, and rotate credentials if exposure is suspected. <br>
Risk: The bot can create reimbursement approvals through Feishu. <br>
Mitigation: Use least-privilege Feishu app permissions, confirm APPROVAL_CODE before deployment, and keep human approval workflows in place for submitted expenses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaorui/lark-invoice-bot) <br>
- [Lark CLI homepage](https://github.com/larksuite/cli) <br>
- [Feishu Open Platform app setup](https://open.feishu.cn/app) <br>
- [Approval template field mapping](references/approval_template.md) <br>
- [Environment variable guide](references/env_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON OCR results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOT_DIR, FEISHU_APP_ID, FEISHU_APP_SECRET, APPROVAL_CODE, python3, lark-cli, and tmux; OCR testing may process invoice images or PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
