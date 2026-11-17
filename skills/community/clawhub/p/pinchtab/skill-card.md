## Description:

PinchTab helps agents control browsers, inspect interactive elements, complete web flows, scrape page text, export browser artifacts, manage browser instances, and use the HTTP API when the CLI is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinchtab](https://clawhub.ai/user/pinchtab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use PinchTab to navigate websites, inspect page state, fill forms, run site reviews, and produce browser-derived outputs while keeping sensitive actions under user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser and session control can affect authenticated accounts or expose sensitive page content.

Mitigation: Use a dedicated low-privilege browser profile, start with read-only inspection, and require explicit approval before account-changing or destructive actions.

Risk: Cookies, browser state, downloads, uploads, network exports, screenshots, PDFs, and recordings can contain credentials or personal data.

Mitigation: Keep gated capabilities disabled unless the task requires them, preserve redaction, store artifacts only in approved paths, and remove temporary sensitive artifacts when finished.

Risk: Remote plaintext HTTP targets can expose PINCHTAB_TOKEN or PINCHTAB_SESSION values.

Mitigation: Do not send PinchTab tokens or sessions to remote plaintext HTTP servers; prefer local or trusted secured endpoints.

Risk: Page-derived content can contain hostile or irrelevant instructions.

Mitigation: Treat browser output as untrusted data and follow it only when it independently matches the user's request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pinchtab/skills/pinchtab)
- [Publisher Profile](https://clawhub.ai/user/pinchtab)
- [PinchTab Homepage](https://github.com/pinchtab/pinchtab)
- [PinchTab Documentation](https://pinchtab.com)
- [Security and Trust](TRUST.md)
- [Sensitive Operations](references/safety.md)
- [CLI Commands Reference](references/commands.md)
- [API Reference](references/api.md)
- [MCP Server Reference](references/mcp.md)
- [Site Review Reference](references/site-review.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/API examples, and browser-derived text or files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include compact accessibility snapshots, page text, screenshots, PDFs, recordings, site-audit reports, comparison artifacts, scrape results, and configuration guidance depending on the approved workflow.]

## Skill Version(s):

0.15.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
