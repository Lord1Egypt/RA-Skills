## Description:

自动化引导用户参与极星会 DuMate 体验活动，包括报名、安装或打开 DuMate、体验功能、准备全屏截图、获取百度云账号 ID，并提交活动参与信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuanjianghu](https://clawhub.ai/user/kaiyuanjianghu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to automate or receive guided assistance for completing a DuMate activity participation workflow. The skill helps navigate activity signup, client setup, screenshots, Baidu Cloud account ID collection, and final information submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-screen screenshots may capture unrelated private information.

Mitigation: Close unrelated applications and notifications, then manually review each screenshot before upload.

Risk: The workflow submits screenshots and a Baidu Cloud account ID through a shortened external activity link.

Mitigation: Resolve the shortened URL destination and approve the exact account ID and files before submission.

Risk: Login and authorization steps can expose account access if delegated too broadly.

Mitigation: Keep login and authorization under direct user control and resume automation only after the user confirms completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuanjianghu/skills/jixinghui-activity-dumate)
- [Activity page](https://wxaurl.cn/3kzrkXaZ4Dh)
- [DuMate download page](https://www.dumate.cn?track=sfhzjxh)
- [Baidu Cloud console](https://cloud.baidu.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with optional shell command output and generated screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local screenshot paths and status reports for signup, account ID collection, and submission steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
