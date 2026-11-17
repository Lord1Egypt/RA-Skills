## Description:

Multi-agent collaboration and task orchestration. Decompose complex tasks, spawn sub-agents, coordinate execution, and synthesize results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcp14262](https://clawhub.ai/user/lcp14262)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to break complex work into sub-tasks, coordinate parallel or sequential sub-agents, and synthesize their results into a final deliverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content may be shared among sub-agents during orchestration.

Mitigation: Avoid using the skill with secrets, regulated data, private sales data, or sensitive code unless the OpenClaw environment and sub-agent sharing rules are approved for that data.

Risk: Multi-agent synthesis can merge inconsistent or incomplete sub-agent results.

Mitigation: Review the synthesized result, flag unresolved conflicts, and use explicit output formats and success criteria for sub-agent tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lcp14262/skills/more-agent-orchestrator)
- [Publisher Profile](https://clawhub.ai/user/lcp14262)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and structured JSON-style orchestration summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task decomposition, sub-agent status, synthesized results, and progress or error summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
