## Description: <br>
Creates tasks from Chinese or English natural-language requests, extracts scheduling and organization details, and sends the task to a user's configured 2Do inbox by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuckiefan](https://clawhub.ai/user/chuckiefan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to capture reminders, todos, and dated tasks from conversational input into 2Do. It is useful when an agent should turn natural-language task requests into 2Do email-capture messages with optional due dates, priority, list names, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text and metadata are sent through the configured SMTP provider to the user's 2Do email account. <br>
Mitigation: Use a dedicated SMTP account or app-specific password, and avoid submitting sensitive task text unless that email path is acceptable. <br>
Risk: The skill has broad natural-language trigger coverage and may send a task when a user did not intend to create one. <br>
Mitigation: Configure the agent to invoke it only for explicit task-creation requests or add a confirmation step before sending email. <br>
Risk: If the built dist/main.js file is missing, the launcher falls back to npx tsx at runtime. <br>
Mitigation: Build the project before deployment and run the compiled dist/main.js path to avoid runtime package execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chuckiefan/moltbot-plugin-2do) <br>
- [Publisher profile](https://clawhub.ai/user/chuckiefan) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [2Do Email to 2Do knowledge base](https://www.2doapp.com/kb/category/ios/email-to-2do/44/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [CLI status text with task details sent through SMTP email] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and configured TWODO_EMAIL, SMTP_HOST, SMTP_PORT, SMTP_USER, and SMTP_PASS environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
