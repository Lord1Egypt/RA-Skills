## Description: <br>
Operate Matrix Client-Server API through UXC with a curated OpenAPI schema, bearer-token auth, and homeserver-aware messaging guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure UXC access to Matrix homeservers, inspect supported Matrix Client-Server operations, read account and room data, and send room messages with explicit guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Matrix access token to read Matrix data and send room messages. <br>
Mitigation: Use a dedicated or least-privileged token where possible, keep tokens out of chats, logs, and repositories, and review any message before sending. <br>
Risk: Matrix operations are homeserver- and room-specific, so an incorrect endpoint or room ID can target the wrong account context or conversation. <br>
Mitigation: Verify the homeserver client-server base URL, auth binding, room IDs, and token owner before performing room reads or message sends. <br>
Risk: Background sync polling can write Matrix event data to local subscription files. <br>
Mitigation: Stop or delete background sync files when they are no longer needed and handle them as potentially sensitive account data. <br>


## Reference(s): <br>
- [Matrix OpenAPI Skill on ClawHub](https://clawhub.ai/jolestar/matrix-openapi-skill) <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/matrix-client-server.openapi.json) <br>
- [Matrix Client-Server API](https://spec.matrix.org/latest/client-server-api/) <br>
- [Matrix spec source](https://github.com/matrix-org/matrix-spec/tree/main/data/api/client-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on UXC commands, homeserver configuration, bearer-token authentication, polling setup, and read-before-write Matrix workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
