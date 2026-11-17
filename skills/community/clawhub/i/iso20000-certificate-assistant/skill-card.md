## Description:

ISO20000辅助认证助手 (ISO20000 Certification Assistant) helps organizations prepare for ISO 20000-1:2018 IT Service Management System certification with document gap analysis, compliance checking, and bilingual Chinese/English document generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

External consultants, IT service organizations, and compliance teams use this skill to parse ITSM documents, check ISO 20000-1:2018 coverage, identify gaps, and draft bilingual certification-support documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing confidential client documents may leave local plaintext conversion files or logs, especially when legacy .doc files are converted before analysis.

Mitigation: Prefer .docx inputs, run the skill in a controlled working directory, and review or delete generated .txt conversion files and logs after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/iso20000-certificate-assistant)
- [Example interactions](artifact/examples/example_interaction.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown reports, JSON analysis data, shell command guidance, and generated document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local logs and converted text files when parsing legacy .doc inputs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
