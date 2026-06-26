## Description: <br>
Manage the Higress AI Gateway via its Console API for consumers, routes, AI providers, and MCP server-related gateway settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MontyCN](https://clawhub.ai/user/MontyCN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to administer a Higress AI Gateway through the local Console API, including consumer credentials, AI routes, provider registration, and gateway access settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent instructions for persistent Higress gateway administration using admin-session credentials. <br>
Mitigation: Install only when the agent is expected to administer the gateway, review every create, update, delete, provider-token, and route-change command before execution, and keep a rollback plan for production gateways. <br>
Risk: Route, provider, and credential changes can affect gateway access or model routing. <br>
Mitigation: Use the documented GET-modify-PUT pattern, verify version fields where required, and confirm the target route, consumer, or provider before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MontyCN/higress-gateway-management) <br>
- [Higress Console API reference](references/higress-api-doc.json) <br>
- [Higress Console project](https://github.com/higress-group/higress-console) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl and jq shell commands plus JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for a local Higress Console API session authenticated with the configured session cookie.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
