## Description:

Memory Optimization helps AI agents recover and maintain working context through TL;DR summaries, structured memory files, daily cleanup, knowledge graph tooling, retrieval, consolidation, decay, and health dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardiitse](https://clawhub.ai/user/richardiitse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add durable memory workflows to AI agents, including fast session recovery, structured project tracking, knowledge graph management, memory consolidation, decay, retrieval, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit conversation memory, session logs, and API credential context to configurable remote LLM or embedding endpoints.

Mitigation: Use only trusted HTTPS endpoints, review endpoint configuration before use, and treat memory extraction and compression as sensitive data-processing operations.

Risk: The security scan reports an unrelated browser-skill override/install path.

Mitigation: Review or remove that section before installation so the deployed skill is limited to the intended memory-management behavior.

Risk: Dependency or endpoint changes could alter behavior after review.

Mitigation: Pin dependencies and configuration used by the memory scripts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardiitse/skills/memory-optimization)
- [Skill definition and usage guide](SKILL.md)
- [Memory Optimization README](README.md)
- [Scripts reference](scripts/README.md)
- [Memory ontology integration guide](ontology/INTEGRATION.md)
- [Memory ontology quick reference](ontology/QUICK_REFERENCE.md)
- [Memory ontology schema](ontology/memory-schema.yaml)
- [Configured LLM endpoint](https://open.bigmodel.cn/api/paas/v4)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces operational memory-management instructions and local tooling outputs such as JSON, Markdown exports, dashboards, and validation results.]

## Skill Version(s):

1.0.4 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
