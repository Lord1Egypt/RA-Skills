## Description: <br>
Automates participation in a Jixinghui DuMate experience activity, including registration guidance, DuMate setup, screenshots, Baidu Cloud account ID collection, and activity information submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuanjianghu](https://clawhub.ai/user/kaiyuanjianghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to coordinate the steps required to participate in a Jixinghui DuMate activity. It helps open the relevant service pages, guide client setup and login, prepare full-screen screenshots, collect the Baidu Cloud account ID, and submit the activity form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to collect and submit account-linked data, including a Baidu Cloud account ID. <br>
Mitigation: Confirm the destination page before submission and avoid repeating the full account ID in chat or reports. <br>
Risk: The skill asks for full-screen desktop screenshots, which may expose private windows, notifications, or unrelated personal information. <br>
Mitigation: Close private content first, then inspect or redact screenshots before uploading them. <br>
Risk: The security summary says the skill lacks sufficient privacy controls for collecting account-linked data and screenshots. <br>
Mitigation: Review the skill carefully before installing and use it only when the user is comfortable with those data flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuanjianghu/jixinghui-activity) <br>
- [DuMate download page](https://www.dumate.cn?track=sfhzjxh) <br>
- [Baidu Cloud console](https://cloud.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown and terminal text with saved screenshot file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshot filenames under ~/Desktop/jixinghui_screenshots/ and report activity status, account ID status, and submission status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
