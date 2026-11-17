## Description:

A multi-agent collaboration framework that adds typed memory retrieval, coordinator-led roles, evidence-based verification, command pre-execution safety checks, and cost/cache observability for agent projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to structure multi-agent workflows with memory retrieval, defined collaboration roles, evidence-based acceptance checks, command safety review, and cost/cache tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store user text and influence later agent runs.

Mitigation: Treat the memory directory as sensitive, review stored memories regularly, and delete entries that should not persist.

Risk: The safety pipeline provides limited pre-execution command checks and does not make commands safe by itself.

Mitigation: Require separate human review before running generated or audited commands, especially installation, network, or destructive shell commands.

Risk: ClawHub security evidence marks the release as suspicious pending review.

Mitigation: Review and scan the skill before deployment, and install only when a local, memory-enabled collaboration framework is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/e2e5g/skills/multi-agent-collaboration)
- [Claude Grade Patterns](references/claude-grade-patterns.md)
- [Workflow Design](references/workflow-design.md)
- [Data Flow](references/data-flow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, structured reports, and command audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved memory, verification status, safety audit results, and cost/cache observations.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
