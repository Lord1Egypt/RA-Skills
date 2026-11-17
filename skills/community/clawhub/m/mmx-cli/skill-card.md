## Description:

MiniMax CLI (mmx) guides agents in using the mmx command-line tool for MiniMax text, image, video, speech, music, vision, search, quota, configuration, and diagnostic workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sswhite](https://clawhub.ai/user/sswhite)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and external agents use this skill to install or configure mmx and run MiniMax multimodal generation, vision understanding, text chat, search, quota, and diagnostic commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if users paste credentials into agent chats or shell commands that are stored in history.

Mitigation: Use a secure secret-handling path for MiniMax credentials and avoid placing API keys directly in prompts or command lines.

Risk: Unpinned global installation of mmx-cli can introduce supply-chain risk.

Mitigation: Install a pinned, trusted mmx-cli release and review the package source before use.

Risk: Prompts, local files, image URLs, search queries, and callback URLs may be sent to MiniMax or related services during command execution.

Mitigation: Review inputs for sensitive data before running mmx commands and use only approved callback endpoints.

## Reference(s):

- [MiniMax CLI repository referenced by the skill](https://github.com/MiniMax-AI/cli)
- [ClawHub skill page](https://clawhub.ai/sswhite/skills/mmx-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/sswhite)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that generate local media files or send prompts, local files, image URLs, search queries, and callback URLs to MiniMax-related services.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
