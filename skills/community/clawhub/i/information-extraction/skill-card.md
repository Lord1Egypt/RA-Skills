## Description:

Extract structured information from unstructured text through a semi-automatic pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quqxui](https://clawhub.ai/user/quqxui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert plain text and Markdown into normalized entities, relations, attributes, events, and exportable triples for downstream review or graph-ready records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads provided text and writes extracted facts to user-selected output files.

Mitigation: Use it only with inputs and output locations appropriate for local processing, and review extracted records before relying on them.

Risk: TSV exports created from adversarial input can be unsafe when opened in spreadsheet software.

Mitigation: Disable formula execution or sanitize exported TSV data before opening it in a spreadsheet.

## Reference(s):

- [Information Extraction Skill Page](https://clawhub.ai/quqxui/skills/information-extraction)
- [Pipeline](references/pipeline.md)
- [Schema](references/schema.md)
- [Relation Taxonomy](references/relation-taxonomy.md)
- [Triple Mapping](references/triple-mapping.md)
- [Event Modeling](references/event-modeling.md)
- [Quality Checklist](references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, JSONL, TSV, or Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output includes triples, entities, attributes, events, and ambiguities with evidence and confidence when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
