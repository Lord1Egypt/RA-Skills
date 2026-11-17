## Description:

飞书日历与日程管理工具集，包含日历管理、日程管理、参会人管理和忙闲查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfa188](https://clawhub.ai/user/chenfa188)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to create, search, update, reply to, and inspect Feishu calendar events, attendees, and free/busy windows with Feishu ID and timezone conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting attendees may receive broad edit permissions by default.

Mitigation: Use narrower attendee permissions where possible and review permission settings before creating shared meetings.

Risk: Calendar updates, attendee removals, or invitations can affect shared schedules.

Mitigation: Require explicit confirmation before modifying events, removing attendees, or sending invitations.

Risk: Timezone assumptions can create events at unintended times.

Mitigation: Confirm Asia/Shanghai timezone expectations and use ISO 8601 or RFC 3339 timestamps with timezone offsets.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [Markdown guidance with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes Asia/Shanghai timezone and Feishu open_id-style identifiers where applicable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
