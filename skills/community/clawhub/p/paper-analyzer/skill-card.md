## Description: <br>
Paper Analyzer helps users structurally read and analyze academic papers across 12 reading elements and save the results as Excel reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipng05-max](https://clawhub.ai/user/yipng05-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and analysts use this skill to break down one or more academic papers into structured reading elements, compare papers, and generate local Excel reports plus a brief Markdown summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper contents may be written into local Excel reports or temporary JSON files. <br>
Mitigation: Use the skill only on papers intended for local analysis, handle sensitive documents according to policy, and delete temporary JSON files when they are no longer needed. <br>
Risk: Generated Excel filenames or output paths could overwrite files the user wanted to keep. <br>
Mitigation: Review the output path and filename before running the export step, and choose a non-conflicting name for important work. <br>


## Reference(s): <br>
- [12 Reading Elements Reference](references/reading_elements.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yipng05-max/paper-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown summary and Excel workbook files (.xlsx) generated from structured paper-analysis data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Excel reports to the analyzed paper's folder; supports single-paper and multi-paper workbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
