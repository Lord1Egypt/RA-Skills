## Description:

MiniMax MMX helps agents use the MMX CLI to access MiniMax multimodal capabilities, including image generation, video generation, speech synthesis, music creation, image understanding, web search, and text chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clx20000410](https://clawhub.ai/user/clx20000410)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to invoke MiniMax's MMX CLI for multimodal generation, analysis, search, and chat tasks from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global npm CLI package.

Mitigation: Install only if the mmx-cli package and MiniMax service are trusted, and prefer a pinned or local install.

Risk: Command-line or chat-based API key entry can expose credentials through shell history, logs, or agent transcripts.

Mitigation: Avoid entering API keys directly in command lines or agent chats; use a safer local authentication flow or secret handling mechanism when available.

Risk: Prompts, images, search queries, and generated media requests are sent to an external provider.

Mitigation: Do not send confidential prompts, images, or queries unless sharing them with the MiniMax service is intended and approved.

## Reference(s):

- [MMX-CLI detailed command reference](references/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce JSON responses and generated media files through the external MiniMax service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
