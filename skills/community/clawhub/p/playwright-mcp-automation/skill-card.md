## Description:

Launch and operate the Playwright MCP server to let agents browse real websites through structured tools for tasks such as login, search, checkout, dashboards, authenticated downloads, screenshots, and UI flow testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanglinghao01-rakuten](https://clawhub.ai/user/zhanglinghao01-rakuten)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure Playwright MCP and run browser automation loops for live websites, including authenticated workflows, form interaction, evidence capture, and UI testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables powerful browser control over sessions that may contain active logins, private data, MFA flows, downloads, or payment actions.

Mitigation: Use task-specific isolated browser profiles where possible, require explicit user confirmation before purchases or account changes, and avoid storing secrets in skill files.

Risk: Remote MCP exposure or permissive host settings can broaden access to browser automation capabilities.

Mitigation: Keep the server bound to localhost unless protected by strong network controls, restrict allowed hosts before non-local use, and secure any exposed port with a firewall or tunnel.

Risk: Mutable package execution through latest-version npx commands can change runtime behavior over time.

Mitigation: Pin package versions for controlled deployments and avoid running npx with elevated privileges.

## Reference(s):

- [Playwright MCP Setup & Configuration](references/setup.md)
- [Playwright MCP Tool Reference](references/tools.md)
- [Playwright MCP upstream repository](https://github.com/microsoft/playwright-mcp)
- [ClawHub skill page](https://clawhub.ai/zhanglinghao01-rakuten/skills/playwright-mcp-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation plans, MCP launch commands, MCP client configuration, Playwright code snippets, troubleshooting guidance, and verification steps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
