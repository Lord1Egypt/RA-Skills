## Description: <br>
Installs reusable OpenClaw continuity templates and an optional runtime patch workflow for workspace continuity, successor rollover, hidden handoff, and silent continuity preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buasakaking](https://clawhub.ai/user/buasakaking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to scaffold reusable workspace continuity files, choose an installation route, and optionally prepare a matching OpenClaw source tree for same-thread continuity behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workspace templates install persistent agent operating rules that may be broader than the user's intended scope. <br>
Mitigation: Start with the workspace-only route in a test workspace and review AGENTS.md and SESSION_CONTINUITY.md before using the files in production. <br>
Risk: The bundled example configuration includes an elevated execution profile with ask=off. <br>
Mitigation: Keep command approvals enabled and do not copy the elevated example settings into production without a separate security review. <br>
Risk: The full runtime patch route requires an independently reviewable patch file and a matching OpenClaw source tree. <br>
Mitigation: Avoid the full runtime patch route until the patch file is supplied, reviewed, and tested against the target OpenClaw version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buasakaking/openclaw-continuity-pack) <br>
- [Overview](references/overview.md) <br>
- [Install](references/install.md) <br>
- [Usage](references/usage.md) <br>
- [Deploy notes](references/deploy-notes.md) <br>
- [Verify](references/verify.md) <br>
- [Rollback](references/rollback.md) <br>
- [Upgrade maintenance](references/upgrade-maintenance.md) <br>
- [Source audit](references/source-audit.md) <br>
- [Release notes](references/release-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, Python scripts, and workspace templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can install workspace files and can guide an optional runtime patch route for a matching OpenClaw source tree.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
