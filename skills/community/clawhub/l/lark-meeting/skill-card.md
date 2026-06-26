## Description: <br>
Helps an agent initialize Lark meeting-room data, find available rooms, and book meetings through the local lark-cli account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gooodplus](https://clawhub.ai/user/gooodplus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and assistants use this skill to initialize Lark room lists, apply meeting-room blacklist rules, check room availability, and create calendar bookings. It is intended for environments where the user has already configured lark-cli with the needed Lark permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Lark credentials to inspect meeting rooms, check availability, create calendar events, and add room resources. <br>
Mitigation: Install and run it only with a trusted lark-cli login, and confirm the exact time, timezone, title, calendar, and room before booking. <br>
Risk: Permission repair commands that change local file ownership can affect unintended paths if copied with the wrong directory. <br>
Mitigation: Avoid sudo ownership commands unless the path is understood and the command is needed to repair local configuration permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gooodplus/lark-meeting) <br>
- [Lark meeting room freebusy API](https://open.feishu.cn/open-apis/meeting_room/freebusy/batch_get) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local meeting-room blacklist configuration and may create or use local meeting-room configuration files during initialization and booking.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
