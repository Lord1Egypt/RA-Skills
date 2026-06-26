## Description: <br>
Scans local agent workspaces for leaked API keys, tokens, passwords, private keys, and other plaintext credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security-conscious agent users use this skill to scan local OpenClaw, Claude Code, Cursor, or Agent Skills-compatible workspaces for exposed secrets and high-risk credential files before committing, sharing, or continuing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects workspace files that may contain sensitive credentials. <br>
Mitigation: Run scan, check, and status with an explicit --workspace path, and avoid sharing raw findings outside the trusted environment. <br>
Risk: Under-documented commands can rewrite files, move files to quarantine, and change repository metadata. <br>
Mitigation: Review the script and maintain backups before using redact, quarantine, defend, or protect; prefer read-only scan workflows first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtlasPA/openclaw-sentry) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline bash commands and plaintext CLI reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return exit codes for clean, warning, and critical findings; advanced commands can create backups, quarantine files, and update local policy or gitignore files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
