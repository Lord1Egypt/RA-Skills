## Description: <br>
Smart LLM routing brain for OpenClaw. Auto-dispatches tasks to Claude, GPT, Gemini, DeepSeek, Kimi via Evolink API. Cascade strategy cuts costs 60-85%. One API key, 20+ text models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route text-model tasks across Evolink-backed Claude, GPT, Gemini, DeepSeek, Kimi, and related providers. It helps choose models by user override, task type, or cascade fallback while producing routing guidance, spawn parameters, and setup configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routed prompts are sent to Evolink and upstream model providers. <br>
Mitigation: Use the skill only for data approved for Evolink and the selected providers; do not send secrets, regulated data, privileged legal material, customer records, or confidential files unless those services are approved for that data. <br>
Risk: EVOLINK_API_KEY grants access to model routing and may affect billing or account exposure if mishandled. <br>
Mitigation: Store the key securely, review Evolink billing and privacy terms, and rotate or revoke the key if exposure is suspected. <br>
Risk: Broad spawn permissions can allow sub-agents to route tasks through any configured model. <br>
Mitigation: Review and narrow spawn permissions in stricter environments instead of using unrestricted spawn access. <br>


## Reference(s): <br>
- [Evolink homepage](https://evolink.ai) <br>
- [Router API Parameter Reference](references/router-api-params.md) <br>
- [Cascade Routing Examples](references/cascade-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with model identifiers, routing decisions, API examples, JSON configuration, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sub-agent spawn parameters, timeout guidance, cleanup recommendations, and Evolink model IDs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
