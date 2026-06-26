## Description: <br>
Publishes supplied article HTML and optional cover media to a WeChat Official Account draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhongchen](https://clawhub.ai/user/wuhongchen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to turn already-prepared article titles, summaries, HTML bodies, and optional cover images into WeChat Official Account drafts for review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat Official Account AppID and AppSecret values to obtain access tokens and create drafts. <br>
Mitigation: Install and run it only when the agent is intended to use those credentials, keep the .env file protected, and avoid exposing credential values in prompts or logs. <br>
Risk: Incorrect title, digest, HTML body, or cover image inputs can create inaccurate or poorly formatted drafts. <br>
Mitigation: Review the article title, digest, HTML, and cover path before running the skill, then inspect the resulting draft in the WeChat backend before publication. <br>
Risk: The cron example can repeatedly create drafts without an interactive review step at creation time. <br>
Mitigation: Enable scheduled execution only deliberately, with explicit prompts and a workflow that reviews generated drafts before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhongchen/mp-draft-push) <br>
- [Publisher profile](https://clawhub.ai/user/wuhongchen) <br>
- [WeChat Official Account platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and WeChat API JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, WECHAT_APPID, and WECHAT_SECRET; creates drafts but still asks the user to review in the WeChat backend before publishing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
