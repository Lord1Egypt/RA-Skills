## Description: <br>
Manage business phone calls, SMS, and contacts via OpenPhone API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwhite-oss](https://clawhub.ai/user/dwhite-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to guide agents through OpenPhone API tasks such as sending SMS messages, managing contacts, listing phone numbers, and reviewing call, voicemail, recording, and transcript data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenPhone API keys can authorize access to sensitive business phone, contact, message, call, voicemail, recording, or transcript data. <br>
Mitigation: Store OPENPHONE_API_KEY as a secret, use the least-privileged key available, and avoid exposing it in prompts, logs, or shared command output. <br>
Risk: Agent actions could send messages or create contacts with incorrect recipients, content, or fields. <br>
Mitigation: Require explicit confirmation of recipients, message content, contact fields, phone number IDs, and record retrieval scope before executing API calls. <br>
Risk: Repeated API requests can hit the documented 60 requests per minute guidance in the artifact. <br>
Mitigation: Batch or throttle loops with delays and retry only after checking response status and user intent. <br>


## Reference(s): <br>
- [OpenPhone API v1](https://api.openphone.com/v1) <br>
- [ClawHub OpenPhone release](https://clawhub.ai/dwhite-oss/openphone) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl examples and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OPENPHONE_API_KEY environment variable and OpenPhone account permissions for the requested API actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
