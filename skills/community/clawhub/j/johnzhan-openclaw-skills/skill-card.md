## Description:

Project-based conversation logging for OpenClaw agents with daily per-project log files, first-turn context loading, manual lookup, and sub-agent logging guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhan5331](https://clawhub.ai/user/zhan5331)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add lightweight project-scoped conversation memory, with structured daily Markdown logs and continuity across sessions. It is intended for workspaces that need isolated histories across multiple projects or agent runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project logs can capture sensitive conversation history.

Mitigation: Use the skill only where persistent memory is intended, protect the log directory, and periodically review or delete old logs.

Risk: Silent logging gives users limited visibility into what is being stored.

Mitigation: Consider adding explicit opt-in, visible logging status, and redaction rules before deploying in sensitive environments.

Risk: Reloaded historical logs can mix trusted project context with untrusted or outdated notes.

Mitigation: Review loaded history before relying on it for security-sensitive decisions and keep project mappings scoped to trusted workspaces.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zhan5331/Johnzhan-OpenClaw-Skills)
- [ClawHub skill page](https://clawhub.ai/zhan5331/skills/johnzhan-openclaw-skills)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with PowerShell, bash, and AGENTS.md configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and logging templates; agents following the skill may create or append local Markdown log files.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
