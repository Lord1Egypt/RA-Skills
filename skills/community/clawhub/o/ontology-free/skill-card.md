## Description:

基于类型约束的知识图谱系统，为智能代理提供基础结构化记忆。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent builders, and automation teams use this skill to create, validate, relate, and query type-constrained local knowledge-graph memory for AI conversations and workflows. It is not intended for critical decisions that require deterministic certainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read and shell execution authority.

Mitigation: Review the skill before installation, run it in a constrained workspace, and limit execution to the documented memory/ontology workflow.

Risk: The skill text includes generic API, file, and command automation claims that exceed the local knowledge-graph memory purpose.

Mitigation: Treat those broader claims as out of scope unless separately reviewed and approved for the target environment.

Risk: Knowledge-graph memory may contain sensitive project, person, document, or task data.

Mitigation: Avoid storing secrets or regulated personal data, and review graph outputs before sharing them outside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ontology-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces entity, relation, query, validation, and error-handling guidance for a local ontology memory workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
