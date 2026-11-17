## Description:

Orchestrates parallel execution of similar independent tasks by decomposing work into isolated units, dispatching subagents, and consolidating results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brightween](https://clawhub.ai/user/brightween)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to process batches of similar independent work, such as files, components, reports, or repeated tasks, by planning isolated work units and coordinating parallel subagents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate multiple subagents and retry failed work automatically, which may increase the effect of an incorrect batch plan.

Mitigation: Review the planned work units, input paths, output paths, retry behavior, and background execution posture before dispatch.

Risk: Parallel tasks may write conflicting outputs if work units are not isolated.

Mitigation: Use unique task identifiers and separate output directories for each subagent before merging results.

## Reference(s):

- [Advanced Patterns for Multi-Task Orchestration](references/advanced-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with structured task plans, subagent prompts, command snippets, progress summaries, and result reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task identifiers, absolute input and output paths, wave sizing, retry status, and final success or failure summaries.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
