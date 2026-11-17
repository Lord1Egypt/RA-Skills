## Description:

OpenRouter API gateway skill for accessing 300+ AI models from 60+ providers through a single OpenAI-compatible API with unified billing, automatic fallbacks, provider routing, and BYOK support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and teams use this skill to configure OpenRouter access, select models and providers, and call an OpenAI-compatible endpoint through shell or SDK examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, attachments, and outputs may be processed by OpenRouter and routed to selected model providers.

Mitigation: Avoid secrets or regulated data unless provider routing, logging restrictions, zero data retention, and required compliance controls are configured.

Risk: The OPENROUTER_API_KEY grants access to the user's OpenRouter credit balance and enabled models.

Mitigation: Store the key in a secrets manager or environment variable, send it only to openrouter.ai, and configure spending limits where appropriate.

Risk: Model availability, pricing, and provider behavior can change after release.

Mitigation: Pin specific model IDs for production workflows and review current OpenRouter model pricing and status before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jononovo/skills/openrouter)
- [OpenRouter homepage](https://openrouter.ai)
- [OpenRouter API base](https://openrouter.ai/api/v1)
- [OpenRouter model catalog and pricing](https://openrouter.ai/models)
- [OpenRouter documentation](https://openrouter.ai/docs)
- [OpenRouter status page](https://status.openrouter.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and uses the OpenRouter OpenAI-compatible API base URL.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
