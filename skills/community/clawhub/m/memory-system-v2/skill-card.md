## Description:

Fast semantic memory system with JSON indexing, auto-consolidation, and <20ms search for capturing learnings, decisions, insights, events, and interactions across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give an AI agent persistent local memory across sessions, including searchable records of decisions, learnings, insights, events, and interactions. It is suited for single-user local workflows that need fast recall and periodic summary generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local storage may preserve sensitive interaction history across sessions.

Mitigation: Avoid capturing secrets, credentials, regulated data, or private conversations; review filesystem permissions and retention before use.

Risk: Recalled memories can contain stale, incorrect, or untrusted historical context.

Mitigation: Treat retrieved memories as notes for review, not instructions or authoritative facts.

Risk: The artifact does not include a deletion or review workflow for stored memories.

Mitigation: Add periodic review and deletion procedures before using the skill for confidential or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kellyclaudeai/skills/memory-system-v2)
- [Publisher profile](https://clawhub.ai/user/kellyclaudeai)
- [Memory System v2.0 design document](artifact/docs/memory-system-v2-design.md)
- [Memory System v2.0 test results](artifact/docs/memory-system-v2-test-results.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown logs, JSON index entries, and terminal text from a Bash CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and jq; stores memory files locally under the user's home directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
