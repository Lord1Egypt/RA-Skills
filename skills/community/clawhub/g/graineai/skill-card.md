## Description: <br>
Manage voice agents, place and transfer calls, handle telephony events, and retrieve call records using the NoddyAI API at graine.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabh171998](https://clawhub.ai/user/rishabh171998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to construct authenticated Graine/NoddyAI API requests for voice-agent management, outbound and inbound telephony, call transfers, batch calls, webhook handling, and call-record retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Phone-call workflows can expose phone numbers, transcripts, summaries, and recording links. <br>
Mitigation: Use the skill only with an explicit privacy, consent, call-recording, retention, and access-control policy appropriate for the deployment. <br>
Risk: Outbound calls, batch calls, transfers, token revocation, agent deletion, and webhook URL changes are high-impact operations. <br>
Mitigation: Require explicit user confirmation before executing these actions, including the exact phone numbers, agent IDs, tokens, or URLs affected. <br>
Risk: Credential mishandling could expose Graine/NoddyAI API keys or organization identifiers. <br>
Mitigation: Load credentials only from the user or host secret store, never from skill text, and redact Bearer tokens in any displayed headers or logs. <br>
Risk: Webhook configuration can route call events to unintended endpoints. <br>
Mitigation: Set or update webhook URLs only after the user confirms the endpoint is under their control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rishabh171998/graineai) <br>
- [NoddyAI API skill instructions](artifact/SKILL.md) <br>
- [NoddyAI API endpoints reference](artifact/endpoints.md) <br>
- [NoddyAI request body examples](artifact/examples.md) <br>
- [NoddyAI webhook payloads](artifact/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with HTTP request details, curl examples, JSON request bodies, and webhook payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user- or host-supplied Graine/NoddyAI credentials and organization identifiers; outputs should redact Bearer tokens when echoed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
