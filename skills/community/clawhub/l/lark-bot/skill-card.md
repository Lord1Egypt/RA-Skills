## Description:

Feishu/Lark Bot API wrapper for full-featured Feishu bot interactions, including sending text, image, audio, file, post, interactive, and share messages; Markdown delivery with card or post routing; file upload and download; user and group queries; and incoming-message listening with LarkBotListener.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate a Feishu/Lark bot for chat messaging, Markdown message formatting, file transfer, user and group lookup, and asynchronous message handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot credentials can grant access to Lark/Feishu chats, users, groups, and files.

Mitigation: Use least-privilege app credentials, store secrets securely, and restrict the bot to intended chats.

Risk: File upload and download workflows can expose sensitive local files or persist untrusted attachments.

Mitigation: Review files before upload, save downloads only in temporary or controlled directories, and clean them up after processing.

Risk: Message listeners can act on unintended chats or duplicate incoming events.

Mitigation: Scope handlers to intended chats or users, validate message context before acting, and keep de-duplication enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/lark-bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Lark/Feishu app credentials and target user, chat, file, or message identifiers.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
