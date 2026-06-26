## Description: <br>
Openclaw Sentinel scans agent skills for obfuscation, known-bad signatures, suspicious install behavior, dependency-confusion patterns, and metadata inconsistencies before or after installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect Agent Skills-compatible packages before installation, scan installed skills, review local threat database status, and produce risk scores that inform accept, review, or reject decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review says this local scanner includes under-documented commands that can disable, move, or automatically quarantine installed skills. <br>
Mitigation: Start with read-only commands such as scan, inspect, status, and threats; pass an explicit --workspace path; import threat lists only from trusted sources; and avoid quarantine, reject, or protect unless the operator intentionally wants to disable or move skill directories and has backups. <br>


## Reference(s): <br>
- [Openclaw Sentinel on ClawHub](https://clawhub.ai/AtlasPA/openclaw-sentinel) <br>
- [AtlasPA publisher profile](https://clawhub.ai/user/AtlasPA) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown documentation with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3 and no external dependencies; commands can scan workspaces, inspect skill directories, manage threat lists, and report status.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
