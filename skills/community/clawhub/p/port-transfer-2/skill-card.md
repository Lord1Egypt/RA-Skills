## Description:

Helps agents use the mcporter CLI to list, configure, authenticate, call, and health-check protocol service connectors and their tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to manage mcporter connector configurations, credentials, tool calls, and health checks from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute mcporter commands that configure or call external connectors.

Mitigation: Use it only for explicit mcporter tasks and review generated commands before execution.

Risk: Credential handling examples can expose API keys or tokens if secrets are pasted directly into command lines or logs.

Mitigation: Prefer environment variables or a secret store and avoid entering real secrets into command text.

Risk: Configured connectors may read or change resources according to their own permissions.

Mitigation: Review each connector's permissions and run health checks or tool calls only against trusted services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/port-transfer-2)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mcporter command examples, connector configuration steps, credential handling guidance, and structured command output examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
