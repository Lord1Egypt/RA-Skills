## Description:

Extracts hierarchical knowledge nodes from PDF or Word documents, labels node types and semantic relationships, and prepares CSV or Excel outputs for import into online course knowledge graph systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and curriculum teams use this skill to convert source course documents into structured knowledge graph data with node hierarchy, prerequisite relationships, related-node links, tags, descriptions, and learning objectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow references a local extraction script that is not shipped in the artifact.

Mitigation: Verify the script source and contents before execution, or replace it with a reviewed local implementation.

Risk: The workflow may require unpinned Python packages for document parsing and spreadsheet generation.

Mitigation: Run the skill in an isolated workspace with pinned dependencies or a locked environment for openpyxl, python-docx, and pdfplumber.

Risk: Source documents are parsed and sent through an LLM extraction workflow.

Mitigation: Provide only documents intended for extraction and review generated knowledge nodes before importing them into a course platform.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/knowledge-graph-extraction-skill)
- [Server-resolved GitHub repository](https://github.com/flyboat403/knowledge-graph-extraction-skill)
- [Server-resolved GitHub commit](https://github.com/flyboat403/knowledge-graph-extraction-skill/commit/492343463f5232a0044a876980a12bb2398ce3b9)
- [Output Format](references/output-format.md)
- [Extraction Prompt](references/extraction-prompt.md)
- [Quality Check Prompt](references/quality-check-prompt.md)
- [Relation Prompt](references/relation-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON knowledge-node structures and shell commands; final artifacts are CSV and XLSX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one source document and one XLSX template, supports hierarchy levels 1-7, and expects English semicolon delimiters for multi-value fields.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
