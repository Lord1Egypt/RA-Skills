## Description: <br>
Message Chunker helps an agent split long outgoing messages into platform-sized chunks, especially to avoid Feishu message length limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[As9530272755](https://clawhub.ai/user/As9530272755) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and workflow developers use this skill to keep long reports, plans, logs, tables, and other multi-section replies within chat platform message limits. It guides chunking by headings, tables, paragraphs, and explicit chunk markers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A single response may be sent as several messages, which can increase exposure in sensitive or public chats. <br>
Mitigation: Review the full response before sending and avoid using the skill for sensitive chats unless multi-message delivery is acceptable. <br>
Risk: Failed chunks may be retried or queued by the host environment. <br>
Mitigation: Check the send status after chunking and remove or reconcile failed queued chunks before retrying. <br>
Risk: Chunking can separate context across messages, especially around tables or section boundaries. <br>
Mitigation: Prefer heading, table, or paragraph boundaries and include continuation markers when a message is split. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/As9530272755/message-chunker) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Chunked plain text or Markdown messages with optional continuation markers and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses platform character limits and prefers splitting at headings, tables, paragraph boundaries, or explicit chunk markers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact config.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
