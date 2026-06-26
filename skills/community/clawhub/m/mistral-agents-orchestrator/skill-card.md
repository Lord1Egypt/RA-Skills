## Description: <br>
Multi-agent orchestration via Mistral's Agents API -- register agents, manage conversations, delegate via handoffs, bind function calling tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build multi-agent systems with Mistral models, coordinate specialist agents, and implement agent-to-agent delegation patterns. The included implementation also demonstrates story orchestration with optional audio, search, image generation, and persistence integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The implementation may send child-focused story content to Mistral and optional providers including ElevenLabs, Tavily, and Gemini. <br>
Mitigation: Review provider use before installation and do not configure optional non-Mistral API keys unless those integrations are intended. <br>
Risk: The workflow may persist child names, prompts, generated stories, audio, and images. <br>
Mitigation: Avoid entering sensitive child information and review storage, retention, and access controls before production use. <br>
Risk: The implementation does more than the Mistral-only summary suggests. <br>
Mitigation: Audit enabled endpoints and provider keys so operators understand which external services and persistence paths are active. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/mistral-agents-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MISTRAL_API_KEY; optional integrations may use additional provider keys when intentionally enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
