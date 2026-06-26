## Description: <br>
Send push notifications via ntfy.sh or self-hosted ntfy server. Supports priorities, titles, tags, icons, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare ntfy CLI notifications for urgent alerts, monitoring updates, email notifications, and system health warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notifications may expose passwords, tokens, personal data, or sensitive operational details if message content is copied into ntfy payloads. <br>
Mitigation: Review notification content before sending and avoid sensitive data unless disclosure has been explicitly approved. <br>
Risk: ntfy topic URLs act like shared secrets, so exposed or guessable topics can allow unintended parties to send or observe notification traffic. <br>
Mitigation: Use trusted HTTPS endpoints, keep topic URLs private, and choose non-guessable topic names. <br>


## Reference(s): <br>
- [ntfy documentation](https://ntfy.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ntfy command-line tool and a configured ntfy topic URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
