## Description: <br>
自动化参与极星会 DuMate 体验活动。当用户说"参加极星会活动"、"报名极星会"、"帮我参与 DuMate 活动"、"自动完成极星会活动"或类似表达时触发。自动完成报名、体验、截图、获取账号 ID 和提交信息的全流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuanjianghu](https://clawhub.ai/user/kaiyuanjianghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to guide and partially automate participation in the Jixinghui DuMate experience activity, including registration, DuMate setup guidance, full-screen screenshot collection, Baidu Cloud account ID lookup, and activity form submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full-screen screenshots may capture sensitive desktop content or notifications. <br>
Mitigation: Close sensitive windows, disable notifications, review each screenshot before upload, and delete saved screenshots after submission. <br>
Risk: The workflow submits account-linked Baidu Cloud information. <br>
Mitigation: Confirm the exact Baidu Cloud account ID before submission and do not use a phone number or nickname in its place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuanjianghu/jixinghui-activity-dumate) <br>
- [Jixinghui activity page](https://wxaurl.cn/3kzrkXaZ4Dh) <br>
- [DuMate download page](https://www.dumate.cn?track=sfhzjxh) <br>
- [Baidu Cloud console](https://cloud.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Step-by-step guidance and status reporting, with shell command or script execution where applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local screenshot file paths under ~/Desktop/jixinghui_screenshots/ and report registration, account ID, and submission status.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
