## Description: <br>
Makes AI-powered outbound phone calls through Twilio using ElevenLabs voices and an OpenAI-powered conversation brain for one-way messages or live two-way calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omerflo](https://clawhub.ai/user/omerflo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and run AI-assisted outbound calls for voice messages, scheduling, reservations, appointments, campaigns, and live phone conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact real people through outbound phone calls. <br>
Mitigation: Require explicit confirmation before each call and verify the recipient, purpose, and applicable consent rules before dialing. <br>
Risk: Call content may pass through Twilio, ElevenLabs, OpenAI, tunnel services, temporary audio hosting, and local messaging. <br>
Mitigation: Avoid sensitive call content unless those services and data paths are approved for the use case. <br>
Risk: Interactive call webhooks may be exposed through a public tunnel. <br>
Mitigation: Authenticate Twilio webhook requests before accepting call events or transcript data. <br>
Risk: Temporary logs, hosted audio, cron jobs, and automatic iMessage summaries may persist or run beyond the intended call. <br>
Mitigation: Clean up temporary files and hosted audio, verify MASTER_PHONE, and disable scheduled jobs or automatic summaries when they are not needed. <br>


## Reference(s): <br>
- [ElevenLabs Voice Reference](references/voices.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/omerflo/phone-caller) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions that can trigger external side effects, including outbound calls, generated audio, webhook traffic, temporary files, and call summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
