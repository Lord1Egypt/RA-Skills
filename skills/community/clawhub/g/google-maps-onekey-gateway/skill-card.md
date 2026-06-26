## Description: <br>
Google Maps tools via OneKey Gateway for geocoding, reverse geocoding, place search, place details, distance matrix, elevation, and directions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Google Maps capabilities through OneKey Gateway for address lookup, place search, routing, travel-time estimates, and elevation queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a fallback access key when DEEPNLP_ONEKEY_ROUTER_ACCESS is not set. <br>
Mitigation: Require users to provide their own scoped OneKey Gateway credential and remove or disable fallback credential use before production deployment. <br>
Risk: Addresses, coordinates, routes, place searches, and place identifiers may be sent through OneKey Gateway to mapping providers. <br>
Mitigation: Avoid sending sensitive location data unless necessary, disclose external processing to users, and document privacy handling for location inputs and responses. <br>
Risk: The security verdict is suspicious because of credential and location-data handling concerns. <br>
Mitigation: Review the skill before installation, scan the package before deployment, and approve it only after the credential and data-handling concerns are acceptable for the intended use case. <br>


## Reference(s): <br>
- [ClawHub Google Maps skill page](https://clawhub.ai/AI-Hub-Admin/google-maps-onekey-gateway) <br>
- [AI-Hub-Admin publisher profile](https://clawhub.ai/user/AI-Hub-Admin) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router documentation](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway documentation](https://deepnlp.org/doc/onekey_agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON tool responses with Markdown usage guidance and shell or Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a OneKey Gateway access key; scripts print JSON responses from the requested maps operation.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
