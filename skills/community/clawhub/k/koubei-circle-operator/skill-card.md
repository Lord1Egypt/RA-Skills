## Description: <br>
口碑圈商家运营自动化技能，用于发帖、活动管理、数据监控、自动提醒和长连接推送，并需要商户 Key 才能执行操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanceng666](https://clawhub.ai/user/quanceng666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchants and community operators use this skill to manage Koubei Circle communities through agent-guided posts, data queries, activity operations, user messaging, point changes, labels, and automation setup. It is intended for operators who administer a Koubei Circle merchant account and can review privileged actions before they run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad merchant community administration capabilities, including posting, messaging, points, labels, and SQL-backed data access. <br>
Mitigation: Install it only for administrators of the merchant account, restrict who can invoke it, and confirm each post, message, points, label, or other write action before execution. <br>
Risk: The merchant Key is sensitive and is required for privileged API access. <br>
Mitigation: Treat the merchant Key as a secret, share it only after user confirmation, and avoid exposing the saved configuration file or command output. <br>
Risk: Data queries or file uploads may expose private community or local information if used carelessly. <br>
Mitigation: Review SQL before it runs, keep queries scoped to the requested time range and allowed fields, and avoid uploading private local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quanceng666/koubei-circle-operator) <br>
- [Koubei Circle website](https://dengluu.com) <br>
- [OpenClaw CLI command reference](references/api.md) <br>
- [Koubei Circle feature guide](references/features.md) <br>
- [Koubei Circle version guide](references/versions.md) <br>
- [Koubei Circle API server](https://ocg.myfans.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger privileged OpenClaw CLI operations after merchant Key configuration and user confirmation.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence and target metadata; artifact package.json reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
