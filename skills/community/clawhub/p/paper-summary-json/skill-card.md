## Description:

Structured academic paper analysis from local paper files or paper URLs, producing evidence-backed extraction JSON, consistency checks, and editable reports in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crw0149](https://clawhub.ai/user/crw0149)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to process academic papers from files or direct paper URLs, extract structured paper facts with evidence spans, verify consistency against the source text, and generate Markdown, HTML, and DOCX reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles untrusted paper URLs and downloaded document content with limited containment.

Mitigation: Use only trusted paper files and URLs, avoid internal or private-network URLs, prefer a constrained workspace, and add URL allowlisting or network blocking before broader deployment.

Risk: Runtime copies, intermediate files, generated JSON, and reports are saved to the Desktop output path by default.

Mitigation: Do not process sensitive papers unless the output path is appropriate; review and remove local outputs after use.

Risk: Untrusted document text can influence model-generated extraction and verification outputs.

Mitigation: Keep strong prompt boundaries, require evidence spans, and review the consistency check before relying on reported claims.

Risk: Generated reports may be shared outside the execution environment.

Mitigation: Sanitize generated HTML and review Markdown, HTML, and DOCX outputs before distribution.

## Reference(s):

- [Prompt Templates](references/prompt_templates.md)
- [Workflow Mapping](references/workflow_mapping.md)
- [ClawHub Skill Page](https://clawhub.ai/crw0149/skills/paper-summary-json)

## Skill Output:

**Output Type(s):** [text, json, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON extraction and verification files plus Markdown, HTML, and DOCX reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese or English report language and writes runtime inputs, intermediate files, generated JSON, and final reports under ~/Desktop/paper_analysis_results/<timestamp>/ by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
