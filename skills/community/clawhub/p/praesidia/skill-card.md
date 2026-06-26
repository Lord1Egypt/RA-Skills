## Description: <br>
Verify AI agents, check trust scores, fetch A2A agent cards, discover marketplace agents, and apply guardrails for security and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msoica](https://clawhub.ai/user/msoica) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to check agent identity and trust scores, discover suitable public agents, and configure or validate guardrails for security, privacy, and compliance needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Praesidia API requests can expose agent metadata or message content selected for guardrail validation to a third-party service. <br>
Mitigation: Use a scoped API key where possible and avoid sending sensitive content unless validation is necessary. <br>
Risk: Applying guardrails can change agent behavior or block, redact, replace, retry, or escalate content unexpectedly if the target agent, scope, or action is wrong. <br>
Mitigation: Review the agent ID, organization ID, guardrail scope, action, severity, and rollback path before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/msoica/praesidia) <br>
- [Praesidia Homepage](https://praesidia.ai) <br>
- [Praesidia API Documentation](https://app.praesidia.ai/docs/api) <br>
- [A2A Protocol](https://a2a-protocol.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, markdown, configuration] <br>
**Output Format:** [Markdown with API request examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRAESIDIA_API_KEY for authenticated Praesidia API requests.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
