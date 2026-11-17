## Description:

Provides a starter OpenClaw workspace template with identity, user profile, memory, operating rules, heartbeat, and setup guide files for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External developers and OpenClaw users use this template to set up an agent workspace with persistent markdown-based identity, memory, task tracking, heartbeat routines, and user preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace rules may give the agent broad persistent memory and background authority.

Mitigation: Review and tighten the workspace rules before installing, and make clear that local standing orders cannot override system, safety, privacy, or current-user instructions.

Risk: No-ask and heartbeat behavior can lead to background file edits, email or calendar checks, external messages, backups, or sensitive data handling without enough user confirmation.

Mitigation: Restrict no-ask actions to read-only or clearly reversible work, and require explicit approval for background edits, communication, backups, and sensitive data handling.

Risk: Persistent memory files can accumulate secrets or highly personal details.

Mitigation: Avoid storing secrets or highly personal details in memory files, and periodically review or prune stored memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/openclaw-workspace-starter)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown files and inline setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only workspace template; no executable scripts detected in the release artifact.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
