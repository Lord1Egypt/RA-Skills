## Description: <br>
Smart HR Assistant for Chinese small and medium businesses that manages employee records, organization structure, attendance, payroll, tax calculations, year-end bonus optimization, and HR reports using local Excel and JSON data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoned0516](https://clawhub.ai/user/stoned0516) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR staff at Chinese small and medium businesses use this skill to initialize local HR spreadsheets, manage employee lifecycle changes, calculate payroll and tax-related deductions, track attendance, and generate HR reports. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change sensitive employee, payroll, attendance, and configuration records, and the security summary says confirmation safeguards described by the instructions are not consistently enforced. <br>
Mitigation: Review before installing, use only on a protected workstation and restricted folder, back up spreadsheets first, and enforce confirmation for delete, batch update, reset, payroll calculation, and export actions before using real HR or payroll data. <br>
Risk: Exports and local data files can expose sensitive HR and payroll information if saved to shared or synced locations. <br>
Mitigation: Avoid shared or synced export locations, restrict file permissions on the local .hr-data directory and exported spreadsheets, and keep backups in approved protected storage. <br>
Risk: Feishu or cloud storage prompts may create expectations beyond the implemented and disclosed local Excel workflow. <br>
Mitigation: Treat Feishu and cloud storage prompts as unsupported unless the publisher updates the implementation and disclosures. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/stoned0516/hr-assistant) <br>
- [README](README.md) <br>
- [Payroll Engine Documentation](docs/payroll_engine.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese natural-language responses with command examples, local file paths, JSON records, and Excel report files when export actions are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local HR data changes and local exports through Python tools; no cloud storage is supported by the release evidence.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
