## Description:

MiniMax AI tools for web search, image analysis, LLM chat, and language translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnlangzi](https://clawhub.ai/user/cnlangzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call MiniMax services for web search, image understanding, LLM chat, streaming chat, translation, and model discovery from CLI commands or Python functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, chat history, searches, translations, and selected image files may be sent to MiniMax or to the configured API host.

Mitigation: Avoid sending sensitive prompts or local files unless that transfer is intended and approved for the deployment.

Risk: The optional MINIMAX_API_HOST override can expose API keys and request data to a non-official endpoint.

Mitigation: Use the official MiniMax API endpoint unless the alternate host is explicitly trusted and reviewed.

## Reference(s):

- [MiniMax API Reference](references/API.md)
- [Available MiniMax Models](assets/models.json)
- [MiniMax Platform](https://platform.minimaxi.com)
- [ClawHub Skill Page](https://clawhub.ai/cnlangzi/skills/minimax-use)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, code, configuration, guidance]

**Output Format:** [JSON responses, plain text model outputs, and CLI or Python usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and can use an optional MINIMAX_API_HOST override.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
