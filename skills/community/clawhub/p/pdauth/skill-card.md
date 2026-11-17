## Description:

Dynamic OAuth for AI agents via Pipedream. Generate OAuth links for 2500+ APIs, let users authorize, then call MCP tools on their behalf.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and AI agent operators use this skill to request user authorization for third-party apps, check connection status, list available tools, and call authorized API tools through pdauth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized app connections can grant broad third-party account access, including actions that read, write, or send data.

Mitigation: Authorize only the apps needed for the task and confirm the exact account, tool, and action before allowing writes or sends.

Risk: The release installs an unpinned executable dependency, so the installed package behavior can change over time.

Mitigation: Use a pinned, reviewed version of the pdauth package before connecting important accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g9pedro/skills/pdauth)
- [pdauth homepage](https://github.com/Versatly/pdauth)
- [Pipedream MCP](https://mcp.pipedream.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth authorization links, JSON-oriented command options, app/tool identifiers, and user identifier guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
