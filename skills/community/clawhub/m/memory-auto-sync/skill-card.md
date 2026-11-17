## Description:

Automatically records user and assistant text conversations to daily Markdown files and OpenClaw memory storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tao-articism](https://clawhub.ai/user/tao-articism)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can use this skill to keep a persistent daily Markdown and memory-store record of user-assistant conversations. It is intended for users who explicitly want conversation text retained long term for later recall or search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic long-term retention of all user and assistant text can capture sensitive, regulated, or credential-like content.

Mitigation: Enable the skill only in environments where persistent conversation recording is intentional, and avoid sharing passwords, tokens, private documents, or regulated data while it is active.

Risk: Conversation records are written to both local Markdown files and OpenClaw memory storage with limited user-facing controls described in the evidence.

Mitigation: Before deployment, verify the storage locations, retention expectations, access permissions, and deletion process for both Markdown files and OpenClaw memory records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tao-articism/skills/memory-auto-sync)
- [Publisher profile](https://clawhub.ai/user/tao-articism)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown memory entries and OpenClaw memory records, with explanatory Markdown guidance for users.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records text conversations persistently and automatically when enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact package.json declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
