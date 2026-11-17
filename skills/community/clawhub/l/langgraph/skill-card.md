## Description:

This skill guides agents in designing and implementing LangGraph pipelines with state schemas, graph nodes, conditional routing, human-in-the-loop workflows, persistence, and streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duanc-chao](https://clawhub.ai/user/duanc-chao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to have an agent produce LangGraph architecture guidance, code patterns, and troubleshooting advice for stateful agent pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated LangGraph designs may include sensitive ToolNode actions.

Mitigation: Choose scoped tools and require human approval before sensitive ToolNode actions are executed.

Risk: Persistent checkpointers or databases may retain conversation state.

Mitigation: Be deliberate about what state is stored, and limit persisted data to what the application requires.

Risk: Documentation-only coding guidance can be misapplied when adapted into a real agent pipeline.

Mitigation: Review generated architecture, code, routing logic, and persistence choices before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duanc-chao/skills/langgraph)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable integration is bundled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
