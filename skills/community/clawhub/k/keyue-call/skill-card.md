## Description:

Creates immediate or scheduled Baidu AIOB outbound call tasks using configured credentials, command-line overrides, and natural-language details mapped to call dialog variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangchengzc](https://clawhub.ai/user/zhangchengzc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create Baidu AIOB outbound calls for reminders, notifications, and follow-ups. It supports immediate calls, one-shot delayed calls through OpenClaw cron, and extraction of phone number, recipient name, requester identity, message intent, and schedule from natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real outbound phone calls.

Mitigation: Confirm recipient number, message content, and schedule before creating any immediate or scheduled call.

Risk: AIOB credentials and access tokens are sensitive.

Mitigation: Use dedicated low-privilege AIOB credentials, keep them out of chat-visible output and logs, and rotate them if exposure is suspected.

Risk: Call details may include personal information.

Mitigation: Restrict access to configuration files and logs, and avoid storing or displaying unnecessary phone numbers or call content.

## Reference(s):

- [AIOB authentication reference](references/aiob-auth.md)
- [AIOB realtime outbound task reference](references/aiob-realtime-task.md)
- [Natural-language extraction rules](references/extraction-rules.md)
- [Baidu AIOB getToken API](https://aiob-open.baidu.com/api/v2/getToken)
- [Baidu AIOB realtime outbound task API](https://aiob-open.baidu.com/api/v3/console/realtime/status/create)
- [ClawHub skill page](https://clawhub.ai/zhangchengzc/skills/keyue-call)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON request/response output from the call script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create real outbound phone call tasks through Baidu AIOB when executed with valid credentials and recipient details.]

## Skill Version(s):

1.0.5 (source: server release metadata and user-supplied target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
