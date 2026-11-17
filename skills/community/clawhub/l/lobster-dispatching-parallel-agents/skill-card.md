## Description:

Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to decide when independent coding or debugging work can be delegated to multiple focused agents in parallel, and how to review and integrate their results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sub-agents may receive broader context or authority than needed for their assigned task.

Mitigation: Review delegated prompts so each sub-agent receives only the context, files, constraints, and authority required for its independent problem domain.

Risk: Parallel agents may interfere when tasks are not truly independent or when they edit shared files.

Mitigation: Use the skill only after grouping work into independent domains, then review summaries, check for file conflicts, and run the full test suite before integrating results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-dispatching-parallel-agents)
- [Publisher profile](https://clawhub.ai/user/wangxiaofei860208-source)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown guidance with prompt examples and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning and delegation guidance for agent workflows; it does not execute tools or spawn agents by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
