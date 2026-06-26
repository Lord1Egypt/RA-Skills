## Description: <br>
Automate Microsoft Forms daily submissions with M365 MFA support and dual-calendar integration to auto-fill training, content development, and learning hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClaireAICodes](https://clawhub.ai/user/ClaireAICodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and automation-focused developers use this skill to prepare and submit recurring Microsoft Forms productivity logs from calendar-derived training, content development, and learning hour data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires high-trust Microsoft 365 credential, session cookie, calendar feed URL, and form data access. <br>
Mitigation: Install only when that access is acceptable, prefer a dedicated or least-privilege account, and protect or remove generated config, session, and screenshot files. <br>
Risk: The skill can submit real Microsoft Forms records with limited safeguards. <br>
Mitigation: Verify the hard-coded form URL and run dry runs or manual tests before enabling regular submissions. <br>
Risk: Scheduled automation can continue submitting forms after it is no longer needed. <br>
Mitigation: Disable any cron or scheduled job when the workflow is paused, retired, or no longer authorized. <br>


## Reference(s): <br>
- [Authentication Workflow Fix - Testing & Verification](references/TESTING_AUTH_WORKFLOW.md) <br>
- [ClawHub release page](https://clawhub.ai/ClaireAICodes/ms-forms-auto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration or form-entry data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local credential, browser session, calendar, and daily-entry files when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
