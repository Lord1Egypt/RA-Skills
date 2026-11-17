## Description:

OpenClaw Workflow gives OpenClaw agents deterministic YAML workflow control for branching, loops, waits, state management, scripts, HTTP calls, messaging, and agent or subagent steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlmh110](https://clawhub.ai/user/wlmh110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to validate, run, monitor, and resume YAML automation workflows for fixed multi-step tasks such as operations, data monitoring, notifications, and personal assistant routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow YAML can drive local code, filesystem, environment, network, messaging, and session actions.

Mitigation: Review workflow files before execution, run them only from trusted sources, and use a low-privilege local account.

Risk: Environment secrets could be exposed through script, code, HTTP, messaging, agent, or subagent nodes.

Mitigation: Avoid running workflows in environments that hold sensitive secrets or API keys.

Risk: HTTP, message, script, code, and subagent nodes can trigger external effects.

Mitigation: Inspect those node types carefully and keep workflows limited to intended destinations and commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wlmh110/skills/openclaw-workflow)
- [README](README.md)
- [Skill Instructions](SKILL.md)
- [Workflow Design Notes](references/readme.md)
- [Basic Workflow Example](references/examples/basic_test.yaml)
- [Comprehensive Workflow Example](references/examples/comprehensive_test.yaml)
- [OpenClaw Integration Example](references/examples/openclaw_integration.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML workflow examples, and JSON run records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution can create local workflow run records and may trigger configured HTTP, messaging, script, code, agent, or subagent actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
