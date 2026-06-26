## Description: <br>
Handle HR workflows -- onboarding, announcements, and employee comms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams and workplace operations agents use this skill to coordinate onboarding calendars, shared documents, new-hire announcements, email-to-task conversion, and employee communications through Google Workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email, post Chat announcements, upload Drive files, and schedule calendar events involving sensitive HR content. <br>
Mitigation: Use a least-privilege Google Workspace account and require human approval for recipients, message text, shared files, and calendar targets before execution. <br>
Risk: HR workflows can expose personally identifiable or sensitive employee information. <br>
Mitigation: Use the documented --sanitize option for PII-sensitive operations and limit access to the needed HR folders, calendars, groups, and Chat spaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/persona-hr-coordinator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Google Workspace CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-gmail, gws-calendar, gws-drive, and gws-chat utility skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
