## Description: <br>
MemClaw is a high-performance OpenClaw memory plugin that improves memory management, retrieval, search precision, and context richness while replacing built-in memory operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external OpenClaw users use MemClaw to configure and operate long-term memory search, recall, storage, migration, and maintenance through the memclaw plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist, migrate, index, and prune long-term conversation memories that may include sensitive information. <br>
Mitigation: Require explicit approval for migration, commits that extract durable memories, and non-dry-run maintenance; avoid storing secrets, regulated data, credentials, or sensitive personal details without a retention and deletion plan. <br>
Risk: Memory retrieval may surface outdated, irrelevant, or overly broad context that influences later agent behavior. <br>
Mitigation: Start with abstract search results, inspect richer memory layers only when relevant, and correct or prune memories that no longer apply. <br>


## Reference(s): <br>
- [MemClaw Tools Reference](references/tools.md) <br>
- [MemClaw Best Practices](references/best-practices.md) <br>
- [Memory Structure](references/memory-structure.md) <br>
- [Security & Trust](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may result in durable memory writes, migration, indexing, or pruning through approved memclaw tool calls.] <br>

## Skill Version(s): <br>
0.9.31 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
