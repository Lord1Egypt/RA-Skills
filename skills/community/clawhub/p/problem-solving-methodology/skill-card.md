## Description:

A structured problem diagnosis and resolution methodology for unclear, multi-component, or risky issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to slow down and diagnose unclear problems before changing code or configuration. It guides them through problem definition, root-cause analysis, solution comparison, scoped execution, verification, and post-mortem learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnosis may require inspecting logs, configuration, databases, or session stores that can contain sensitive data.

Mitigation: Confirm the task scope and permissions before inspecting those sources, and avoid exposing unnecessary sensitive details in responses or notes.

Risk: The workflow can lead the agent to write reusable learning notes or hand work to another coding agent.

Mitigation: Record only non-sensitive reusable lessons and get appropriate confirmation before delegation or risky changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text guidance with optional code, shell commands, and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; behavior is a diagnostic workflow for agent responses and task execution.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
