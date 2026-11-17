## Description:

在 BOSS 直聘中筛选候选人、主动打招呼、处理未读消息/接收简历的浏览器自动化技能，触发词：BOSS直聘、招聘、简历、未读消息、打招呼。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liaofuyan](https://clawhub.ai/user/liaofuyan)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and recruiting operators use this skill to automate authorized BOSS Zhipin candidate screening, outreach, unread-message triage, resume handling, and Markdown reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive candidate information, including resume receipt, download, reporting, and possible Feishu export.

Mitigation: Use it only with authorized recruiting accounts; confirm candidate data handling, Feishu destination, and retention policy before exporting reports or resumes.

Risk: The skill can perform live account actions such as sending greetings, requesting resumes, and downloading resumes.

Mitigation: Require explicit per-run approval before outreach, resume requests, downloads, or external report exports.

Risk: The security verdict is suspicious because consent, stop, export, and retention controls are weak.

Mitigation: Review the skill before installation and stop execution when login, captcha, rate-limit, or authorization conditions are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liaofuyan/skills/mama-cli)
- [Publisher profile](https://clawhub.ai/user/liaofuyan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and tabular reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate screening summaries, status tables, operational guidance, and Feishu export instructions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
