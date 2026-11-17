## Description:

Feishu/Lark message listener for real-time WebSocket message processing with async handlers, message deduplication, attachment cleanup, and optional replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Feishu/Lark bot listeners that process text, image, file, and rich post messages in real time. It is suited for agents that need to provide integration guidance, Python handler examples, and safe handling notes for message and attachment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot credentials and incoming Feishu/Lark messages or attachments may be sensitive.

Mitigation: Keep app_id and app_secret out of source control, grant only required bot permissions, and treat incoming content as sensitive.

Risk: Handlers that automatically reply or re-send files can expose processed content to unintended chats.

Mitigation: Review handler code and chat routing before enabling automatic replies or file sends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/lark-bot-listener)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for app credentials, async handlers, message filtering, temporary file handling, and automatic replies.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
