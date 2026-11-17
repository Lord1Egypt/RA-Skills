## Description:

OpenClaw Diary Core helps an assistant record user thoughts, article discussions, and collaboration notes to local Markdown, with optional Feishu synchronization and configurable interaction styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smorzandos](https://clawhub.ai/user/smorzandos)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to capture diary entries from conversations, shared articles, and collaborative work. The skill is intended for personal journaling workflows that store Markdown locally by default and can optionally synchronize entries to Feishu when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may capture and persist sensitive personal thoughts, article discussions, and collaboration notes.

Mitigation: Install only for intentional journaling use, review entries before sharing them, and choose a local storage path with appropriate filesystem protections.

Risk: Optional Feishu synchronization can send diary content to an external service when enabled.

Mitigation: Keep Feishu sync disabled unless external synchronization is desired, and verify Feishu credentials, folder settings, and document access controls before use.

Risk: The configured user identity feature may read profile and preference files to tailor responses.

Mitigation: Disable user_identity or review the configured identity directory before use if profile or preference files should not be read.

Risk: Configurable personality.file and storage paths affect what files are read or written.

Mitigation: Review diary-config.json before installation and keep personality and storage paths pointed only at expected local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smorzandos/skills/openclaw-diary-core)
- [Project homepage from ClawHub metadata](https://github.com/openclaw-community/diary-system)
- [Publisher profile](https://clawhub.ai/user/smorzandos)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown diary entries and concise status guidance, with shell commands or JSON configuration snippets when setup or troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write monthly local Markdown diary files and, when Feishu is enabled, may create or update Feishu documents.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
