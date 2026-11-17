## Description:

帮助用户预约会议室, 当用户需要预约会议室时执行此技能

This skill is ready for commercial/non-commercial use.

## Publisher:

[gooodplus](https://clawhub.ai/user/gooodplus)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to initialize Lark meeting-room configuration, check room availability, apply a room blacklist, and create calendar bookings with a selected available room.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in Lark account to create calendar events and reserve rooms.

Mitigation: Confirm the exact start time, end time, meeting title, and room selection before executing booking commands.

Risk: Debug logging may expose sensitive meeting, room, or API response details.

Mitigation: Review logging settings before use and disable or reduce debug logging in environments where meeting metadata is sensitive.

Risk: The skill documentation suggests a sudo ownership command when configuration files are not writable.

Mitigation: Run privileged ownership changes only after verifying the target path and confirming that the permission change is necessary.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration edits, and user-facing booking status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local meeting-room configuration and may create Lark calendar events when run with an authenticated Lark account.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
