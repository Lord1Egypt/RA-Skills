## Description: <br>
Intelligent log analysis tool for monitoring cron jobs, detecting errors, analyzing patterns, and generating reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw cron, system, and application logs, detect errors and warnings, generate Markdown reports, update status JSON, and send Discord notifications for important findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log-derived reports may include secrets, personal data, or sensitive operational details and are sent to a fixed Discord destination. <br>
Mitigation: Disable Discord sending by default, make the destination configurable, and redact secrets and personal data before any notification leaves the local environment. <br>
Risk: Unsafe shell command construction can allow command injection when report content is passed into the notification command. <br>
Mitigation: Replace execSync string interpolation with safe argument passing such as spawn or execFile. <br>
Risk: Running the analyzer against sensitive logs can expose private system, application, or user activity in generated reports. <br>
Mitigation: Review the script and configured log sources before installing, and avoid scheduling it against sensitive logs until the notification and redaction controls are fixed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/openclaw-log-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/sunnyhot) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Analyzer Script](artifact/scripts/analyzer.cjs) <br>
- [Analysis Rules](artifact/config/rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON status files, console text, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May truncate Discord notification text to 1900 characters; writes local status JSON and can send log-derived reports to Discord.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
