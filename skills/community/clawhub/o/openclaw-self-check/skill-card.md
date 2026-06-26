## Description: <br>
Checks an OpenClaw environment for configuration, file integrity, gateway status, backups, log errors, disk usage, permissions, and API key presence, then reports issues with suggested manual fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangsuann](https://clawhub.ai/user/tangsuann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run local OpenClaw health checks before troubleshooting, after environment changes, or during routine maintenance. It reports findings and suggested commands without automatically modifying files, services, or configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The diagnostic report can reveal local services, logs, paths, backups, permissions, and whether API keys are present. <br>
Mitigation: Review the report before sharing it outside the trusted operating context. <br>
Risk: Suggested fix commands may be inappropriate for a specific OpenClaw installation if applied without review. <br>
Mitigation: Treat fixes as recommendations and execute them only after user confirmation and environment-specific review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangsuann/openclaw-self-check) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with pass, warning, and issue sections plus inline suggested shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports whether sensitive credentials are configured but does not display secret values.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
