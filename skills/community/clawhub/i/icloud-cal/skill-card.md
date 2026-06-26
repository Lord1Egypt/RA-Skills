## Description: <br>
Manage iCloud calendars via natural language to create, query, update, and delete events synced to an iPhone calendar using CalDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickhuang28](https://clawhub.ai/user/rickhuang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage iCloud calendar events, including creation, search, query, update, deletion, reminders, recurrence, and calendar selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs sensitive iCloud calendar credentials and can change real calendar events. <br>
Mitigation: Use an Apple app-specific password, protect the OpenClaw config file, and install only when the publisher is trusted with calendar access. <br>
Risk: Broad update or delete requests can affect unintended calendar events. <br>
Mitigation: Preview deletions with DELETE_DRY_RUN=1, require confirmation for destructive actions, and use narrow keywords and date ranges. <br>
Risk: Incorrect timezone configuration can create events at the wrong local time. <br>
Mitigation: Set the timezone to the user's actual IANA locale before creating or updating events. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rickhuang28/icloud-cal) <br>
- [Apple ID App-Specific Passwords](https://appleid.apple.com) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires iCloud email and app-specific password environment variables; update and delete actions use confirmation environment variables.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
