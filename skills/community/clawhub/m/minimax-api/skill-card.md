## Description:

Enables image understanding and web search via MiniMax's Token Plan API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew77](https://clawhub.ai/user/matthew77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to describe or extract information from images and to retrieve current web search results through MiniMax APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, search queries, and selected image contents are sent to MiniMax.

Mitigation: Do not submit secrets, confidential documents, sensitive screenshots, or private URLs unless that upload is intended and approved.

Risk: The image client can upload arbitrary local files or fetched internal URLs to MiniMax without strong validation, size limits, or consent checks.

Mitigation: Use only intended image files or public image URLs; add file validation, private-network URL blocking, size limits, and explicit upload confirmation before broad deployment.

Risk: Passing the API key directly on the command line can expose it in shell history or process listings.

Mitigation: Prefer a safer credential source and avoid entering API keys directly in reusable shell commands.

## Reference(s):

- [MiniMax Token Plan API Specification](references/api_spec.md)
- [MiniMax Platform](https://platform.minimaxi.com)
- [ClawHub Skill Page](https://clawhub.ai/matthew77/skills/minimax-api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text image descriptions and formatted or JSON-style web search results, with shell command examples for setup and use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key and sends prompts, search queries, and selected image contents to MiniMax.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
