## Description:

Multi-agent coding orchestrator using Gas Town and Claude Code to coordinate parallel coding work with git-backed state, Beads work tracking, merge queues, and health monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saesak](https://clawhub.ai/user/saesak)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to delegate non-trivial coding work across multiple Claude Code agents, track tasks through Beads and convoys, and coordinate implementation, testing, and merge workflows through Gas Town.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad automatic execution authority through multi-agent workflows that can spawn agents, run shell commands, alter repositories, and manage merge workflows.

Mitigation: Install only for repositories and credentials the user is comfortable exposing to those agents, and keep human review on merge and repository-changing workflows.

Risk: The setup path includes high-impact installation steps, including tool installation from remote sources and latest-version Go installs.

Mitigation: Review scripts/setup.sh and setup commands before running them, and prefer pinned, verified tool versions in managed environments.

Risk: Autonomous hook execution can carry untrusted tasks forward without additional confirmation.

Mitigation: Avoid autonomous hook execution for untrusted tasks and review the queued work, hook state, and merge queue before allowing changes to land.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/saesak/skills/openclaw-skill-gastown)
- [Gas Town Architecture](artifact/references/architecture.md)
- [Gas Town GitHub](https://github.com/steveyegge/gastown)
- [Beads GitHub](https://github.com/steveyegge/beads)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and code or configuration changes produced through coordinated agent workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May spawn multiple coding agents, run repository commands, and coordinate merge workflows through Gas Town.]

## Skill Version(s):

0.1.4 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
