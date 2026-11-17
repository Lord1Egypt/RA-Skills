## Description:

Send files to Feishu/Lark users and groups via the message tool, with guidance for file path validation, recipient selection, captions, and delivery formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare Feishu/Lark message-tool sends for local files such as documents, reports, images, archives, and generated outputs. It is most useful when an agent needs to validate a file path, choose a user or chat target, and include an optional caption before sharing a file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help an agent send local files to external Feishu/Lark users or chats, which may expose sensitive or unintended content.

Mitigation: Require confirmation of the exact file path, recipient or chat, and caption before each send, and avoid sending files whose contents have not been reviewed.

Risk: The helper formats send commands from file paths and message text, and untrusted input could produce misleading or unsafe command text.

Mitigation: Use trusted filenames and captions, quote or escape values before use, and review the final command before execution.

Risk: The artifact gives broad file-sharing examples without enforcing confirmation safeguards.

Mitigation: Adopt a policy that requires explicit user approval before every external file send, especially for generated reports, archives, and batch transfers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skills/lark-file-sender)
- [README](artifact/README.md)
- [Usage examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples and tool-call snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces message-tool send commands and optional file-checking guidance; does not generate or transform the shared file.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
