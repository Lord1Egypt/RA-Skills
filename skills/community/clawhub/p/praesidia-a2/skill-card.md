## Description: <br>
Verify AI agents, check trust scores (0-100), fetch A2A agent cards, discover marketplace agents, and apply guardrails for security and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msoica](https://clawhub.ai/user/msoica) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security teams, and OpenClaw users use this skill to verify agent identity, inspect trust scores, discover marketplace agents, fetch A2A agent cards, and manage guardrails for agent security, compliance, and content moderation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live agent guardrails through authenticated Praesidia API calls. <br>
Mitigation: Use a scoped API key and require explicit user confirmation before applying guardrail changes to production agents. <br>
Risk: The skill can send validation text to Praesidia for guardrail checks. <br>
Mitigation: Avoid submitting confidential, regulated, or sensitive content unless sharing it with Praesidia is acceptable. <br>
Risk: Guardrail or trust-score guidance may affect agent selection and security decisions. <br>
Mitigation: Fetch current agent-card and guardrail data before making recommendations, and present trust scores with their level and relevant limitations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msoica/praesidia-a2) <br>
- [Praesidia homepage](https://praesidia.ai) <br>
- [Praesidia API documentation](https://app.praesidia.ai/docs/api) <br>
- [A2A Protocol](https://a2a-protocol.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with JSON and JavaScript request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRAESIDIA_API_KEY and may return trust scores, agent-card details, guardrail summaries, and suggested actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
