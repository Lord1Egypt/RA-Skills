## Description: <br>
AI agent for local businesses to handle appointment scheduling, reminders, cancellations, and service inquiries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dotdance](https://clawhub.ai/user/dotdance) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Local business operators and developers can use this skill to set up a conversational appointment assistant for booking, cancellations, rescheduling, business hours, and service listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect customer names, phone numbers, and appointment details without a documented privacy notice. <br>
Mitigation: Publish a clear privacy notice before real customer use, including data use, retention, deletion, consent for reminders, and any SMS/email provider sharing. <br>
Risk: Appointment details may be lost because the sample implementation stores bookings only in memory. <br>
Mitigation: Use durable storage and operational backups before relying on the skill for live scheduling. <br>
Risk: Calendar and reminder integrations require access to external services and customer communications. <br>
Mitigation: Review calendar permissions and reminder consent flows before connecting production calendars or SMS/email providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dotdance/local-business-appointment-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style setup guidance with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. The sample command-line implementation stores appointment details in memory, so users should add durable storage and privacy controls before handling real customers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
