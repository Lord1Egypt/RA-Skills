## Description:

Mission control dashboard for OpenClaw - real-time session monitoring, LLM usage tracking, cost intelligence, and system vitals. View all your AI agents in one place.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jontsai](https://clawhub.ai/user/jontsai)

### License/Terms of Use:

MIT

## Use Case:

External developers and OpenClaw users use this skill to run a local command center for monitoring AI agent sessions, LLM usage, costs, system vitals, scheduled tasks, topics, and privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose sensitive OpenClaw session data and controls beyond the local user if it is reachable from an untrusted network.

Mitigation: Bind it explicitly to loopback, avoid exposing port 3333 to LAN, VPN, or public interfaces, and enable token or properly enforced proxy authentication before remote use.

Risk: Persistent operator discovery from transcripts may reveal workspace participants or activity patterns.

Mitigation: Review whether transcript-derived operator tracking is acceptable for the workspace and use privacy controls when sharing demos or screenshots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jontsai/skills/openclaw-command-center)
- [OpenClaw Command Center repository](https://github.com/jontsai/openclaw-command-center)
- [OpenClaw Command Center documentation](https://github.com/jontsai/openclaw-command-center#readme)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a Node.js dashboard server on port 3333 by default.]

## Skill Version(s):

1.4.1 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
