## Description: <br>
个人财务管理助手 analyzes personal finance CSV exports for validation, transaction categorization, income and expense summaries, reports, and savings guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhaofeng-max](https://clawhub.ai/user/wangzhaofeng-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to process local bank or credit-card CSV exports, validate required fields, categorize spending with keyword rules, and produce summaries or reports without uploading transaction data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal finance CSVs may contain sensitive account and transaction data. <br>
Mitigation: Use the skill locally, review commands before running them, and rely on account masking for any displayed or exported results. <br>
Risk: Scheduled Feishu report delivery could send financial summaries outside the local environment. <br>
Mitigation: Enable scheduled delivery only deliberately, verify the report contents before use, and keep account data masked whenever reports are shared. <br>
Risk: The security summary notes tension between offline-processing claims and described scheduled delivery behavior. <br>
Mitigation: Treat offline analysis as the default posture and separately review any notification or scheduled-report configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhaofeng-max/personal-finance-pro) <br>
- [Publisher profile](https://clawhub.ai/user/wangzhaofeng-max) <br>
- [Artifact README](artifact/README.md) <br>
- [Category rules configuration](artifact/config/category-rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command examples and CSV/configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; categorized CSV files are written only when an output path is explicitly provided.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
