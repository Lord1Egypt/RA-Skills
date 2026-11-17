## Description:

卖家之家(跨境电商)私信查询和发送

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users can have an agent query MJZJ private-message conversations, retrieve message history, and send private messages through the MJZJ API using their configured MJZJ_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access MJZJ private-message account data and send private messages when authorized.

Mitigation: Install only when that access is intended, and review message-retrieval or send actions before execution.

Risk: MJZJ_API_KEY is a sensitive credential.

Mitigation: Store it only in trusted environments and revoke or rotate it if the environment is no longer trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-msg)
- [MJZJ homepage](https://mjzj.com)
- [MJZJ agent API key page](https://mjzj.com/user/agentapikey)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MJZJ_API_KEY; message IDs and pagination cursors should be passed through as strings.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
