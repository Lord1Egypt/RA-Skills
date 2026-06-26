## Description: <br>
OpenClaw version upgrade assessment and execution skill that checks update availability, compares releases, assesses risks, backs up user configuration, runs the appropriate update path, restarts the gateway, and supports recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Davis1216](https://clawhub.ai/user/Davis1216) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to evaluate whether an OpenClaw installation should be upgraded, review release and issue signals, create backups, execute updates, restart services, and recover from backups when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change an OpenClaw installation, run installer or package-manager commands, restore or delete state, and restart services. <br>
Mitigation: Require explicit user approval after assessment and before backup, install or update, restore, deletion, restart, or scheduled-check setup actions. <br>
Risk: Backup and restore behavior may copy credentials, configuration, and workspace data. <br>
Mitigation: Treat backups as sensitive, store them in user-controlled locations, avoid sharing backup archives, and verify the selected backup before restore. <br>
Risk: The documented update paths include remote installer and moving-branch commands. <br>
Mitigation: Use official release notes and trusted sources, avoid curl-to-bash or moving-branch installs unless independently verified, and prefer reviewed package or release channels. <br>
Risk: The optional daily scheduled check creates background automation that can keep monitoring versions and writing reports. <br>
Mitigation: Enable scheduled checks only when the operator knows how to audit, disable, and remove the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Davis1216/openclaw-auto-update) <br>
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw) <br>
- [OpenClaw releases](https://github.com/openclaw/openclaw/releases) <br>
- [OpenClaw issues](https://github.com/openclaw/openclaw/issues) <br>
- [Example assessment report](references/example-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and bilingual status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce backup locations, recovery instructions, update recommendations, scheduled-check setup guidance, and service restart guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
