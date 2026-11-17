## Description:

Work with Google Chat spaces, members, messages, attachments, and threaded conversations via the Google Chat API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect Google Chat through ClawLink, inspect spaces, members, messages, reactions, attachments, and threads, and perform confirmed write actions such as sending messages or managing spaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Google Chat through ClawLink gives the integration access to Chat data available to the connected Google account.

Mitigation: Connect only accounts whose Chat access is appropriate for this integration, and verify the Google Chat connection before use.

Risk: Write-capable tools can send or modify messages, spaces, memberships, reactions, sections, or custom emoji.

Mitigation: Preview write or destructive actions and execute them only after explicit user confirmation.

Risk: Using an unpinned plugin release can make the installed behavior harder to review over time.

Mitigation: Prefer a pinned or verified ClawLink plugin release when available.

## Reference(s):

- [Google Chat API Reference](https://developers.google.com/workspace/chat/api/reference/rest)
- [Google Chat API Overview](https://developers.google.com/workspace/chat/api/guides/overview)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-chat-messaging)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected ClawLink Google Chat integration; write and destructive actions require explicit user confirmation; Google Chat messages are limited to 32000 bytes.]

## Skill Version(s):

1.0.6 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
