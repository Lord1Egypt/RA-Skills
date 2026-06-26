## Description: <br>
Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, configure, authenticate to, and call MCP servers and tools through the mcporter CLI, including HTTP and stdio servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call MCP tools and control MCP server configuration through mcporter, including create, update, delete, or config-changing actions. <br>
Mitigation: Review schemas before calling tools and confirm any action that modifies data or configuration. <br>
Risk: Ad-hoc HTTP MCP servers and stdio commands may expose secrets or run untrusted behavior. <br>
Mitigation: Use trusted MCP servers and stdio commands, and avoid sending secrets to ad-hoc URLs. <br>
Risk: OAuth or daemon sessions may remain active after use. <br>
Mitigation: Stop daemons, reset auth, or log out when access is no longer needed. <br>


## Reference(s): <br>
- [McPorter homepage](http://mcporter.dev) <br>
- [ClawHub skill page](https://clawhub.ai/wuliyuan2026/mcporter-local) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce mcporter CLI commands, MCP tool-call guidance, auth and config instructions, and generated CLI or TypeScript command suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
