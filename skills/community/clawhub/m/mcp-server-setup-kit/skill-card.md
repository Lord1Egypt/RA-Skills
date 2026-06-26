## Description: <br>
Guides agents through connecting Claude or OpenClaw to Notion, Linear, Slack, and GitHub MCP servers with checklists, configuration templates, tests, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flynndavid](https://clawhub.ai/user/flynndavid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to set up and validate MCP integrations for common work tools, including GitHub, Notion, Slack, and Linear. It provides readiness checks, copyable configuration examples, verification prompts, and troubleshooting guidance for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting an agent to work services with API keys or OAuth tokens can expose sensitive data or enable unintended write actions if credentials are over-scoped. <br>
Mitigation: Use least-privilege tokens, verify MCP packages from official sources, test in sandbox projects or private channels, and revoke tokens or remove config entries when no longer needed. <br>
Risk: Cross-tool workflows and Slack posting can share sensitive summaries with broader audiences than intended. <br>
Mitigation: Avoid posting sensitive summaries to broad Slack channels and validate sharing behavior in private channels before using the setup with production data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flynndavid/mcp-server-setup-kit) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes readiness checks, validation prompts, troubleshooting steps, and a setup scoring rubric.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
