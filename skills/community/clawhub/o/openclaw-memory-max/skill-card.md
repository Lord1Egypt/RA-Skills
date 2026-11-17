## Description:

Memory suite for OpenClaw that adds auto-recall, cross-encoder reranking, multi-hop deep search, causal knowledge graph, episodic memory, and nightly consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanistolberg](https://clawhub.ai/user/stanistolberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this memory plugin to provide agents with automatic retrieval, reinforced memory ranking, causal experience lookup, session history, and context rescue across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memories can be injected into high-priority agent context and steer future behavior.

Mitigation: Review memory contents before deployment and install only where this behavior is acceptable.

Risk: Rule pinning can let content in MEMORY.md influence the agent prompt when enabled.

Mitigation: Keep rule pinning disabled unless MEMORY.md is tightly controlled.

Risk: Episodic logs and auto-captured summaries may contain sensitive conversation details.

Mitigation: Review or clear local episodic and auto-capture logs when conversations may include secrets.

Risk: Model artifacts and vulnerable transitive dependencies may need release-level review.

Mitigation: Prefer a version that pins model artifacts and updates vulnerable transitive dependencies.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/stanistolberg/skills/openclaw-memory-max)
- [Project homepage](https://github.com/stanistolberg/openclaw-memory-max)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown context injection and structured JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local sidecar memory files and consolidation summaries when enabled.]

## Skill Version(s):

3.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
