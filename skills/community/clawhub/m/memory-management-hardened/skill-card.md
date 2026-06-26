## Description: <br>
Guides implementation of agent memory systems, compares production frameworks including Mem0, Zep/Graphiti, Letta, LangMem, and Cognee, and designs persistence architectures for cross-session knowledge retention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose, design, and harden memory architectures for agents that need persistent knowledge, entity consistency, temporal reasoning, or framework selection guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent memory can expose sensitive user, tenant, or project data if retrieval is too broad. <br>
Mitigation: Scope retrieval to the specific query, entity, user, and time range; avoid bulk memory enumeration. <br>
Risk: Memory write paths can be poisoned or abused without strong access control. <br>
Mitigation: Require authentication and authorization for memory ingestion, updates, and write endpoints. <br>
Risk: Cross-tenant memory access can disclose private data. <br>
Mitigation: Enforce tenant isolation and only retrieve memory for the authenticated user or approved scope. <br>
Risk: Memory contents can be exfiltrated when sent to external services or third-party APIs. <br>
Mitigation: Get explicit approval for each external destination before transmitting memory data. <br>
Risk: Long-lived memory stores can retain data beyond user expectations. <br>
Mitigation: Define retention and deletion controls for memory data before production use. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/snazar-faberlens/memory-management-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/memory-management) <br>
- [Zep temporal knowledge graph paper](https://arxiv.org/abs/2501.13956) <br>
- [Mem0 production architecture paper](https://arxiv.org/abs/2504.19413) <br>
- [Cognee optimized knowledge graph and LLM reasoning paper](https://arxiv.org/abs/2505.24478) <br>
- [Graphiti open-source temporal knowledge graph engine](https://github.com/getzep/graphiti) <br>
- [Cognee open-source knowledge graph memory](https://github.com/topoteretes/cognee) <br>
- [Cognee comparison: Form vs Function](https://www.cognee.ai/blog/deep-dives/competition-comparison-form-vs-function) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with comparison tables and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only design guidance; no executable tool behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
