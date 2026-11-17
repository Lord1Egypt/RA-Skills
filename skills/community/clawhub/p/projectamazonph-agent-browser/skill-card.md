## Description:

Automate complex web workflows with fast, deterministic browser control using accessibility tree snapshots and session isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectamazonph](https://clawhub.ai/user/projectamazonph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to drive web workflows through the agent-browser CLI with ref-based element selection, session isolation, snapshots, and browser state handling. Review the package before installing because the artifact also contains self-improvement hook material that can influence future agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package combines browser automation guidance with self-improvement hooks that can persistently influence later agent sessions.

Mitigation: Review the full artifact before installation and enable only the browser workflow or hook behavior that is explicitly needed.

Risk: Global hook setup can inject reminders across unrelated projects or sessions.

Mitigation: Avoid global hook installation; prefer project-scoped configuration and narrow matchers.

Risk: Browser state files, cookies, and storage snapshots can contain credentials or session tokens.

Mitigation: Treat saved browser state as sensitive credentials and keep it out of logs, commits, and shared artifacts.

Risk: Self-improvement scripts and prompts can encourage writes to learning or agent instruction files.

Mitigation: Require explicit user approval before writing SOUL.md, AGENTS.md, TOOLS.md, or .learnings files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/projectamazonph/skills/projectamazonph-agent-browser)
- [Agent Browser skill guide](artifact/SKILL.md)
- [OpenClaw integration guide](artifact/references/openclaw-integration.md)
- [Hook setup guide](artifact/references/hooks-setup.md)
- [Entry examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with CLI command examples, JSON configuration snippets, and optional shell, TypeScript, and JavaScript helper files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser automation patterns, state-management guidance, and optional hook reminders that may affect later agent sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
