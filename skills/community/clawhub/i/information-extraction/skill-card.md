## Description: <br>
Extract structured entities, relations, attributes, events, and triples from plain text or Markdown through a semi-automatic pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quqxui](https://clawhub.ai/user/quqxui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and knowledge-graph builders use this skill to convert copied text, notes, reports, transcripts, and Markdown into normalized entities, relations, attributes, events, and graph-ready triples for review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive source text may be transformed into local entities, evidence snippets, and triples that persist in user-selected output files. <br>
Mitigation: Avoid processing sensitive documents unless those local structured outputs are acceptable, and review output paths and retention before running the scripts. <br>
Risk: Semi-automatic extraction can miss facts, mis-normalize relations, or include unsupported inferences. <br>
Mitigation: Preserve evidence spans, confidence values, and ambiguity records, then manually review results before relying on them for high-stakes or downstream graph use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quqxui/information-extraction) <br>
- [Extraction Pipeline](references/pipeline.md) <br>
- [Intermediate Schema](references/schema.md) <br>
- [Relation Taxonomy](references/relation-taxonomy.md) <br>
- [Triple Mapping](references/triple-mapping.md) <br>
- [Event Modeling](references/event-modeling.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured JSON by default, with JSONL or TSV exports when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include evidence spans, confidence values, normalized triples, entities, attributes, events, and ambiguities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
