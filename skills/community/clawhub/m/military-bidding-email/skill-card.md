## Description:

A military procurement opportunity reporting skill that gathers data from three military procurement channels, generates an Excel report, and sends the report by SMTP email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpengle](https://clawhub.ai/user/zhangpengle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to collect Chinese military procurement opportunities, filter them by date or keywords, and send a summarized email report with an Excel attachment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send outbound email without an interactive confirmation step, which may cause unintended reports to reach configured recipients.

Mitigation: Use a dedicated SMTP account or app password, keep EMAIL_TO and EMAIL_CC limited to intended recipients, and test with the --to option before routine use.

Risk: Broad trigger phrases may invoke the reporting workflow when the user intended a different email-related action.

Mitigation: Review the command and selected date, keywords, and recipient settings before execution, and prefer adding a preview or confirmation step in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpengle/skills/military-bidding-email)
- [ClawHub publisher profile](https://clawhub.ai/user/zhangpengle)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Plain-text email summary with an Excel report attachment and CLI status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMTP and recipient configuration before sending reports.]

## Skill Version(s):

0.2.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
