## Description:

Generate structured execution plans for medical and molecular biology protocols such as RNA extraction, reverse transcription, qPCR, cell culture, CRISPR, or other healthcare/biomedical procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbingrock](https://clawhub.ai/user/mengbingrock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and lab teams use this skill to draft safety-conscious execution plans or compare protocol options for biomedical and molecular biology workflows. Outputs are planning aids that should be reviewed against validated protocols, institutional approvals, and local safety requirements before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate detailed biomedical procedures that may be incorrect, incomplete, or inappropriate for a specific lab or clinical context.

Mitigation: Require qualified scientific, biosafety, and clinical governance review before using generated plans, and verify all procedures against validated protocols and institutional approvals.

Risk: The skill may read local protocol documents that contain confidential lab SOPs, unpublished research, clinical context, or regulated biomedical information.

Mitigation: Use it only in workspaces selected by the user and confirm which local files may be read before generating plans.

Risk: The skill may send sensitive task details to web search when gathering supplementary protocol information.

Mitigation: Confirm that web search is allowed for the task and remove confidential or regulated details before any external lookup.

## Reference(s):

- [Protocol Planning Guide](references/protocol-planning-guide.md)
- [Medical and Healthcare Domain Knowledge](references/medical-domain-knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown document with checklists, tables, protocol options, references, and safety notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce protocol options when steps are absent or a detailed execution plan when steps are supplied.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
