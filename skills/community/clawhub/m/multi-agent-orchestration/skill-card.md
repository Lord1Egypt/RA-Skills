## Description:

Orchestrates multi-agent task delegation and workflows with audit logging, checkpoint approvals, and agent learning for coordinated project execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dabruhce](https://clawhub.ai/user/dabruhce)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use Colony to route tasks to specialized agents and run multi-stage workflows for research, product planning, coding, content, QA, audit, and process retrospectives. It is useful when work benefits from coordinated handoffs, checkpoints, audit trails, and persistent agent learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell command construction could let crafted configuration or workflow metadata execute unintended commands.

Mitigation: Install only from trusted sources, review process definitions and notification settings before use, and avoid shared or untrusted repositories until shell command handling is fixed.

Risk: Path containment issues could let crafted inputs write files outside the intended Colony area.

Mitigation: Run in a controlled workspace, review generated paths before approval, and avoid using the skill around sensitive files or credentials until path containment is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dabruhce/skills/multi-agent-orchestration)
- [Colony Skill Instructions](artifact/SKILL.md)
- [Colony Documentation](artifact/COLONY-DOCS.md)
- [Agent Registry](artifact/colony/agents.yaml)
- [Process Definitions](artifact/colony/processes.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, command-line output, JSON/YAML configuration, code changes, and workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update task, run, audit, memory, and process state files in the Colony workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
