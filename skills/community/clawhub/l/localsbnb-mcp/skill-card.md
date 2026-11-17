## Description:

LocalsBnb MCP helps MCP-capable clients such as OpenClaw, Hermes Agent, and Cursor use the localsbnb-mcp-server npm package to query LocalsBnb/Lukeyun room status, prices, orders, and operating metrics through the official API with user-provided APP_ID and APP_SECRET.

This skill is ready for commercial/non-commercial use.

## Publisher:

[localsbnb](https://clawhub.ai/user/localsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

External hotel and short-term rental operators use this skill to configure an MCP client and route questions about room availability, rates, orders, order details, and operating metrics to the appropriate LocalsBnb tools. Agents use the guidance to preserve date-range semantics, order categories, and credential handling expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run an npm MCP server while providing sensitive API credentials.

Mitigation: Install only after trusting the package publisher and deployment path, prefer a pinned reviewed package version, and use a controlled install instead of ad-hoc npx execution.

Risk: APP_SECRET exposure could grant access to LocalsBnb operational data.

Mitigation: Use least-privilege read-only credentials where possible, avoid sharing secrets in public channels or repositories, and rotate APP_SECRET if package or environment exposure is suspected.

## Reference(s):

- [localsbnb-mcp-server npm package](https://www.npmjs.com/package/localsbnb-mcp-server)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration examples and tool-routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided APP_ID and APP_SECRET environment variables.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
