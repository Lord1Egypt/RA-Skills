## Description: <br>
Automates Toutiao article and short-post publishing, including topic selection, content drafting, image handling, cookie-based login, mixed text-image publishing, scheduling, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin1220](https://clawhub.ai/user/kevin1220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to generate and publish Toutiao articles or short posts from configured topics, images, account cookies, and notification settings. It is suited for users who intentionally want an agent to operate a live Toutiao account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use raw account cookies to operate a live Toutiao account. <br>
Mitigation: Keep cookie files private and out of repositories, use a dedicated browser or profile, and rotate cookies when access changes. <br>
Risk: Publishing and scheduler flows can create live public posts without a clear final approval gate. <br>
Mitigation: Use generation-only or dry-run modes where available, review generated content before publication, and enable scheduled runs only with monitoring and a stop procedure. <br>
Risk: Feishu notifications may send publication metadata to a third party. <br>
Mitigation: Configure Feishu notifications only when that disclosure is acceptable and limit message content to necessary status information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevin1220/kevin-toutiao-auto-publisher) <br>
- [Toutiao Creator Platform](https://mp.toutiao.com) <br>
- [Toutiao Article Publish Page](https://mp.toutiao.com/profile_v4/graphic/publish) <br>
- [Toutiao Short Post Publish Page](https://mp.toutiao.com/profile_v4/weitoutiao/publish) <br>
- [Feishu Open Platform Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu Open Platform Message API](https://open.feishu.cn/open-apis/message/v4/send) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with Python scripts, configuration examples, generated post text, publication status, logs, and notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish live public content when configured with valid account cookies and publishing commands.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
