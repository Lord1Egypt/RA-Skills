## Description: <br>
Creates Baidu AIOB outbound call tasks for immediate calls, scheduled reminders, and calls that pass extracted name, caller identity, and message intent into dialog variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangchengzc](https://clawhub.ai/user/zhangchengzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Baidu AIOB credentials, extract call parameters from natural-language requests, and create one-off or scheduled outbound call tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound phone calls. <br>
Mitigation: Confirm the recipient, permission to call, scheduled time, and message content before running or scheduling the call. <br>
Risk: The skill uses access keys, secret keys, access tokens, phone numbers, and call content. <br>
Mitigation: Keep credentials, tokens, phone numbers, and call content out of shared logs, repositories, and user-visible responses; rotate credentials if exposed. <br>
Risk: A call to the wrong recipient can occur if a default phone number is used for someone other than the user. <br>
Mitigation: Use the default phone number only for explicit self-calls and require an explicit phone number for third-party recipients. <br>


## Reference(s): <br>
- [AIOB Authentication](references/aiob-auth.md) <br>
- [AIOB Realtime Outbound Call Task](references/aiob-realtime-task.md) <br>
- [Natural Language Parameter Extraction Rules](references/extraction-rules.md) <br>
- [Baidu AIOB getToken API](https://aiob-open.baidu.com/api/v2/getToken) <br>
- [Baidu AIOB realtime task API](https://aiob-open.baidu.com/api/v3/console/realtime/status/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API request/response output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or schedules one outbound call task at a time and may print request and response JSON from the helper script.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
