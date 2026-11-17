## Description:

Provides JSON-RPC method invocation and OpenRPC-style method discovery through a Xiaobenyang-backed MCP API wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to call JSON-RPC methods on a specified server URL and inspect available methods via rpc.discover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Xiaobenyang API key in a local .env file.

Mitigation: Use test-scoped or rotated credentials and review local key storage before production use.

Risk: JSON-RPC target URLs and parameters are sent through the Xiaobenyang service.

Mitigation: Avoid sensitive or internal server URLs and review URL validation and endpoint scoping before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/json-rpc)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [Xiaobenyang](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key before tool calls can be made.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
