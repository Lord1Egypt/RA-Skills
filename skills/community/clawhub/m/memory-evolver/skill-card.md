## Description:

Memory Evolver diagnoses an OpenClaw three-layer memory setup, generates prioritized optimization plans, and records memory-system optimization cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizoncove](https://clawhub.ai/user/horizoncove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect OpenClaw memory files, identify missing or thin memory artifacts, produce prioritized improvement guidance, and append an optimization-cycle log for a workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw memory and project files from a hard-coded Administrator workspace path.

Mitigation: Run it only against a confirmed workspace and review or adjust the configured paths before installation or execution.

Risk: The skill can write an optimization log to persistent memory and its documentation encourages scheduled unattended runs.

Mitigation: Run it manually first, review the log output, and enable cron scheduling only after path scope and write behavior are accepted.

Risk: The optimization log can report actions as completed without actually changing the underlying memory files.

Mitigation: Treat the log as advisory and verify any claimed memory improvements before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horizoncove/skills/memory-evolver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text with Markdown log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an optimization log under the configured OpenClaw memory directory; generated plans should be treated as advisory.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact config.json and SKILL.md state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
