## Description:

自动化参与极星会 DuMate 体验活动，包括报名、体验、截图、获取百度云账号 ID 和提交信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuanjianghu](https://clawhub.ai/user/kaiyuanjianghu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to guide or automate participation in the 极星会 DuMate experience activity, including event signup, DuMate setup, required screenshots, Baidu Cloud account ID retrieval, and final submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to collect a Baidu Cloud account ID and submit it to an activity form.

Mitigation: Have the user verify the activity destination and approve the account ID before submission; do not substitute a phone number, nickname, or unrelated identifier.

Risk: The skill asks for full-screen screenshots, which may capture other apps, notifications, or sensitive desktop content.

Mitigation: Review and redact screenshots before upload, close unrelated apps, and avoid capturing private notifications or documents.

Risk: Security evidence marks the release suspicious because screenshot upload and account-ID collection have weak scoping and consent controls.

Mitigation: Prefer manual final submission unless the destination is clearly trusted and the user has explicitly approved the files and account ID.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuanjianghu/skills/jixinghui-activity)
- [DuMate download page](https://www.dumate.cn?track=sfhzjxh)
- [Baidu Cloud console](https://cloud.baidu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown or plain-text procedural guidance, status reporting, and optional Python command-line output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reference three full-screen screenshot files under the user's Desktop and report the collected Baidu Cloud account ID.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
