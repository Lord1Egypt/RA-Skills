## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banalit](https://clawhub.ai/user/banalit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to operate the agent-browser CLI for deterministic browser navigation, element interaction, state handling, and browser-session workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser auth state, cookies, and storage can expose secrets if committed, shared, or logged.

Mitigation: Treat saved state files as secrets, use test accounts where possible, and avoid printing sensitive values in logs.

Risk: Unpinned global installation of the agent-browser CLI can introduce supply-chain or version-drift risk on sensitive systems.

Mitigation: Prefer a sandboxed or project-local pinned installation before running browser automation in sensitive environments.

## Reference(s):

- [agent-browser homepage](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/banalit/skills/luke-agent-browser-clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide agents toward command-line browser automation workflows; command results depend on the local agent-browser CLI and target websites.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
