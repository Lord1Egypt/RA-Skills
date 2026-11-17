## Description:

Provides a Node.js chat helper for using OpenRouter-compatible free model tiers as a GPT-5.5-like demonstration experience.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[leic8959-sudo](https://clawhub.ai/user/leic8959-sudo)

### License/Terms of Use:

MIT

## Use Case:

Developers and learners use this skill to run a local Node.js chat helper against OpenRouter-compatible free models for experimentation and demonstrations. It is not positioned for production high-concurrency workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key and prompts may be sent to any endpoint configured through OPENROUTER_API_URL.

Mitigation: Use only the default trusted HTTPS endpoint or a controlled compatible endpoint, and do not set OPENROUTER_API_URL to an untrusted destination.

Risk: Confidential prompts may be disclosed to the selected API or model provider.

Mitigation: Do not submit sensitive prompts unless the provider's data handling terms are acceptable for the intended use.

Risk: The documented free model tiers have rate limits and are not recommended for production high-concurrency workloads.

Mitigation: Use this as a learning or demonstration helper, or add provider review, throttling, monitoring, and operational controls before broader deployment.

## Reference(s):

- [OpenRouter](https://openrouter.ai)
- [ClawHub skill page](https://clawhub.ai/leic8959-sudo/skills/gpt5-5free)
- [Publisher profile](https://clawhub.ai/user/leic8959-sudo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and JavaScript examples; the CLI returns plain text model responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; supports an optional OPENROUTER_API_URL endpoint override and model selection in code.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
