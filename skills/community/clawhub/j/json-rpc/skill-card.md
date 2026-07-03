## Description: <br>
Provides JSON-RPC method discovery and call execution for MCP workflows, routing requests through the xiaobenyang API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover JSON-RPC methods on a server and call specified methods with parameters. It requires a xiaobenyang API key and should be used only when the server URL and parameters are appropriate to send through that service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a xiaobenyang API key locally and sends JSON-RPC server URLs, method names, and parameters through the xiaobenyang API. <br>
Mitigation: Use it only with non-sensitive endpoints and parameters, protect the local .env file, and avoid internal or private URLs unless the publisher clarifies the data flow and credential handling. <br>
Risk: Server evidence marks the release as suspicious because the apparent JSON-RPC workflow depends on a third-party API path. <br>
Mitigation: Review the publisher, API-key requirement, and expected data flow before installation or operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/json-rpc) <br>
- [xiaobenyang API key site](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown summary with JSON-derived results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes raw JSON-RPC response data plus success and status messages from the tool wrapper.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
