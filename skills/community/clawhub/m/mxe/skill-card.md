## Description: <br>
Convert Markdown files to PDF, DOCX, or HTML with advanced formatting, Mermaid diagrams, custom fonts, and table of contents support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanpmt](https://clawhub.ai/user/tuanpmt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document authors use this skill to export Markdown documents into PDF, DOCX, HTML, or clipboard-ready Markdown with diagrams, table of contents, bookmarks, custom fonts, and optional custom styling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path can build and globally link an unreviewed local Node tool from a hard-coded developer path. <br>
Mitigation: Install only after inspecting and trusting the actual mxe source at the referenced local path, or replace it with a reviewed and pinned package. <br>
Risk: URL inputs can contact third-party sites during document retrieval. <br>
Mitigation: Use trusted URLs and review network access expectations before running conversions. <br>
Risk: Local images referenced by Markdown may be embedded into exported documents. <br>
Mitigation: Review source Markdown and referenced local images before exporting or sharing generated documents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tuanpmt/mxe) <br>
- [Publisher Profile](https://clawhub.ai/user/tuanpmt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands that produce PDF, DOCX, HTML, or clipboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact third-party sites for URL inputs and may embed local images into exported documents.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
