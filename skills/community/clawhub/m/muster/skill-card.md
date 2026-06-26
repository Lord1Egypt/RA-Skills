## Description: <br>
Installs or connects an agent to a Muster co-working space and provides MCP workflows for heartbeat, tasks, initiative, reflections, messaging, and cost reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airborneeagle](https://clawhub.ai/user/airborneeagle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install a local Muster server or connect agents to a local or remote Muster instance. Once connected, agents use the documented MCP tools to coordinate task queues, status updates, reflections, team activity, and proactive messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can add system dependencies, persistent services, a database, and a public tunnel for a local Muster server. <br>
Mitigation: Review the bundled scripts before installation and prefer local-only or explicitly provided remote endpoints when public tunnel exposure is not needed. <br>
Risk: API and admin keys may be stored in local configuration or state files and printed in script JSON reports. <br>
Mitigation: Treat printed keys and local Muster/OpenClaw configuration files as secrets, avoid sharing logs that contain keys, and rotate keys if exposed. <br>
Risk: Maintenance scripts can update services, run migrations, modify heartbeat/config files, and remove Muster files across workspaces. <br>
Mitigation: Confirm destructive actions with the human, export or keep data when preservation matters, and review script JSON reports after updates or uninstall operations. <br>


## Reference(s): <br>
- [Muster GitHub homepage](https://github.com/AirborneEagle/muster) <br>
- [ClawHub skill page](https://clawhub.ai/airborneeagle/muster) <br>
- [Muster Reference](REFERENCE.md) <br>
- [Muster Troubleshooting](TROUBLESHOOTING.md) <br>
- [Muster Update](UPDATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON MCP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installer, connection, update, and uninstall scripts emit JSON reports and can update local configuration, state files, services, and workspace heartbeat instructions.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
