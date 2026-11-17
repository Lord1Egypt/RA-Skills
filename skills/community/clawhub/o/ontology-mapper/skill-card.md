## Description:

Map construction data to standard ontologies and create semantic mappings between different data schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data teams, developers, and project managers use this skill to map project schemas and field values to construction ontologies such as IFC, COBie, Uniclass, OmniClass, MasterFormat, and UniFormat. It supports semantic interoperability work by reporting mappings, confidence levels, coverage, unmapped fields, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read user-specified local project files that contain unintended or sensitive construction data.

Mitigation: Provide only files intended for ontology mapping and review inputs before running mapping workflows.

Risk: Ontology mappings can be low confidence, incomplete, or incorrect for project-specific schemas.

Mitigation: Review confidence levels, unmapped fields, and recommendations before using results in downstream construction workflows.

## Reference(s):

- [Ontology Mapper skill source](artifact/SKILL.md)
- [DataDrivenConstruction](https://datadrivenconstruction.io)
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/ontology-mapper)
- [datadrivenconstruction publisher profile](https://clawhub.ai/user/datadrivenconstruction)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports, structured tables, JSON exports, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include mapping confidence, coverage summaries, unmapped fields, recommendations, and optional CSV, Excel, or JSON export guidance.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
