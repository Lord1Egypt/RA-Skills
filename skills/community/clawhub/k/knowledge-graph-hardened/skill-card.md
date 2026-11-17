## Description:

Maintains Clawdbot's compounding knowledge graph under life/areas/** by adding or superseding atomic facts, regenerating entity summaries, and keeping IDs consistent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain local file-based knowledge graph entries with deterministic commands for adding facts, superseding facts, and regenerating entity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local knowledge graph files that may contain personal data.

Mitigation: Keep data local and avoid storing sensitive personal information unless the data subject has explicitly consented to that specific data category.

Risk: Superseding a fact changes the active record and marks the prior fact as superseded.

Mitigation: Confirm the exact fact ID and replacement text with the user before running a supersession.

Risk: Generated summaries can expose or propagate stored knowledge graph data to later agents.

Mitigation: Treat generated summaries as untrusted local data and do not pipe kg.py output or knowledge graph file contents to network-transmitting commands.

## Reference(s):

- [Safety Evaluation](artifact/SAFETY.md)
- [Faberlens Knowledge Graph Safety Report](https://faberlens.ai/explore/knowledge-graph)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/knowledge-graph-hardened)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates local items.json facts and summary.md entity summaries through a dependency-free Python helper script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
