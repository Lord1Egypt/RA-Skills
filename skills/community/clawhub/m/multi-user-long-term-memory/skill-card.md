## Description:

This skill lets an agent maintain separate Markdown long-term memory files for multiple users by deriving a username from sender_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an OpenClaw agent persistent per-user context across sessions in multi-user chats or conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local persistent memory can retain user identifiers, preferences, and context indefinitely.

Mitigation: Use the skill only with user consent and define a process to review, delete, and retire stored memory files.

Risk: The sender_id-to-filename mapping can collide when different sessions or users share the same prefix before the pipe character.

Mitigation: Use trusted caller identities and verify that sender_id prefixes are unique for the deployment before sharing the memory directory.

Risk: Stored memory content is untrusted user data and may later influence agent behavior.

Mitigation: Review memory contents before relying on them for consequential actions and treat retrieved memories as untrusted context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/multi-user-long-term-memory)
- [README.md](README.md)
- [user-memory.js](references/user-memory.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown memory files with JavaScript API and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local files are persisted under the skill's users directory; evidence reports no external dependency or network behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
