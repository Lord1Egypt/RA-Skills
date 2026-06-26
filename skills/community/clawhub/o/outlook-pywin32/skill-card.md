## Description: <br>
Provides command-line Outlook automation through local pywin32 for mail, calendar, account, and folder management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathanhuangfirst](https://clawhub.ai/user/jonathanhuangfirst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and automation agents use this skill to inspect and update a local Microsoft Outlook profile, including mailbox folders, messages, accounts, calendar events, and default folders. It is intended for Windows environments with Outlook and pywin32 installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive local mailbox and calendar data. <br>
Mitigation: Use it only with Outlook accounts the agent is authorized to access, preferably through a limited Outlook profile. <br>
Risk: Mail and calendar commands can change local Outlook state, including marking messages as read and editing events. <br>
Mitigation: Review and confirm commands before execution, especially message reads and calendar changes. <br>
Risk: Calendar edits involving attendees may have effects beyond a local note. <br>
Mitigation: Confirm attendee-related calendar operations before running them and validate the resulting Outlook item. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonathanhuangfirst/outlook-pywin32) <br>
- [Publisher profile](https://clawhub.ai/user/jonathanhuangfirst) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output with Python return values for Outlook operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, a local Outlook client, and pywin32; account selection may come from command arguments, OUTLOOK_ACCOUNT, or scripts/config.json.] <br>

## Skill Version(s): <br>
0.8.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
