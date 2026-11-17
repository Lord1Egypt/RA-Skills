## Description:

Multi Agent Config Manager orchestrates OpenClaw multi-agent research workflows with planning, subagent execution, validation, retry, aggregation, and workspace configuration checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjmrcft-hash](https://clawhub.ai/user/bjmrcft-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to plan, execute, monitor, validate, and aggregate multi-agent research or project workflows. It is suited to complex tasks that need task decomposition, role-specific subagents, review loops, and final report assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or modify OpenClaw workspace files while orchestrating subagents.

Mitigation: Install and run it only in workspaces where the publisher is trusted and file changes can be reviewed or restored.

Risk: Security evidence flags unsafe configuration parsing and recommends removing an eval fallback.

Mitigation: Review configuration parsing paths before use and require validated structured parsing for any path or model configuration inputs.

Risk: Security guidance notes destructive rm -rf documentation.

Mitigation: Use backup or dry-run cleanup workflows and review generated cleanup commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bjmrcft-hash/skills/multi-agent-config-manager)
- [Module reference](artifact/references/modules.md)
- [Protocol reference](artifact/references/protocols.md)
- [Test lessons](artifact/references/test-lessons.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON plans, shell command examples, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw workspace directories, configuration files, logs, archives, and final research reports.]

## Skill Version(s):

7.2.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
