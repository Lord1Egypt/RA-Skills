## Description: <br>
This skill helps agents use the workspace mailbox protocol under .mailbox, including reading inbox items, composing private scratch replies, and delivering completed messages to reply inbox paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoustc](https://clawhub.ai/user/leoustc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to exchange structured Markdown mailbox messages between agent workspaces, with preserved request IDs, channel metadata, and reply routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox metadata and local Markdown can steer message routing and file writes. <br>
Mitigation: Install only in trusted workspaces, require path canonicalization, and keep inbox and reply paths inside approved .mailbox/inbox directories. <br>
Risk: Context from one sender or channel could be applied to the wrong mailbox reply. <br>
Mitigation: Preserve REQUEST_ID and CHANNEL_ID, reply one message at a time, and avoid cross-sender or cross-channel context sharing without explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leoustc/mailbox-skill) <br>
- [Send flow example](references/send_flow_example.md) <br>
- [Reply flow example](references/reply_flow_example.md) <br>
- [Channel flow example](references/channel_flow_example.md) <br>
- [New message example](references/new_message_example.md) <br>
- [Reply scratch example](references/reply_scratch_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown mailbox messages with YAML frontmatter, optional shell commands, and Python helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages may be written or copied as files under .mailbox inbox and scratch paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
