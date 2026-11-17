## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser navigation, inspect page state, interact with forms and controls, capture screenshots or PDFs, and collect structured page output during web workflows and UI testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable authenticated browser state can expose cookies, credentials, or session data if saved state files are mishandled.

Mitigation: Use test or low-privilege accounts when possible, protect state files like credentials, and do not commit or share recordings or state files.

Risk: Inline credentials and automated browser actions can affect real services if run against production accounts.

Mitigation: Review commands before execution, avoid storing real authenticated state unless necessary, and prefer a pinned or isolated install of the agent-browser CLI.

## Reference(s):

- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser state, recordings, screenshots, PDFs, and trace files may be created by the underlying CLI.]

## Skill Version(s):

0.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
