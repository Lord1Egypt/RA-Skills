## Description:

将聊天记录、截图文字、链接和随手记等碎片灵感整理为可检索知识库。支持快速收录、智能分类、语义检索和灵感反刍。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nycxk](https://clawhub.ai/user/nycxk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this Chinese-language skill to capture inspiration fragments as local JSON cards, classify them with editable topic rules, search them later, and generate review prompts for older material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured notes may contain sensitive user-provided text because the skill stores material in a local JSON database.

Mitigation: Use an approved local storage path, avoid capturing secrets, and review the JSON database before sharing, syncing, or migrating it.

Risk: Path override environment variables can direct the skill to create or update unintended local files.

Mitigation: Set INSPIRATION_DB_PATH and INSPIRATION_TOPIC_RULES_PATH only to dedicated skill data and configuration files.

## Reference(s):

- [Reference Guide](artifact/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/nycxk/skills/inspiration-material-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill stores captured material in a local JSON database and uses editable JSON topic rules.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
