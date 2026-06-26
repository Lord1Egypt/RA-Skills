## Description: <br>
MakeX lets agents discover and execute actions in third-party services through the OpenClaw Integrations API with organization-level authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkejr](https://clawhub.ai/user/tkejr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to let an agent search available MakeX integrations, inspect action schemas, check connected accounts, and execute actions against connected third-party services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run real actions in connected third-party services using an organization token. <br>
Mitigation: Use the narrowest token and connected accounts available, and require explicit approval before actions that send, post, delete, or change data. <br>
Risk: Organization-level integration access may expose sensitive connected-service data or perform high-impact operations. <br>
Mitigation: Install only when the publisher, MakeX, and Composio are trusted with that access, and avoid giving the token to broadly autonomous agents. <br>
Risk: Execution tracing may retain operational details beyond what is needed for a task. <br>
Mitigation: Keep tracing disabled unless it is specifically needed for debugging or review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkejr/makex) <br>
- [MakeX app](https://www.makex.app/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include raw third-party action results whose shape varies by selected integration and action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
