## Description:

Provides guidance for building, querying, merging, visualizing, and configuring a persistent JSON-backed knowledge graph with KGML summaries for agent context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a local structured knowledge graph, query and merge entities, manage configuration, and generate compact KGML or visualization outputs for workflow context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify assistant instruction files and persist local knowledge or configuration.

Mitigation: Request exact file paths, a dry run, backups, and rollback steps before installation or execution.

Risk: The skill describes credential vault handling and includes secret-like examples.

Mitigation: Replace example secrets before use and only provide real API keys after confirming storage paths, encryption behavior, and access controls.

Risk: The security verdict is suspicious because scoping and safeguards are not sufficiently clear.

Mitigation: Review the skill carefully before installing and run it only in environments where persistent local changes and credential management are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, KGML text, JSON-backed data, and optional self-contained HTML visualization output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local knowledge graph data, configuration files, summaries, and credential vault entries when the described scripts are installed and run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
