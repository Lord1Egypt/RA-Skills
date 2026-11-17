## Description:

HR助手 helps Chinese small and medium businesses manage employee rosters, organization structure, attendance, payroll, tax and social contribution calculations, year-end bonus optimization, and local HR reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoned0516](https://clawhub.ai/user/stoned0516)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams at Chinese small and medium businesses use this skill to initialize local Excel-based HR data, manage employee and department records, calculate payroll and attendance deductions, and generate HR reports.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can change or delete sensitive employee records and run payroll, bulk status changes, and exports.

Mitigation: Require manual review and explicit approval before employee deletion, bulk changes, payroll runs, or exports.

Risk: HR, payroll, audit, and conversation data are persisted locally and may contain sensitive personal information.

Mitigation: Install only in a trusted, access-controlled environment, protect the .hr-data directory, avoid shared machines, and back up HR spreadsheets before use.

Risk: Generated or modified Excel files may carry spreadsheet-specific risks until stronger hardening is confirmed.

Mitigation: Treat generated Excel files carefully and review exported spreadsheets before sharing or opening them in higher-trust environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stoned0516/skills/hr-assistant)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Payroll Engine Documentation](artifact/docs/payroll_engine.md)
- [Onboarding Prompt](artifact/prompts/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Chinese text or Markdown with optional shell commands and local Excel or JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-provided Excel files and write local .hr-data configuration, audit, payroll, conversation, and report files.]

## Skill Version(s):

1.2.5 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
