## Description:

Systematic knowledge internalization and capability self-assessment engine for learning new domains, building reusable knowledge bases, and stating mastery boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonlinearhuman](https://clawhub.ai/user/nonlinearhuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to research a subject, structure the resulting knowledge, generate capability self-assessments, and preserve reusable knowledge artifacts for later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research on private, sensitive, or proprietary topics may be saved to long-term memory and reused in future sessions.

Mitigation: Ask for explicit confirmation before persistence, avoid sensitive topics unless approved, and provide a clear delete or rollback path for stored entries.

Risk: Web-derived research can carry untrusted or prompt-injection content into generated knowledge artifacts.

Mitigation: Treat fetched pages as untrusted evidence, filter instructions from external content, and review generated artifacts before relying on them.

## Reference(s):

- [Knowledge Graph Guide](references/knowledge_graph_guide.md)
- [Rating Standards](references/rating_standards.md)
- [ClawHub Skill Page](https://clawhub.ai/nonlinearhuman/skills/learn-knowledge)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports and JSON knowledge artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a concept-relation knowledge graph, hierarchical knowledge framework, Q&A pairs, capability assessment report, and memory index update guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact footer says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
