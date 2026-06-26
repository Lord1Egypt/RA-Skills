## Description: <br>
Controls a MoviePilot media library automation server through its MCP interface for media search, subscriptions, downloads, library organization, PT site maintenance, and plugin management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyangupday](https://clawhub.ai/user/yangyangupday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators of MoviePilot media servers use this skill to search media, manage subscriptions and downloads, organize files into a media library, maintain PT sites, and administer plugins and system workflows through agent-guided tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and uses a powerful MoviePilot API token that can administer the connected server. <br>
Mitigation: Use a dedicated or least-privilege token where supported, restrict access to config.json, and avoid sharing tokens in chat or command history. <br>
Risk: The skill exposes delete, plugin, system-setting, site-credential, browser, slash-command, and local-file actions. <br>
Mitigation: Require manual confirmation before allowing destructive or administrative actions, especially file deletion, plugin changes, site credential updates, and system setting changes. <br>
Risk: The security scan verdict is suspicious due to broad administration capability and limited built-in safety guidance. <br>
Mitigation: Install only from a trusted publisher and scan or review the skill before deployment. <br>


## Reference(s): <br>
- [MoviePilot MCP setup guide](references/setup-guide.md) <br>
- [MoviePilot MCP tools reference](references/tools.md) <br>
- [MoviePilot MCP workflow guide](references/workflows.md) <br>
- [ClawHub release page](https://clawhub.ai/yangyangupday/moviepilot-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls return MoviePilot MCP JSON-RPC responses; configuration is stored in config.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
