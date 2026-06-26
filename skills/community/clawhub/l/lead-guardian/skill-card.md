## Description: <br>
Lead Guardian provides an AI-assisted workflow for responding to real estate leads, qualifying intent and readiness, tracking conversations, and handing off hot leads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonbarnato](https://clawhub.ai/user/jonbarnato) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real estate agents and teams use this skill to respond quickly to inbound buyer or seller leads, qualify timeline, pre-approval, budget, and intent, and route high-priority leads for direct follow-up. <br>

### Deployment Geography for Use: <br>
United States, with default prompt content tailored to Sacramento, California <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive lead conversation data and workflow controls may be exposed without adequate access controls. <br>
Mitigation: Require authentication and authorization for the dashboard and APIs, restrict network exposure, and define consent, retention, deletion, and privacy practices before deployment. <br>
Risk: SMS webhook processing can be abused if inbound requests are not verified. <br>
Mitigation: Validate Twilio webhook signatures and reject unauthenticated webhook requests. <br>
Risk: Provider API keys and messaging spend can be misused. <br>
Mitigation: Use dedicated Twilio and OpenRouter keys with spending limits, rotate credentials, and monitor usage. <br>
Risk: Debug mode and broad network binding can expose application internals in production. <br>
Mitigation: Disable debug mode and run behind a production server with controlled host binding and network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonbarnato/lead-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [SMS text responses, JSON API responses, HTML dashboard, and Markdown setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Twilio and OpenRouter credentials; stores lead conversations in a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
