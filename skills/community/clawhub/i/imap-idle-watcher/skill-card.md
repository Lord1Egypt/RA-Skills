## Description: <br>
Real-time email monitoring using IMAP IDLE that sets up a persistent connection to an IMAP server and triggers a user-defined command when new email arrives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axellageraldinc](https://clawhub.ai/user/axellageraldinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a Linux systemd service that watches an IMAP inbox in real time and runs a handler script or shell command for matching incoming mail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A long-running local email automation service can execute arbitrary shell commands when matching mail arrives. <br>
Mitigation: Review the handler command carefully, set narrow sender or subject filters, and run the service under a dedicated low-privilege user or user-level systemd service. <br>
Risk: Mailbox app passwords and service environment files can expose account access if handled insecurely. <br>
Mitigation: Avoid passing app passwords on the command line, restrict service and environment file permissions, and revoke the mailbox app password when uninstalling. <br>
Risk: The installed service may run with elevated local privileges depending on how it is configured. <br>
Mitigation: Use the least-privileged service account that can perform the intended automation and review file permissions before enabling the service. <br>


## Reference(s): <br>
- [Gmail Setup](references/gmail.md) <br>
- [Outlook / Hotmail / Live Setup](references/outlook.md) <br>
- [Yahoo Mail Setup](references/yahoo.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/axellageraldinc/imap-idle-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include systemd service configuration, environment variables, and handler script guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
