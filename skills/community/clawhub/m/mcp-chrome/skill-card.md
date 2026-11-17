## Description:

mcp-chrome connects an AI agent to a user's existing Chrome browser through MCP to navigate pages, capture screenshots, fill forms, extract page content, search history, manage bookmarks, and monitor network activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femto](https://clawhub.ai/user/femto)

### License/Terms of Use:


## Use Case:

Developers and users of MCP-compatible AI clients use this skill to automate browser workflows in an existing Chrome session, including navigation, screenshots, form interaction, page extraction, history and bookmark access, and network inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose an active Chrome profile, including logged-in sessions, page content, browsing history, bookmarks, and cookies.

Mitigation: Use a dedicated Chrome profile with minimal logged-in accounts and only connect the skill when that access is acceptable.

Risk: Browser automation can submit forms, click elements, change bookmarks, search history, capture network traffic, or make cookie-backed requests.

Mitigation: Require explicit confirmation before sensitive browser actions and pin and verify the bridge package and extension versions before use.

## Reference(s):

- [mcp-chrome GitHub repository](https://github.com/femto/mcp-chrome)
- [mcp-chrome releases](https://github.com/femto/mcp-chrome/releases)
- [mcp-chrome-bridger npm package](https://www.npmjs.com/package/mcp-chrome-bridger)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP client setup instructions and browser automation tool guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
