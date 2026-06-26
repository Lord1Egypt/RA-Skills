## Description: <br>
Lobster Doctor helps OpenClaw users inspect workspace health, clean local files, slim skill descriptions, archive memory files, and audit cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masongmx](https://clawhub.ai/user/masongmx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw workspace operators use this skill to generate local health reports, identify cleanup opportunities, reduce skill description overhead, archive stale memory files, and review scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect sensitive local OpenClaw history, configuration, installed skills, memory files, cron jobs, and workspace contents. <br>
Mitigation: Run it only in workspaces where local inspection is acceptable, review reports before sharing them, and avoid exposing generated diagnostics outside the trusted environment. <br>
Risk: Cleanup, skill-slim apply, and memory archive modes can make broad persistent changes to files and installed skill descriptions. <br>
Mitigation: Start with report or dry-run modes, review exact targets, keep backups, and use apply or cleanup modes only after confirming the proposed changes. <br>
Risk: The authoritative security verdict is suspicious because the tool has broad local visibility and limited confirmation controls. <br>
Mitigation: Treat installation as a local maintenance decision, restrict use to trusted operators, and prefer manual review for destructive or persistent actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/masongmx/lobster-doctor-skill-slim) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text reports with command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run previews, workspace statistics, cleanup plans, token estimates, and backup or restart guidance.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
