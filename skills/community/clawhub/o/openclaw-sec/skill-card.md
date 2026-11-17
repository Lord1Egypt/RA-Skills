## Description:

AI Agent Security Suite - Real-time protection against prompt injection, command injection, SSRF, path traversal, secrets exposure, and content policy violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paolorollo](https://clawhub.ai/user/paolorollo)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to validate AI agent prompts, tool calls, URLs, file paths, shell commands, and content for common injection, SSRF, traversal, secret exposure, and obfuscation risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic persistent hooks can intercept prompts and tool parameters after installation.

Mitigation: Require an explicit hook installation step and review enabled hooks before use.

Risk: Prompts, tool parameters, or secrets may be stored locally in plaintext.

Mitigation: Disable or minimize raw database logging, reduce retention, and verify database file permissions.

Risk: Outbound notifications may transmit sensitive security event data.

Mitigation: Only enable notifications to trusted endpoints and review webhook, Slack, or Discord destinations.

## Reference(s):

- [Openclaw Sec ClawHub page](https://clawhub.ai/paolorollo/skills/openclaw-sec)
- [Publisher profile](https://clawhub.ai/user/paolorollo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-style text with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return severity, action, findings, recommendations, event summaries, statistics, or configuration status depending on the command.]

## Skill Version(s):

0.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
