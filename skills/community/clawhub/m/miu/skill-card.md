## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingxiangmiu](https://clawhub.ai/user/mingxiangmiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate authorized web navigation, page inspection, interaction, form handling, data extraction, and UI testing through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad browser and session access.

Mitigation: Use it only with sites and accounts the operator is authorized to automate, and avoid production or highly sensitive sessions where possible.

Risk: Saved state files, screenshots, traces, recordings, cookies, and storage dumps may contain secrets.

Mitigation: Treat those artifacts as secrets, store them securely, and remove them when they are no longer needed.

Risk: The installation guidance uses an unpinned global npm install.

Mitigation: Prefer a pinned local installation of agent-browser and review package updates before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingxiangmiu/skills/miu)
- [agent-browser upstream repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser CLI skill repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference browser artifacts such as screenshots, PDFs, traces, recordings, cookies, storage dumps, and saved session state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
