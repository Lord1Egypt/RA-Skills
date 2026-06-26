## Description: <br>
Auto-monitor MCP servers and AI services with health checks, auto-restart on failure, and Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reikys](https://clawhub.ai/user/reikys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up local recurring health checks for MCP servers and AI services, with structured logs, optional failure alerts, and configured restarts for selected services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can restart configured local services, which may disrupt running MCP or AI services if service entries or labels are incorrect. <br>
Mitigation: Review and edit the SERVICES array before scheduling the script, set launchctl labels to none for services that should not be restarted, and test with a manual run first. <br>
Risk: Telegram alerts can expose service names or failure details outside the local environment. <br>
Mitigation: Use approved Telegram destinations only, avoid sensitive infrastructure names in alert text, and leave Telegram credentials unset when external alerts are not needed. <br>
Risk: Recurring execution reads a local environment file and writes local logs, which can expose configuration details if file permissions or retention are not managed. <br>
Mitigation: Store the environment file and logs with appropriate local permissions, choose a controlled log path, and configure log rotation or cleanup for scheduled use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reikys/mcp-health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Bash commands, configuration examples, and a health-check script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes editable service definitions, environment variables, scheduling examples, structured log entries, and failure alert text.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
