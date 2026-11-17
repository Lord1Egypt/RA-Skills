## Description:

Orchestrate complex multi-agent workflows with explicit coordinator planning, execution governance, and automatic output management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubencoppensongit](https://clawhub.ai/user/rubencoppensongit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate complex work across multiple agents with explicit planning, dependency analysis, ordered execution groups, output verification, and final reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asserts strict mandatory control over execution phases and may conflict with higher-priority user or safety instructions.

Mitigation: Confirm before use that higher-priority instructions remain authoritative and review the planned phases before allowing execution to proceed.

Risk: The skill can spawn multiple agents and write run artifacts, increasing workspace activity and output volume.

Mitigation: Confirm the agent count, output directory, and expected artifacts before execution, and review generated files after the run.

Risk: The skill may apply retention cleanup to prior runs.

Mitigation: Confirm whether cleanup is enabled and preserve any runs that must not be removed before invoking the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and workspace files, including planning artifacts, prompts, logs, and final reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates isolated run directories and may apply retention cleanup according to skill behavior.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
