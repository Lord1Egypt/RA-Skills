## Description:

Memory Bridge helps an agent preserve lightweight session context across restarts by creating and maintaining local Markdown memory files for user identity, task handoff, entities, preferences, and lessons learned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwertyu7894](https://clawhub.ai/user/qwertyu7894)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Memory Bridge to give an AI assistant continuity between sessions through a small index file and on-demand Markdown records. It is useful when a workspace needs persistent context for current tasks, user preferences, project entities, and prior corrections without loading large history files at startup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reloads personal conversation context in local plaintext Markdown files.

Mitigation: Do not store passwords, API keys, private keys, financial data, or sensitive personal details in the memory files; review and delete the files regularly.

Risk: Persistent memory has weak consent, privacy, and cleanup controls.

Mitigation: Initialize memory only after explicit user confirmation, make the file locations clear, and provide deletion by removing MEMORY.md, memory/, and .learnings/.

Risk: Outdated or incorrect memory can influence later agent behavior.

Mitigation: Keep MEMORY.md as a short index, clean stale entries, and verify remembered task or preference details before relying on them.

## Reference(s):

- [Memory Bridge Skill Page](https://clawhub.ai/qwertyu7894/skills/memory-bridge)
- [MEMORY-GUIDE.md](artifact/MEMORY-GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local plaintext Markdown memory files under the user's workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
