## Description: <br>
Deploy a three-agent meeting assistant system for scheduling, note taking, and action tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a three-agent Pilot meeting workflow that schedules meetings, captures structured notes and decisions, and routes action items to reminders or downstream tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting titles, attendee identifiers, notes, decisions, action items, reminders, and links can contain sensitive or confidential information. <br>
Mitigation: Use test data in examples, redact confidential content where possible, and confirm attendee or company approval before sharing meeting data. <br>
Risk: The workflow can send meeting information to configured calendar, Slack, archive, or other downstream destinations. <br>
Mitigation: Review retention, access controls, and destination configuration before connecting production meeting workflows. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-meeting-assistant-setup) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, and a running daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
