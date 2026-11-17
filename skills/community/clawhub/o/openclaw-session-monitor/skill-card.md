## Description:

Session Monitor tails OpenClaw JSONL session transcripts and sends formatted live updates to a configured Telegram chat as a persistent background monitor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jusaka](https://clawhub.ai/user/jusaka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and manage continuous monitoring of OpenClaw agent sessions, including multi-agent transcript polling, message formatting, and Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuous monitoring can forward unredacted prompts, responses, commands, filenames, URLs, and tool outputs to Telegram.

Mitigation: Install only when every monitored session owner expects forwarding to the configured chat, and treat the Telegram destination as authorized to receive transcript excerpts.

Risk: Telegram bot credentials and chat identifiers are sensitive because they control where monitoring updates are delivered.

Mitigation: Store the bot token and chat ID only in the local environment configuration and limit access to the skill directory and logs.

Risk: Auto-restart guidance can make monitoring persist beyond the initiating agent session.

Mitigation: Use watchdog or heartbeat restart configuration only when persistent monitoring is explicitly required, and verify the monitor status before and after deployment.

## Reference(s):

- [Session Monitor Reference](artifact/references/REFERENCE.md)
- [ClawHub Skill Release](https://clawhub.ai/jusaka/skills/openclaw-session-monitor)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for a persistent Node.js monitor that formats transcript excerpts as Telegram HTML messages.]

## Skill Version(s):

9.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
