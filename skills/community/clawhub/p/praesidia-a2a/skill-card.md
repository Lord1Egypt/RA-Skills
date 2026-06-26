## Description: <br>
Verify AI agents, check trust scores (0-100), fetch A2A agent cards, discover marketplace agents, and apply guardrails for security and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msoica](https://clawhub.ai/user/msoica) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to verify A2A agents, inspect trust scores, discover public marketplace agents, and configure or validate Praesidia guardrails for security, compliance, and content moderation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read organization-scoped agent and security data and can change Praesidia guardrails. <br>
Mitigation: Use a least-privilege Praesidia API key and require explicit preview and approval of the organization, agent, template, scope, action, severity, and enabled state before guardrail changes. <br>
Risk: A misconfigured Praesidia API endpoint or overbroad key could send requests to the wrong service or expose more data than intended. <br>
Mitigation: Verify PRAESIDIA_API_URL before use, keep PRAESIDIA_API_KEY scoped to the intended account or organization, and avoid using this skill for generic security discussion unless Praesidia API calls are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msoica/praesidia-a2a) <br>
- [Praesidia homepage](https://praesidia.ai) <br>
- [Praesidia API documentation](https://app.praesidia.ai/docs/api) <br>
- [A2A protocol](https://a2a-protocol.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown with JSON and JavaScript request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRAESIDIA_API_KEY for private Praesidia data and guardrail changes; PRAESIDIA_API_URL may override the default API base URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
