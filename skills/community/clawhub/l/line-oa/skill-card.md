## Description:

Operate LINE Official Account Manager (chat.line.biz) via browser automation to check messages, reply to customers, and manage the LINE OA chat interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picseeinc](https://clawhub.ai/user/picseeinc)

### License/Terms of Use:

MIT

## Use Case:

Customer support and operations teams use this skill to work with LINE Official Account Manager through an agent-controlled browser. It helps check unread chats, review message history, reply to customers, manage notes and tags, and switch official accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer chat content can be accessed or exported from a logged-in LINE OA browser session.

Mitigation: Use only with authorized LINE OA accounts, require explicit confirmation before exporting customer images, and use a skill-specific download folder.

Risk: The skill can send replies and manage notes or tags in a live business account.

Mitigation: Require human confirmation before customer-facing replies or account-record changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/picseeinc/skills/line-oa)
- [Publisher profile](https://clawhub.ai/user/picseeinc)
- [LINE Official Account Manager](https://chat.line.biz/)
- [LINE Official Account Manager entry](https://manager.line.biz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with JavaScript snippets, browser actions, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize LINE OA chat data and guide browser actions in an isolated OpenClaw session.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
