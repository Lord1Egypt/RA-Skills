## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penglovemeng](https://clawhub.ai/user/penglovemeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, page inspection, UI interaction, form filling, screenshots, PDFs, recordings, and browser state management through structured shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned or untrusted agent-browser installs can introduce supply-chain or runtime risk.

Mitigation: Install only from a trusted agent-browser version, prefer a pinned package version or reviewed commit, and avoid elevated privileges for install commands.

Risk: Saved browser state, cookies, storage dumps, screenshots, videos, PDFs, and traces can contain private page data or account sessions.

Mitigation: Treat generated browser artifacts as sensitive, delete them when no longer needed, and do not commit or share them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/penglovemeng/skills/peng-agent-browser)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, PDFs, videos, traces, saved browser state, cookies, storage data, and other browser artifacts when those commands are used.]

## Skill Version(s):

0.2.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
