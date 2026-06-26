## Description: <br>
Use when the user explicitly wants to send outbound messages with the OpenClaw CLI rather than built-in tools, especially for `openclaw message send` commands with a specific channel, target, and message body. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoustc](https://clawhub.ai/user/leoustc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill when they explicitly want an agent to prepare or run OpenClaw CLI commands for outbound messages to a specific channel and target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send real outbound communications through the OpenClaw CLI. <br>
Mitigation: Confirm the channel, recipient, and exact message before allowing the command to run. <br>
Risk: Message text may contain shell-sensitive characters. <br>
Mitigation: Quote message text safely and review generated shell commands before execution. <br>
Risk: A misconfigured or untrusted OpenClaw CLI could send messages through unintended accounts or channels. <br>
Mitigation: Use a trusted OpenClaw CLI installation and verify its configuration before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leoustc/openclaw-message-cli-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users should confirm the channel, recipient, and message before command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
