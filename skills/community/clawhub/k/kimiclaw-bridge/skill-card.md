## Description:

KimiClaw Bridge helps configure OpenClaw, Claude Code, and spawned coding agents to use Kimi K2.5 through an Anthropic-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw, Claude Code CLI, and ACP coding-agent sessions to route Anthropic Messages API traffic to Kimi K2.5.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, repository context, and coding-agent tasks may be sent to Kimi as an external provider.

Mitigation: Confirm organizational approval before use, avoid sending secrets or regulated data, and route API keys through approved secret management.

Risk: Setting Kimi as a global default could route all spawned coding-agent sessions to that provider.

Mitigation: Review default model settings before global rollout and scope provider configuration to approved workflows.

## Reference(s):

- [Kimi Code Console](https://www.kimi.com/code/console)
- [Kimi Coding API Base URL](https://api.kimi.com/coding)
- [Kimi Anthropic Messages Endpoint](https://api.kimi.com/coding/v1/messages)
- [ClawHub Skill Page](https://clawhub.ai/jack-yang-ai/skills/kimiclaw-bridge)
- [Publisher Profile](https://clawhub.ai/user/jack-yang-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, bash, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider configuration, environment variables, API request examples, and operational gotchas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
