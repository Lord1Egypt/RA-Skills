## Description:

Guides implementation of agent memory systems, compares production frameworks such as Mem0, Zep/Graphiti, Letta, LangMem, and Cognee, and designs persistence architectures for cross-session knowledge retention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose, design, and harden agent memory systems for cross-session persistence, retrieval quality, entity consistency, and temporal reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can expose sensitive user data if agents enumerate broad memory stores or transmit retrieved memories externally.

Mitigation: Scope retrieval to a specific query, entity, or time range, and do not share memory results with external services unless the user explicitly authorizes the destination.

Risk: Memory stores can be poisoned or leak data across tenants if write paths and retrieval calls lack identity controls.

Mitigation: Require authenticated and authorized write paths, tenant isolation, and deletion or retention controls before applying memory-system examples in production.

Risk: Stored memories can become stale or conflict with newer facts, causing agents to use outdated context.

Mitigation: Track temporal validity, consolidate memories periodically, preserve history when facts change, and surface low-confidence conflicts to the user.

## Reference(s):

- [Memory Management Hardened release page](https://clawhub.ai/snazar-faberlens/skills/memory-management-hardened)
- [Faberlens safety evaluation report](https://faberlens.ai/explore/memory-management)
- [Zep temporal knowledge graph paper](https://arxiv.org/abs/2501.13956)
- [Mem0 production architecture paper](https://arxiv.org/abs/2504.19413)
- [Cognee optimized knowledge graph and LLM reasoning paper](https://arxiv.org/abs/2505.24478)
- [Graphiti open-source temporal knowledge graph engine](https://github.com/getzep/graphiti)
- [Cognee open-source knowledge graph memory](https://github.com/topoteretes/cognee)
- [Cognee comparison: Form vs Function](https://www.cognee.ai/blog/deep-dives/competition-comparison-form-vs-function)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with tables and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes framework comparisons, architecture decision guidance, retrieval strategies, and memory safety guardrails.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
