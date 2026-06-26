## Description: <br>
Real-time OpenClaw session monitor that tails JSONL transcripts and sends formatted activity updates to a Telegram chat as a persistent background process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jusaka](https://clawhub.ai/user/jusaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run continuous monitoring of OpenClaw session transcripts, with live activity summaries delivered to a trusted Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor continuously forwards local agent transcripts to Telegram, which may expose secrets or sensitive business data. <br>
Mitigation: Install only for sessions intended to be monitored, send updates only to a trusted private chat, and avoid monitoring directories that may contain sensitive content. <br>
Risk: A persistent background process or HEARTBEAT watchdog can keep forwarding transcript updates until explicitly stopped. <br>
Mitigation: Use narrowly scoped AGENTS or SESSIONS_DIR values, track the PID file for the correct skill directory, and remove any watchdog entry when stopping the monitor. <br>
Risk: Telegram bot credentials and chat IDs control where transcript data is sent. <br>
Mitigation: Use a dedicated bot, keep BOT_TOKEN and CHAT_ID private, and verify the destination chat before starting the monitor. <br>


## Reference(s): <br>
- [Session Monitor Reference](artifact/references/REFERENCE.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/jusaka/openclaw-session-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values; runtime monitor messages are formatted as Telegram HTML text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Telegram bot credentials and a target chat ID; monitors configured OpenClaw session directories continuously.] <br>

## Skill Version(s): <br>
9.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
