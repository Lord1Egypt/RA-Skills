## Description:

Integrates MuninnDB as a cognitive memory system for Hermes Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsonwheels](https://clawhub.ai/user/bitsonwheels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Hermes Agent to connect to a local MuninnDB MCP server and use MuninnDB as cognitive memory. It also documents setup checks and a periodic memory snapshot workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Hermes to a local MuninnDB service can persist agent memory outside a single session.

Mitigation: Verify that local MuninnDB integration is intended before installing or activating the skill.

Risk: A separate cron-based memory snapshot workflow can continue capturing memory periodically after setup.

Mitigation: Review and explicitly enable any periodic memory snapshot workflow only when persistent capture is acceptable.

Risk: Incorrect Hermes MCP header configuration can cause authentication failures while the server appears enabled.

Mitigation: Use the documented `headers` key for the MCP Authorization bearer token and check this key first when troubleshooting 401 responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bitsonwheels/skills/muninndb-integration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on local MuninnDB and Hermes MCP configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
