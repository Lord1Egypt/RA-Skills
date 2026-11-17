## Description:

Mempalace Memory provides a local memory recall layer that searches MemPalace, strips metadata, filters credentials, deduplicates results, applies Chinese keyword and identity boosts, and optionally reranks results with MMR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve, store, mine, and prune local workspace memories so an agent can receive relevant context during conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly index and duplicate private workspace memories into local persistent stores.

Mitigation: Use narrow mining paths, treat the MemPalace and SuperMem storage directories as sensitive, and avoid bridge synchronization for sensitive memories unless credential scanning is improved.

Risk: Credential handling is limited and may not catch every secret before memory storage or synchronization.

Mitigation: Do not store passwords, tokens, API keys, or regulated data in memory content; keep credentials in a dedicated protected store and review content before remember or bridge operations.

Risk: Forget operations delete memory IDs from local collections and recovery behavior is not documented.

Mitigation: Back up local memory stores and verify the target memory ID before running forget.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars82311111/skills/mempalace-memory)
- [Publisher profile](https://clawhub.ai/user/mars82311111)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and memory commands accept query, limit, agent, room, source, memory ID, and path parameters.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
