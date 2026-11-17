## Description:

Minimax Token checks remaining MiniMax API token quota and supports scheduled monitoring with optional Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sherlockfate](https://clawhub.ai/user/sherlockfate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check MiniMax API quota, configure hourly monitoring, and receive low-balance alerts through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to handle MiniMax API and Telegram credentials.

Mitigation: Store credentials outside shell history and command-line arguments, preferably in environment variables or a secrets manager.

Risk: Telegram notifications can send quota or account-related information to a third-party service.

Mitigation: Send notifications only to trusted chats and avoid including sensitive account details beyond what is necessary.

Risk: The documented systemd setup creates a persistent service.

Mitigation: Review the service behavior before enabling it and confirm how to stop, disable, and remove it.

Risk: The packaged artifact lacks the referenced script and service files.

Mitigation: Review or supply the missing script and service implementation before installation or scheduled execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that depend on user-supplied MiniMax and optional Telegram credentials.]

## Skill Version(s):

2.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
