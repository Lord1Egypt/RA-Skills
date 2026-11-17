## Description:

Lists free OpenRouter chat models and sends prompts to a selected free model through the OpenRouter API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binsonhao](https://clawhub.ai/user/binsonhao)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to discover no-cost OpenRouter chat models and run simple command-line conversations with them using a personal OpenRouter API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, chat content, and model requests are sent to OpenRouter.

Mitigation: Avoid sending secrets, regulated data, or private information in chat prompts unless OpenRouter use is approved for that data.

Risk: The script silently searches a fixed root workspace .env file for OPENROUTER_API_KEY.

Mitigation: Provide OPENROUTER_API_KEY explicitly, keep .env files out of version control, and review or remove the fallback .env lookup before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binsonhao/skills/openrouter-free)
- [ClawHub Homepage Metadata](https://clawhub.ai/skills/openrouter-free)
- [OpenRouter API](https://openrouter.ai/api/v1)
- [OpenRouter API Keys](https://openrouter.ai/settings/keys)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Command-line text, Markdown-formatted model lists, JSON model data, and chat responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and uses a 2048 token cap for chat completions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
