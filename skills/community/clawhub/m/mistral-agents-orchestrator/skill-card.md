## Description:

Multi-agent orchestration via Mistral's Agents API to register agents, manage conversations, delegate via handoffs, and bind function-calling tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Mistral-based multi-agent applications where an orchestrator coordinates specialist agents for conversations, handoffs, structured responses, and tool-backed story or audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release presents a Mistral-focused orchestrator, while security evidence reports additional paid AI services and storage behavior.

Mitigation: Deploy only with intended provider keys, disclose enabled providers, and remove or disable unused ElevenLabs, Tavily, Gemini, database, and prompt-cache integrations.

Risk: Generated story workflows can store child-related names, prompts, language, story content, audio, and images.

Mitigation: Run behind authentication, quotas, access controls, and explicit retention policies before collecting or storing user data.

Risk: Outbound calls to external model, search, audio, and image services can transmit prompts or generated media and may incur provider costs.

Mitigation: Use scoped credentials, provider allowlists, rate limits, logging review, and tenant isolation for production deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/mistral-agents-orchestrator)
- [ClawHub publisher profile](https://clawhub.ai/user/nissan)
- [Mistral API endpoint](https://api.mistral.ai)
- [ElevenLabs Text-to-Speech endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})
- [Tavily search endpoint](https://api.tavily.com/search)
- [Gemini generation endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, API patterns, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MISTRAL_API_KEY. Optional behavior may use ElevenLabs, Tavily, Gemini, database, and prompt-cache integrations when enabled.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
