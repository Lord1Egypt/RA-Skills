## Description: <br>
OpenClaw Workspace Starter Agent Home Template provides editable workspace files and setup guides that give an OpenClaw agent identity, memory, operating rules, and heartbeat routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent builders use this template to bootstrap a local agent workspace with identity, memory, planning, setup, and operating documentation so an agent can recover useful context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The template gives an agent broad local memory and background-maintenance authority, which may lead to unexpected edits during sessions or scheduled heartbeats. <br>
Mitigation: Before use, edit AGENTS.md and HEARTBEAT.md to limit writes to specific memory files and require confirmation for file organization or documentation changes. <br>
Risk: Local memory, daily notes, and backups may capture secrets or highly sensitive personal details if users place them in workspace files. <br>
Mitigation: Avoid storing secrets or highly sensitive personal details, and review memory and backup contents before syncing or sharing the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/openclaw-workspace-starter) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown workspace template files and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The template produces local workspace files for identity, memory, planning, tool notes, heartbeat routines, and user-editable setup documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
