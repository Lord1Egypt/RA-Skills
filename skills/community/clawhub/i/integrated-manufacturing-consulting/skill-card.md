## Description:

Generates manufacturing consulting project-summary reports and related deliverables from uploaded materials using built-in survey, diagnosis, report-template, document-processing, and industry-search references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericshao2025](https://clawhub.ai/user/ericshao2025)

### License/Terms of Use:

MIT-0

## Use Case:

External consultants, manufacturing transformation teams, and business users use this skill to turn uploaded project materials into executive-facing consulting reports, slide decks, document outputs, diagnostic summaries, and improvement plans for manufacturing, lean production, planning, quality, logistics, and digital transformation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill self-modifies its instructions and scans other installed skills.

Mitigation: Review before installation, disable self-repair writes to SKILL.md, and restrict skill scanning to approved directories.

Risk: The security review says the skill mandates external delivery of generated reports.

Mitigation: Make WeChat, email, and Tencent Docs delivery opt-in per file and confirm destinations before handling confidential client materials.

Risk: The security guidance flags automatic local logging, broad attachment processing, curl-to-shell installation, unpinned dependencies, and Ollama exposure.

Mitigation: Use a controlled environment, pin dependencies, avoid curl-to-shell installation, restrict Ollama to localhost, and remove unnecessary logging before processing sensitive materials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericshao2025/skills/integrated-manufacturing-consulting)
- [Digital Manufacturing Consulting Methodology](artifact/references/methodology.md)
- [Diagnosis Framework and Improvement Library](artifact/references/diagnosis_framework.md)
- [Improvement Project Definition and Planning](artifact/references/project_definition.md)
- [Consulting Project Report Templates](artifact/references/report-templates.md)
- [Discrete Manufacturing Consulting Report Template](artifact/assets/report_template.md)
- [iResearch and QuestMobile Report Source Notes](artifact/references_industry_search/iresearch-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with generated Python, shell commands, and report files such as PPTX, DOCX, PDF, and mind-map PDF outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process uploaded attachments, reuse extracted images, call external report sources, and generate local logs or delivery records depending on the selected workflow.]

## Skill Version(s):

7.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
