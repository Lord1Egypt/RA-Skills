## Description:

Read, search and send Hike Messenger chats via the hkcli command-line tool. Use when the user asks about their Hike messages or wants to message someone on Hike.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinaycodeaxe](https://clawhub.ai/user/vinaycodeaxe)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to read, search, or summarize chats from the Hike account logged in to hkcli, or to send a specified message or file after confirming the recipient and exact content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner found no issues with medium confidence, but one local path-like reference could not be matched to a bundled artifact.

Mitigation: Review the unresolved reference before installing if it affects your decision.

Risk: Hike chats and the account session contain private information, and sending can affect external recipients.

Mitigation: Access only the requested messages, quote only what is needed, protect the session file, and confirm the resolved recipient and exact message before sending.

## Reference(s):

- [hkcli documentation](https://vinaycodeaxe.github.io/hkcli/)
- [ClawHub skill page](https://clawhub.ai/vinaycodeaxe/skills/hkcli)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Text or Markdown summaries, CLI commands, and downloaded media files as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output depends on the requested Hike action; sent messages require explicit recipient and content confirmation.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
