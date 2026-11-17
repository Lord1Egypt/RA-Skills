## Description:

Builds a standalone layered knowledge runtime with typed links across knowledge entries, entities, memories, and reusable assets for agent memory, retrieval, entity linking, and stable write-back.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or implement layered agent memory systems that retrieve relevant knowledge, link it to canonical entities and reusable assets, and write back only durable findings after successful runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable write-back can persist sensitive, stale, or low-signal knowledge if enabled too broadly.

Mitigation: Define allowed memory files before enabling write-back, require review where appropriate, and set a removal policy for old or sensitive entries.

Risk: Noisy entity extraction or broad write-back can reduce retrieval quality over time.

Mitigation: Prefer canonical entities, deduplicate repeated findings, and write back only stable findings with evidence.

## Reference(s):

- [README.md](README.md)
- [examples.md](examples.md)
- [reference.md](reference.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with JSON examples and JavaScript helper exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compact retrieval bundle shapes, record schemas, adapter guidance, and default local storage layout recommendations.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
