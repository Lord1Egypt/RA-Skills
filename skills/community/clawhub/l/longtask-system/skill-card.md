## Description:

LongTask System is a state-file driven long task manager that breaks work into sequential subtasks, coordinates multi-agent execution, and renders a visual cockpit for monitoring progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate long-running OpenClaw workflows by splitting work into ordered JSON-defined steps, assigning steps to agents, tracking completion, and recovering through an inbox fallback when direct delivery fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task JSON files have broad influence over agent sessions and persistent local state.

Mitigation: Review task files before launching the daemon, restrict which agents and sessions the skill may target, and avoid untrusted task parameters.

Risk: The security guidance identifies jq and HTML escaping issues for shared or untrusted inputs.

Mitigation: Fix the jq and HTML escaping issues before using the skill with shared or untrusted task definitions.

Risk: The skill sends a /new command before subtask execution, which can reset agent conversation context.

Mitigation: For single-agent use, remove /new from the notification message construction if preserving context is required.

## Reference(s):

- [LongTask System on ClawHub](https://clawhub.ai/noah-1106/skills/longtask-system)
- [Publisher profile](https://clawhub.ai/user/noah-1106)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task-state updates, inbox entries, logs, and an HTML cockpit when the bundled scripts are executed.]

## Skill Version(s):

1.2.2 (source: ClawHub release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
