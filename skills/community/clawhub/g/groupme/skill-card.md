## Description: <br>
Bridge OpenClaw to GroupMe for team communication by sending scheduled messages, broadcast announcements, shift reminders, and other automated group messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, teams, clubs, and developers use this skill to send on-demand or scheduled messages from OpenClaw to a GroupMe group through a GroupMe bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A GroupMe access token or bot ID could allow unwanted posts to the selected group if exposed. <br>
Mitigation: Store credentials only in the private secrets file or environment variables and never commit them to source control. <br>
Risk: Scheduled or automated messages may send incorrect, sensitive, or poorly timed content. <br>
Mitigation: Review cron jobs and generated announcements before enabling them, and avoid sending secrets or sensitive personal data through automated messages. <br>
Risk: The GroupMe bot can post outbound messages but cannot handle two-way conversations without a callback server. <br>
Mitigation: Use the skill for outbound announcements and add a callback service if the workflow requires receiving and responding to messages. <br>


## Reference(s): <br>
- [GroupMe Skill Page](https://clawhub.ai/bgoodwinstudio/groupme) <br>
- [bgoodwinstudio Publisher Profile](https://clawhub.ai/user/bgoodwinstudio) <br>
- [GroupMe API Base URL](https://api.groupme.com/v3) <br>
- [GroupMe Bot Setup](https://dev.groupme.com/bots) <br>
- [GroupMe Image Service](https://dev.groupme.com/docs/image_service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, GROUPME_ACCESS_TOKEN, and GROUPME_BOT_ID; GROUPME_GROUP_ID is optional for group discovery.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
