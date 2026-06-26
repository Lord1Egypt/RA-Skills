## Description: <br>
OpenClaw Bastion scans agent workspaces and ingested text files for prompt injection patterns, boundary risks, hidden instructions, and command policy issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect local workspace content, user-supplied documents, and agent instruction files for prompt-injection indicators before an agent acts on them. It is also useful for reviewing command policy and content-boundary posture in Agent Skills-compatible workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review classifies the release as suspicious because it includes commands that can modify, move, or persistently mark workspace and agent instruction files. <br>
Mitigation: Start with scan, check, boundaries, allowlist, and status; avoid protect, quarantine, unquarantine, sanitize, canary, and enforce unless backups exist and the affected files and hooks have been reviewed. <br>
Risk: The tool can create persistent workspace artifacts such as command policy files, canary manifests, hook configuration, quarantine records, or modified sanitized files. <br>
Mitigation: Run it first in a disposable or backed-up workspace and review generated files before adopting the active defense commands in routine workflows. <br>


## Reference(s): <br>
- [OpenClaw Bastion ClawHub listing](https://clawhub.ai/AtlasPA/openclaw-bastion) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text reports and Markdown documentation with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python CLI output; some commands can create or modify workspace policy, hook, quarantine, canary, or sanitized files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
