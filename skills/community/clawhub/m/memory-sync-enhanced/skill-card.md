## Description:

Enhanced memory system combining an Ebbinghaus forgetting curve with a Hebbian co-occurrence graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to set up and operate an enhanced memory workflow that combines CortexGraph semantic search, Ebbinghaus decay scoring, and Hebbian co-occurrence tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the tracker script can create or update a persistent local CortexGraph co-occurrence database.

Mitigation: Review the target database path first, back up existing CortexGraph memory state, and run only in a controlled environment until explicit dry-run and backup safeguards are available.

Risk: The package documents memory mutation and deletion workflows without complete command implementations or safety details.

Mitigation: Treat documented commands as proposals and require human review before using them on production or personally valuable memory stores.

## Reference(s):

- [CortexGraph](https://github.com/prefrontal-systems/cortexgraph)
- [Memory Sync Enhanced on ClawHub](https://clawhub.ai/guohongbin-git/skills/memory-sync-enhanced)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local SQLite co-occurrence database under the CortexGraph configuration directory when the included tracker script is run.]

## Skill Version(s):

2.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
