## Description:

Subagent-driven development. Dispatch fresh subagent per task with 2-stage review (spec + quality). Cost-aware model routing. From Superpowers by Jesse Vincent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to coordinate subagent-driven software development by dispatching a fresh subagent for each planned task, then requiring specification and quality reviews before completion. The workflow is intended for development tasks where the agent may create or review code, run tests, and make commits when directed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to change code or make commits when applied to a development plan.

Mitigation: Install and use it only for intended development work; review planned changes, run the relevant tests, and confirm commits are desired.

Risk: A subagent may produce incomplete work if it receives too little task context.

Mitigation: Provide the exact task requirements and necessary file context, and re-dispatch when the agent reports that it needs more context.

Risk: Skipping the staged reviews could allow incorrect or low-quality implementation work to proceed.

Mitigation: Require the specification review to pass before quality review, resolve open review issues, and run the full test suite after all tasks complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-subagent-dev)
- [Superpowers project](https://github.com/obra/superpowers)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with workflow steps, routing tables, and review criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create task tracking, code changes, tests, reviews, and commits when applied to a development plan.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
