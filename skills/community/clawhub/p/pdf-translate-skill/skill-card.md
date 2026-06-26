## Description: <br>
Translates local PDFs and arXiv papers while preserving document structure by extracting or downloading source content, translating text, and generating LaTeX-based PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[overdue-lin](https://clawhub.ai/user/overdue-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document translation users use this skill to translate PDFs or arXiv papers into a target language while preserving layout, figures, mathematical notation, citations, and bibliography structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may download and unpack remote arXiv source archives. <br>
Mitigation: Use a dedicated working directory or sandbox, review downloaded TeX before compiling, and avoid sensitive output locations. <br>
Risk: The workflow compiles generated or downloaded TeX, which can affect local files through compiler side effects. <br>
Mitigation: Compile only reviewed TeX in an isolated directory and inspect generated intermediate files before sharing or retaining them. <br>
Risk: Intermediate page images, extracted figures, LaTeX files, and PDFs may contain sensitive source-document content. <br>
Mitigation: Treat all generated intermediates as copies of the source document and clean them up according to the document's data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/overdue-lin/pdf-translate-skill) <br>
- [LaTeX Layout Templates](references/latex_templates.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [arXiv e-print source endpoint](https://arxiv.org/e-print/{arxiv_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with LaTeX snippets, shell commands, and generated document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce translated LaTeX source, page images, extracted images, logs, and compiled PDF files during the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
