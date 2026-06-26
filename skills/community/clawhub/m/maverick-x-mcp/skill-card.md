## Description: <br>
Search, read, and work with X posts, users, timelines, and search through a local XMCP wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search, read, and manage X posts, users, timelines, and recent search results through local MCP tooling. It is appropriate for X-related workflows that can provide OAuth credentials and review any externally visible write or delete action before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use OAuth credentials with X read and write scopes, including posting and deleting content. <br>
Mitigation: Require explicit user confirmation for every externally visible write or delete action and prefer a read-only configuration when search and timeline access are sufficient. <br>
Risk: The local server downloads XMCP server code and installs dependencies at runtime without a pinned upstream revision in the artifact. <br>
Mitigation: Pin, vendor, or review the downloaded XMCP server and dependency set before use in sensitive environments. <br>
Risk: The skill stores and refreshes sensitive X OAuth credentials through the local mcporter vault. <br>
Mitigation: Use least-privilege OAuth grants where possible, rotate credentials on suspected exposure, and avoid passing unrelated sensitive content through the X tools. <br>


## Reference(s): <br>
- [X MCP documentation](https://docs.x.com/tools/mcp) <br>
- [mcporter MCP CLI](https://github.com/steipete/mcporter) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-x-mcp) <br>
- [Maverick publisher profile](https://clawhub.ai/user/maverick) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [MCP tool responses as text or JSON, plus shell commands and setup guidance for local invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local loopback MCP wrapper, requires X OAuth credentials, and can perform X read/write actions within the allowed tool set.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
