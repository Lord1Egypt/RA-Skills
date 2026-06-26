## Description: <br>
Add a simple "Claude has finished." alert to Claude Code or other agent workflows through an OpenClaw-configured transport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyoiii](https://clawhub.ai/user/kyoiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install or test a Claude Code completion hook that sends a short OpenClaw WhatsApp notification when a task finishes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer persistently rewrites Claude hook settings and enables automatic future command execution. <br>
Mitigation: Review and back up ~/.claude/settings.json before installation, especially if existing Claude hooks are configured. <br>
Risk: A misconfigured notification target could send completion messages to the wrong WhatsApp recipient. <br>
Mitigation: Set OPENCLAW_NOTIFY_TARGET carefully and use OPENCLAW_NOTIFY_SELF_TARGET for self-only delivery. <br>
Risk: Completion notifications may continue after the user no longer wants automatic delivery. <br>
Mitigation: Remove the installed hook and settings entries manually when persistent notifications are no longer desired. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [ClawHub release page](https://clawhub.ai/kyoiii/personal-finish-notifier) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write Claude hook settings and uses OpenClaw WhatsApp delivery when installed and configured.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
