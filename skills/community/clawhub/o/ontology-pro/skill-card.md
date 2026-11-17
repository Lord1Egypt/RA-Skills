## Description:

Ontology Pro builds and continuously updates knowledge graphs from text, supports multi-step and causal reasoning, and produces actionable strategy recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill to extract entities and relationships from text, maintain a persistent ontology graph, reason over causal paths, and turn conclusions into prioritized strategies and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-derived knowledge may be persisted across sessions, including confidential or regulated material.

Mitigation: Use persistent memory only with explicit intent, scope graph storage to a known directory, and avoid saving secrets or sensitive source text.

Risk: Stored graph content may be reused later without clear consent, deletion, or retention boundaries.

Mitigation: Inspect stored graph files periodically and establish consent, deletion, and retention practices before using the skill on sensitive work.

Risk: Extracted relationships, reasoning chains, or strategy recommendations may reflect incorrect or prompt-injected source material.

Mitigation: Review graph evidence and recommendations before acting, especially for high-impact decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zmy1006-sudo/skills/ontology-pro)
- [Cognitive Graph Protocol](artifact/references/cognitive-graph.md)
- [Memory Protocol](artifact/references/memory-protocol.md)
- [Reasoning Engine](artifact/references/reasoning-engine.md)
- [Strategy Output](artifact/references/strategy-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON, Markdown reports, Mermaid diagrams, and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist graph JSON under the configured ontology storage directory when memory workflows are used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
