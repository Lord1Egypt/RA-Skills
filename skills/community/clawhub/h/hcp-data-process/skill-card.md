## Description:

Extracts standardized summary tables from HCP instrument result workbooks or UTF-16 tab-separated exports that contain Group sections such as Sample, QC, and Standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cantonbio-skill](https://clawhub.ai/user/cantonbio-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Laboratory operations staff, analysts, and automation agents use this skill to process HCP Excel exports into normalized summary workbooks. It is intended for files that follow the documented HCP export structure with Group sections and Sample, MeanResult, and CV columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malicious spreadsheet text could become active formulas in generated XLSX files.

Mitigation: Use trusted HCP exports, review generated workbooks before sharing, and patch formula-leading text escaping before processing untrusted inputs.

Risk: Directory input batch-processes all supported workbook files in that directory.

Mitigation: Run the skill on a reviewed input directory or pass individual files when only specific exports should be processed.

Risk: The --overwrite option replaces existing generated output files.

Mitigation: Use a separate output directory or omit --overwrite unless replacement is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cantonbio-skill/skills/hcp-data-process)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with shell commands; generated XLSX workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes .xlsx, .xlsm, and UTF-16 tab-separated .xls inputs; directory inputs batch-process supported workbook files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
