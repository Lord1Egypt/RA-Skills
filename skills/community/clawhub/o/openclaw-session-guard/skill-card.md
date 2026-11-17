## Description:

OpenClaw Session Guard helps agents manage long OpenClaw sessions by installing and reporting on an automatic session rotator that archives high-token sessions, creates handoff prompts, and switches main sessions at an 80% threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tel18610240060-collab](https://clawhub.ai/user/tel18610240060-collab)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, check, or remove a local OpenClaw session rotation job and to understand archive, handoff, threshold, and cooldown behavior for long-running agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent local job that monitors OpenClaw sessions and automatically rotates session state.

Mitigation: Install it only when persistent automated rotation is intended, and review the scripts before enabling the LaunchAgent.

Risk: Recent conversation text is archived in plaintext during rotation.

Mitigation: Protect archive directory permissions, redact sensitive content where needed, and add retention cleanup appropriate to the environment.

Risk: Automatic rewrites of session metadata can disrupt active work or cause data loss if the stored state is unexpected.

Mitigation: Back up session metadata before enabling rotation and restrict processing to the intended agents and session keys.

Risk: Installation may fail because the package appears to be missing its LaunchAgent plist template.

Mitigation: Confirm the plist template exists or supply a reviewed template before running the installer.

## Reference(s):

- [OpenClaw Session Guard reference](reference.md)
- [ClawHub skill page](https://clawhub.ai/tel18610240060-collab/skills/openclaw-session-guard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports threshold, cooldown, scan interval, latest archive path, latest rotated session ID, and executable repair commands when failures occur.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
