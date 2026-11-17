## Description:

Build, review, and debug OpenClaw plugins with the official plugin SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazyork](https://clawhub.ai/user/pazyork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, implement, validate, package, and debug OpenClaw plugins, including plugin manifests, shipped skills, tools, hooks, slash commands, tests, and install handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled observability-lab example can write prompts, responses, tool activity, and context to a local telemetry.jsonl file when capture is enabled.

Mitigation: Avoid sensitive sessions when using the example, or add redaction, file permission controls, retention limits, and a purge command before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pazyork/skills/plugin-creator)
- [Official Documentation Entry Points](references/official-docs.md)
- [Plugin Layout and Registration](references/plugin-layout-and-registration.md)
- [Hooks and Event Types](references/hooks-and-events.md)
- [Development, Testing, and Validation Workflow](references/testing-and-workflow.md)
- [Pitfalls and Debugging Guide](references/pitfalls-and-debugging.md)
- [In-Repo Example Map](references/example-map.md)
- [Observability Lab](references/observability-lab-source/README.md)
- [OpenClaw plugin documentation](https://docs.openclaw.ai/plugins/building-plugins)
- [OpenClaw plugin SDK overview](https://docs.openclaw.ai/plugins/sdk-overview)
- [OpenClaw plugin manifest documentation](https://docs.openclaw.ai/plugins/manifest)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation checklists, package handoff details, and risk notes for plugin behavior.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
