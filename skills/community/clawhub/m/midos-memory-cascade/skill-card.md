## Description:

Auto-escalating multi-tier memory search that cascades from in-memory cache through SQLite, grep, and LanceDB vector search to find the best answer with minimal latency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msruruguay](https://clawhub.ai/user/msruruguay)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to let an agent search memory across cache, JSON state, SQLite, grep, and optional LanceDB tiers without manually choosing a storage layer. It also supports storing routed memory entries and learning shortcuts from prior cascade results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports broad persistent write and import behavior that can affect local workspace state and future routing.

Mitigation: Review before installation and use only in a contained private workspace with trusted dependencies and patched path validation.

Risk: The store API can write files based on caller-supplied filenames and content.

Mitigation: Do not pass secrets or untrusted filenames to store(), and restrict writable paths before use.

Risk: Memory search results can be low-confidence, stale, or drawn from broad local indexes.

Mitigation: Review returned sources, confidence, and escalation details before relying on an answer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/msruruguay/skills/midos-memory-cascade)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance]

**Output Format:** [Python dictionaries, CLI text output, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recall results include answer, confidence, latency, tiers tried, resolved tier, question routing, shortcut use, and escalation details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
