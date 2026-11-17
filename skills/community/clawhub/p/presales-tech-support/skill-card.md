## Description:

Provides Chinese-language presales technical diagnosis briefs for customer test scenarios, error logs, root-cause analysis, resolution planning, validation, and risk communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[892577738-bot](https://clawhub.ai/user/892577738-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Presales engineers and technical support teams use this skill to turn customer test requirements, software and hardware stack details, error logs, and prior remediation attempts into a structured Chinese technical diagnosis and remediation brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste sensitive customer logs, stack details, or incident data into the prompt.

Mitigation: Review and redact secrets, credentials, personal data, and confidential customer identifiers before using the skill.

Risk: The skill may propose troubleshooting commands, configuration changes, or architecture changes that need environment-specific validation.

Mitigation: Have qualified engineers review recommendations and test changes in a controlled environment before applying them to production systems.

Risk: The artifact requests comparison with current vendor errata, GitHub issues, or expert knowledge, but server-resolved provenance is unavailable.

Mitigation: Treat external-current claims as unverified unless separately checked against authoritative sources during use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/892577738-bot/skills/presales-tech-support)
- [Skill artifact](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown diagnostic brief with structured sections and optional command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only; does not execute commands, write files, or persist data by itself.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
