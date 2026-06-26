## Description: <br>
Automation Master is a Windows office automation skill for file conversion, batch renaming, Excel data merging, template-based document generation, invoice extraction, and tax reconciliation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mk1350](https://clawhub.ai/user/mk1350) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external business users can use this skill to automate common office document workflows, including file conversion, batch renaming, template-based document generation, invoice extraction, and Excel-based tax reconciliation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad Windows side effects while processing local documents. <br>
Mitigation: Run it in an isolated Windows environment with copies of documents and review file operations before deployment. <br>
Risk: The skill may process sensitive financial, tax, invoice, and identity data. <br>
Mitigation: Treat generated spreadsheets and logs as sensitive and avoid using the skill on shared workstations. <br>
Risk: Conversion and printing workflows can interact with LibreOffice processes and shared printer routing. <br>
Mitigation: Close LibreOffice before conversion and avoid shared printers until process cleanup and printer routing are reviewed. <br>
Risk: Custom executable paths could expand the execution surface. <br>
Mitigation: Use trusted default application paths and avoid providing custom executable paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mk1350/mk1350-automation-master) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, structured data, configuration] <br>
**Output Format:** [Generated office files, Excel workbooks, extracted invoice fields, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only execution path; some conversions may require LibreOffice or Microsoft Excel.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
