## Description:

Guides architectural decisions for LangGraph applications. Use when deciding between LangGraph vs alternatives, choosing state management strategies, designing multi-agent systems, or selecting persistence and streaming approaches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide when LangGraph is appropriate and to choose state, routing, persistence, streaming, human-in-the-loop, multi-agent, and reliability patterns before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture guidance may be stale or mismatched with the user's LangGraph version or deployment environment.

Mitigation: Review the recommendations against the target LangGraph version and deployment needs before adopting persistence, routing, or streaming choices.

Risk: Persistence backend choices can affect durability, concurrency, and production reliability.

Mitigation: Validate checkpointer selection for the target environment and avoid test-only persistence backends in production designs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/langgraph-architecture)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with tables, checklists, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only architecture guidance; no hidden execution, data access, or unsafe persistence behavior was found in the inspected artifact.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
