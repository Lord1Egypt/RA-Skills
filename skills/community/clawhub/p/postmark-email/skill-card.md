## Description: <br>
Inspect transactional email activity, manage templates, review message delivery events, and configure webhooks in Postmark via the Postmark API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Postmark transactional email activity, manage message templates and streams, review delivery, bounce, spam, and engagement data, and configure transactional email webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawLink brokers access to the user's Postmark account. <br>
Mitigation: Install only if the user trusts ClawLink to handle the Postmark connection and avoid pasting real API tokens or authorization headers into chat examples. <br>
Risk: Create, update, delete, suppression, webhook, template, and server-configuration actions can change Postmark resources. <br>
Mitigation: Review the target resource and intended effect before confirming any write action. <br>


## Reference(s): <br>
- [Postmark API Documentation](https://postmarkapp.com/developer/api/overview) <br>
- [Postmark Message Streams API](https://postmarkapp.com/developer/api/message-streams) <br>
- [Postmark Templates API](https://postmarkapp.com/developer/api/templates) <br>
- [Postmark Webhooks API](https://postmarkapp.com/developer/api/webhooks) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Postmark account through ClawLink; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
