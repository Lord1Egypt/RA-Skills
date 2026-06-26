## Description: <br>
Operate LINE Messaging API through UXC with a curated OpenAPI schema, bearer-token auth, and messaging-core guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure bearer-token access and operate a focused LINE Messaging API surface for bot lookup, profile lookup, message sends, quota reads, and webhook endpoint management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message send operations can affect real LINE users, groups, or rooms. <br>
Mitigation: Confirm recipients and message text before executing push or reply message operations, and use a token limited to the intended bot. <br>
Risk: Webhook endpoint changes can alter delivery behavior for the channel. <br>
Mitigation: Confirm the current and proposed webhook URLs before set or test operations. <br>
Risk: Schema changes could affect generated commands or operation shapes. <br>
Mitigation: Prefer a pinned or reviewed local schema for production use. <br>


## Reference(s): <br>
- [LINE OpenAPI Skill page](https://clawhub.ai/jolestar/line-openapi-skill) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated LINE Messaging OpenAPI Schema](references/line-messaging.openapi.json) <br>
- [LINE Messaging API reference](https://developers.line.biz/en/reference/messaging-api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to keep automation on the JSON output envelope and to parse stable response fields before acting on results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
