## Description:

Chrome DevTools MCP gives agents browser automation and testing capabilities through Puppeteer and the Chrome DevTools Protocol, including navigation, input automation, screenshots, performance traces, network inspection, and console debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banalit](https://clawhub.ai/user/banalit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and testing agents use this skill to automate Chrome sessions for browser testing, web automation, performance analysis, UI testing, form filling, visual regression, and debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent powerful control over a Chrome browser session.

Mitigation: Use an isolated browser profile or container and avoid logged-in or sensitive browsing sessions.

Risk: The setup and examples repeatedly use an unpinned npm package version.

Mitigation: Prefer a pinned, reviewed chrome-devtools-mcp version instead of @latest before installation.

Risk: Usage statistics and performance CrUX features can share telemetry or trace-related data.

Mitigation: Disable telemetry and CrUX features when privacy matters.

## Reference(s):

- [Chrome DevTools MCP homepage](https://github.com/ChromeDevTools/chrome-devtools-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup commands, MCP configuration snippets, browser automation workflow guidance, and security guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
