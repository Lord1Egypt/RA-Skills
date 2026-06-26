## Description: <br>
Reviews standards documents against GB/T 1.1-2020 using a checklist pass and a deeper source-based review, then produces a structured findings report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Standards writers, reviewers, quality teams, and training facilitators use this skill to check draft standards for GB/T 1.1-2020 structure, terminology, numbering, wording, tables, figures, and reference issues. It is best suited to standards-document review rather than general document editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is narrowly designed for GB/T 1.1-oriented standards-document review and may produce misleading guidance on unrelated documents. <br>
Mitigation: Use it only for standards-document checks and have a knowledgeable reviewer confirm findings before applying changes. <br>
Risk: The example PDF workflow may create temporary rendered page images under /tmp during analysis. <br>
Mitigation: Avoid sending unrelated private documents, and remove temporary rendered images after reviews that involve sensitive material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-git1-1-checker) <br>
- [GB/T 1.1-2020 PDF structure guide](references/pdf-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Structured Markdown reports with checklist results, issue tables, severity labels, clause references, and suggested corrections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python/PyMuPDF page-rendering snippets and guidance for visual PDF review when text extraction is unreliable.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
