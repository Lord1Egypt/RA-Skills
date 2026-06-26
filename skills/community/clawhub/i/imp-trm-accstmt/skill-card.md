## Description: <br>
Converts MT940, Excel, and PDF bank statements into standard treasury or ERP bank transaction import spreadsheets for BIPV5, Kingdee EAS_YXH, Fingard ATS, NSTC, and Yonyou NCC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jreadstone](https://clawhub.ai/user/jreadstone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, treasury, and implementation teams use this skill to convert bank statement files into import-ready spreadsheet templates for supported treasury and ERP systems. It supports single-file conversion, batch conversion, and merged output workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download spreadsheet templates from an external host when local templates are missing. <br>
Mitigation: Pre-provision trusted local templates and block outbound network access during conversion in finance or regulated environments. <br>
Risk: Converted files may contain sensitive financial transaction data. <br>
Mitigation: Choose explicit output paths and store outputs only in approved locations with appropriate access controls. <br>


## Reference(s): <br>
- [Currency List](references/currency.md) <br>
- [Tesseract OCR setup reference](https://github.com/UB-Mannheim/tesseract/wiki) <br>
- [ClawHub release page](https://clawhub.ai/jreadstone/imp-trm-accstmt) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [Excel or XLS/XLSX import files with concise CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written to user-selected paths or, by default, alongside the input file or input directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
