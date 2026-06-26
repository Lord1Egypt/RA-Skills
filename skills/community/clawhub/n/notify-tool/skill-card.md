## Description: <br>
Notify Tool sends desktop notifications from command-line scripts and automated tasks for alerts, reminders, and process completion updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to send Linux desktop notifications for task completion, reminders, and operational alerts from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted notification titles or messages can trigger unintended local shell command execution through shell interpolation. <br>
Mitigation: Use only trusted notification text until the script calls notify-send through a subprocess argument list; do not pass logs, filenames, user input, or process output as titles or messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/notify-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces notification title, message, and urgency guidance for notify-send-based desktop alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
