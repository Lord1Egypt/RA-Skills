## Description:

Liu Longterm Memory helps AI agents persist and recall working context through local memory files, optional vector search, git-notes, and backup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louiseliu](https://clawhub.ai/user/louiseliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add durable working memory, daily logs, semantic recall, git-notes based decisions, and backup or restore commands to AI-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store broad conversation details, including sensitive user or project information.

Mitigation: Use local-only memory by default, minimize stored sensitive data, and review memory files before sharing or syncing them.

Risk: Optional vector search or batch extraction can send memory content to external embedding or LLM providers.

Mitigation: Use a trusted provider only after review, redact sensitive data first, or choose the documented local/offline option when external processing is not acceptable.

Risk: Backup and git sync workflows can copy memory files to archives or remotes.

Mitigation: Check configured git remotes and access controls before backup, and avoid pushing memory files to untrusted or public repositories.

Risk: Restore workflows unpack archive contents into the workspace.

Mitigation: Restore only archives from trusted sources after inspecting their contents.

Risk: Unpinned npm execution or registry changes can alter the installed package source.

Mitigation: Pin the npm package version for repeatable installs and avoid global registry changes unless they are intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/louiseliu/skills/liu-longterm-memory)
- [Skill instructions and setup guide](artifact/SKILL.md)
- [English README](artifact/README.md)
- [Chinese README](artifact/README_CN.md)
- [npm package](https://www.npmjs.com/package/liu-longterm-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory files, backup archives, and git commits when the documented CLI commands are run.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter and package.json list 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
