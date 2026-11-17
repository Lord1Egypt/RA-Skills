## Description:

Memory Focal System manages AI assistant memory with message classification, on-demand memory loading, automatic tags, a forgetting curve, and claimed 40-60% token optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcz-user](https://clawhub.ai/user/zcz-user)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this OpenClaw skill to classify conversation messages into memory modes, load relevant stored memories, and persist new preferences or rules when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist raw conversation text by default.

Mitigation: Review the memory behavior before installation, disable auto_write unless intentional, and avoid storing secrets or sensitive personal data.

Risk: Stored memory files may retain sensitive or outdated content.

Mitigation: Inspect and clear the memory-focal data files regularly, and keep backups only where appropriate.

Risk: Classifier code is loaded from a mutable external workspace path.

Mitigation: Do not use this package where the memory-focal scripts directory can be modified by untrusted code or users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zcz-user/skills/memory-focal-system)
- [Publisher profile](https://clawhub.ai/user/zcz-user)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell command, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-like memory context summaries and append-only JSONL memory records when memory writing is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
