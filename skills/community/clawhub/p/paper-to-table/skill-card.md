## Description: <br>
Extract structured data from academic papers (PDF/DOCX/TXT) into literature review tables (XLSX/CSV) with fidelity, batch support, and multi-domain handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2025biophilia-coder](https://clawhub.ai/user/2025biophilia-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to extract explicitly stated information from English or Chinese academic papers into structured literature review tables. It supports single-paper and batch workflows for XLSX or CSV templates across psychology, cognitive neuroscience, computer science, and brain science domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch processing can save excerpts of paper text in local JSON logs, which may retain confidential, unpublished, copyrighted, or sensitive paper content. <br>
Mitigation: Review before installing for sensitive-paper workflows, choose output folders deliberately, and delete generated logs when they are no longer needed. <br>


## Reference(s): <br>
- [Extraction Patterns](references/extraction-patterns.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples; generated table outputs are XLSX or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extraction fields include value, confidence, and source location; batch runs may create local JSON logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
