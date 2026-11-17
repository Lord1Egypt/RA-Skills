## Description:

Create and switch between AI assistant personalities while preserving shared user context, saved SOUL.md and IDENTITY.md files, backups, and heartbeat-based restoration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robb1010](https://clawhub.ai/user/robb1010)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill to create, list, switch, rename, and delete assistant personalities while keeping USER.md shared across personalities. It is intended for agents that need persistent persona files, JSON command responses, backup handling, and heartbeat-based restoration across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personality names or state values may resolve outside the intended personalities directory.

Mitigation: Strictly validate personality names, reject traversal and absolute paths, and require every resolved personality path to remain a direct child of the personalities directory before copying, loading, renaming, or deleting files.

Risk: Heartbeat restoration may trust malformed personality state before writing persistent assistant identity files.

Mitigation: Validate the state file before restoration, ignore unknown or malformed active personality values, and keep a recoverable backup before replacing SOUL.md or IDENTITY.md.

## Reference(s):

- [Personality Template Guide](references/personality-template.md)
- [ClawHub Skill Page](https://clawhub.ai/robb1010/skills/personality-switcher)
- [Publisher Profile](https://clawhub.ai/user/robb1010)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, shell commands, JSON command responses, and generated SOUL.md and IDENTITY.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists assistant personality state in local workspace files and returns structured JSON from helper scripts.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
