## Description: <br>
把 Gmail 招聘邮件转成中文 Apple Reminders。用户提到“检查邮件里的面试/笔试/测评/授权”“把招聘邮件转成提醒事项”“别漏掉面试时间”“同步到 iPhone 提醒”等需求时触发。优先识别 ATS 邮件和面试信息更新，忽略投递成功回执。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissoncx](https://clawhub.ai/user/nissoncx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking macOS and Gmail users use this skill to identify recruiting emails about interviews, written exams, assessments, authorization, or deadlines and convert high-confidence events into Chinese Apple Reminders that can sync to iPhone or iPad. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to the intended Gmail account, Apple Mail, and Apple Reminders. <br>
Mitigation: Grant access only for the intended account, verify Apple Mail and Reminders permissions, and run an initial scan-only command before enabling reminder writes. <br>
Risk: Reminder synchronization can modify or remove reminders, and the security summary flags under-disclosed deletion and bulk-clear commands. <br>
Mitigation: Keep writes scoped to a dedicated OpenClaw reminders list, review scan output first, avoid clear-list or sync-plan --clear unless intentionally emptying that list, and enable recurring automation only after checking the generated reminders. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nissoncx/openclaw-offer-radar) <br>
- [Artifact README](artifact/README.md) <br>
- [OpenClaw Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON status summaries from the scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, or delete Apple Reminders when synchronization is enabled; scan-only mode reports detected recruiting events without writing reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
