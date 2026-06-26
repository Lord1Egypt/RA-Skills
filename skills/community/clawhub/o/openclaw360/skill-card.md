## Description: <br>
Runtime security skill for AI agents: prompt injection detection, tool call authorization, sensitive data leak prevention, skill security scanning, and one-click backup and restore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[326668808](https://clawhub.ai/user/326668808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run local security checks on prompts, tool calls, model outputs, installed skills, audit logs, and OpenClaw360 backups before or during agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a third-party GitHub project at a pinned commit. <br>
Mitigation: Before installing, verify that you trust the referenced GitHub project and pinned commit. <br>
Risk: When enabled, the tool inspects prompts, tool parameters, and outputs locally and keeps audit logs, signing keys, and backups under ~/.openclaw360/. <br>
Mitigation: Review the local storage location before use and protect the ~/.openclaw360/ directory according to the sensitivity of the workflows being checked. <br>
Risk: Restore and backup-clean commands can change OpenClaw360 local backup state. <br>
Mitigation: Use the documented confirmation and dry-run flows before restore or cleanup operations. <br>


## Reference(s): <br>
- [OpenClaw360 source repository](https://github.com/milu-ai/openclaw360) <br>
- [Openclaw360 ClawHub page](https://clawhub.ai/326668808/openclaw360) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-backed security summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/.openclaw360/ for configuration, identity, audit logs, and backups; security guidance says sensitive audit data is hashed and commands are local after installation.] <br>

## Skill Version(s): <br>
0.1.11 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
