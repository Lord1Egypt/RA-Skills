## Description:

为 OpenCode AI 助手提供轻量级记忆持久化，面向灵芯派等低资源设备保存跨会话上下文并支持 Gitee 同步。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmww](https://clawhub.ai/user/nmww)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenCode on SmartPi, ARM64, Debian, or other low-resource devices use this skill to preserve local memory across sessions, restore recent context, and sync notes to a Git remote for backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes plaintext device credentials and specific device details.

Mitigation: Remove the credentials, rotate them if they are real, and replace device-specific values with placeholders before use or publication.

Risk: The sync script stages all changes and pushes memory contents to a configured Git remote.

Mitigation: Keep the remote repository private, restrict what memory files are synced, and review contents for secrets, tokens, private project data, or personal information before running sync.sh.

Risk: Memory files can preserve sensitive local context across sessions.

Mitigation: Audit MEMORY.md, daily logs, and indexes before sharing or syncing, and avoid storing private credentials or personal information in the memory directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nmww/skills/opencode-lingxin-memory1)
- [Publisher profile](https://clawhub.ai/user/nmww)
- [Artifact homepage](https://gitee.com/st_gitee_1/old-version-of-lingxin-sect)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included scripts create and sync files under ~/.opencode-memory when run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
