## Description:

Operate an Obsidian knowledge base as a persistent LLM wiki using a raw-to-source-to-wiki pattern for ingesting notes, maintaining source summaries, compiling formal wiki pages, writing back reusable outputs, and running recurring maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ducheneadas-source](https://clawhub.ai/user/ducheneadas-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to have an agent maintain an Obsidian vault as a living wiki, including ingesting raw notes, preserving source summaries, promoting stable knowledge, saving reusable query outputs, and running scheduled maintenance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may reorganize or write local Obsidian notes during maintenance.

Mitigation: Set the vault path, folder scope, loose-note movement policy, and approval requirements before broad runs.

Risk: Raw notes, source summaries, formal conclusions, and reusable outputs may be mixed together if the vault model is not adapted first.

Mitigation: Use the adaptation checklist to define raw, source, wiki, and output folders before ingest or migration work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ducheneadas-source/skills/obsidian-karpathy-wiki)
- [Object Model](references/object-model.md)
- [Workflow](references/workflow.md)
- [Adaptation Checklist](references/adaptation-checklist.md)
- [Heartbeat](references/heartbeat.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance and Obsidian-compatible note structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Obsidian wiki links and YAML frontmatter for formal pages when maintaining a vault.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
