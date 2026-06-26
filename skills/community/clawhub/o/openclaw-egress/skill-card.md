## Description: <br>
OpenClaw Egress scans agent workspaces and skills for outbound URLs, suspected data exfiltration endpoints, suspicious domains, and network function calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security-minded agent users use this skill to inspect local agent workspaces for outbound network references, suspicious domains, and possible exfiltration patterns before trusting or deploying skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags this defensive local egress scanner as suspicious because some commands can rewrite code files or disable installed skills. <br>
Mitigation: Run scan, status, and domains first; use protect, block, or quarantine only with supervision, backups, and acceptance that they can modify a workspace. <br>


## Reference(s): <br>
- [OpenClaw Egress on ClawHub](https://clawhub.ai/AtlasPA/openclaw-egress) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text reports with findings, domain lists, exit codes, and status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands can create allowlist files, create backup files, comment out code lines, or rename skill directories.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
