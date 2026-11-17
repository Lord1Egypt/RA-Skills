## Description:

nmail helps agents and humans read, search, watch, configure, and send Naver and Daum email from a command-line interface with JSON-first output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harlockius](https://clawhub.ai/user/harlockius)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use nmail to connect an agent to Korean email accounts, inspect inbox contents, search messages, monitor new mail, and send plain-text replies through provider IMAP and SMTP services. It is most useful when an agent needs structured email input or explicit email-send commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool requires an email app password that can read and send mail.

Mitigation: Use a dedicated low-risk mailbox or app password, confirm the installed repository and version, and avoid entering passwords in shell history.

Risk: The watch workflow can turn untrusted email metadata into system events.

Mitigation: Avoid the system-event watch pipeline unless email metadata is treated as untrusted and any follow-on action requires explicit user confirmation.

Risk: Configured credentials are stored locally in ~/.nmail/config.yaml.

Mitigation: Limit account privileges where possible and protect the local configuration file and host account.

## Reference(s):

- [nmail ClawHub page](https://clawhub.ai/harlockius/skills/nmail)
- [Publisher profile](https://clawhub.ai/user/harlockius)
- [Artifact README](artifact/README.md)
- [Artifact skill guide](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying nmail CLI returns JSON by default and pretty text when requested.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
