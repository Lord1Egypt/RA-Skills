## Description:

Analyzes images with OpenRouter's vision API using x-ai/grok-4.1-fast and returns concise descriptions, explanations, or interpretations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gawainchin](https://clawhub.ai/user/gawainchin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route image-description and image-interpretation requests through OpenRouter's vision API when an OpenRouter API key and public image URL are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, image URLs, and prompts are sent to OpenRouter for analysis.

Mitigation: Do not use the skill with private, sensitive, regulated, or confidential images unless the provider's data-handling terms have been reviewed and accepted.

Risk: The skill requires an OpenRouter API key and publicly accessible image URLs.

Mitigation: Confirm OPENROUTER_API_KEY is configured and use only intended public HTTP/HTTPS image URLs.

## Reference(s):

- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/gawainchin/skills/openrouter-vision-skill)
- [Publisher profile](https://clawhub.ai/user/gawainchin)

## Skill Output:

**Output Type(s):** [Analysis, API calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON API request examples and parsed text response content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and sends image URLs, uploaded image content, and prompts to OpenRouter; the documented response token range is 500-2000.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
