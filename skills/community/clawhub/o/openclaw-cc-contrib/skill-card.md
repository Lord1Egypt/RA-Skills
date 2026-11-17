## Description:

Openclaw Cc Contrib provides OpenClaw skills for extracting, organizing, and consolidating conversation memories, plus a prompt-based code simplification review skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jofiction918](https://clawhub.ai/user/jofiction918)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill bundle to retain useful conversation memories, organize and consolidate memory topics, and request structured simplification reviews of code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save conversation details into long-term memory files.

Mitigation: Use it only in conversations where long-term note retention is intended, and avoid chats containing secrets, credentials, private URLs, or sensitive account details.

Risk: Background consolidation can rewrite or delete memory content.

Mitigation: Disable or avoid the cron job unless background consolidation is desired, and keep backups of memory files before enabling automated workflows.

Risk: Memory extraction may persist inaccurate or unwanted details.

Mitigation: Review proposed memories before saving when possible and periodically audit MEMORY.md and topic files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jofiction918/skills/openclaw-cc-contrib)
- [OpenClaw](https://openclaw.org/)
- [WeaveMind](https://weavemind.com)
- [simplify prompt template](simplify/references/prompt-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, memory topic files, index updates, shell commands, and structured review proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows read, append, rewrite, or delete local memory files after trigger conditions or user approval.]

## Skill Version(s):

1.0.12 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
