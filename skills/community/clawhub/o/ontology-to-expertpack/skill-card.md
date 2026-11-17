## Description:

Convert an Ontology skill knowledge graph into a structured ExpertPack with multi-layer retrieval support, Obsidian-compatible Markdown files, and portable deployment metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge engineers use this skill to migrate an Ontology skill graph.jsonl, with optional schema.yaml, into a structured ExpertPack for review, retrieval, and publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter can transform private ontology memory into shareable ExpertPack files.

Mitigation: Run it on a copy of the ontology graph and inspect the generated pack before sharing or publishing.

Risk: Credential-like fields are only partially filtered and untrusted source content may be copied into Markdown.

Mitigation: Review generated Markdown and YAML for secrets, sensitive details, and injected instructions before distribution.

Risk: The output directory receives newly generated pack files.

Mitigation: Use a fresh empty output directory to avoid mixing generated content with existing files.

## Reference(s):

- [ExpertPack](https://expertpack.ai)
- [ClawHub skill page](https://clawhub.ai/brianhearn/skills/ontology-to-expertpack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance and generated ExpertPack files including YAML configuration, Markdown content, indexes, glossary, and relation graph files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a source Ontology graph.jsonl; schema.yaml is optional.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
