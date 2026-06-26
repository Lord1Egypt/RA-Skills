## Description: <br>
Verify AI agents, check trust scores (0-100), fetch A2A agent cards, discover marketplace agents, and apply guardrails for security and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msoica](https://clawhub.ai/user/msoica) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI operators use this skill to verify agent identities, inspect trust scores, discover marketplace agents, retrieve A2A agent cards, and manage security or compliance guardrails through Praesidia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user content and agent details to an external Praesidia service. <br>
Mitigation: Use a scoped API key when available and avoid sending secrets, regulated data, or private content unless external processing is intended. <br>
Risk: Guardrail changes can persist and affect production agent behavior. <br>
Mitigation: Require explicit user confirmation before applying, changing, or enabling guardrails, and review the target agent and organization before submitting API requests. <br>
Risk: Trust scores and verification results may influence whether users rely on third-party agents. <br>
Mitigation: Present trust scores, levels, verification status, and compliance details clearly so users can make their own deployment decision. <br>


## Reference(s): <br>
- [Praesidia](https://praesidia.ai) <br>
- [Praesidia API Documentation](https://app.praesidia.ai/docs/api) <br>
- [A2A Protocol](https://a2a-protocol.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/msoica/praesidia-ai-a2a) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Markdown, Configuration] <br>
**Output Format:** [Markdown with API request examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PRAESIDIA_API_KEY and may call Praesidia API endpoints when the agent follows the skill guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
