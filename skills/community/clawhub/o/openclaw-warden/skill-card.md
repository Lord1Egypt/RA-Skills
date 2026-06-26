## Description: <br>
OpenClaw Warden verifies local workspace file integrity and scans agent identity, memory, configuration, and skill files for prompt injection patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to create a local integrity baseline, check for unauthorized workspace changes, and scan trusted agent files before relying on them in sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some commands can restore, roll back, or quarantine workspace files and installed skills, which can overwrite legitimate edits or disable a skill. <br>
Mitigation: Use report-only commands such as verify, scan, full, and status for routine checks; run restore, rollback, quarantine, or protect only after reviewing target files and keeping backups. <br>
Risk: Integrity results depend on the current baseline, so an outdated or unreviewed baseline can cause expected changes to appear suspicious or preserve unwanted file states. <br>
Mitigation: Review findings before acting, accept legitimate file changes intentionally, and refresh the baseline only after the workspace state has been checked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtlasPA/openclaw-warden) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text scanner reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3 and no network dependency; some actions can modify workspace files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
