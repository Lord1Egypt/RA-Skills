## Description:

Design, implement, and debug memory systems for persistent autonomous AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timesandplaces](https://clawhub.ai/user/timesandplaces)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design durable memory files, choose among continuous memory, semantic RAG, and temporal knowledge graph patterns, and diagnose continuity or staleness failures in persistent agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste temporal knowledge graph setup can expose a persistent Neo4j database too broadly.

Mitigation: Bind services to localhost or a private network and restrict access to trusted hosts before deployment.

Risk: Example install and container commands can drift or introduce unexpected dependencies when versions are not pinned.

Mitigation: Pin package versions and container image digests, then review dependency changes before use.

Risk: Sample credentials are unsafe for a persistent memory database.

Mitigation: Generate a unique secret outside shell history and store it in a managed secret mechanism.

Risk: Persistent memory systems may retain sensitive or inappropriate agent state.

Mitigation: Define allowed memory contents, audit stored memory regularly, and avoid retaining secrets or unnecessary personal data.

## Reference(s):

- [Memory Architecture Reference](references/memory-architecture.md)
- [Temporal Memory Discipline](references/temporal-discipline.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes architecture comparisons, memory file conventions, temporal annotation practices, and setup cautions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
