## Description: <br>
在 BOSS 直聘中筛选候选人、主动打招呼、处理未读消息/接收简历的浏览器自动化技能，触发词：BOSS直聘、招聘、简历、未读消息、打招呼。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liaofuyan](https://clawhub.ai/user/liaofuyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters and hiring teams use this skill to operate BOSS Zhipin workflows for candidate screening, greeting candidates, handling unread messages, receiving or requesting resumes, and producing hiring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in BOSS Zhipin recruiting account, including sending messages and taking resume-related actions. <br>
Mitigation: Set explicit candidate-count limits and require approval before sending messages or requesting, receiving, or downloading resumes. <br>
Risk: Downloaded resumes and exported reports may contain personal data. <br>
Mitigation: Confirm the Feishu destination and permissions before export, and define retention or deletion rules for downloaded resumes and reports before use. <br>
Risk: Recruiting automation may trigger platform controls or continue beyond the user's intended scope. <br>
Mitigation: Use the documented rate limits, stop on verification challenges or platform limits, and define clear stop conditions before starting a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liaofuyan/mama-cli) <br>
- [Publisher profile](https://clawhub.ai/user/liaofuyan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and browser automation guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include candidate screening summaries, action status tables, resume-handling notes, and Feishu report handoff guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
