## Description:

OpenClaw Diary Setup guides users through initializing an OpenClaw diary system, including personality selection, optional user profile creation, storage setup, authorization collection, and configuration generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smorzandos](https://clawhub.ai/user/smorzandos)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to set up a personal diary workflow, create local configuration files, and optionally connect identity import or sync services such as Feishu, Notion, and Flomo. It is intended for normal ClawHub release use rather than a demo or research-only workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may install global packages or dependent skills.

Mitigation: Review install commands before execution and prefer manual, pinned installs from trusted package sources.

Risk: The skill can collect or store cloud-service credentials for Feishu, Notion, Flomo, or other import sources.

Mitigation: Use short-lived or scoped credentials where possible, avoid pasting long-lived secrets into chat, and do not store secrets in shell profiles unless that matches local security policy.

Risk: Diary entries, identity profiles, and imported digital-life data may be stored locally or synchronized to third-party services.

Mitigation: Review each selected source and destination path before import or sync, and use local-only storage when cloud synchronization is not required.

## Reference(s):

- [OpenClaw Diary System Homepage](https://github.com/openclaw-community/diary-system)
- [ClawHub Skill Page](https://clawhub.ai/smorzandos/skills/openclaw-diary-setup)
- [Notion MCP Documentation](https://developers.notion.com/docs/mcp)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup dialogue, dependency-install commands, directory-creation commands, diary configuration JSON, and credential-handling guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
