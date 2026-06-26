## Description: <br>
Provides Qianlu inquiry-management spreadsheet header, filename, terminology, workflow, and quote-comparison standards for agents reviewing Excel documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kami1983](https://clawhub.ai/user/kami1983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external collaborators who work with Qianlu inquiry-management documents use this skill to check Excel headers, aliases, filenames, quote-comparison expectations, and terminology before importing, exporting, or discussing inquiry-side records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect spreadsheet header, filename, or terminology guidance could lead to failed imports or mismatched Qianlu inquiry records. <br>
Mitigation: Use REFERENCE.md for full header tables and naming rules, and treat SKILL.md as a routing summary rather than the complete source of truth. <br>
Risk: A filebrowser upload could transfer a spreadsheet to an unintended destination if another upload-capable skill is invoked without clear approval. <br>
Mitigation: Only approve uploads when the user intentionally wants that spreadsheet transferred and understands the destination and permissions. <br>
Risk: The skill covers inquiry-management standards, while WMS and warehouse-side formats are still outside its authoritative scope. <br>
Mitigation: Flag WMS or warehouse-side questions as out of scope and use the relevant WMS requirements or implementation documents instead. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kami1983/kam-qianlu-doc-standards) <br>
- [REFERENCE.md - Qianlu spreadsheet and filename standards](artifact/REFERENCE.md) <br>
- [naming-and-terminology.md - Qianlu terminology standards](artifact/naming-and-terminology.md) <br>
- [process-and-rules.md - Qianlu workflow and validation rules](artifact/process-and-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, analysis] <br>
**Output Format:** [Markdown or concise text summaries with spreadsheet header mappings, filename checks, and workflow guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local reference documents for full table headers; any filebrowser upload should be separately approved by the user.] <br>

## Skill Version(s): <br>
6.1.2 (source: server release evidence and SKILL.md frontmatter v6.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
