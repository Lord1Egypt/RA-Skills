## Description: <br>
飞书日历与日程管理工具集，支持日历管理、日程管理、参会人管理和忙闲查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfa188](https://clawhub.ai/user/chenfa188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to create, search, update, reply to, and troubleshoot Feishu calendar events, attendees, meeting rooms, and free/busy queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can create or change persistent Feishu calendar data. <br>
Mitigation: Confirm the meeting time, timezone, attendees, RSVP change, room booking, and target event before executing create, patch, reply, or attendee changes. <br>
Risk: The artifact describes broad attendee permissions that can let invitees edit events or manage participants. <br>
Mitigation: Review whether invitees should be allowed to modify the event or manage participants before applying attendee permissions. <br>
Risk: Incorrect timezone or identifier formats can create events for the wrong time or participants. <br>
Mitigation: Use Asia/Shanghai with RFC 3339 timestamps and verify Feishu identifiers such as user open_id, chat ID, room ID, and email address before making API calls. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API call parameters] <br>
**Output Format:** [Markdown guidance with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Asia/Shanghai time, RFC 3339 timestamps, and Feishu open_id, chat, room, and email identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
