## Description:

Interactive CSA MAESTRO threat modeling skill for agentic AI systems and OpenCode Skills that produces Markdown, JSON, DOCX, and XLSX risk assessment outputs with AI risk classification mapping to China's AI security governance framework.

This skill is for research and development only.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Developers, security engineers, and AI governance reviewers use this skill to run a structured MAESTRO threat-modeling conversation for agentic AI systems or OpenCode Skills. It supports a quick MVTM checklist mode and a fuller 10-phase assessment mode with risk reports and classification outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment inputs, architecture details, and reviewed source code may be sent to the user's AI provider during the workflow.

Mitigation: Use the skill only in environments where that data sharing is acceptable, and minimize or redact sensitive inputs before assessment.

Risk: Generated threat-model reports can contain sensitive architecture, risk, and mitigation details.

Mitigation: Store generated reports as sensitive local records and apply normal access control, retention, and sharing rules.

Risk: XLSX exports from adversarial or untrusted assessment inputs may be unsafe until formula-prefix sanitization is added.

Mitigation: Use Markdown or DOCX output for untrusted inputs, or inspect and sanitize spreadsheet content before opening XLSX files.

Risk: The DOCX and XLSX helpers require Python dependencies.

Mitigation: Install python-docx and openpyxl through the user's normal controlled dependency management process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-maestro-evaluate)
- [Publisher profile](https://clawhub.ai/user/43622283)
- [OWASP MAESTRO Threat Modeling Playbook](https://github.com/agentic-threat-modeling/MAESTRO)
- [ClawHub Registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Code, Shell commands, Configuration, Files]

**Output Format:** [Conversational guidance plus Markdown, JSON, DOCX, and XLSX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped local threat-model directories; DOCX and XLSX exports require python-docx and openpyxl or an equivalent office workflow.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter, manifest.json, CHANGELOG.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
