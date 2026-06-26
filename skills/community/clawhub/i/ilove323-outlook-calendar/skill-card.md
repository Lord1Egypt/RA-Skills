## Description: <br>
Reads Microsoft 365 Outlook calendar events for requested date ranges and helps summarize schedules, meetings, and total meeting time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilove323](https://clawhub.ai/user/ilove323) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees with Microsoft 365 accounts use this skill to retrieve Outlook calendar events for today, tomorrow, a week, a month, or a custom date range and summarize meetings or total scheduled time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for and stores Microsoft 365 credentials, cookies, and bearer tokens under ~/.outlook. <br>
Mitigation: Use an official Microsoft OAuth or Graph calendar integration with calendar-read-only scopes when possible; otherwise restrict ~/.outlook permissions and delete cookies, tokens, logs, and debug screenshots after use. <br>
Risk: Stored authentication material can expose calendar and account access if used on an untrusted or shared machine. <br>
Mitigation: Run the skill only on a trusted single-user machine and invoke it only for explicit calendar requests. <br>
Risk: Keeping an account password in config.json increases credential exposure. <br>
Mitigation: Avoid keeping the Microsoft 365 account password in config.json after setup or use a safer authentication flow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ilove323/ilove323-outlook-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON calendar event output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar events include subject, start and end times, duration, status, organizer, and all-day state when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
