## Description:

Uses ncm-cli to operate NetEase Cloud Music, including playback, song search, playback controls, queue management, status checks, and playlist playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junfengl](https://clawhub.ai/user/junfengl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent operate NetEase Cloud Music through ncm-cli for music search, playback, queue control, login guidance, and playlist actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards contextual summaries of recent conversation to ncm-cli for non-playback actions.

Mitigation: Review and minimize the summary before execution, and avoid using the skill when recent conversation contains private or sensitive information.

Risk: API private keys may be exposed through visible command lines, chat history, shell history, or process inspection.

Mitigation: Use a secure credential flow or protected configuration mechanism if ncm-cli supports one, and avoid pasting private keys into chat or visible terminal commands.

Risk: The skill can initiate login, playback, search, playlist, and queue-management commands on the user's local environment.

Mitigation: Confirm the installed ncm-cli is trusted, inspect command help when parameters are unclear, and review proposed commands before running them.

## Reference(s):

- [NetEase Cloud Music Open Platform API Key documentation](https://developer.music.163.com/st/developer/document?docId=9504d35aa41a47c6ac9830b2dbf48f94)
- [ClawHub skill page](https://clawhub.ai/junfengl/skills/netease-music-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and music service links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ncm-cli commands, login links, API key configuration guidance, and NetEase Cloud Music resource URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
