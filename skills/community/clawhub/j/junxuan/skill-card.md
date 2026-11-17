## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junxuan666](https://clawhub.ai/user/junxuan666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to drive browser automation workflows, including navigation, DOM interaction, form filling, structured page snapshots, screenshots, recordings, and browser state management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-controlled browser sessions can expose sensitive cookies, local storage, screenshots, PDFs, recordings, uploads, and saved state files.

Mitigation: Use isolated sessions where possible, avoid saving authenticated state unless necessary, protect generated files as sensitive data, and delete saved state when it is no longer needed.

Risk: Mutable global installation commands can change behavior over time or install unexpected versions.

Mitigation: Prefer a pinned or isolated agent-browser installation and avoid running install commands with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junxuan666/skills/junxuan)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, PDFs, recordings, traces, cookies, storage exports, and saved browser state files through agent-browser commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
