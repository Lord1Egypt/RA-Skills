## Description: <br>
Google Workspace Admin SDK: Audit logs and usage reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace administrators and developers use this skill to inspect and prepare gws CLI commands for Google Workspace Admin SDK Reports API audit logs, usage reports, notification channels, and watch management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may access sensitive Google Workspace audit and usage report data. <br>
Mitigation: Use the least-privileged Google Workspace admin account available and confirm report parameters before running commands. <br>
Risk: Watch channels can continue sending notifications after they are no longer needed. <br>
Mitigation: Stop watch channels when reporting workflows are complete. <br>
Risk: The skill depends on the local gws CLI and generated shared Google Workspace instructions for authentication and security behavior. <br>
Mitigation: Verify that the local gws CLI and generated gws-shared instructions come from a trusted source before installing or using the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/gws-admin-reports) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gws CLI and generated gws-shared instructions for authentication, global flags, and security rules.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact metadata.version: 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
