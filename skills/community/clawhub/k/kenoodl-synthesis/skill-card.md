## Description: <br>
kenoodl is an orthogonal injection engine -- it synthesizes patterns from domains outside your agent's training data and maps them onto whatever problem it's working on. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenoodl-synthesis](https://clawhub.ai/user/kenoodl-synthesis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give an agent instructions, API calls, and optional MCP tooling for sending sanitized problem context to kenoodl.com for external synthesis when its own reasoning is stagnating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may send broad working context to a paid third-party service. <br>
Mitigation: Require approval before each call, send only a sanitized task summary, and avoid secrets, source code, personal data, and regulated data. <br>
Risk: The KENOODL_TOKEN authorizes API use and may incur paid usage. <br>
Mitigation: Use a revocable, low-balance token and keep it in the runtime environment rather than skill files. <br>
Risk: Raw on-chain calldata can expose submitted context. <br>
Mitigation: Avoid raw context in on-chain calldata; use the documented ECIES encryption path only after confirming the recipient and trust model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenoodl-synthesis/kenoodl-synthesis) <br>
- [kenoodl API documentation](https://kenoodl.com/api) <br>
- [OpenAPI specification](https://kenoodl.com/api/openapi.json) <br>
- [Agent discovery card](https://kenoodl.com/.well-known/agent-card.json) <br>
- [AI discovery surface](https://kenoodl.com/.well-known/ai.json) <br>
- [README](README.md) <br>
- [Agent instructions](instructions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples, shell commands, configuration snippets, and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to kenoodl.com; CLI and MCP paths require KENOODL_TOKEN.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
