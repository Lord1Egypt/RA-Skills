## Description:

Contract-driven multi-agent orchestration with ACP, contract sync, webhook and dispatch-queue dispatch, cross-review, auto-retry, and batch progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayao99315](https://clawhub.ai/user/ayao99315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use OpenNexum to coordinate multi-agent coding workflows through Contract YAML, ACP session handoff, generator/evaluator cross-review, retry handling, and progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenNexum processes repository contracts and configuration that can influence how coding agents are dispatched.

Mitigation: Install and run it only in repositories you trust, and review nexum contracts and config files before dispatching agents.

Risk: Webhook gateway URLs and callback tokens can route orchestration events to endpoints the user did not intend.

Mitigation: Avoid custom webhook gatewayUrl values unless the endpoint is trusted and the token is scoped to that endpoint.

Risk: Generated shell and git commands can modify code or repository history when executed by agents.

Mitigation: Review generated commands and agent changes before execution, merge, or release.

Risk: The watch or install workflow can enable a persistent user-level background service.

Mitigation: Enable persistent watching only when dispatch replay is intended, and monitor or disable the service when it is no longer needed.

## Reference(s):

- [Orchestrator Guide](references/orchestrator-guide.md)
- [Contract Schema Reference](references/contract-schema.md)
- [OpenNexum Architecture](docs/design/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline YAML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce contract YAML, prompt payload guidance, CLI command sequences, state workflow guidance, and configuration advice.]

## Skill Version(s):

2.1.4 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
