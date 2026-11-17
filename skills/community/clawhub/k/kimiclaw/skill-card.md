## Description:

KimiClaw helps configure OpenClaw, Claude Code CLI, and spawned coding agents to use Kimi K2.5 through an Anthropic-compatible backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route OpenClaw, Claude Code, or ACP coding-agent sessions through Kimi K2.5 by setting provider configuration, environment variables, and API request details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, repository content, and agent context may be sent to Kimi when this backend is configured.

Mitigation: Use the skill only when Kimi is an acceptable third-party backend for the data being processed.

Risk: API keys may be exposed if real credentials are placed in shared configuration files.

Mitigation: Keep real API keys in local environment variables or private configuration and avoid committing shared files containing secrets.

Risk: Making Kimi the global default can route all spawned coding agents through a third-party backend.

Mitigation: Scope Kimi configuration to the intended project or agent session unless global routing is explicitly desired.

## Reference(s):

- [Kimi Code Console](https://www.kimi.com/code/console)
- [Kimi Coding API base URL](https://api.kimi.com/coding)
- [Kimi Anthropic Messages endpoint](https://api.kimi.com/coding/v1/messages)
- [ClawHub skill page](https://clawhub.ai/jack-yang-ai/skills/kimiclaw)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Code, Guidance]

**Output Format:** [Markdown with JSON, shell, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
