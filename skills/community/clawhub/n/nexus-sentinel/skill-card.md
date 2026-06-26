## Description: <br>
Autonomous SRE agent for monitoring server health, rotating logs, managing configuration backups, and guiding service recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect host health, diagnose Docker or PM2 service failures, prepare status reports, rotate logs, and coordinate configuration backups with safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad host administration capabilities, including service control, file access, backups, and external notifications. <br>
Mitigation: Restrict the skill to specific approved services and backup paths, use least-privilege Maton credentials, and require confirmation before cleanup, restart, or backup actions. <br>
Risk: Logs, configuration files, or backup contents may expose secrets or sensitive operational data if shared with external services. <br>
Mitigation: Avoid sending unredacted logs or configuration data externally, exclude sensitive files by default, and require explicit approval before handling files that may contain secrets, keys, or tokens. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status reports and operational guidance with shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference host services, logs, environment variables, backup paths, and external notification settings supplied by the user.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
