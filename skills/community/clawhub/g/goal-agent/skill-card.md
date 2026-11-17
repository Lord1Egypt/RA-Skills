## Description:

Scaffold a self-learning goal-oriented agent that takes a goal, metric, target, and constraints, then generates a workspace for iterative measurement, learning, and strategy adaptation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theashbhat](https://clawhub.ai/user/theashbhat)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to scaffold a goal-specific autonomous agent workspace with generated goal tracking, strategy, learning, heartbeat, and metric evaluation files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated autonomous loop instructions can lead an agent to take broad actions if the goal or constraints are too open-ended.

Mitigation: Run the goal workspace in a dedicated workspace or VM, use explicit constraints, start with a low iteration limit, and monitor early runs.

Risk: Crafted goal, metric, or constraint values can trigger command execution through the documented shell templating flaw.

Mitigation: Avoid untrusted --goal, --metric, and --constraints values, keep metric commands read-only, and inspect generated files before activation.

Risk: Using an output directory with important existing files can expose those files to generated autonomous workflows.

Mitigation: Use a fresh output directory and review generated HEARTBEAT.md and evaluate.sh before copying HEARTBEAT.md into the active agent location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theashbhat/skills/goal-agent)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration]

**Output Format:** [Generated Markdown files and shell script files, with setup guidance shown in Markdown and bash commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GOAL.md, STRATEGY.md, LEARNINGS.md, HEARTBEAT.md, and evaluate.sh in the selected output directory.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
