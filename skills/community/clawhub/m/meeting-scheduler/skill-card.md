## Description: <br>
Schedule meetings between your owner and another person by coordinating with their PA, finding available slots in both calendars, and sending a calendar invite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and assistants use this skill to coordinate meetings, propose available time slots, create calendar invites, and confirm scheduling details with both sides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar reads, invite creation, or event deletion could expose private schedule details or change a user's calendar without enough confirmation. <br>
Mitigation: Confirm the calendar account, attendees, times, time zones, descriptions, and exact event ID with the user before reading calendars, creating invites, rescheduling, or deleting events. <br>
Risk: The artifact is marked deprecated and points users to a broader meetings skill. <br>
Mitigation: Prefer the maintained meetings workflow when available, and review this skill before deployment if using it directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/meeting-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, text] <br>
**Output Format:** [Markdown guidance with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduling steps, message templates, calendar CLI examples, and availability-checking code for an agent to adapt before action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
