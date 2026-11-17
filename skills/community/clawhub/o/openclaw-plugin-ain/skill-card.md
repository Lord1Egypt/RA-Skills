## Description:

Integrates AIN providers into OpenClaw with provider bridging, model routing, and tools for prompt execution and task classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipematos](https://clawhub.ai/user/felipematos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this plugin to expose AIN-configured model providers in OpenClaw, execute prompts through AIN, classify prompt tasks, and route model requests according to AIN policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that prompts can be routed to unintended providers because the documented config path is ignored and routing is enabled by default.

Mitigation: Review provider configuration before installation, avoid using sensitive prompts or regulated data until fixed, and disable enableRouting when deterministic provider selection is required.

Risk: The plugin exposes prompt execution tools and depends on @felipematos/ain-cli for provider access and routing behavior.

Mitigation: Use trusted default AIN configuration, consider disabling exposeTools where agents should not initiate external model calls, and pin or independently verify @felipematos/ain-cli before use.

Risk: Building or testing from source may rely on outdated development dependency lockfile entries.

Mitigation: Update and review the development dependency lockfile before building, testing, or publishing from source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felipematos/skills/openclaw-plugin-ain)
- [AIN project](https://github.com/felipematos/ain)
- [@felipematos/ain-cli package](https://www.npmjs.com/package/@felipematos/ain-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [OpenClaw provider registrations, routing decisions, and JSON-compatible tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results can include selected provider, selected model, token usage, parsed structured output, task type, and complexity.]

## Skill Version(s):

0.11.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
