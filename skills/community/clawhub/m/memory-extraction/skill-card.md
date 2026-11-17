## Description:

Automatically identifies entities, relationships, and factual observations in conversations, then updates a knowledge graph to maintain user memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paibwhgs](https://clawhub.ai/user/paibwhgs)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to extract user facts, preferences, projects, tools, locations, and related observations from conversation and preserve them as structured memory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to automatically store broad personal details from conversation without clear consent, review, deletion, or retention controls.

Mitigation: Require explicit opt-in before memory writes and provide preview or confirmation for new records.

Risk: Conversation memory may capture sensitive personal information or facts that users did not intend to persist.

Mitigation: Define sensitive-data exclusions and provide a clear way to inspect, correct, and delete stored records.

Risk: Stored memories may lack provenance, making it harder to audit where a record came from or whether it remains accurate.

Mitigation: Attach source context and timestamps to memory entries when deployed, and review stale or uncertain records before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paibwhgs/skills/memory-extraction)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and structured memory record descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for entity, relation, and observation extraction, plus knowledge graph update behavior and Markdown memory views.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
