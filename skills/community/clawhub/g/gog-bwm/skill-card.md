## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and run the gog Google Workspace CLI, configure OAuth access, and execute common Gmail, Calendar, Drive, Contacts, Sheets, and Docs commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth setup and sensitive Google Workspace credentials. <br>
Mitigation: Review requested Google service scopes, store credential files securely, and use the least-privileged account suitable for the task. <br>
Risk: Commands can send email, modify calendars, or update Google Sheets content. <br>
Mitigation: Confirm high-impact commands before execution and prefer json and no-input modes for scripted workflows. <br>


## Reference(s): <br>
- [gog homepage](https://gogcli.sh) <br>
- [ClawHub listing](https://clawhub.ai/blueworldmarketing/gog-bwm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OAuth setup steps, install metadata for the gog binary, and example commands for Google Workspace services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
